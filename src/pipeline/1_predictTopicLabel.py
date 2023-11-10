import os
from dotenv import load_dotenv
load_dotenv()
import argparse
from pymongo import MongoClient
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne
import pandas as pd

from bertopic import BERTopic  # Ensure bertopic is installed （modified）

def add_topic_label(collection):
    '''
    load pretrained bert model and generate topic labeling.
    can adjust batch size to control parallel

    Args:
        collection:

    Returns:

    '''

    import bson

    batch_size = 1000
    topic_model = BERTopic.load("Alprocco/Bert_Ukr_in_Swiss")  # Load your pretrained BERTopic model （modified）
    # Load mapping（modified）
    topic_mapping = {-1: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 0: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Asylum'}, 1: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 2: {'cluster_id': 1.0, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Medical Insurance'}, 3: {'cluster_id': 2.0, 'cluster_name': 'Pet', 'sub_cluster': 'Pet'}, 4: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Asylum'}, 5: {'cluster_id': 3.0, 'cluster_name': 'Transportation', 'sub_cluster': 'Ticket Information'}, 6: {'cluster_id': 3.0, 'cluster_name': 'Transportation', 'sub_cluster': 'Transport to and from Ukraine'}, 7: {'cluster_id': 4.0, 'cluster_name': 'Accommodation', 'sub_cluster': 'Seeking'}, 8: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 9: {'cluster_id': 5.0, 'cluster_name': 'Volunteering', 'sub_cluster': 'Volunteering'}, 10: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Communication'}, 11: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Communication'}, 12: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Passport'}, 13: {'cluster_id': 1.0, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Dentistry'}, 14: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Status Acquisition'}, 15: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Currency'}, 16: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Banking'}, 17: {'cluster_id': 8.0, 'cluster_name': 'Social Services', 'sub_cluster': 'Protocols'}, 18: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Mail'}, 19: {'cluster_id': 9.0, 'cluster_name': 'Education', 'sub_cluster': 'Education'}, 20: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Clothing'}, 21: {'cluster_id': 8.0, 'cluster_name': 'Social Services', 'sub_cluster': 'Financial Assistance'}, 22: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 23: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 24: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Logistics'}, 25: {'cluster_id': 9.0, 'cluster_name': 'Education', 'sub_cluster': 'Education'}, 26: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 27: {'cluster_id': 3.0, 'cluster_name': 'Transportation', 'sub_cluster': 'Public Transportation'}, 28: {'cluster_id': 4.0, 'cluster_name': 'Accommodation', 'sub_cluster': 'Leasing Regulation'}, 29: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 30: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Open Chat'}, 31: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Communication'}, 32: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 33: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 34: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Food'}, 35: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 36: {'cluster_id': 3.0, 'cluster_name': 'Transportation', 'sub_cluster': 'Transport to and from Ukraine'}, 37: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Vehicle'}, 38: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 39: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 40: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Shopping'}, 41: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Currency'}, 42: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Status Acquisition'}, 43: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Consultate Services'}, 44: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 45: {'cluster_id': 3.0, 'cluster_name': 'Transportation', 'sub_cluster': 'Public Transportation'}, 46: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 47: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 48: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Vehicle'}, 49: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Other Item Request'}, 50: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Immigration Procedure'}, 51: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'War Chat'}, 52: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 53: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 54: {'cluster_id': 9.0, 'cluster_name': 'Education', 'sub_cluster': 'Education'}, 55: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Other Item Request'}, 56: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Electronics'}, 57: {'cluster_id': 8.0, 'cluster_name': 'Social Services', 'sub_cluster': 'Financial Assistance'}, 58: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 59: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Leisure and Fitness'}, 60: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Tax'}, 61: {'cluster_id': 4.0, 'cluster_name': 'Accommodation', 'sub_cluster': 'Expense'}, 62: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Other Item Request'}, 63: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 64: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Communication'}, 65: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Other Item Request'}, 66: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 67: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 68: {'cluster_id': 3.0, 'cluster_name': 'Transportation', 'sub_cluster': 'Public Transportation'}, 69: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Family Reunion'}, 70: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 71: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Clothing'}, 72: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 73: {'cluster_id': 3.0, 'cluster_name': 'Transportation', 'sub_cluster': 'Public Transportation'}, 74: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 75: {'cluster_id': 1.0, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Vaccinations'}, 76: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Police'}, 77: {'cluster_id': 8.0, 'cluster_name': 'Social Services', 'sub_cluster': 'Financial Assistance'}, 78: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Regulation'}, 79: {'cluster_id': 3.0, 'cluster_name': 'Transportation', 'sub_cluster': 'Transport to and from Ukraine'}, 80: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 81: {'cluster_id': 1.0, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Medical Request'}, 82: {'cluster_id': 3.0, 'cluster_name': 'Transportation', 'sub_cluster': 'Public Transportation'}, 83: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Parking'}, 84: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 85: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 86: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 87: {'cluster_id': 11.0, 'cluster_name': 'Legal information', 'sub_cluster': 'Legal information'}, 88: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 89: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 90: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Sustainability'}, 91: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Electronics'}, 92: {'cluster_id': 9.0, 'cluster_name': 'Education', 'sub_cluster': 'Education'}, 93: {'cluster_id': 4.0, 'cluster_name': 'Accommodation', 'sub_cluster': 'Seeking'}, 94: {'cluster_id': 12.0, 'cluster_name': 'Religious Information', 'sub_cluster': 'Religious Information'}, 95: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Electronics'}, 96: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 97: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 98: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 99: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 100: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Banking'}, 101: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 102: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Sustainability'}, 103: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Other Item Request'}, 104: {'cluster_id': 8.0, 'cluster_name': 'Social Services', 'sub_cluster': 'Library'}, 105: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Tax'}, 106: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Police'}, 107: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 108: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 109: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Electronics'}, 110: {'cluster_id': 11.0, 'cluster_name': 'Legal information', 'sub_cluster': 'Legal information'}, 111: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Passport'}, 112: {'cluster_id': 9.0, 'cluster_name': 'Education', 'sub_cluster': 'Education'}, 113: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Regulation'}, 114: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Immigration Procedure'}, 115: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 116: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 117: {'cluster_id': 9.0, 'cluster_name': 'Education', 'sub_cluster': 'Education'}, 118: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Job'}, 119: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 120: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 121: {'cluster_id': 4.0, 'cluster_name': 'Accommodation', 'sub_cluster': 'Seeking'}, 122: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Translate Service'}, 123: {'cluster_id': 1.0, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Medical Insurance'}, 124: {'cluster_id': 4.0, 'cluster_name': 'Accommodation', 'sub_cluster': 'Seeking'}, 125: {'cluster_id': 11.0, 'cluster_name': 'Legal information', 'sub_cluster': 'Legal information'}, 126: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 127: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 128: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Water'}, 129: {'cluster_id': 1.0, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Psychotherapy'}, 130: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 131: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Open Chat'}, 132: {'cluster_id': 4.0, 'cluster_name': 'Accommodation', 'sub_cluster': 'Seeking'}, 133: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Immigration Procedure'}, 134: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 135: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Clothing'}, 136: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 137: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 138: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 139: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Tax'}, 140: {'cluster_id': 1.0, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Vaccinations'}, 141: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 142: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Other Item Request'}, 143: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Shopping'}, 144: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 145: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 146: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 147: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Job'}, 148: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Vehicle'}, 149: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 150: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 151: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Status Acquisition'}, 152: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Shopping'}, 153: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Shopping'}, 154: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 155: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 156: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 157: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 158: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Leisure and Fitness'}, 159: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 160: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Communication'}, 161: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Leisure and Fitness'}, 162: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 163: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 164: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 165: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Shopping'}, 166: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 167: {'cluster_id': 3.0, 'cluster_name': 'Transportation', 'sub_cluster': 'Public Transportation'}, 168: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Communication'}, 169: {'cluster_id': 12.0, 'cluster_name': 'Religious Information', 'sub_cluster': 'Religious Information'}, 170: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Shopping'}, 171: {'cluster_id': 3.0, 'cluster_name': 'Transportation', 'sub_cluster': 'Taxi Services'}, 172: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 173: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 174: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Other Item Request'}, 175: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Open Chat'}, 176: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Other Item Request'}, 177: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 178: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 179: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Immigration Procedure'}, 180: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 181: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 182: {'cluster_id': 11.0, 'cluster_name': 'Legal information', 'sub_cluster': 'Divorce'}, 183: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 184: {'cluster_id': 8.0, 'cluster_name': 'Social Services', 'sub_cluster': 'Protocols'}, 185: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Shopping'}, 186: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 187: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Immigration Procedure'}, 188: {'cluster_id': 11.0, 'cluster_name': 'Legal information', 'sub_cluster': 'Marriage'}, 189: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Job'}, 190: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 191: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 192: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Leisure and Fitness'}, 193: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 194: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 195: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Other Item Request'}, 196: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 197: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Leisure and Fitness'}, 198: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Shopping'}, 199: {'cluster_id': 5.0, 'cluster_name': 'Volunteering', 'sub_cluster': 'Volunteering'}, 200: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Job'}, 201: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Logistics'}, 202: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 203: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Consultate Services'}, 204: {'cluster_id': 4.0, 'cluster_name': 'Accommodation', 'sub_cluster': 'Seeking'}, 205: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Other Item Request'}, 206: {'cluster_id': 4.0, 'cluster_name': 'Accommodation', 'sub_cluster': 'Leasing Regulation'}, 207: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Other Item Request'}, 208: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Job'}, 209: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 210: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 211: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 212: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 213: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Infant & Toddler Care '}, 214: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 215: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Infant & Toddler Care '}, 216: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 217: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Regulation'}, 218: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 219: {'cluster_id': 1.0, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Medical Request'}, 220: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Other Item Request'}, 221: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 222: {'cluster_id': 1.0, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Hospice Care'}, 223: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 224: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 225: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Shopping'}, 226: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 227: {'cluster_id': 1.0, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Dentistry'}, 228: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 229: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 230: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 231: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Customs'}, 232: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Shopping'}, 233: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Customs'}, 234: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Customs'}, 235: {'cluster_id': 1.0, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Disability'}, 236: {'cluster_id': 8.0, 'cluster_name': 'Social Services', 'sub_cluster': 'Financial Assistance'}, 237: {'cluster_id': 13.0, 'cluster_name': 'Hoax', 'sub_cluster': 'Hoax'}, 238: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Other Item Request'}, 239: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 240: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Regulation'}, 241: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Electronics'}, 242: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 243: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 244: {'cluster_id': 13.0, 'cluster_name': 'Hoax', 'sub_cluster': 'Hoax'}, 245: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Leisure and Fitness'}, 246: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 247: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 248: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 249: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Leisure and Fitness'}, 250: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Immigration Procedure'}, 251: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Regulation'}, 252: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 253: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Open Chat'}, 254: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 255: {'cluster_id': 1.0, 'cluster_name': 'Healthcare and Insurance', 'sub_cluster': 'Medical Request'}, 256: {'cluster_id': 0.0, 'cluster_name': 'Immigration', 'sub_cluster': 'Immigration Procedure'}, 257: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 258: {'cluster_id': 10.0, 'cluster_name': 'Social Activity', 'sub_cluster': 'Travel'}, 259: {'cluster_id': 8.0, 'cluster_name': 'Social Services', 'sub_cluster': 'Protocols'}, 260: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 261: {'cluster_id': -1.0, 'cluster_name': 'Unknown', 'sub_cluster': 'Unknown'}, 262: {'cluster_id': 6.0, 'cluster_name': 'Integration', 'sub_cluster': 'Job'}, 263: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Other Item Request'}, 264: {'cluster_id': 7.0, 'cluster_name': 'Living Essentials', 'sub_cluster': 'Shopping'}, 265: {'cluster_id': 5.0, 'cluster_name': 'Volunteering', 'sub_cluster': 'Volunteering'}}
    
    selection_criteria = {
        "topicUpdateDate": {'$exists': False},
    }
    projection = {'_id': 1,  'messageText': 1}
    cursor = collection.find_raw_batches(selection_criteria, projection, batch_size=batch_size)

    # Iterate through the cursor in batches
    for batch in cursor:
        data = bson.decode_all(batch)
        df = pd.DataFrame(list(data))

        # Use BERTopic to give topic label to messages in batch         
        documents = df['messageText'].tolist()  
        topics, _ = topic_model.transform(documents) 
        df['predicted_key'] = topics
        df['predicted_class'] = df['predicted_key'].map(lambda x: topic_mapping[x]['cluster_name'])

        # Update the documents in the collection with the new 'predicted_class'
        # By using UpdateOne with the $set operator, the code updates the documents without disturbing any other existing fields
        update_operations = [
            UpdateOne({'_id': row['_id']}, {'$set': {'predicted_class': row['predicted_class'], 'predicted_key': row['predicted_key']}})
            for index, row in df.iterrows()
        ]
        if update_operations:
            collection.bulk_write(update_operations)

if __name__ == '__main__':

    '''
    Add messageDate to the whole collection: scrape.telegram
    use command:
        （1） prd dataset
        python src/pipeline/1_predictTopicLabel.py -o scrape.telegram
        （2） testing dataset
        python src/pipeline/1_predictTopicLabel.py -o test.telegram        
    '''

    # parse parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output_database', help="Specify the output database", required=True)
    args = parser.parse_args()

    # connect to db
    ATLAS_TOKEN = os.environ["ATLAS_TOKEN"]
    ATLAS_USER = os.environ["ATLAS_USER"]
    cluster = MongoClient(
        "mongodb+srv://{}:{}@cluster0.fcobsyq.mongodb.net/".format(ATLAS_USER, ATLAS_TOKEN))
    db_name, collection_name = args.output_database.split('.')
    collection = cluster[db_name][collection_name]

    # update embedding for new coming data
    add_topic_label(collection)

    cluster.close()

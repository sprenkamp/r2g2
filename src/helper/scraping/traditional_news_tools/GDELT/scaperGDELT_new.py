from google.cloud import bigquery

# Constants
GDELT_TABLE = '`gdelt-bq.gdeltv2.events`'
DATE_START = '20230201'
DATE_END = '20230228'

# Establish client
client = bigquery.Client(project='gdelt-bq')

#project ID=gdeltscapper

# This function will generate the WHERE clause based on the search terms
def generate_where_clause(country_code, search_terms):
    terms = ' OR '.join([f"SOURCEURL LIKE '%{term}%'" for term in search_terms])
    return f"(ActionGeo_CountryCode = '{country_code}' AND ({terms}))"

countries = {
    "DE": {"de": ["Ukraine + Flüchtlinge", "Ukraine + flüchten", "Ukraine + Migranten", "Ukraine + migrieren", "Ukraine + Asyl"]},
    "CH": {"de": ["Ukraine + Flüchtlinge", "Ukraine + flüchten", "Ukraine + Migranten", "Ukraine + migrieren", "Ukraine + Asyl"],
           "fr": ["Ukraine + réfugiés", "Ukraine + réfugiant", "Ukraine + migrants", "Ukraine + migrant", "Ukraine + asile"],
           "it": ["Ucraina + rifugiati", "Ucraina + rifugiato", "Ucraina + migranti", "Ucraina + migrante", "Ucraina + asilo"]},
}

for country_code, languages in countries.items():
    for language, search_terms in languages.items():
        where_clause = generate_where_clause(country_code, search_terms)
        
        query = f"""
            SELECT *
            FROM {GDELT_TABLE}
            WHERE SQLDATE BETWEEN {DATE_START} AND {DATE_END} AND {where_clause}

        """
        
        query_job = client.query(query)
        results = query_job.result()
        
        for row in results:
            print(row)

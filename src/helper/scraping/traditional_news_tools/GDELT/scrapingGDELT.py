from google.cloud import bigquery

client = bigquery.Client(project='gdeltscrapper')

query = """
    SELECT SQLDATE
    FROM `gdelt-bq.gdeltv2.events`
    WHERE ActionGeo_CountryCode = 'US'
    AND SQLDATE BETWEEN '20230201' AND '20230228'
    LIMIT 10
"""

query_job = client.query(query)

results = query_job.result()

for row in results:
    print(row)
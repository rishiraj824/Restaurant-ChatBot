import boto3
import json

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

categories = ["japanese", "chinese", "indian", "cafes", "burgers"]

def put_into_elasticsearch():
    client = boto3.client("es")

    host = "search-chat-concierge-cloud-anq6myrjo7reh4vgcawtoq3v6u.us-east-1.es.amazonaws.com"
    region = "us-east-1"

    service = "es"
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service)

    es = Elasticsearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )

    for c in categories:
        # Re-read crawled data
        fn = "yelp-restaurants.json".format(c)
        with open(fn, "r") as f:
            rawjson = json.load(f)

        for biz in rawjson["yelp-restaurants"]:
            restID = biz["id"]
            cuis = biz["categories"]

            # Prepare the document to be put
            document = {
                "restaurantId" : restID,
                "cuisine": cuis
            }
            es.index(index="restaurants", doc_type="Restaurant", id=restID, body=document)

            # Verify that the document was successfully indexed
            check = es.get(index="restaurants", doc_type="Restaurant", id=restID)
            if check["found"]:
                print("Index %s succeeded" % restID)


put_into_elasticsearch()

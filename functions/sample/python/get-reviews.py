'''
getting dealership review by dealer ID 
'''

import sys

from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    databaseName = "reviews"

    # Create the authenticator.
    authenticator = IAMAuthenticator(dict["IAM_API_KEY"])
    
    # Construct the service instance.
    service = CloudantV1(authenticator)
    
    service.set_service_url(dict["COUCH_URL"])

    try:

        # version-01 [https://github.com/IBM/cloudant-python-sdk/blob/master/examples/getAllDbs/example_request.py]: 
        #response = service.get_all_dbs().get_result()
        
        # version-02 [https://github.com/IBM/cloudant-python-sdk/blob/master/examples/postAllDocs/example_request.py]:
        # response = service.post_all_docs(
        #     db=databaseName,
        #     include_docs=True,
        #     limit=10
        #     ).get_result()
            
        # version-03 :    
        response = service.post_find(
            db=databaseName,
            selector={'dealership': {'$eq': int(dict["dealer_ID"])}},
            ).get_result()
        
        result= {
            'headers': {'Content-Type':'application/json'}, 
            'body': {'data':response} 
        }        
        return result
        
    except:
        return {
            'statusCode': 404,
            'message': 'function_error: get_reviews'
        }

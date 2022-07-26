'''
posting dealership reviews
'''

import sys

from ibmcloudant.cloudant_v1 import Document, CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    databaseName = "reviews"

    # Create the authenticator.
    authenticator = IAMAuthenticator(dict["IAM_API_KEY"])
    
    # Construct the service instance.
    service = CloudantV1(authenticator)
    
    service.set_service_url(dict["COUCH_URL"])

    
    '''
    # version-01 [https://github.com/IBM/cloudant-python-sdk/blob/master/examples/postDocument/example_request.py]:
    try:
        reviews_doc = Document( 
            id = dict["id"],
            name = dict["name"]
            dealership = dict["dealership"],
            review = dict["review"],
            purchase = dict["purchase"],
            purchase_date = dict["purchase_date"],
            car_make = dict["car_make"],
            car_model = dict["car_model"],
            car_year = dict["car_year"]
        )
        
        response = service.post_document(db=databaseName, document=reviews_doc).get_result()
        
        result= {
            'headers': {'Content-Type':'application/json'}, 
            'body': {'data':response},
            'message': 'cloud_function_success: post_review' 
        }        
        
        return result
        
    except:
        return {
            'statusCode': 404,
            'message': 'cloud_function_error: post_review'
        }

    
    '''
    '''
    # version-02:
    '''
    try:
        review_doc = dict["review"]
        
        response = service.post_document(db=databaseName, document=review_doc).get_result()
        
        result= {
            'headers': {'Content-Type':'application/json'}, 
            'body': {'data':response},
            'message': 'cloud_function_success: post_review' 
        }        
        
        return result
        
    except:
        return {
            'statusCode': 404,
            'message': 'cloud_function_error: post_review'
        }
    
import os
import requests
import json

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions, EntitiesOptions, KeywordsOptions

# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

from django.conf import settings

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)



# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        '''
        version-01:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        '''
        
        '''
        version-02
        '''
        api_key = kwargs.get("api_key")
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            
            # Basic authentication GET
            response = requests.get(url, 
                    params=params, 
                    headers= {
                        'Content-Type': 'application/json'
                    }, 
                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # no authentication GET
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)

    except:
        # If any error occurs
        print("Network exception occurred")
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data



# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# Create a get_dealers_from_cf method to get dealers by state (i.e., st) from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):

    results = []

    '''
    version-01:

    '''

    try:
        state = kwargs['st']
    except:
        state = ""
    
    if not state:
        # Call get_request with a URL parameter
        json_result = get_request(url)
    else:     
        # Call get_request with a URL parameter
        json_result = get_request(url, state)


    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealers_from_cf method to get dealer by dealer_id from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealer_by_id(url, dealer_id):
    result = []
    print("dealer_id[get_dealer_by_id in restapis]", dealer_id)
    json_result = get_request(url, id=dealer_id)
    
    if json_result:
        # Get the row list in JSON as dealer
        print("json_result['docs'] [get_dealer_by_id in restapis]", json_result["docs"])

        dealer = json_result["docs"]
        # Get its content in `doc` object
        dealer_doc = dealer[0]


        print("dealer_doc [get_dealer_by_id in restapis]:")
        print(dealer_doc)

        # Create a CarDealer object with values in `dealer_doc` object
        '''
        version-01: 
        '''
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"], st=dealer_doc["st"], state=dealer_doc["state"],
                                   zip=dealer_doc["zip"])


        print("dealer_obj:")
        print(dealer_obj)

        print("dealer_obj.id:", dealer_obj.id)
        print()

        print("dealer_id", dealer_id)

        result.append(dealer_obj)

    return result


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):

    results = []
    dealer_id = kwargs['dealer_id']
        
    # Call get_request with a URL parameter
    json_result = get_request(url, dealer_id=dealer_id)
    
    print("json_result[get_dealer_reviews_from_cf in restapis.py]", json_result)

    if json_result:
        # Get the row list in JSON as reviews
        reviews = json_result["body"]["data"]["docs"]

        print("reviews", reviews)

        # For each review object
        for review in reviews:
            # Get its content in review object
            # That is, create a CarDealer object with values in review object
            
            review_obj = DealerReview(
                dealership=review["dealership"], name=review["name"], review=review["review"],
                purchase=review["purchase"], sentiment=analyze_review_sentiments(review["review"]), id=review["id"])
            '''
            Optional fields
            '''
            if "purchase_date" in review:
                review_obj.purchase_date = review["purchase_date"]
            if "purchase_date" in review:
                review_obj.car_make = review["car_make"]
            if "car_model" in review:
                review_obj.car_model = review["car_model"]
            if "car_year" in review:
                review_obj.car_year = review["car_year"]

            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
    
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealer_review):

    sentiment_result = []

    # version-01:
    api_key = settings.SENTIMENT_API_KEY
    api_url = settings.SENTIMENT_API_URL
    # version-02:
    # api_key = os.getenv('SENTIMENT_ANALYZER_API_KEY')
    # api_url = os.getenv('SENTIMENT_ANALYZER_API_URL')

    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator)

    natural_language_understanding.set_service_url(api_url)

    '''
    version-01:
    .. sectionauthor:: Coursera. IBM. Course-06. Module-05.
    .. sectionauthor:: https://cloud.ibm.com/apidocs/natural-language-understanding?code=python#analyze

        response = natural_language_understanding.analyze(
        text=dealer_review,
        features=Features(
        entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
        keywords=KeywordsOptions(emotion=True, sentiment=True,
                                 limit=2))).get_result()
    '''
    response = natural_language_understanding.analyze(
        text=dealer_review,
        language='en',
        features=Features(
        sentiment=SentimentOptions(),
        entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
        keywords=KeywordsOptions(emotion=True, sentiment=True, limit=2)))
        

    sentiment_result = response.result['sentiment']
    
    sentiment = sentiment_result['document']['label']

    return sentiment

def post_request(url, json_payload, **kwargs):
    print("kwargs [post_request in restapis.py]", kwargs)
    print("json_payload [post_request in restapis.py]", json_payload)
    print("POST from {} ".format(url))
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, params=kwargs, json=json_payload)

    except:
        # If any error occurs
        print("Network exception occurred")
    
    status_code = response.status_code
    print("With status {} ".format(status_code))

    print(" -------------------------------------------------------------------------------------- ")

    print("response.content [post_request in restapis]: ", response.content)
    print("response.headers [post_request in restapis]: ", response.headers)

    json_data = json.loads(response.text)
    print("json_data [post_request in restapis.py]:")
    print("json_data [post_request in restapis.py]: ", json_data)



    print(" -------------------------------------------------------------------------------------- ")

    return json_data

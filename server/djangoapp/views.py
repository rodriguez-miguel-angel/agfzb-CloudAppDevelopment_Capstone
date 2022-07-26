from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel, CarDealer
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_by_id, get_dealer_reviews_from_cf, post_request

from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging

import json


# Get an instance of a logger
logger = logging.getLogger(__name__)


# global 
counter = 10

# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

'''
.. sectionauthor:: Coursera. IBM. Course-09. Module-05.

'''

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/registration.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)
'''
version-01:

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)
'''

'''
version-02:
'''
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        #url = "your-cloud-function-domain/dealerships/dealer-get"
        url = "https://33a5508d.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context['dealership_list'] = dealerships
        # Return a list of dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        #url = "your-cloud-function-domain/dealerships/dealer-get"
        dealer_url = "https://33a5508d.us-south.apigw.appdomain.cloud/api/dealership"
        review_url = "https://33a5508d.us-south.apigw.appdomain.cloud/api/review"
        # Get dealer from the URL and dealer_id
        dealer = get_dealer_by_id(dealer_url, dealer_id)[0]
        context['dealership'] = dealer

        print("dealer[get_dealer_details in views]:", dealer)
        print("dealer.id [get_dealer_details in views]:", dealer.id)


        # Get reviews from the dealer
        reviews = get_dealer_reviews_from_cf(review_url, dealer_id=dealer_id)
        context['review_list'] = reviews
        # Return a list of reviews
        return render(request, 'djangoapp/dealer_details.html', context)    

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    context = {}

    # Get user object, then check if user is authenticated because only authenticated users can post reviews for a dealer
    user = request.user
    if(user.is_authenticated):

        print("request[add_review]", request) 
        print()
        print("dealer_id[add_review]", dealer_id)
        print()


        #url = "your-cloud-function-domain/dealerships/dealer-get"
        dealer_url = "https://33a5508d.us-south.apigw.appdomain.cloud/api/dealership"
        review_url = "https://33a5508d.us-south.apigw.appdomain.cloud/api/review"
        # Get dealer from the URL and dealer_id
        dealer = get_dealer_by_id(dealer_url, dealer_id=dealer_id)[0]
        context['dealership'] = dealer

        print("dealer[add_review in views.py]:", dealer)
        print()
        print("dealer.id [add_review in views.py]:", dealer.id)

        #print("dealer[add_review]", dealer)
        print()
        

        if request.method == "GET" :            
            cars = CarModel.objects.all()
            
            print("cars",cars)
            # car = get_object_or_404(CarModel, pk=car_id)
            
            context['cars'] = cars

            return render(request, 'djangoapp/add_review.html', context)
            #return HttpResponseRedirect(reverse(viewname='djangoapp:dealer_details.html', args=(dealer.id)))

        if request.method == "POST":
            #url = "your-cloud-function-domain/dealerships/dealer-get"
            review_url = "https://33a5508d.us-south.apigw.appdomain.cloud/api/review"
            # Get json payload from the request
            '''
            Create a dictionary object called review to append keys like (time, name, dealership, review, purchase). 
            And any attributes you defined in your review-post cloud function.
            '''
            review = {}
            review["time"] = datetime.utcnow().isoformat()
            
            global counter
            counter += 1
            review['id'] = counter
            print("counter: ", counter)

            name = user.first_name + ' ' + user.last_name
            review["name"] = name    
            review["dealership"] = dealer_id
            review["review"] = request.POST['content']

            # create and initialize purchase
            purchase = False
            print("request.POST:", request.POST)

            if "allow-purchase-information" in request.POST:
                if request.POST["allow-purchase-information"] == 'on':
                    purchase = True
                else: 
                    purchase = False
            
            print("purchase [add_review in views.py]", purchase)
            review["purchase"] = purchase

            if purchase:                
                review["purchase_date"] = request.POST['purchase_date']
                car_id = request.POST['car']
                car = CarModel.objects.get(pk=car_id)
                review["car_make"] = car.car_make.name
                review["car_model"] = car.name
                review["car_year"] = car.year.strftime("%Y")


            '''
            Create another dictionary object called json_payload with one key called review. 
            The json_payload will be used as the request body.
            '''
            json_payload = {}
            json_payload["review"] = review

            result = post_request(review_url, json_payload, dealer_id=dealer_id)

            print("result[add_review in views.py]: ", result)
            context['result'] = result
            context['message'] = "Success: Review added."
            # Redirect to dealer_details with the dealer id
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)    
    else:
        '''
        version-01:
        return (json.dumps({}), 403)
        '''
        
        '''
        version-02:
        '''
        context['message'] = "Error: User is unauthenticated."
        return render(request, 'djangoapp/add_review.html', context)
        
        

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return(render(request, 'djangoapp/about.html', context))


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return(render(request, 'djangoapp/contact.html', context))

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
            context['message'] = "Invalid username or password"
            return render(request, 'djangoapp/index.html',context)
    else:
        return render(request, 'djangoapp/index.html',context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == "POST":
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

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/matthew-riddle_space1-mr/dealership-package/dealership"
        
        context["dealerships"] = get_dealers_from_cf(url)

        
        return render(request, 'djangoapp/index.html', context)




# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    context = {}
    if request.method == "GET":
        url = f'https://us-east.functions.appdomain.cloud/api/v1/web/matthew-riddle_space1-mr/dealership-package/review?id={id}'
        reviews = get_dealer_reviews_from_cf(url, id=id)

        print("REVIEWS")
        print(reviews)

        context = {
            "reviews":  reviews, 
            "dealer_id": id
        }

        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):

    if request.user.is_authenticated:

        if request.method == "GET":
            url = f'https://us-east.functions.appdomain.cloud/api/v1/web/matthew-riddle_space1-mr/dealership-package/dealership?id={dealer_id}'
            context = {
                "cars": CarModel.objects.all(),
                "dealer": get_dealers_from_cf(url),
            }
            print(CarModel.objects.count())
            return render(request, 'djangoapp/add_review.html', context)
        if request.method == "POST":
            form = request.POST
            review = dict()
            review["name"] = f"{request.user.first_name} {request.user.last_name}"
            review["dealership"] = dealer_id
            review["review"] = form["content"]
            review["purchase"] = form.get("purchasecheck")
            if review["purchase"]:
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
            car = CarModel.objects.get(pk=form["car"])
            review["car_make"] = car.car_make.name
            review["car_model"] = car.name
            review["car_year"] = car.car_year

            if form.get("purchasecheck"):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
            else: 
                review["purchase_date"] = None

            url = "https://us-east.functions.appdomain.cloud/api/v1/web/matthew-riddle_space1-mr/dealership-package/review"
            json_payload = {"review" : review}

            result = post_request(url, json_payload, dealerId=dealer_id)
            if int(result.status_code) == 200:
                print("Review posted successfully.")

            return redirect("djangoapp:dealer_details", id=dealer_id)

    else:
        print("please log in")
        return redirect('djangoapp:login')


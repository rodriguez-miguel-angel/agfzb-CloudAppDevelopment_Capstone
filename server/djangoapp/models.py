import sys
import datetime

from django.utils.timezone import now
from django.utils import timezone

try:
    from django.db import models
    from django.core.validators import MaxValueValidator, MinValueValidator
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

# CarMake model
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
# CarModel model
class CarModel(models.Model):

    # Many-To-One relationship to CarMake model (One car make has many car models, using a ForeignKey field)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE) # car_make_id
    
    name = models.CharField(null=False, max_length=200)
    # Dealer Id (IntegerField) refers to a dealer created in Cloudant database
    '''
    version-01:
    dealer_id = models.IntegerField(null=False) # dealer_id
    
    version-02:
    dealer_id = models.ForeignKey(CarDealer, on_delete=models.CASCADE) # dealer_id
    '''
    dealer_id = models.IntegerField(null=False) # dealer_id


    SEDAN = 'sedan'
    SUV = 'sports_utility_vehicle'
    WAGON = 'station_wagon'
    HATCHBACK = 'hatchback'
    CUV = 'crossover_utility_vehicle'
    COUPE = 'coupe'
    ELECTRIC = 'electric'
    TRUCK = 'pickup_truck'
    MPV = 'minivan'

    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'Sports Utility Vehicle'),
        (WAGON, 'Station Wagon'),
        (HATCHBACK, 'Hatchback'),
        (CUV, "Crossover Utility Vehicle"),
        (COUPE, "Coupe"),
        (ELECTRIC, "Electric"),
        (TRUCK, "Pickup Truck"),
        (MPV, "Minivan")
    ]

    type = models.CharField(
        null=False,
        max_length=50,
        choices=TYPE_CHOICES,
        default=SEDAN
    )

    '''
    version-01:
    year = models.DateField(null=False)
    version-02:
    year = models.DateField(null=False, default=datetime.datetime.now().year)
    '''
    year = models.DateField(null=False, default=datetime.datetime.now().year)

    '''
    version-03:
    .. sectionauthor:: stackoverflow.

    year = models.IntegerField(null=False, validators=[MinValueValidator(1908), MaxValueValidator(datetime.datetime.now().year + 1)], default=datetime.datetime.now().year)
     
    # Format 'year' to datetime object. Convert `year` to str if it is `IntergerField`. ex: str(self.year).
    @property
    def get_year(self):
        date = timezone.datetime.strptime('%Y', str(self.year))  
        return date

    '''
    
    def __str__(self):
        return "Dealer Id: " + str(self.dealer_id) + "," + \
               "Name: " + self.name + "," + \
               "Type: " + self.type + "," + \
               "Year: " + str(self.year)

    

'''

a plain Python class `CarDealer` to hold dealer data

'''
# CarDealer model
class CarDealer(models.Model):
    full_name = models.CharField(max_length=200, default="full_name")
    short_name = models.CharField(max_length=100, default="short_name")
    address =  models.CharField(max_length=200, default="address")
    city =  models.CharField(max_length=200, default="city")
    state =  models.CharField(max_length=200, default="state")
    st =  models.CharField(max_length=5, default="st")
    zip =  models.CharField(max_length=20, default="zip")
    lat = models.FloatField(default=37.662937, validators=[MaxValueValidator(90), MinValueValidator(-90)]) # Latitude
    long = models.FloatField(default=-122.433014, validators=[MaxValueValidator(180), MinValueValidator(-180)]) # Longitude
    

    def __str__(self):
        return "Full Name: " + self.full_name + "," + \
                "Short Name: " + self.short_name + "," + \
                "Address: " + self.address + "," + \
                "City: " + self.city + "," + \
                "State: " + self.state + "," + \
                "ST: " + self.st + "," + \
                "Zip: " + self.zip + "," + \
                "Latitude: " + self.lat + "," + \
                "Longitude: " + self.long


'''
a plain Python class `DealerReview` to hold review data

'''
# DealerReview model
class DealerReview(models.Model):
    dealership = models.ForeignKey(CarDealer, on_delete=models.CASCADE) # dealer_id

    name = models.CharField(max_length=200, default="name")
    review = models.CharField(max_length=1000)
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(default=now)

    car_make = models.CharField(max_length=100, default="car_make")
    car_model = models.CharField(max_length=100, default="car_model")
    car_year = models.CharField(max_length=20, default="car_year")


    def __str__(self):
        return "Full Name: " + self.name + "," + \
                "Review: " + self.review + "," + \
                "Purchase: " + self.purchase + "," + \
                "Purchase Date: " + self.purchase_date + "," + \
                "Car Make: " + self.car_make + "," + \
                "Car Model: " + self.car_model + "," + \
                "Car Year: " + self.car_year
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path('about/', views.about, name='about'),
    # path for contact us view
    path('contact/', views.contact, name='contact'),
    # path for registration [sectionauthor:: Coursera. IBM. Course-09. Module-05.]
    path('registration/', views.registration_request, name='registration'),
    # path for login [sectionauthor:: Coursera. IBM. Course-09. Module-05.]
    path('login/', views.login_request, name='login'),
    # path for logout [sectionauthor:: Coursera. IBM. Course-09. Module-05.] 
    path('logout/', views.logout_request, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer details view
    # ex: /dealer/15/
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path('dealer/<int:dealer_id>/review/', views.add_review, name='add_review')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
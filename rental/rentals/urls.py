from django.urls import path, include
from . import views
from django.views.generic import RedirectView
app_name = 'rentals'

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars_list, name='cars_list'),
    path('all/', views.rentals_list, name='rentals_list'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
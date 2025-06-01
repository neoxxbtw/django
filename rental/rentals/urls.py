from django.urls import path, include
from . import views
from django.views.generic import RedirectView
app_name = 'rentals'

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars_list, name='cars_list'),
    path('all/', views.rentals_list, name='rentals_list'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('favorite/<int:car_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_cars, name='favorite_cars'),
    path('car/add/', views.car_add, name='car_add'),
    path('car/<int:pk>/edit/', views.car_edit, name='car_edit'),
    path('car/<int:pk>/delete/', views.car_delete, name='car_delete'),


]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
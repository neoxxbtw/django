from django.contrib import admin
from django.urls import path, include
from rentals import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rentals/', include('rentals.urls', namespace='rentals')),
    path('all/', views.rentals_list, name='rentals_list'),
    path('', views.landing_page, name='landing_page'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.shortcuts import render
from django.db.models import Count, Sum, Avg
from django.utils.timezone import now
from datetime import timedelta
from .models import Car, Rental, Payment
from django.shortcuts import render, get_object_or_404

def landing_page(request):
    return render(request, 'rentals/index.html')


def index(request):
    search_query = request.GET.get('q', '')

    available_cars = Car.objects.filter(is_available=True)
    if search_query:
        available_cars = available_cars.filter(brand__icontains=search_query)

    popular_cars = Car.objects.annotate(
        rental_count=Count('rental')
    ).order_by('-rental_count')[:3]

    latest_rentals = Rental.objects.order_by('-start_date')[:5]

    payments_stats = Payment.objects.aggregate(
        total_amount=Sum('amount'),
        count=Count('id'),
        avg_amount=Avg('amount'),
    )

    return render(request, 'rentals/index.html', {
        'available_cars': available_cars,
        'popular_cars': popular_cars,
        'latest_rentals': latest_rentals,
        'payments_stats': payments_stats,
        'search_query': search_query,
    })


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'rentals/car_detail.html', {'car': car})

def cars_list(request):
    cars = Car.objects.all()  # пример
    return render(request, 'rentals/cars_list.html', {'cars': cars})

def cars_list(request):
    cars = Car.objects.all()

    # Фильтры
    brand = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_year = request.GET.get('min_year')
    max_year = request.GET.get('max_year')
    max_mileage = request.GET.get('max_mileage')
    sort_by = request.GET.get('sort_by')

    if brand:
        cars = cars.filter(brand__icontains=brand)
    if min_price:
        cars = cars.filter(rental_cost_per_day__gte=min_price)
    if max_price:
        cars = cars.filter(rental_cost_per_day__lte=max_price)
    if min_year:
        cars = cars.filter(year__gte=min_year)
    if max_year:
        cars = cars.filter(year__lte=max_year)
    if max_mileage:
        cars = cars.filter(mileage__lte=max_mileage)

    if sort_by == 'price':
        cars = cars.order_by('rental_cost_per_day')
    elif sort_by == '-price':
        cars = cars.order_by('-rental_cost_per_day')
    elif sort_by == '-popularity':
        cars = cars.order_by('-rental_count')

    return render(request, 'rentals/cars_list.html', {
        'cars': cars
    })

def rentals_list(request):
    rentals = Rental.objects.all()
    return render(request, 'rentals/rentals_list.html', {'rentals': rentals})

def rentals_list(request):
    return render(request, 'rentals/rentals_list.html')


from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Sum, Avg
from django.utils.timezone import now
from .models import Car, Rental, Payment
from datetime import timedelta


def landing_page(request):
    return render(request, 'rentals/index.html')


def index(request):
    search_query = request.GET.get('q', '')
    brand = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_year = request.GET.get('min_year')
    max_year = request.GET.get('max_year')
    max_mileage = request.GET.get('max_mileage')
    sort_by = request.GET.get('sort_by')

    available_cars = Car.objects.filter(is_available=True)

    if search_query:
        available_cars = available_cars.filter(brand__icontains=search_query)
    if brand:
        available_cars = available_cars.filter(brand__icontains=brand)
    if min_price:
        available_cars = available_cars.filter(rental_cost_per_day__gte=min_price)
    if max_price:
        available_cars = available_cars.filter(rental_cost_per_day__lte=max_price)
    if min_year:
        available_cars = available_cars.filter(year__gte=min_year)
    if max_year:
        available_cars = available_cars.filter(year__lte=max_year)
    if max_mileage:
        available_cars = available_cars.filter(mileage__lte=max_mileage)

    if sort_by == 'price':
        available_cars = available_cars.order_by('rental_cost_per_day')
    elif sort_by == '-price':
        available_cars = available_cars.order_by('-rental_cost_per_day')
    elif sort_by == '-popularity':
        available_cars = available_cars.annotate(rental_count=Count('rental')).order_by('-rental_count')

    popular_cars = Car.objects.annotate(rental_count=Count('rental')).order_by('-rental_count')[:3]
    latest_rentals = Rental.objects.select_related('car', 'client').order_by('-start_date')[:5]
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
        'request': request,
    })


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'rentals/car_detail.html', {'car': car})


def cars_list(request):
    cars = Car.objects.all()

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
        cars = cars.annotate(rental_count=Count('rental')).order_by('-rental_count')

    return render(request, 'rentals/cars_list.html', {'cars': cars})


def rentals_list(request):
    rentals = Rental.objects.all()

# Страница со списком избранных авто
def favorite_cars(request):
    favorite_ids = request.session.get('favorites', [])
    cars = Car.objects.filter(id__in=favorite_ids)
    return render(request, 'rentals/favorites.html', {'cars': cars})

def toggle_favorite(request, car_id):
    favorites = request.session.get('favorites', [])
    car_id_str = str(car_id)

    if car_id_str in favorites:
        favorites.remove(car_id_str)
    else:
        favorites.append(car_id_str)

    request.session['favorites'] = favorites
    return redirect(request.META.get('HTTP_REFERER', 'rentals:index'))


# --- Сложная бизнес-логика ---
def is_car_available(car, start_date, end_date):
    overlapping = Rental.objects.filter(
        car=car,
        end_date__gte=start_date,
        start_date__lte=end_date
    )
    return not overlapping.exists()


def calculate_rental_cost(car, start_date, end_date, extra_services_cost=0):
    duration_days = (end_date - start_date).days + 1
    base_cost = car.rental_cost_per_day * duration_days
    return base_cost + extra_services_cost

from .forms import CarForm

def car_add(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('rentals:cars_list')
    else:
        form = CarForm()
    return render(request, 'rentals/car_form.html', {'form': form, 'title': 'Добавить автомобиль'})


def car_edit(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('rentals:car_detail', pk=pk)
    else:
        form = CarForm(instance=car)
    return render(request, 'rentals/car_form.html', {'form': form, 'title': 'Редактировать автомобиль'})


def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car.delete()
        return redirect('rentals:cars_list')
    return render(request, 'rentals/car_delete.html', {'car': car})

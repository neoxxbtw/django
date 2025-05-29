from django.contrib import admin
from .models import Client, Car, Rental, Damage, Maintenance, ExtraService, Payment
from django.utils.html import format_html

class ExtraServiceInline(admin.TabularInline):
    model = ExtraService
    extra = 1


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1


class DamageInline(admin.TabularInline):
    model = Damage
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "driver_license")
    search_fields = ("full_name", "phone", "driver_license")
    list_display_links = ("full_name",)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "license_plate", "year", "is_available", "rental_cost_per_day", "mileage", "image")
    list_filter = ("is_available", "year", "color")
    search_fields = ("brand", "model", "license_plate")
    list_display_links = ("brand", "model")

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image.url)
        return "Нет фото"

    image_preview.short_description = 'Фото'


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = (
        "client", "car", "start_date", "end_date", "is_available",
        "duration_display", "total_cost_display"
    )
    list_filter = ("is_available", "start_date")
    date_hierarchy = "start_date"
    raw_id_fields = ("client", "car")
    search_fields = ("client__full_name", "car__license_plate")
    inlines = [ExtraServiceInline, PaymentInline, DamageInline]
    readonly_fields = ("duration_days", "total_cost")
    list_display_links = ("client", "car")

    @admin.display(description="Срок аренды (дн.)")
    def duration_display(self, obj):
        return obj.duration_days

    @admin.display(description="Итоговая стоимость")
    def total_cost_display(self, obj):
        return f"{obj.total_cost:.2f} ₽" if obj.total_cost else "-"


@admin.register(Damage)
class DamageAdmin(admin.ModelAdmin):
    list_display = ("car", "damage_type", "repair_cost")
    list_filter = ("car",)
    search_fields = ("damage_type", "car__license_plate")
    raw_id_fields = ("rental",)
    readonly_fields = ("car",)


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ("car", "service_date", "mileage")
    date_hierarchy = "service_date"
    search_fields = ("car__license_plate",)
    list_filter = ("car",)
    raw_id_fields = ("car",)


@admin.register(ExtraService)
class ExtraServiceAdmin(admin.ModelAdmin):
    list_display = ("rental", "service_name", "service_cost")
    search_fields = ("service_name",)
    raw_id_fields = ("rental",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("client", "rental", "amount", "payment_type")
    list_filter = ("payment_type",)
    search_fields = ("client__full_name",)
    raw_id_fields = ("client", "rental")

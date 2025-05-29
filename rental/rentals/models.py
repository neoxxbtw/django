from django.db import models


class Client(models.Model):
    full_name = models.CharField("ФИО клиента", max_length=255)
    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)
    driver_license = models.CharField("Водительское удостоверение", max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.full_name


class Car(models.Model):
    brand = models.CharField("Марка", max_length=50)
    model = models.CharField("Модель", max_length=50)
    year = models.IntegerField("Год выпуска")
    license_plate = models.CharField("Гос. номер", max_length=9)
    color = models.CharField("Цвет", max_length=20, blank=True, null=True)
    mileage = models.IntegerField("Пробег", blank=True, null=True)
    rental_cost_per_day = models.DecimalField("Цена за день", max_digits=10, decimal_places=2)
    is_available = models.BooleanField(verbose_name="Доступен", default=True)
    image = models.ImageField(verbose_name="Добавить фото", upload_to='car_images/', blank=True, null=True)

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"


class Rental(models.Model):
    client = models.ForeignKey(Client, verbose_name="Клиент", on_delete=models.CASCADE)
    car = models.ForeignKey(Car, verbose_name="Автомобиль", on_delete=models.CASCADE, related_name='rental')
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата окончания")
    cost_per_day = models.IntegerField("Стоимость в день")
    is_available = models.BooleanField(verbose_name="Активна", default=True)

    duration_days = models.IntegerField("Длительность аренды", editable=False)
    total_cost = models.DecimalField("Итого", max_digits=10, decimal_places=2, editable=False)

    class Meta:
        verbose_name = "Аренда"
        verbose_name_plural = "Аренды"

    def __str__(self):
        return f"Аренда #{self.pk} - {self.client}"

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.duration_days = (self.end_date - self.start_date).days + 1
            self.total_cost = self.duration_days * self.cost_per_day
        super().save(*args, **kwargs)


class Damage(models.Model):
    rental = models.ForeignKey(Rental, verbose_name="Аренда", on_delete=models.CASCADE)
    car = models.ForeignKey(Car, verbose_name="Автомобиль", on_delete=models.CASCADE, editable=False)
    damage_type = models.TextField("Тип повреждения")
    repair_cost = models.DecimalField("Стоимость ремонта", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Повреждение"
        verbose_name_plural = "Повреждения"

    def save(self, *args, **kwargs):
        if self.rental:
            self.car = self.rental.car
        super().save(*args, **kwargs)



class Maintenance(models.Model):
    car = models.ForeignKey(Car, verbose_name="Авто", on_delete=models.CASCADE)
    service_date = models.DateField("Дата обслуживания")
    description = models.TextField("Описание")
    mileage = models.IntegerField("Пробег на момент обслуживания", blank=True, null=True)

    class Meta:
        verbose_name = "Обслуживание"
        verbose_name_plural = "Обслуживания"

    def __str__(self):
        return f"{self.car} - {self.service_date}"


class ExtraService(models.Model):
    rental = models.ForeignKey(Rental, verbose_name="Аренда", on_delete=models.CASCADE)
    service_name = models.CharField("Доп. услуга", max_length=255)
    service_cost = models.DecimalField("Стоимость", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Дополнительная услуга"
        verbose_name_plural = "Дополнительные услуги"

    def __str__(self):
        return self.service_name


class Payment(models.Model):
    rental = models.ForeignKey(Rental, verbose_name="Аренда", on_delete=models.CASCADE)
    client = models.ForeignKey(Client, verbose_name="Клиент", on_delete=models.CASCADE)
    amount = models.DecimalField("Сумма", max_digits=10, decimal_places=2)
    payment_type = models.CharField("Тип оплаты", max_length=15)

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.amount} ₽ - {self.payment_type}"

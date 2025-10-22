from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class RentalListing(models.Model):
    """Модель объектов недвижимости."""
    PROPERTY_TYPES = [
        ('apartment', 'Апартаменты'),
        ('house', 'Дом'),
        ('flat', 'Квартира'),
        ('villa', 'Вилла')
    ]

    # Базовая информация о помещении
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    address = models.CharField('Адрес', max_length=400)
    property_type = models.CharField('Тип жилья', choices=PROPERTY_TYPES)

    # Детали аренды(стоимость, максимальное колличество гостей и т.д.)
    price_per_night = models.DecimalField(
        'Цена за ночь',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1),]
    )
    max_guests = models.PositiveSmallIntegerField(
        'Максимальное колличество гостей',
        validators=[MinValueValidator(1),]
    )
    bedrooms = models.PositiveSmallIntegerField(
        'Спальных компнат',
        validators=[MinValueValidator(1),]
    )
    bathrooms = models.PositiveSmallIntegerField(
        'Ванных комнат',
        validators=[MinValueValidator(1),]
    )

    # Удобства
    amenities = models.TextField('Удобства')

    # Геолокация на будущее
    latitude = models.FloatField('Широта', null=True, blank=True)
    longitude = models.FloatField('Долгота', null=True, blank=True)

    # Владелец и статусы
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='listings',
        verbose_name='Владелец'
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Изменено', auto_now=True)

    class Meta:
        verbose_name = 'Недвижимость'
        verbose_name_plural = 'Недвижимости'

    def __str__(self):
        return f'{self.title} - {self.property_type} - {self.price_per_night}'
    

class Booking(models.Model):
    """Модель бронирования."""
    STATUS_CHOICES = [
        ('pending', 'Рассматривается'),
        ('confirmed', 'Подтверждён'),
        ('cancelled', 'Отменён'),
        ('completed', 'Исполнен')
    ]

    # Необходимые связи
    rental_listing = models.ForeignKey(
        RentalListing,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Список объектов недвижимости'
    )
    guest = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Гость'
    )

    # Даты бронировани + кол-во гостей
    check_in_date = models.DateField('Дата начала бронирования')
    check_out_date = models.DateField('Дата окончания бронирования')
    guest_count = models.PositiveSmallIntegerField(
        'Колличество посетителей',
        validators=[MinValueValidator(1),]
    )

    # Статус и стоимость
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    total_price = models.DecimalField(
        'Общая цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0),]
    )

    # Даты создания/изменения
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Изменено', auto_now=True)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f'Бронирование №{self.id} - {self.rental_listing.title}'
    
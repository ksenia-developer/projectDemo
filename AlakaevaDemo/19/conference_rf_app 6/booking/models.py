from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField('ФИО', max_length=180)
    phone = models.CharField('Телефон', max_length=30)

    def __str__(self):
        return self.full_name or self.user.username

class Room(models.Model):
    ROOM_TYPES = [
        ('auditorium', 'Аудитория'),
        ('coworking', 'Коворкинг'),
        ('cinema', 'Кинозал'),
    ]
    name = models.CharField('Название', max_length=120)
    room_type = models.CharField('Тип помещения', max_length=30, choices=ROOM_TYPES)
    capacity = models.PositiveIntegerField('Вместимость', default=20)
    description = models.TextField('Описание', blank=True)

    class Meta:
        ordering = ['room_type', 'name']

    def __str__(self):
        return f'{self.name} ({self.get_room_type_display()})'

class Application(models.Model):
    STATUS_NEW = 'new'
    STATUS_ASSIGNED = 'assigned'
    STATUS_DONE = 'done'
    STATUS_CHOICES = [
        (STATUS_NEW, 'Новая'),
        (STATUS_ASSIGNED, 'Мероприятие назначено'),
        (STATUS_DONE, 'Мероприятие завершено'),
    ]
    PAYMENT_CHOICES = [
        ('card', 'Банковская карта'),
        ('cash', 'Наличные'),
        ('invoice', 'Счет для организации'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications', verbose_name='Пользователь')
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='applications', verbose_name='Помещение')
    conference_date = models.DateField('Дата начала конференции')
    payment_method = models.CharField('Способ оплаты', max_length=20, choices=PAYMENT_CHOICES)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлена', auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Заявка #{self.pk}: {self.user.username} — {self.room.name}'

    @property
    def can_review(self):
        return self.status != self.STATUS_NEW and not hasattr(self, 'review')

class Review(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='review', verbose_name='Заявка')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews', verbose_name='Пользователь')
    rating = models.PositiveSmallIntegerField('Оценка')
    text = models.TextField('Отзыв')
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв {self.rating}/5 к заявке #{self.application_id}'

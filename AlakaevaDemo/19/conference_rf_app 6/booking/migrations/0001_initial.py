# Generated manually for demo exam project
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('room_type', models.CharField(choices=[('auditorium', 'Аудитория'), ('coworking', 'Коворкинг'), ('cinema', 'Кинозал')], max_length=30, verbose_name='Тип помещения')),
                ('capacity', models.PositiveIntegerField(default=20, verbose_name='Вместимость')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
            options={
                'ordering': ['room_type', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=180, verbose_name='ФИО')),
                ('phone', models.CharField(max_length=30, verbose_name='Телефон')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conference_date', models.DateField(verbose_name='Дата начала конференции')),
                ('payment_method', models.CharField(choices=[('card', 'Банковская карта'), ('cash', 'Наличные'), ('invoice', 'Счет для организации')], max_length=20, verbose_name='Способ оплаты')),
                ('status', models.CharField(choices=[('new', 'Новая'), ('assigned', 'Мероприятие назначено'), ('done', 'Мероприятие завершено')], default='new', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создана')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлена')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='applications', to='booking.room', verbose_name='Помещение')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(verbose_name='Оценка')),
                ('text', models.TextField(verbose_name='Отзыв')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='booking.application', verbose_name='Заявка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]

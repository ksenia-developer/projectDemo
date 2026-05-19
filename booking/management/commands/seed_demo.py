from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from booking.models import Room

class Command(BaseCommand):
    help = 'Создам демонстрационного администратора Admin26/Demo20 и помещения'

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(username='Admin26', defaults={'email': 'admin26@example.local', 'is_staff': True, 'is_superuser': True})
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password('Demo20')
        admin.save()
        admin.profile.full_name = 'Администратор демоэкзамена'
        admin.profile.phone = '+7 000 000-00-00'
        admin.profile.save()

        rooms = [
            ('Аудитория Север', 'auditorium', 80, 'Просторная аудитория для докладов и лекций.'),
            ('Аудитория Восток', 'auditorium', 120, 'Зал с проектором и удобной посадкой.'),
            ('Коворкинг Центр', 'coworking', 35, 'Гибкое пространство для рабочих групп.'),
            ('Коворкинг Лаборатория', 'coworking', 45, 'Помещение для командной работы и мастер-классов.'),
            ('Кинозал Премьер', 'cinema', 160, 'Кинозал для презентаций и медиапоказов.'),
            ('Кинозал Малый', 'cinema', 70, 'Компактный зал с большим экраном.'),
        ]
        for name, room_type, capacity, description in rooms:
            Room.objects.get_or_create(name=name, defaults={'room_type': room_type, 'capacity': capacity, 'description': description})
        self.stdout.write(self.style.SUCCESS('Готово: Admin26/Demo20 и демонстрационные помещения созданы.'))

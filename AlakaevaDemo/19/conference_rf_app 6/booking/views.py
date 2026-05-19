from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ApplicationForm, LoginForm, RegisterForm, ReviewForm
from .models import Application, Review, Room


def home(request):
    rooms = Room.objects.all()[:6]
    reviews = Review.objects.select_related('user', 'application__room')[:4]
    return render(request, 'booking/home.html', {'rooms': rooms, 'reviews': reviews})


def rooms_list(request):
    room_type = request.GET.get('type', '')
    rooms = Room.objects.all()
    if room_type in dict(Room.ROOM_TYPES):
        rooms = rooms.filter(room_type=room_type)
    return render(request, 'booking/rooms.html', {
        'rooms': rooms,
        'room_types': Room.ROOM_TYPES,
        'current_type': room_type,
    })


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )
            user.profile.full_name = form.cleaned_data['full_name']
            user.profile.phone = form.cleaned_data['phone']
            user.profile.save()
            login(request, user)
            messages.success(request, 'Регистрация выполнена. Добро пожаловать!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'booking/form.html', {'form': form, 'title': 'Регистрация', 'button': 'Зарегистрироваться'})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if form.get_user().username == 'Admin26':
                return redirect('admin_panel')
            return redirect('dashboard')
        messages.error(request, 'Неверный логин или пароль.')
    else:
        form = LoginForm()
    return render(request, 'booking/form.html', {'form': form, 'title': 'Авторизация', 'button': 'Войти'})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    applications = request.user.applications.select_related('room').all()
    return render(request, 'booking/dashboard.html', {'applications': applications})


@login_required
def application_create(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Заявка создана и отправлена администратору.')
            return redirect('dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'booking/form.html', {'form': form, 'title': 'Оформление заявки', 'button': 'Отправить заявку'})


@login_required
def review_create(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    if not application.can_review:
        messages.warning(request, 'Отзыв можно оставить только после изменения статуса заявки администратором и только один раз.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.application = application
            review.user = request.user
            review.save()
            messages.success(request, 'Спасибо, отзыв сохранен.')
            return redirect('dashboard')
    else:
        form = ReviewForm()
    return render(request, 'booking/form.html', {'form': form, 'title': f'Отзыв по заявке #{application.pk}', 'button': 'Сохранить отзыв'})


def is_demo_admin(user):
    return user.is_authenticated and user.username == 'Admin26'


@user_passes_test(is_demo_admin, login_url='login')
def admin_panel(request):
    applications = Application.objects.select_related('user', 'room').all()
    status = request.GET.get('status', '')
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '-created_at')
    allowed_sorts = ['created_at', '-created_at', 'conference_date', '-conference_date', 'status', 'room__name']
    if status:
        applications = applications.filter(status=status)
    if search:
        applications = applications.filter(Q(user__username__icontains=search) | Q(room__name__icontains=search) | Q(user__profile__full_name__icontains=search))
    if sort in allowed_sorts:
        applications = applications.order_by(sort)
    paginator = Paginator(applications, 5)
    page_obj = paginator.get_page(request.GET.get('page'))
    stats = Application.objects.values('status').annotate(total=Count('id'))
    return render(request, 'booking/admin_panel.html', {
        'page_obj': page_obj,
        'statuses': Application.STATUS_CHOICES,
        'current_status': status,
        'search': search,
        'sort': sort,
        'stats': stats,
        'new_count': Application.objects.filter(status=Application.STATUS_NEW).count(),
    })


@user_passes_test(is_demo_admin, login_url='login')
def admin_change_status(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, f'Статус заявки #{application.pk} изменен.')
    return redirect('admin_panel')

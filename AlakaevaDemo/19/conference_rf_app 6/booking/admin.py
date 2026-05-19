from django.contrib import admin
from .models import Application, Profile, Review, Room

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'user')
    search_fields = ('full_name', 'phone', 'user__username')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_type', 'capacity')
    list_filter = ('room_type',)
    search_fields = ('name', 'description')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'conference_date', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'room__room_type', 'payment_method')
    search_fields = ('user__username', 'user__profile__full_name', 'room__name')
    ordering = ('-created_at',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('text', 'user__username')

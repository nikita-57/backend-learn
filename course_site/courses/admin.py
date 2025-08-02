
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Course, Lesson, Material, UserProgress

# Регистрируем стандартные модели
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Material)
admin.site.register(UserProgress)

# Если нужно добавить кастомные поля в админку пользователя
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    
    # Добавляем фильтрацию по группам и правам
    filter_horizontal = ('groups', 'user_permissions',)

# Перерегистрируем стандартную модель User с кастомной админкой
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
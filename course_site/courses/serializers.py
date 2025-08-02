from rest_framework import serializers
from .models import Course, Lesson, Material, UserProgress
from django.contrib.auth import get_user_model

User = get_user_model()

# Базовые сериализаторы
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    materials = MaterialSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'students', 'lessons', 'created_at']

# Сериализаторы для прогресса
class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = '__all__'
        read_only_fields = ['completed_at']

class CourseWithProgressSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    lessons_completed = serializers.SerializerMethodField()
    total_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'progress', 'lessons_completed', 'total_lessons']

    def get_progress(self, obj):
        user = self.context.get("request").user
        if not user.is_authenticated:
            return 0
            
        completed = UserProgress.objects.filter(
            user=user, 
            course=obj, 
            is_completed=True
        ).count()
        total_lessons = obj.lessons.count()
        
        return round((completed / total_lessons) * 100, 2) if total_lessons > 0 else 0

    def get_lessons_completed(self, obj):
        user = self.context.get("request").user
        if not user.is_authenticated:
            return 0
            
        return UserProgress.objects.filter(
            user=user,
            course=obj,
            is_completed=True
        ).count()

    def get_total_lessons(self, obj):
        return obj.lessons.count()
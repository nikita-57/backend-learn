from rest_framework import serializers
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson, Material  # Импортируем модели из courses

User = get_user_model()  # Получаем модель пользователя (стандартную или кастомную)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]  # Добавил базовые поля
        extra_kwargs = {
            'email': {'required': True}  # Делаем email обязательным
        }

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"
        read_only_fields = ['id', 'created_at']  # Защищаем от изменения

class LessonSerializer(serializers.ModelSerializer):
    materials = MaterialSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ['id', 'created_at']  # Защищаем от изменения

class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    students = UserSerializer(many=True, read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    students_count = serializers.SerializerMethodField()  # Добавляем счетчик студентов
    
    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'instructor']  # Защищаем от изменения
        
    def get_students_count(self, obj):
        return obj.students.count()  # Добавляем информацию о количестве студентов
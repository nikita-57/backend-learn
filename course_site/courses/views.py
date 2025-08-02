from django.utils import timezone  # Добавлено
from rest_framework import viewsets, permissions
from .models import Course, Lesson, Material, UserProgress  # Добавлено UserProgress
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound  # Добавлено для обработки ошибок
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    MaterialSerializer,
    CourseWithProgressSerializer,
    UserProgressSerializer  
)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
    
    @action(detail=True, methods=["post"])
    def complete_lesson(self, request, pk=None):
        course = self.get_object()
        lesson_id = request.data.get("lesson_id")
        
        try:
            lesson = Lesson.objects.get(id=lesson_id, course=course)  # Проверяем, что урок принадлежит курсу
        except Lesson.DoesNotExist:
            raise NotFound("Урок не найден или не принадлежит этому курсу.")
        
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            course=course,
            lesson=lesson,
        )
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()
        
        return Response({"status": "Lesson marked as completed"})

    @action(detail=False, methods=["get"])
    def my_courses(self, request):
        courses = Course.objects.filter(students=request.user)
        serializer = CourseWithProgressSerializer(
            courses,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
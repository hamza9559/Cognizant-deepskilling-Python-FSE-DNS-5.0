from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import hello_view, DepartmentViewSet, CourseViewSet, StudentViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'students', StudentViewSet)
router.register(r'enrollments', EnrollmentViewSet)

urlpatterns = [
    path('hello/', hello_view, name='hello'),  # /api/hello/
    path('', include(router.urls)),           # Auto-generates standard /api/courses/, etc.
]
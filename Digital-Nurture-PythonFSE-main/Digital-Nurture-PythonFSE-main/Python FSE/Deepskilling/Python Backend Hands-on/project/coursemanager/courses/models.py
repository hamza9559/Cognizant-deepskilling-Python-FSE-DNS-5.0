from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)
    head_of_dept = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.head_of_dept})"
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code}- ({self.name})"
    
class Student(models.Model):
    name= models.CharField(max_length=100)
    reg_no= models.CharField(max_length=20)
    email= models.EmailField()
    department= models.ForeignKey(Department, on_delete=models.CASCADE)
    enrollment_year= models.IntegerField()

    def __str__(self):
        return f"{self.name}-({self.reg_no})"
    
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=2, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course') 
    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.name} on {self.enrollment_date}"
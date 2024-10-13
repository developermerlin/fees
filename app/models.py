from django.db import models

# Create your models here.
GENDER = (
        ('Male','Male'),
        ('Female','Female'),
)


LEVEL = (
    ('First Year','First Year'),
    ('Second Year','Second Year'),
    ('Third Year','Third Year'),
    ('Final Year','Final Year')
)


class Department(models.Model):
    department_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.department_name

class Program(models.Model):
    program_name = models.CharField(max_length=100)
    program_duration = models.PositiveIntegerField()  # Duration in months or years
    program_fees = models.DecimalField(max_digits=10, decimal_places=2)  # Fees as a currency
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    def __str__(self):
        return self.program_name
    

# ======student model=============
class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)  # Unique student ID
    student_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    level = models.CharField(max_length=50, choices=LEVEL)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to='profiles/', blank=True)

    def __str__(self):
        return self.student_name

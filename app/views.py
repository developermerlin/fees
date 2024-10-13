
from django.shortcuts import render, redirect
from .models import Student, Program, Department
from django.shortcuts import get_object_or_404
from django.contrib import messages
# Create your views here.

def first_home(request):
    return render(request, 'first_home.html')

def main_home(request):
    return render(request, 'main_home.html')



# Add Students
def student(request):
    if request.method == 'POST':
        # Extracting form data
        student_id = request.POST.get('student_id')
        student_name = request.POST.get('student_name')
        gender = request.POST.get('gender')
        department_name = request.POST.get('department')
        program_id = request.POST.get('program')
        email = request.POST.get('email')
        level = request.POST.get('level')
        phone = request.POST.get('phone')
        file = request.FILES.get('file')

        # Fetching the Department and Program instances
        department = Department.objects.get(department_name=department_name)
        program = Program.objects.get(id=program_id)

        # Creating the Student instance
        student = Student(
            student_id=student_id,
            student_name=student_name,
            gender=gender,
            program=program,
            email=email,
            level=level,
            phone=phone,
            department=department,
            profile=file
        )

        # Save the student instance
        student.save()

        # Add a success message
        messages.success(request, "Student information saved successfully!")

        return redirect('student')  

    # If it's a GET request, render the form
    departments = Department.objects.all()
    programs = Program.objects.all()
    students = Student.objects.all()
    return render(request, 'student.html', {
        'students':students,
        'departments': departments,
        'programs': programs,
    })

#  Edit Students
def edit_student(request, student_id):
    # Get the student object by ID
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        # Update student data with the new form data
        student.student_id = request.POST.get('student_id')
        student.student_name = request.POST.get('student_name')
        student.gender = request.POST.get('gender')
        department_name = request.POST.get('department')
        program_id = request.POST.get('program')
        student.email = request.POST.get('email')
        student.level = request.POST.get('level')
        student.phone = request.POST.get('phone')

        # Fetching the Department and Program instances
        department = Department.objects.get(department_name=department_name)
        program = Program.objects.get(id=program_id)

        student.department = department
        student.program = program

        # If a new file is uploaded, update the profile image
        if request.FILES.get('file'):
            student.profile = request.FILES.get('file')

        # Save the updated student
        student.save()

        # Add a success message
        messages.success(request, "Student information updated successfully!")

        return redirect('student')  # Redirect to the student list

    # If it's a GET request, render the edit form with the student's current data
    departments = Department.objects.all()
    programs = Program.objects.all()

    return render(request, 'edit_student.html', {
        'student': student,
        'departments': departments,
        'programs': programs
    })


#  Delete Student
def delete_student(request, student_id):
    # Get the student object by ID
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        # Delete the student record
        student.delete()
        # Add a success message
        messages.success(request, "Student information deleted successfully!")
        return redirect('student')  # Redirect back to the student list
    return render(request, 'delete_student.html')


# View Student

def view_student(request, student_id):
    # Get the student object by ID
    student = get_object_or_404(Student, id=student_id)
    # Render the student detail template
    return render(request, 'view_student.html', {
        'student': student,
    })

 
 
 
# Create A new program
def program(request):
    programs = Program.objects.all()
    if request.method == 'POST':
        program_name = request.POST.get('program_name')
        program_duration = request.POST.get('program_duration')
        program_fees = request.POST.get('program_fees')
        department_id = request.POST.get('department')

        department = get_object_or_404(Department, id=department_id)

        # Create and save the new Program
        program = Program(
            program_name=program_name,
            program_duration=program_duration,
            program_fees=program_fees,
            department=department
        )
        program.save()

        messages.success(request, "Program created successfully!")
        return redirect('program')

    departments = Department.objects.all()
    return render(request, 'program.html', {'departments': departments,'programs':programs,})



# Edit a program
def edit_program(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    if request.method == 'POST':
        program.program_name = request.POST.get('program_name')
        program.program_duration = request.POST.get('program_duration')
        program.program_fees = request.POST.get('program_fees')
        department_id = request.POST.get('department')
        program.department = get_object_or_404(Department, id=department_id)

        program.save()
        messages.success(request, "Program updated successfully!")
        return redirect('program')

    departments = Department.objects.all()
    return render(request, 'edit_program.html', {
        'program': program,
        'departments': departments
    })
    
    
# Delete a program
def delete_program(request, program_id):
    if request.method == 'POST':
        program = get_object_or_404(Program, id=program_id)
        program.delete()
        messages.success(request, "Program deleted successfully!")
        return redirect('program')
    return render(request, 'delete_program.html')

from django.shortcuts import render, redirect # type: ignore
from .models import Student, Department, CS_Cost1, CS_Cost2, CS_Cost3, CS_Cost4,Programs,CS_Fees1,CS_Fees2,CS_Fees3,CS_Fees4
from django.shortcuts import get_object_or_404 # type: ignore
from django.contrib import messages # type: ignore
from django.http import JsonResponse # type: ignore
from decimal import Decimal
from django.utils import timezone # type: ignore
from django.core.exceptions import ValidationError # type: ignore
from django.utils.dateparse import parse_date # type: ignore
from django.utils.dateparse import parse_date # type: ignore

def first_home(request):
    return render(request, 'first_home.html')

def main_home(request):
    return render(request, 'main_home.html')

def main_second_home(request):
    return render(request, 'main_second_home.html')



# Add Students
def student(request):
    if request.method == 'POST':
        # Extracting form data
        student_id = request.POST.get('student_id')
        student_name = request.POST.get('student_name')
        gender = request.POST.get('gender')
        department_name = request.POST.get('department')
        program_id = request.POST.get('program_id')  # This matches the form

        email = request.POST.get('email')
        phone = request.POST.get('phone')
        file = request.FILES.get('file')

        try:
            # Fetching the Department and Program instances
            department = get_object_or_404(Department, department_name=department_name)
            program = get_object_or_404(Programs, id=program_id)

            # Creating the Student instance
            student = Student(
                student_id=student_id,
                student_name=student_name,
                gender=gender,
                program=program,
                email=email,
                phone=phone,
                department=department,
                profile=file
            )

            # Save the student instance
            student.save()

            # Add a success message
            messages.success(request, "Student information saved successfully!")

            return redirect('student')  

        except Department.DoesNotExist:
            messages.error(request, "The specified department does not exist.")
        except Programs.DoesNotExist:
            messages.error(request, "The specified program does not exist.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    # If it's a GET request, render the form
    departments = Department.objects.all()
    programs = Programs.objects.all()
    students = Student.objects.all()
    return render(request, 'student.html', {
        'students': students,
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
        # student.level = request.POST.get('level')
        student.phone = request.POST.get('phone')

        # Fetching the Department and Program instances
        department = Department.objects.get(department_name=department_name)
        program = Programs.objects.get(id=program_id)

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
    programs = Programs.objects.all()

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
def department(request):
    programs = Department.objects.all()
    if request.method == 'POST':
        department_name = request.POST.get('department_name')

        department = Department(
            department_name=department_name,
        )
        department_name = department.department_name
        department.save()

        messages.success(request, f"{department_name} created successfully!")
        return redirect('department')

    departments = Department.objects.all()
    return render(request, 'department.html', {'departments': departments})



def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    
    if request.method == 'POST':
        department_name = request.POST.get('department_name') 
        department.department_name = department_name  
        department.save() 
        messages.success(request, f"{department_name} updated successfully!")
        return redirect('department')

    return render(request, 'edit_department.html', {
        'department': department
    })
    
    
# Delete a program
def delete_department(request, department_id):
    if request.method == 'POST':
        department = get_object_or_404(Department, id=department_id)
        department_name = department.department_name
        department.delete()
        messages.success(request, f"{department_name} deleted successfully!")
        return redirect('department')
    return render(request, 'delete_department.html')



# Create A new program
def all_program(request):
    programs = Programs.objects.all()
    if request.method == 'POST':
        program_name = request.POST.get('program_name')
        department_id = request.POST.get('department')

        department = get_object_or_404(Department, id=department_id)

        # Create and save the new Program
        program = Programs(
            program_name=program_name,
            department=department
        )
        program.save()

        messages.success(request, "Program created successfully!")
        return redirect('all_program')

    departments = Department.objects.all()
    return render(request, 'all_program.html', {'departments': departments,'programs':programs,})



# Edit a program
def edit_all_program(request, program_id):
    program = get_object_or_404(Programs, id=program_id)
    if request.method == 'POST':
        program.program_name = request.POST.get('program_name')
        department_id = request.POST.get('department')
        program.department = get_object_or_404(Department, id=department_id)

        program.save()
        messages.success(request, "Program updated successfully!")
        return redirect('all_program')

    departments = Department.objects.all()
    return render(request, 'edit_all_program.html', {
        'program': program,
        'departments': departments
    })
    
    
# Delete a program
def delete_all_program(request, program_id):
    if request.method == 'POST':
        program = get_object_or_404(Programs, id=program_id)
        program.delete()
        messages.success(request, "Program deleted successfully!")
        return redirect('all_program')
    return render(request, 'delete_all_program.html')




# Create A new program cost

def cs_cost1(request):
    programs = CS_Cost1.objects.all()  # Query for existing Program entries
    if request.method == 'POST':
        program_duration = request.POST.get('program_duration')
        program_fees = request.POST.get('program_fees')
        department_id = request.POST.get('department')
        all_program_id = request.POST.get('all_program_id')  # Get the all_program_id from the form

        # Fetch the department and the related Programs (all_program)
        department = get_object_or_404(Department, id=department_id)
        all_program = get_object_or_404(Programs, id=all_program_id)  # Fetch from Programs model

        # Now create and save the new Program
        new_program = CS_Cost1(
            program_name=all_program.program_name,  # Get the program name from the selected all_program
            program_duration=program_duration,
            program_fees=program_fees,
            department=department,
            all_program=all_program,  # Link it to the selected all_program
        )
        new_program.save()

        messages.success(request, "Program Cost created successfully!")
        return redirect('cs_cost1')

    departments = Department.objects.all()
    all_programs = Programs.objects.all()  # Fetch all Programs to display in the form dropdown

    return render(request, 'cs_cost1.html', {
        'departments': departments,
        'programs': programs,
        'all_programs': all_programs,  # Send all_programs to the template
    })


# Edit a program
def edit_cs_cost1(request, program_id):
    program = get_object_or_404(CS_Cost1, id=program_id)
    if request.method == 'POST':
        program.program_name = request.POST.get('program_name')
        program.program_duration = request.POST.get('program_duration')
        program.program_fees = request.POST.get('program_fees')
        department_id = request.POST.get('department')
        program.department = get_object_or_404(Department, id=department_id)

        program.save()
        messages.success(request, "Program Cost updated successfully!")
        return redirect('cs_cost1')

    departments = Department.objects.all()
    return render(request, 'edit_cs_cost1.html', {
        'program': program,
        'departments': departments
    })
    
# Delete a program
def delete_cs_cost1(request, program_id):
    if request.method == 'POST':
        program = get_object_or_404(CS_Cost1, id=program_id)
        program.delete()
        messages.success(request, "Program Cost deleted successfully!")
        return redirect('cs_cost1')
    return render(request, 'delete_cs_cost1.html')



# level two

def cs_cost2(request):
    programs = CS_Cost2.objects.all()  
    if request.method == 'POST':
        program_duration = request.POST.get('program_duration')
        program_fees = request.POST.get('program_fees')
        department_id = request.POST.get('department')
        all_program_id = request.POST.get('all_program_id')  

        # Fetch the department and the related Programs (all_program)
        department = get_object_or_404(Department, id=department_id)
        all_program = get_object_or_404(Programs, id=all_program_id)  # Fetch from Programs model

        # Now create and save the new Program
        new_program = CS_Cost2(
            program_name=all_program.program_name,  # Get the program name from the selected all_program
            program_duration=program_duration,
            program_fees=program_fees,
            department=department,
            all_program=all_program,  # Link it to the selected all_program
        )
        new_program.save()

        messages.success(request, "Program created successfully!")
        return redirect('cs_cost2')

    departments = Department.objects.all()
    all_programs = Programs.objects.all()  # Fetch all Programs to display in the form dropdown

    return render(request, 'cs_cost2.html', {
        'departments': departments,
        'programs': programs,
        'all_programs': all_programs,  # Send all_programs to the template
    })




def edit_cs_cost2(request, program_id):
    program = get_object_or_404(CS_Cost2, id=program_id)
    if request.method == 'POST':
        program.program_name = request.POST.get('program_name')
        program.program_duration = request.POST.get('program_duration')
        program.program_fees = request.POST.get('program_fees')
        department_id = request.POST.get('department')
        program.department = get_object_or_404(Department, id=department_id)

        program.save()
        messages.success(request, "Program Cost updated successfully!")
        return redirect('cs_cost2')

    departments = Department.objects.all()
    return render(request, 'edit_cs_cost2.html', {
        'program': program,
        'departments': departments
    })


def delete_cs_cost2(request, program_id):
    if request.method == 'POST':
        program = get_object_or_404(CS_Cost2, id=program_id)
        program.delete()
        messages.success(request, "Program Cost deleted successfully!")
        return redirect('cs_cost2')
    return render(request, 'delete_cs_cost2.html')
    


# level three

def cs_cost3(request):
    programs = CS_Cost3.objects.all()  
    if request.method == 'POST':
        program_duration = request.POST.get('program_duration')
        program_fees = request.POST.get('program_fees')
        department_id = request.POST.get('department')
        all_program_id = request.POST.get('all_program_id')  

        # Fetch the department and the related Programs (all_program)
        department = get_object_or_404(Department, id=department_id)
        all_program = get_object_or_404(Programs, id=all_program_id)  # Fetch from Programs model

        # Now create and save the new Program
        new_program = CS_Cost3(
            program_name=all_program.program_name,  # Get the program name from the selected all_program
            program_duration=program_duration,
            program_fees=program_fees,
            department=department,
            all_program=all_program,  # Link it to the selected all_program
        )
        new_program.save()

        messages.success(request, "Program Cost created successfully!")
        return redirect('cs_cost3')

    departments = Department.objects.all()
    all_programs = Programs.objects.all()  # Fetch all Programs to display in the form dropdown

    return render(request, 'cs_cost3.html', {
        'departments': departments,
        'programs': programs,
        'all_programs': all_programs,  # Send all_programs to the template
    })

def edit_cs_cost3(request, program_id):
    program = get_object_or_404(CS_Cost3, id=program_id)
    if request.method == 'POST':
        program.program_name = request.POST.get('program_name')
        program.program_duration = request.POST.get('program_duration')
        program.program_fees = request.POST.get('program_fees')
        department_id = request.POST.get('department')
        program.department = get_object_or_404(Department, id=department_id)

        program.save()
        messages.success(request, "Program Cost updated successfully!")
        return redirect('cs_cost3')

    departments = Department.objects.all()
    return render(request, 'edit_cs_cost3.html', {
        'program': program,
        'departments': departments
    })


def delete_cs_cost3(request, program_id):
    if request.method == 'POST':
        program = get_object_or_404(CS_Cost3, id=program_id)
        program.delete()
        messages.success(request, "Program Cost deleted successfully!")
        return redirect('cs_cost3')
    return render(request, 'delete_cs_cost3.html')
    



def cs_cost4(request):
    programs = CS_Cost4.objects.all()  
    if request.method == 'POST':
        program_duration = request.POST.get('program_duration')
        program_fees = request.POST.get('program_fees')
        department_id = request.POST.get('department')
        all_program_id = request.POST.get('all_program_id')  

        # Fetch the department and the related Programs (all_program)
        department = get_object_or_404(Department, id=department_id)
        all_program = get_object_or_404(Programs, id=all_program_id)  # Fetch from Programs model

        # Now create and save the new Program
        new_program = CS_Cost4(
            program_name=all_program.program_name,  # Get the program name from the selected all_program
            program_duration=program_duration,
            program_fees=program_fees,
            department=department,
            all_program=all_program,  # Link it to the selected all_program
        )
        new_program.save()

        messages.success(request, "Program created successfully!")
        return redirect('cs_cost4')

    departments = Department.objects.all()
    all_programs = Programs.objects.all()  # Fetch all Programs to display in the form dropdown

    return render(request, 'cs_cost4.html', {
        'departments': departments,
        'programs': programs,
        'all_programs': all_programs,  # Send all_programs to the template
    })



def edit_cs_cost4(request, program_id):
    program = get_object_or_404(CS_Cost4, id=program_id)
    if request.method == 'POST':
        program.program_name = request.POST.get('program_name')
        program.program_duration = request.POST.get('program_duration')
        program.program_fees = request.POST.get('program_fees')
        department_id = request.POST.get('department')
        program.department = get_object_or_404(Department, id=department_id)

        program.save()
        messages.success(request, "Program Cost updated successfully!")
        return redirect('cs_cost4')

    departments = Department.objects.all()
    return render(request, 'edit_cs_cost4.html', {
        'program': program,
        'departments': departments
    })


def delete_cs_cost4(request, program_id):
    if request.method == 'POST':
        program = get_object_or_404(CS_Cost4, id=program_id)
        program.delete()
        messages.success(request, "Program deleted successfully!")
        return redirect('cs_cost4')
    return render(request, 'delete_cs_cost4.html')
    


# ========================================computer science first year fees==================================================================

def cs_fees1(request):
    fees1 = CS_Fees1.objects.all()
    cs_cost1 = CS_Cost1.objects.all()
    departments = Department.objects.all()  
    all_programs = Programs.objects.all()  

    if request.method == 'POST':
        # Get form values
        id_number = request.POST.get('id_number')
        student_name = request.POST.get('student_name')
        level = request.POST.get('level')
        department_id = request.POST.get('department')
        program_id = request.POST.get('program')
        cost_of_program_id = request.POST.get('cost_of_program')
        sum_of = request.POST.get('sum_of')
        amount_paid_str = request.POST.get('amount_paid', '0')
        payment_date_str = request.POST.get('payment_date')
        second_payment_date_str = request.POST.get('second_payment_date')
        payment_status = request.POST.get('payment_status')
        payment_slip = request.FILES.get('payment_slip')
        check_no_str = request.POST.get('check_no')  
        paid_for_str = request.POST.get('paid_for', 'Tuition Fees')  

        # Convert the amount paid to Decimal
        new_payment = Decimal(amount_paid_str)

        # Validate and parse the dates
        payment_date = parse_date(payment_date_str)
        if not payment_date:
            messages.error(request, "Please enter a valid payment date.")
            return redirect('cs_fees1')  # Redirect to the form in case of error
        
        second_payment_date = parse_date(second_payment_date_str) if second_payment_date_str else None

        # Fetch the department and program objects
        department = get_object_or_404(Department, id=department_id)
        program = get_object_or_404(Programs, id=program_id)
        cost_of_program = get_object_or_404(CS_Cost1, id=cost_of_program_id)

        # Check if a fees record exists for the student
        existing_fees = CS_Fees1.objects.filter(id_number=id_number, program=program, department=department).first()

        if existing_fees:
            # If record exists, update it
            existing_fees.paid_fees += new_payment  
            existing_fees.amount_paid = new_payment
            existing_fees.payment_date = payment_date  
            existing_fees.second_payment_date = second_payment_date
            existing_fees.payment_status = payment_status

            if payment_slip:
                existing_fees.payment_slip = payment_slip
            
            # Update check_no and paid_for if provided
            if check_no_str:
                existing_fees.check_no = check_no_str
            existing_fees.paid_for = paid_for_str  

            existing_fees.save()
            messages.success(request, "Fees details updated successfully!")
        else:
            fees1 = CS_Fees1(
                id_number=id_number,
                student_name=student_name,
                level=level,
                department=department,
                program=program,  
                cost_of_program=cost_of_program,
                amount_paid=new_payment,
                sum_of=sum_of,
                paid_fees=new_payment,
                payment_date=payment_date,  
                second_payment_date=second_payment_date,  
                payment_status=payment_status,
                payment_slip=payment_slip,
                check_no=check_no_str,  
                paid_for=paid_for_str,  
            )
            fees1.save()
            messages.success(request, "New fees entry created successfully!")

        return redirect('cs_fees1')

    return render(request, 'cs_fees1.html', {
        'cs_cost1': cs_cost1,
        'fees1': fees1,
        'departments': departments,
        'all_programs': all_programs,  
    })


def edit_cs_fees1(request, fee_id):
    fees_entry = get_object_or_404(CS_Fees1, id=fee_id)
    cs_cost1 = CS_Cost1.objects.all()
    departments = Department.objects.all()
    all_programs = Programs.objects.all()

    if request.method == 'POST':
        # Update fee entry with other fields
        fees_entry.student_name = request.POST.get('student_name')
        fees_entry.id_number = request.POST.get('id_number')
        fees_entry.department = get_object_or_404(Department, id=request.POST.get('department'))
        fees_entry.program = get_object_or_404(Programs, id=request.POST.get('program'))
        fees_entry.cost_of_program = get_object_or_404(CS_Cost1, id=request.POST.get('cost_of_program'))
        fees_entry.sum_of = request.POST.get('sum_of')  # Added sum_of field
        fees_entry.check_no = request.POST.get('check_no')  # Added check_no field
        fees_entry.paid_for = request.POST.get('paid_for', 'Tuition Fees')  # Default to 'Tuition Fees'

        # Handle new payment
        new_payment_str = request.POST.get('amount_paid', '0')
        new_payment = Decimal(new_payment_str)

        # Add the new payment and update the paid fees and balance
        fees_entry.add_payment(new_payment)

        # Parse the payment dates
        payment_date_str = request.POST.get('payment_date', '')
        second_payment_date_str = request.POST.get('second_payment_date', '')

        payment_date = parse_date(payment_date_str)  # Convert string to date object
        second_payment_date = parse_date(second_payment_date_str)  # Convert string to date object

        # Validate payment dates
        if not payment_date:
            messages.error(request, "Invalid payment date format. Please provide a valid date.")
            return redirect('edit_cs_fees1', fee_id=fee_id)

        fees_entry.payment_date = payment_date
        if second_payment_date:  # Only update second_payment_date if it's provided
            fees_entry.second_payment_date = second_payment_date
        else:
            fees_entry.second_payment_date = None  # Ensure it's set to None if not provided

        fees_entry.payment_status = request.POST.get('payment_status')

        # Handle payment slips if provided
        payment_slip = request.FILES.get('payment_slip')
        second_payment_slip = request.FILES.get('second_payment_slip')
        if payment_slip:
            fees_entry.payment_slip = payment_slip
        if second_payment_slip:
            fees_entry.second_payment_slip = second_payment_slip

        # Save the updated fees entry
        fees_entry.save()

        messages.success(request, "Fees details updated successfully!")
        return redirect('cs_fees1')

    return render(request, 'edit_cs_fees1.html', {
        'fees_entry': fees_entry,
        'cs_cost1': cs_cost1,
        'departments': departments,
        'all_programs': all_programs,
    })



def view_cs_fees1(request, fee_id):
    # Get the fee record by ID
    fee_record = get_object_or_404(CS_Fees1, id=fee_id)
    current_date = timezone.now().date()
    # Render the fee detail template
    return render(request, 'view_cs_fees1.html', {
        'fee_record': fee_record,
        'current_date': current_date,
    })

# computer science year one fees transaction

def cs1_transaction(request):
    fees1 = CS_Fees1.objects.all()
    return render(request, 'cs1_transaction.html', {'fees1':fees1})

def view_cs1_transaction(request, trans_id):
    # Get the fee record by ID
    trans1_record = get_object_or_404(CS_Fees1, id=trans_id)
    current_date = timezone.now().date()
    # Render the fee detail template
    return render(request, 'view_cs1_transaction.html', {
        'trans1_record': trans1_record,
        'current_date': current_date,
    })





# ==================================computer science second year fees======================================================================

def cs_fees2(request):
    fees2 = CS_Fees2.objects.all()
    cs_cost2 = CS_Cost2.objects.all()
    departments = Department.objects.all()  
    all_programs = Programs.objects.all()  

    if request.method == 'POST':
        # Get form values
        id_number = request.POST.get('id_number')
        student_name = request.POST.get('student_name')
        level = request.POST.get('level')
        department_id = request.POST.get('department')
        program_id = request.POST.get('program')
        cost_of_program_id = request.POST.get('cost_of_program')
        sum_of = request.POST.get('sum_of')
        amount_paid_str = request.POST.get('amount_paid', '0')
        payment_date_str = request.POST.get('payment_date')
        second_payment_date_str = request.POST.get('second_payment_date')
        payment_status = request.POST.get('payment_status')
        payment_slip = request.FILES.get('payment_slip')
        check_no_str = request.POST.get('check_no')  
        paid_for_str = request.POST.get('paid_for', 'Tuition Fees')  

        # Convert the amount paid to Decimal
        new_payment = Decimal(amount_paid_str)

        # Validate and parse the dates
        payment_date = parse_date(payment_date_str)
        if not payment_date:
            messages.error(request, "Please enter a valid payment date.")
            return redirect('cs_fees2')  # Redirect to the form in case of error
        
        second_payment_date = parse_date(second_payment_date_str) if second_payment_date_str else None

        # Fetch the department and program objects
        department = get_object_or_404(Department, id=department_id)
        program = get_object_or_404(Programs, id=program_id)
        cost_of_program = get_object_or_404(CS_Cost2, id=cost_of_program_id)

        # Check if a fees record exists for the student
        existing_fees = CS_Fees2.objects.filter(id_number=id_number, program=program, department=department).first()

        if existing_fees:
            # If record exists, update it
            existing_fees.paid_fees += new_payment  
            existing_fees.amount_paid = new_payment
            existing_fees.payment_date = payment_date  
            existing_fees.second_payment_date = second_payment_date
            existing_fees.payment_status = payment_status

            if payment_slip:
                existing_fees.payment_slip = payment_slip
            
            # Update check_no and paid_for if provided
            if check_no_str:
                existing_fees.check_no = check_no_str
            existing_fees.paid_for = paid_for_str  

            existing_fees.save()
            messages.success(request, "Fees details updated successfully!")
        else:
            fees2 = CS_Fees2(
                id_number=id_number,
                student_name=student_name,
                level=level,
                department=department,
                program=program,  
                cost_of_program=cost_of_program,
                amount_paid=new_payment,
                sum_of=sum_of,
                paid_fees=new_payment,
                payment_date=payment_date,  
                second_payment_date=second_payment_date,  
                payment_status=payment_status,
                payment_slip=payment_slip,
                check_no=check_no_str,  
                paid_for=paid_for_str,  
            )
            fees2.save()
            messages.success(request, "New fees entry created successfully!")

        return redirect('cs_fees2')

    return render(request, 'cs_fees2.html', {
        'cs_cost2': cs_cost2,
        'fees2': fees2,
        'departments': departments,
        'all_programs': all_programs,  
    })


def edit_cs_fees2(request, fee_id):
    fees_entry = get_object_or_404(CS_Fees2, id=fee_id)
    cs_cost2 = CS_Cost2.objects.all()
    departments = Department.objects.all()
    all_programs = Programs.objects.all()

    if request.method == 'POST':
        # Update fee entry with other fields
        fees_entry.student_name = request.POST.get('student_name', fees_entry.student_name)
        fees_entry.id_number = request.POST.get('id_number', fees_entry.id_number)
        
        # Update department if provided
        department_id = request.POST.get('department')
        if department_id:
            fees_entry.department = get_object_or_404(Department, id=department_id)

        # Update program if provided
        program_id = request.POST.get('program')
        if program_id:
            fees_entry.program = get_object_or_404(Programs, id=program_id)

        # Update cost_of_program if provided
        cost_of_program_id = request.POST.get('cost_of_program')
        if cost_of_program_id:
            fees_entry.cost_of_program = get_object_or_404(CS_Cost2, id=cost_of_program_id)

        fees_entry.sum_of = request.POST.get('sum_of', fees_entry.sum_of)
        fees_entry.check_no = request.POST.get('check_no', fees_entry.check_no)
        fees_entry.paid_for = request.POST.get('paid_for', 'Tuition Fees')

        # Handle new payment
        new_payment_str = request.POST.get('amount_paid', '0')
        new_payment = Decimal(new_payment_str)

        # Add the new payment and update the paid fees and balance
        fees_entry.add_payment(new_payment)

        # Parse the payment dates
        payment_date_str = request.POST.get('payment_date', '')
        second_payment_date_str = request.POST.get('second_payment_date', '')

        payment_date = parse_date(payment_date_str)
        second_payment_date = parse_date(second_payment_date_str)

        # Validate payment dates
        if not payment_date:
            messages.error(request, "Invalid payment date format. Please provide a valid date.")
            return redirect('edit_cs_fees2', fee_id=fee_id)

        fees_entry.payment_date = payment_date
        fees_entry.second_payment_date = second_payment_date if second_payment_date else None

        fees_entry.payment_status = request.POST.get('payment_status', fees_entry.payment_status)

        # Handle payment slips if provided
        payment_slip = request.FILES.get('payment_slip')
        second_payment_slip = request.FILES.get('second_payment_slip')
        if payment_slip:
            fees_entry.payment_slip = payment_slip
        if second_payment_slip:
            fees_entry.second_payment_slip = second_payment_slip

        # Save the updated fees entry
        fees_entry.save()

        messages.success(request, "Fees details updated successfully!")
        return redirect('cs_fees2')

    return render(request, 'edit_cs_fees2.html', {
        'fees_entry': fees_entry,
        'cs_cost2': cs_cost2,
        'departments': departments,
        'all_programs': all_programs,
    })


def view_cs_fees2(request, fee_id):
    # Get the fee record by ID
    fee_record = get_object_or_404(CS_Fees2, id=fee_id)
    current_date = timezone.now().date()
    # Render the fee detail template
    return render(request, 'view_cs_fees2.html', {
        'fee_record': fee_record,
        'current_date': current_date,
    })



def cs2_transaction(request):
    fees2 = CS_Fees2.objects.all()
    return render(request, 'cs2_transaction.html', {'fees2':fees2})

def view_cs2_transaction(request, trans_id):
    # Get the fee record by ID
    trans2_record = get_object_or_404(CS_Fees2, id=trans_id)
    current_date = timezone.now().date()
    # Render the fee detail template
    return render(request, 'view_cs2_transaction.html', {
        'trans2_record': trans2_record,
        'current_date': current_date,
    })




# ==================================computer science Third year fees======================================================================

def cs_fees3(request):
    fees3 = CS_Fees3.objects.all()
    cs_cost3 = CS_Cost3.objects.all()
    departments = Department.objects.all()  
    all_programs = Programs.objects.all()  

    if request.method == 'POST':
        # Get form values
        id_number = request.POST.get('id_number')
        student_name = request.POST.get('student_name')
        level = request.POST.get('level')
        department_id = request.POST.get('department')
        program_id = request.POST.get('program')
        cost_of_program_id = request.POST.get('cost_of_program')
        sum_of = request.POST.get('sum_of')
        amount_paid_str = request.POST.get('amount_paid', '0')
        payment_date_str = request.POST.get('payment_date')
        second_payment_date_str = request.POST.get('second_payment_date')
        payment_status = request.POST.get('payment_status')
        payment_slip = request.FILES.get('payment_slip')
        check_no_str = request.POST.get('check_no')  
        paid_for_str = request.POST.get('paid_for', 'Tuition Fees')  

        # Convert the amount paid to Decimal
        new_payment = Decimal(amount_paid_str)

        # Validate and parse the dates
        payment_date = parse_date(payment_date_str)
        if not payment_date:
            messages.error(request, "Please enter a valid payment date.")
            return redirect('cs_fees3')  # Redirect to the form in case of error
        
        second_payment_date = parse_date(second_payment_date_str) if second_payment_date_str else None

        # Fetch the department and program objects
        department = get_object_or_404(Department, id=department_id)
        program = get_object_or_404(Programs, id=program_id)
        cost_of_program = get_object_or_404(CS_Cost3, id=cost_of_program_id)

        # Check if a fees record exists for the student
        existing_fees = CS_Fees3.objects.filter(id_number=id_number, program=program, department=department).first()

        if existing_fees:
            # If record exists, update it
            existing_fees.paid_fees += new_payment  
            existing_fees.amount_paid = new_payment
            existing_fees.payment_date = payment_date  
            existing_fees.second_payment_date = second_payment_date
            existing_fees.payment_status = payment_status

            if payment_slip:
                existing_fees.payment_slip = payment_slip
            
            # Update check_no and paid_for if provided
            if check_no_str:
                existing_fees.check_no = check_no_str
            existing_fees.paid_for = paid_for_str  

            existing_fees.save()
            messages.success(request, "Fees details updated successfully!")
        else:
            fees3 = CS_Fees3(
                id_number=id_number,
                student_name=student_name,
                level=level,
                department=department,
                program=program,  
                cost_of_program=cost_of_program,
                amount_paid=new_payment,
                sum_of=sum_of,
                paid_fees=new_payment,
                payment_date=payment_date,  
                second_payment_date=second_payment_date,  
                payment_status=payment_status,
                payment_slip=payment_slip,
                check_no=check_no_str,  
                paid_for=paid_for_str,  
            )
            fees3.save()
            messages.success(request, "New fees entry created successfully!")

        return redirect('cs_fees3')

    return render(request, 'cs_fees3.html', {
        'cs_cost3': cs_cost3,
        'fees3': fees3,
        'departments': departments,
        'all_programs': all_programs,  
    })


def edit_cs_fees3(request, fee_id):
    fees_entry = get_object_or_404(CS_Fees3, id=fee_id)
    cs_cost3 = CS_Cost3.objects.all()
    departments = Department.objects.all()
    all_programs = Programs.objects.all()

    if request.method == 'POST':
        # Update fee entry with other fields
        fees_entry.student_name = request.POST.get('student_name', fees_entry.student_name)
        fees_entry.id_number = request.POST.get('id_number', fees_entry.id_number)
        
        # Update department if provided
        department_id = request.POST.get('department')
        if department_id:
            fees_entry.department = get_object_or_404(Department, id=department_id)

        # Update program if provided
        program_id = request.POST.get('program')
        if program_id:
            fees_entry.program = get_object_or_404(Programs, id=program_id)

        # Update cost_of_program if provided
        cost_of_program_id = request.POST.get('cost_of_program')
        if cost_of_program_id:
            fees_entry.cost_of_program = get_object_or_404(CS_Cost3, id=cost_of_program_id)

        fees_entry.sum_of = request.POST.get('sum_of', fees_entry.sum_of)
        fees_entry.check_no = request.POST.get('check_no', fees_entry.check_no)
        fees_entry.paid_for = request.POST.get('paid_for', 'Tuition Fees')

        # Handle new payment
        new_payment_str = request.POST.get('amount_paid', '0')
        new_payment = Decimal(new_payment_str)

        # Add the new payment and update the paid fees and balance
        fees_entry.add_payment(new_payment)

        # Parse the payment dates
        payment_date_str = request.POST.get('payment_date', '')
        second_payment_date_str = request.POST.get('second_payment_date', '')

        payment_date = parse_date(payment_date_str)
        second_payment_date = parse_date(second_payment_date_str)

        # Validate payment dates
        if not payment_date:
            messages.error(request, "Invalid payment date format. Please provide a valid date.")
            return redirect('edit_cs_fees3', fee_id=fee_id)

        fees_entry.payment_date = payment_date
        fees_entry.second_payment_date = second_payment_date if second_payment_date else None

        fees_entry.payment_status = request.POST.get('payment_status', fees_entry.payment_status)

        # Handle payment slips if provided
        payment_slip = request.FILES.get('payment_slip')
        second_payment_slip = request.FILES.get('second_payment_slip')
        if payment_slip:
            fees_entry.payment_slip = payment_slip
        if second_payment_slip:
            fees_entry.second_payment_slip = second_payment_slip

        # Save the updated fees entry
        fees_entry.save()

        messages.success(request, "Fees details updated successfully!")
        return redirect('cs_fees3')

    return render(request, 'edit_cs_fees3.html', {
        'fees_entry': fees_entry,
        'cs_cost3': cs_cost3,
        'departments': departments,
        'all_programs': all_programs,
    })


def view_cs_fees3(request, fee_id):
    # Get the fee record by ID
    fee_record = get_object_or_404(CS_Fees3, id=fee_id)
    current_date = timezone.now().date()
    # Render the fee detail template
    return render(request, 'view_cs_fees3.html', {
        'fee_record': fee_record,
        'current_date': current_date,
    })


def cs3_transaction(request):
    fees3 = CS_Fees3.objects.all()
    return render(request, 'cs3_transaction.html', {'fees3':fees3})

def view_cs3_transaction(request, trans_id):
    # Get the fee record by ID
    trans3_record = get_object_or_404(CS_Fees3, id=trans_id)
    current_date = timezone.now().date()
    # Render the fee detail template
    return render(request, 'view_cs3_transaction.html', {
        'trans3_record': trans3_record,
        'current_date': current_date,
    })



# ==================================computer science Final year fees======================================================================

def cs_fees4(request):
    fees4 = CS_Fees4.objects.all()
    cs_cost4 = CS_Cost4.objects.all()
    departments = Department.objects.all()  
    all_programs = Programs.objects.all()  

    if request.method == 'POST':
        # Get form values
        id_number = request.POST.get('id_number')
        student_name = request.POST.get('student_name')
        level = request.POST.get('level')
        department_id = request.POST.get('department')
        program_id = request.POST.get('program')
        cost_of_program_id = request.POST.get('cost_of_program')
        sum_of = request.POST.get('sum_of')
        amount_paid_str = request.POST.get('amount_paid', '0')
        payment_date_str = request.POST.get('payment_date')
        second_payment_date_str = request.POST.get('second_payment_date')
        payment_status = request.POST.get('payment_status')
        payment_slip = request.FILES.get('payment_slip')
        check_no_str = request.POST.get('check_no')  
        paid_for_str = request.POST.get('paid_for', 'Tuition Fees')  

        # Convert the amount paid to Decimal
        new_payment = Decimal(amount_paid_str)

        # Validate and parse the dates
        payment_date = parse_date(payment_date_str)
        if not payment_date:
            messages.error(request, "Please enter a valid payment date.")
            return redirect('cs_fees4')  # Redirect to the form in case of error
        
        second_payment_date = parse_date(second_payment_date_str) if second_payment_date_str else None

        # Fetch the department and program objects
        department = get_object_or_404(Department, id=department_id)
        program = get_object_or_404(Programs, id=program_id)
        cost_of_program = get_object_or_404(CS_Cost4, id=cost_of_program_id)

        # Check if a fees record exists for the student
        existing_fees = CS_Fees4.objects.filter(id_number=id_number, program=program, department=department).first()

        if existing_fees:
            # If record exists, update it
            existing_fees.paid_fees += new_payment  
            existing_fees.amount_paid = new_payment
            existing_fees.payment_date = payment_date  
            existing_fees.second_payment_date = second_payment_date
            existing_fees.payment_status = payment_status

            if payment_slip:
                existing_fees.payment_slip = payment_slip
            
            # Update check_no and paid_for if provided
            if check_no_str:
                existing_fees.check_no = check_no_str
            existing_fees.paid_for = paid_for_str  

            existing_fees.save()
            messages.success(request, "Fees details updated successfully!")
        else:
            fees4 = CS_Fees4(
                id_number=id_number,
                student_name=student_name,
                level=level,
                department=department,
                program=program,  
                cost_of_program=cost_of_program,
                amount_paid=new_payment,
                sum_of=sum_of,
                paid_fees=new_payment,
                payment_date=payment_date,  
                second_payment_date=second_payment_date,  
                payment_status=payment_status,
                payment_slip=payment_slip,
                check_no=check_no_str,  
                paid_for=paid_for_str,  
            )
            fees4.save()
            messages.success(request, "New fees entry created successfully!")

        return redirect('cs_fees4')

    return render(request, 'cs_fees4.html', {
        'cs_cost4': cs_cost4,
        'fees4': fees4,
        'departments': departments,
        'all_programs': all_programs,  
    })


def edit_cs_fees4(request, fee_id):
    fees_entry = get_object_or_404(CS_Fees4, id=fee_id)
    cs_cost4 = CS_Cost4.objects.all()
    departments = Department.objects.all()
    all_programs = Programs.objects.all()

    if request.method == 'POST':
        # Update fee entry with other fields
        fees_entry.student_name = request.POST.get('student_name', fees_entry.student_name)
        fees_entry.id_number = request.POST.get('id_number', fees_entry.id_number)
        
        # Update department if provided
        department_id = request.POST.get('department')
        if department_id:
            fees_entry.department = get_object_or_404(Department, id=department_id)

        # Update program if provided
        program_id = request.POST.get('program')
        if program_id:
            fees_entry.program = get_object_or_404(Programs, id=program_id)

        # Update cost_of_program if provided
        cost_of_program_id = request.POST.get('cost_of_program')
        if cost_of_program_id:
            fees_entry.cost_of_program = get_object_or_404(CS_Cost4, id=cost_of_program_id)

        fees_entry.sum_of = request.POST.get('sum_of', fees_entry.sum_of)
        fees_entry.check_no = request.POST.get('check_no', fees_entry.check_no)
        fees_entry.paid_for = request.POST.get('paid_for', 'Tuition Fees')

        # Handle new payment
        new_payment_str = request.POST.get('amount_paid', '0')
        new_payment = Decimal(new_payment_str)

        # Add the new payment and update the paid fees and balance
        fees_entry.add_payment(new_payment)

        # Parse the payment dates
        payment_date_str = request.POST.get('payment_date', '')
        second_payment_date_str = request.POST.get('second_payment_date', '')

        payment_date = parse_date(payment_date_str)
        second_payment_date = parse_date(second_payment_date_str)

        # Validate payment dates
        if not payment_date:
            messages.error(request, "Invalid payment date format. Please provide a valid date.")
            return redirect('edit_cs_fees4', fee_id=fee_id)

        fees_entry.payment_date = payment_date
        fees_entry.second_payment_date = second_payment_date if second_payment_date else None

        fees_entry.payment_status = request.POST.get('payment_status', fees_entry.payment_status)

        # Handle payment slips if provided
        payment_slip = request.FILES.get('payment_slip')
        second_payment_slip = request.FILES.get('second_payment_slip')
        if payment_slip:
            fees_entry.payment_slip = payment_slip
        if second_payment_slip:
            fees_entry.second_payment_slip = second_payment_slip

        # Save the updated fees entry
        fees_entry.save()

        messages.success(request, "Fees details updated successfully!")
        return redirect('cs_fees4')

    return render(request, 'edit_cs_fees4.html', {
        'fees_entry': fees_entry,
        'cs_cost4': cs_cost4,
        'departments': departments,
        'all_programs': all_programs,
    })


def view_cs_fees4(request, fee_id):
    # Get the fee record by ID
    fee_record = get_object_or_404(CS_Fees4, id=fee_id)
    current_date = timezone.now().date()
    # Render the fee detail template
    return render(request, 'view_cs_fees3.html', {
        'fee_record': fee_record,
        'current_date': current_date,
    })



def cs4_transaction(request):
    fees4 = CS_Fees4.objects.all()
    return render(request, 'cs4_transaction.html', {'fees4':fees4})

def view_cs4_transaction(request, trans_id):
    # Get the fee record by ID
    trans4_record = get_object_or_404(CS_Fees4, id=trans_id)
    current_date = timezone.now().date()
    # Render the fee detail template
    return render(request, 'view_cs4_transaction.html', {
        'trans4_record': trans4_record,
        'current_date': current_date,
    })



# ===============CS1 FEES STATUS=================

def cs1_fees_status(request):
    return render(request, 'cs1_fees_status.html')
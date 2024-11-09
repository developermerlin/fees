from django.db import models # type: ignore
from decimal import Decimal
from django.utils import timezone # type: ignore
GENDER = (
        ('Male','Male'),
        ('Female','Female'),
)


LEVEL1 = (
    ('First Year','First Year'),

)

LEVEL2 = (
    ('Second Year','Second Year'),
)

LEVEL3 = (
    ('Third Year','Third Year'),
)

LEVEL4 = (
    ('Final Year','Final Year')
)


class Department(models.Model):
    department_name = models.CharField(max_length=100)
    def __str__(self):
        return self.department_name
    
class Programs(models.Model):
    program_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    def __str__(self):
        return self.program_name

class CS_Cost1(models.Model):
    program_name = models.CharField(max_length=255, null=True)
    program_duration = models.CharField(max_length=255)
    program_fees = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    all_program = models.ForeignKey(Programs, on_delete=models.CASCADE)
    def __str__(self):
        return self.program_name

class CS_Cost2(models.Model):
    program_name = models.CharField(max_length=100,null=True)
    program_duration = models.PositiveIntegerField()  
    program_fees = models.DecimalField(max_digits=10, decimal_places=2)  
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    all_program = models.ForeignKey(Programs, on_delete=models.CASCADE)
    def __str__(self):
        return self.program_name
    
class CS_Cost3(models.Model):
    program_name = models.CharField(max_length=100,null=True)
    program_duration = models.PositiveIntegerField()  
    program_fees = models.DecimalField(max_digits=10, decimal_places=2)  
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    all_program = models.ForeignKey(Programs, on_delete=models.CASCADE)
    def __str__(self):
        return self.program_name
    
class CS_Cost4(models.Model):
    program_name = models.CharField(max_length=100,null=True)
    program_duration = models.PositiveIntegerField()  
    program_fees = models.DecimalField(max_digits=10, decimal_places=2)  
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    all_program = models.ForeignKey(Programs, on_delete=models.CASCADE)
    def __str__(self):
        return self.program_name

# ======student model=============
class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)  
    student_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER)
    program = models.ForeignKey(Programs, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to='profiles/', blank=True)

    def __str__(self):
        return self.student_name


class CS_Fees1(models.Model):
    student_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=20)
    program = models.ForeignKey(Programs, on_delete=models.CASCADE)
    program_details = models.ForeignKey(Programs, on_delete=models.CASCADE, related_name='program_details_payments', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    sum_of = models.CharField(max_length=200)
    paid_for = models.CharField(max_length=200, default='Tuition Fees')
    check_no = models.BigIntegerField(null=True, blank=True)  
    receipt_no = models.CharField(max_length=20, unique=True, blank=True) 
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  
    level = models.CharField(max_length=20, choices=LEVEL1)
    payment_date = models.DateField(null=True)
    second_payment_date = models.DateField(null=True, blank=True)  
    cost_of_program = models.ForeignKey(CS_Cost1, on_delete=models.CASCADE, related_name='cost_of_program_payments')
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    payment_slip = models.FileField(upload_to='payment_slips/', blank=True, null=True)
    second_payment_slip = models.FileField(upload_to='payment_slips/', blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[
        ('Paid Full', 'Paid Full'),
        ('Incomplete Fees', 'Incomplete Fees'),
    ])

    def save(self, *args, **kwargs):
        if not self.receipt_no:  # 
            current_year = timezone.now().year  
            super().save(*args, **kwargs)  
            self.receipt_no = f"{current_year}-{self.pk}"  
        super().save(*args, **kwargs) 

    def balance(self):
        """Calculate the remaining balance as the cost of the program minus the total paid fees."""
        return Decimal(self.cost_of_program.program_fees) - self.paid_fees

    def add_payment(self, new_payment, payment_slip=None):
        """Add a new payment, update the cumulative paid fees, and recalculate the balance."""
        self.paid_fees += Decimal(new_payment)  # Add new payment to cumulative paid fees
        self.amount_paid = Decimal(new_payment)  # Store the latest payment
        if payment_slip:
            self.payment_slip = payment_slip  # Save the payment slip if provided
        self.save()

    def __str__(self):
        return f"{self.student_name} - {self.program.program_name} - Paid Fees: {self.paid_fees} - Balance: {self.balance()}"


class CS_Fees2(models.Model):
    student_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=20)
    program = models.ForeignKey(Programs, on_delete=models.CASCADE, related_name='cs_fees2_programs')  # Added related_name to avoid clash
    program_details = models.ForeignKey(Programs, on_delete=models.CASCADE, related_name='cs_fees2_program_details', null=True, blank=True)  # Updated related_name
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='cs_fees2_departments')  # Added related_name to avoid clash
    sum_of = models.CharField(max_length=200)
    paid_for = models.CharField(max_length=200, default='Tuition Fees')
    check_no = models.BigIntegerField(null=True, blank=True)  
    receipt_no = models.CharField(max_length=20, unique=True, blank=True) 
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  
    level = models.CharField(max_length=20, choices=LEVEL1)
    payment_date = models.DateField(null=True)
    second_payment_date = models.DateField(null=True, blank=True)  
    cost_of_program = models.ForeignKey(CS_Cost2, on_delete=models.CASCADE, related_name='cs_fees2_cost_of_program_payments')  # Updated related_name
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    payment_slip = models.FileField(upload_to='payment_slips/', blank=True, null=True)
    second_payment_slip = models.FileField(upload_to='payment_slips/', blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[
        ('Paid Full', 'Paid Full'),
        ('Incomplete Fees', 'Incomplete Fees'),
    ])

    def save(self, *args, **kwargs):
        if not self.receipt_no:  # Generate receipt_no if not provided
            current_year = timezone.now().year  
            super().save(*args, **kwargs)  
            self.receipt_no = f"{current_year}-{self.pk}"  
        super().save(*args, **kwargs)

    def balance(self):
        """Calculate the remaining balance as the cost of the program minus the total paid fees."""
        return Decimal(self.cost_of_program.program_fees) - self.paid_fees

    def add_payment(self, new_payment, payment_slip=None):
        """Add a new payment, update the cumulative paid fees, and recalculate the balance."""
        self.paid_fees += Decimal(new_payment)  # Add new payment to cumulative paid fees
        self.amount_paid = Decimal(new_payment)  # Store the latest payment
        if payment_slip:
            self.payment_slip = payment_slip  # Save the payment slip if provided
        self.save()

    def __str__(self):
        return f"{self.student_name} - {self.program.program_name} - Paid Fees: {self.paid_fees} - Balance: {self.balance()}"
    

class CS_Fees3(models.Model):
    student_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=20)
    program = models.ForeignKey(Programs, on_delete=models.CASCADE, related_name='cs_fees3_programs')  # Added related_name to avoid clash
    program_details = models.ForeignKey(Programs, on_delete=models.CASCADE, related_name='cs_fees3_program_details', null=True, blank=True)  # Updated related_name
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='cs_fees3_departments')  # Added related_name to avoid clash
    sum_of = models.CharField(max_length=200)
    paid_for = models.CharField(max_length=200, default='Tuition Fees')
    check_no = models.BigIntegerField(null=True, blank=True)  
    receipt_no = models.CharField(max_length=20, unique=True, blank=True) 
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  
    level = models.CharField(max_length=20, choices=LEVEL1)
    payment_date = models.DateField(null=True)
    second_payment_date = models.DateField(null=True, blank=True)  
    cost_of_program = models.ForeignKey(CS_Cost3, on_delete=models.CASCADE, related_name='cs_fees3_cost_of_program_payments')  # Updated related_name
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    payment_slip = models.FileField(upload_to='payment_slips/', blank=True, null=True)
    second_payment_slip = models.FileField(upload_to='payment_slips/', blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[
        ('Paid Full', 'Paid Full'),
        ('Incomplete Fees', 'Incomplete Fees'),
    ])

    def save(self, *args, **kwargs):
        if not self.receipt_no:  # Generate receipt_no if not provided
            current_year = timezone.now().year  
            super().save(*args, **kwargs)  
            self.receipt_no = f"{current_year}-{self.pk}"  
        super().save(*args, **kwargs)

    def balance(self):
        """Calculate the remaining balance as the cost of the program minus the total paid fees."""
        return Decimal(self.cost_of_program.program_fees) - self.paid_fees

    def add_payment(self, new_payment, payment_slip=None):
        """Add a new payment, update the cumulative paid fees, and recalculate the balance."""
        self.paid_fees += Decimal(new_payment)  # Add new payment to cumulative paid fees
        self.amount_paid = Decimal(new_payment)  # Store the latest payment
        if payment_slip:
            self.payment_slip = payment_slip  # Save the payment slip if provided
        self.save()

    def __str__(self):
        return f"{self.student_name} - {self.program.program_name} - Paid Fees: {self.paid_fees} - Balance: {self.balance()}"
    


class CS_Fees4(models.Model):
    student_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=20)
    program = models.ForeignKey(Programs, on_delete=models.CASCADE, related_name='cs_fees4_programs')  # Added related_name to avoid clash
    program_details = models.ForeignKey(Programs, on_delete=models.CASCADE, related_name='cs_fees4_program_details', null=True, blank=True)  # Updated related_name
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='cs_fees4_departments')  # Added related_name to avoid clash
    sum_of = models.CharField(max_length=200)
    paid_for = models.CharField(max_length=200, default='Tuition Fees')
    check_no = models.BigIntegerField(null=True, blank=True)  
    receipt_no = models.CharField(max_length=20, unique=True, blank=True) 
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  
    level = models.CharField(max_length=20, choices=LEVEL1)
    payment_date = models.DateField(null=True)
    second_payment_date = models.DateField(null=True, blank=True)  
    cost_of_program = models.ForeignKey(CS_Cost4, on_delete=models.CASCADE, related_name='cs_fees4_cost_of_program_payments')  # Updated related_name
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    payment_slip = models.FileField(upload_to='payment_slips/', blank=True, null=True)
    second_payment_slip = models.FileField(upload_to='payment_slips/', blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[
        ('Paid Full', 'Paid Full'),
        ('Incomplete Fees', 'Incomplete Fees'),
    ])

    def save(self, *args, **kwargs):
        if not self.receipt_no:  # Generate receipt_no if not provided
            current_year = timezone.now().year  
            super().save(*args, **kwargs)  
            self.receipt_no = f"{current_year}-{self.pk}"  
        super().save(*args, **kwargs)

    def balance(self):
        """Calculate the remaining balance as the cost of the program minus the total paid fees."""
        return Decimal(self.cost_of_program.program_fees) - self.paid_fees

    def add_payment(self, new_payment, payment_slip=None):
        """Add a new payment, update the cumulative paid fees, and recalculate the balance."""
        self.paid_fees += Decimal(new_payment)  # Add new payment to cumulative paid fees
        self.amount_paid = Decimal(new_payment)  # Store the latest payment
        if payment_slip:
            self.payment_slip = payment_slip  # Save the payment slip if provided
        self.save()

    def __str__(self):
        return f"{self.student_name} - {self.program.program_name} - Paid Fees: {self.paid_fees} - Balance: {self.balance()}"
    




    from django.db import models


class CS_Fees(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="fees")
    year = models.IntegerField(choices=[(1, 'Year 1'), (2, 'Year 2'), (3, 'Year 3'), (4, 'Year 4')])
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_date = models.DateField(null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=[('Paid Full', 'Paid Full'), ('Incomplete', 'Incomplete')])

    def balance(self):
        # Assume program fees is accessible and defined for calculation
        return self.cost_of_program.program_fees - self.paid_fees
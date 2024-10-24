from django.contrib import admin # type: ignore
from .models import Department, Student, CS_Cost1, CS_Cost2, CS_Cost3, CS_Cost4,Programs,CS_Fees1,CS_Fees2,CS_Fees3,CS_Fees4
# Register your models here.
admin.site.register(Department)
admin.site.register(Student)
admin.site.register(CS_Cost1)
admin.site.register(CS_Cost2)
admin.site.register(CS_Cost3)
admin.site.register(CS_Cost4)
admin.site.register(Programs)
admin.site.register(CS_Fees1)
admin.site.register(CS_Fees2)
admin.site.register(CS_Fees3)
admin.site.register(CS_Fees4)

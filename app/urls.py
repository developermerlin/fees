from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.first_home, name='first_home'),
    path('main_home/', views.main_home, name='main_home'),
    path('main_second_home/', views.main_second_home, name='main_second_home'),
    
    path('student/', views.student, name='student'),
    path('edit_student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('view_student/<int:student_id>/', views.view_student, name='view_student'),

    path('department/', views.department, name='department'),
    path('edit_department/<int:department_id>/', views.edit_department, name='edit_department'),
    path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),
    
    path('all_program/', views.all_program, name='all_program'),
    path('edit_all_program/<int:program_id>/', views.edit_all_program, name='edit_all_program'),
    path('delete_all_program/<int:program_id>/', views.delete_all_program, name='delete_all_program'),

    path('cs_cost1/', views.cs_cost1, name='cs_cost1'),
    path('edit_cs_cost1/<int:program_id>/', views.edit_cs_cost1, name='edit_cs_cost1'),
    path('delete_cs_cost1/<int:program_id>/', views.delete_cs_cost1, name='delete_cs_cost1'),

    path('cs_cost2/', views.cs_cost2, name='cs_cost2'),
    path('edit_cs_cost2/<int:program_id>/', views.edit_cs_cost2, name='edit_cs_cost2'),
    path('delete_cs_cost2/<int:program_id>/', views.delete_cs_cost2, name='delete_cs_cost2'),


    path('cs_cost3/', views.cs_cost3, name='cs_cost3'),
    path('edit_cs_cost3/<int:program_id>/', views.edit_cs_cost3, name='edit_cs_cost3'),
    path('delete_cs_cost3/<int:program_id>/', views.delete_cs_cost3, name='delete_cs_cost3'),

    path('cs_cost4/', views.cs_cost4, name='cs_cost4'),
    path('edit_cs_cost4/<int:program_id>/', views.edit_cs_cost4, name='edit_cs_cost4'),
    path('delete_cs_cost4/<int:program_id>/', views.delete_cs_cost4, name='delete_cs_cost4'),

    path('cs_fees1/', views.cs_fees1, name='cs_fees1'),
    path('cs_fees1/<int:fee_id>/', views.edit_cs_fees1, name='edit_cs_fees1'),
    path('view_cs_fees1/<int:fee_id>/', views.view_cs_fees1, name='view_cs_fees1'),

    path('cs_fees2/', views.cs_fees2, name='cs_fees2'),
    path('cs_fees2/<int:fee_id>/', views.edit_cs_fees2, name='edit_cs_fees2'),
    path('view_cs_fees2/<int:fee_id>/', views.view_cs_fees2, name='view_cs_fees2'),

    path('cs_fees3/', views.cs_fees3, name='cs_fees3'),
    path('cs_fees3/<int:fee_id>/', views.edit_cs_fees3, name='edit_cs_fees3'),
    path('view_cs_fees3/<int:fee_id>/', views.view_cs_fees3, name='view_cs_fees3'),

    path('cs_fees4/', views.cs_fees4, name='cs_fees4'),
    path('cs_fees4/<int:fee_id>/', views.edit_cs_fees4, name='edit_cs_fees4'),
    path('view_cs_fees4/<int:fee_id>/', views.view_cs_fees4, name='view_cs_fees4'),

    path('cs1_transaction/', views.cs1_transaction, name='cs1_transaction'),
    path('view_cs1_transaction/<int:trans_id>/', views.view_cs1_transaction, name='view_cs1_transaction'),

    path('cs2_transaction/', views.cs2_transaction, name='cs2_transaction'),
    path('view_cs2_transaction/<int:trans_id>/', views.view_cs2_transaction, name='view_cs2_transaction'),

    path('cs3_transaction/', views.cs3_transaction, name='cs3_transaction'),
    path('view_cs3_transaction/<int:trans_id>/', views.view_cs3_transaction, name='view_cs3_transaction'),

    path('cs4_transaction/', views.cs4_transaction, name='cs4_transaction'),
    path('view_cs4_transaction/<int:trans_id>/', views.view_cs4_transaction, name='view_cs4_transaction'),


    path('cs_fees_status/', views.cs_fees_status, name='cs_fees_status'),

    path('admin_cs1_transaction/', views.admin_cs1_transaction, name='admin_cs1_transaction'),
    path('admin_cs2_transaction/', views.admin_cs2_transaction, name='admin_cs2_transaction'),
    path('admin_cs3_transaction/', views.admin_cs3_transaction, name='admin_cs3_transaction'),
    path('admin_cs4_transaction/', views.admin_cs4_transaction, name='admin_cs4_transaction'),
    path('view_admin_cs1_transaction/<int:trans_id>/', views.view_admin_cs1_transaction, name='view_admin_cs1_transaction'),
    path('view_admin_cs2_transaction/<int:trans_id>/', views.view_admin_cs2_transaction, name='view_admin_cs2_transaction'),
    path('view_admin_cs3_transaction/<int:trans_id>/', views.view_admin_cs3_transaction, name='view_admin_cs3_transaction'),
    path('view_admin_cs4_transaction/<int:trans_id>/', views.view_admin_cs4_transaction, name='view_admin_cs4_transaction'),

    # path('students/', views.all_students_view, name='all_students'),
    path('students/<str:id_number>/', views.student_fee_details_view, name='student_fee_details'),
    path('fee-report/', views.student_fee_report_view, name='student_fee_report'),
    path('fee-status-report/', views.fee_status_report_view, name='fee_status_report'),




]

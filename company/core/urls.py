from django.urls import path
from . import views

urlpatterns = [
    path('department/', views.create_department),
    path('employee/', views.create_employee),
    path('salary/<int:emp_id>/', views.set_base_salary),
    path('leave/<int:emp_id>/', views.update_leave),
    path('calculate/<int:emp_id>/', views.calculate_salary),
    path('high-earners/<str:dept_id>/', views.high_earners),
    path('high-earners/<str:month>/<str:year>/', views.high_earners_month),
]
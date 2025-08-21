from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Department, Employee, LeaveApplication
from .serializers import DepartmentSerializer, EmployeeSerializer, LeaveSerializer
from django.db.models import F

# 1. POST API to create department
@api_view(['POST'])
def create_department(request):
    serializer = DepartmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2. POST API to create employee
@api_view(['POST'])
def create_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 3. POST API to set base salary for employee
@api_view(['POST'])
def set_base_salary(request, emp_id):
    try:
        emp = Employee.objects.get(id=emp_id)
        emp.baseSalary = request.data['baseSalary']
        emp.save()
        return Response({"message": "Base salary updated"})
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=404)

# 4. UPDATE API to increase leave count
@api_view(['POST','PUT'])
def update_leave(request, emp_id):
    try:
        leave = LeaveApplication.objects.get(employee_id=emp_id, month=request.data['month'], year=request.data['year'])
        leave.leaves += int(request.data['leaves'])
        leave.save()
    except LeaveApplication.DoesNotExist:
        leave = LeaveApplication.objects.create(
            employee_id=emp_id,
            month=request.data['month'],
            year=request.data['year'],
            leaves=request.data['leaves']
        )
    return Response({"message": "Leave updated"})

# 5. POST API to calculate payable salary
@api_view(['POST'])
def calculate_salary(request, emp_id):
    try:
        emp = Employee.objects.get(id=emp_id)
        leave = LeaveApplication.objects.get(employee_id=emp_id, month=request.data['month'], year=request.data['year'])
        deduction = leave.leaves * (emp.baseSalary / 25)
        payable = emp.baseSalary - deduction
        return Response({"Payable Salary": payable})
    except:
        return Response({"error": "Data not found"}, status=404)

# 6. GET API - high earners in department (top 3 unique base salaries)
@api_view(['GET'])
def high_earners(request, dept_id):
    employees = Employee.objects.filter(department_id=dept_id).order_by('-baseSalary')
    top_salaries = list({emp.baseSalary for emp in employees})[:3]
    result = [emp.name for emp in employees if emp.baseSalary in top_salaries]
    return Response(result)

# 7. GET API - employees who are high earners in a specific month
@api_view(['GET'])
def high_earners_month(request, month, year):
    employees = Employee.objects.all().order_by('-baseSalary')
    top_salaries = list({emp.baseSalary for emp in employees})[:3]
    leave_apps = LeaveApplication.objects.filter(month=month, year=year)
    result = []
    for leave in leave_apps:
        deduction = leave.leaves * (leave.employee.baseSalary / 25)
        payable = leave.employee.baseSalary - deduction
        if leave.employee.baseSalary in top_salaries:
            result.append({"name": leave.employee.name, "payable_salary": payable})
    return Response(result)

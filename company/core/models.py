from django.db import models

class Department(models.Model):
    id = models.CharField(max_length=100, primary_key=True)   # UUID string
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    baseSalary = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class LeaveApplication(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    year = models.CharField(max_length=10)
    leaves = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.employee.name} - {self.month}/{self.year}"
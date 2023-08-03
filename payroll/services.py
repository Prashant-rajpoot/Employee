import csv

from employees.models import Employee, StatutoryDeduction, Deduction
from employees.selectors import get_active_employees, get_employee, get_employee_statutory_deduction, \
    get_employee_deduction
from payroll.simple_payslip import SimplePayslip
from payroll.models import Payslip, CSV
from payroll.procedures import get_overtime_pay
from settings.selectors import get_currency, get_currency_from_code


def create_payslip_list_service(payroll_record):
    payslips = []
    employees = get_active_employees()

    for employee in employees:
        bonus = employee.bonus
        overtime_pay = get_overtime_pay(employee)
        payslip = create_payslip_service(employee, payroll_record, bonus=bonus, overtime_pay=overtime_pay)
        payslips.append(payslip)

    return payslips


def create_payslip_service(employee: object, payroll_record: object, overtime_pay: object = None,
                           bonus: object = None) -> object:
    simple_payslip = SimplePayslip(employee, overtime_pay=overtime_pay, bonus=bonus)
    payslip = Payslip.objects.create(
        employee=employee,
        payroll_record=payroll_record,
        employee_nssf=simple_payslip.employee_nssf,
        employer_nssf=simple_payslip.employer_nssf,
        gross_salary=simple_payslip.gross_salary,
        net_salary=simple_payslip.net_salary,
        paye=simple_payslip.paye,
        total_nssf_contrib=simple_payslip.total_nssf_deduction,
        overtime=simple_payslip.overtime_pay,
        bonus=simple_payslip.bonus,
        local_service_tax=simple_payslip.local_service_tax,
        local_service_tax_deduction=simple_payslip.local_service_tax_deduction,
        sacco_deduction=simple_payslip.sacco_deduction_amount,
        damage_deduction=simple_payslip.damage_deduction_amount,
        salary_advance=simple_payslip.salary_advance_amount,
        police_fine=simple_payslip.police_fine_amount,
        currency=employee.currency,
        basic_salary=employee.basic_salary,
    )

    return payslip


def update_employee_financial_details(csv_obj):
    with open(csv_obj.file_name.path, 'r') as f:
        reader = csv.reader(f)
        employees = []
        statutory_deductions = []
        non_statutory_deductions = []
        for i, row in enumerate(reader):
            if i < 2:  # Ignore first 2 rows
                pass
            else:
                employee_id = row[0]
                currency_code = row[2]
                basic_salary = row[3]
                bonus = row[4]
                local_service_allowance = row[5]
                meal_allowance = row[6]
                sacco = row[7]
                damage = row[8]
                salary_advance = row[9]
                police_fine = row[10]
                local_service_tax = row[11]

                employee = get_employee(employee_id)
                old_statutory_deduction = get_employee_statutory_deduction(employee)
                old_non_statutory_deduction = get_employee_deduction(employee)
                currency = get_currency_from_code(currency_code)
                new_employee = Employee(id=employee_id, currency=currency, basic_salary=basic_salary, bonus=bonus,
                                        local_service_tax=local_service_allowance,
                                        lunch_allowance=meal_allowance)
                employees.append(new_employee)
                new_statutory_deduction = StatutoryDeduction(id=old_statutory_deduction.id, employee=employee,
                                                             local_service_tax=local_service_tax)
                statutory_deductions.append(new_statutory_deduction)
                non_statutory_deduction = Deduction(id=old_non_statutory_deduction.id,
                                                    employee=employee, sacco=sacco, damage=damage,
                                                    salary_advance=salary_advance, police_fine=police_fine)
                non_statutory_deductions.append(non_statutory_deduction)

        Employee.objects.bulk_update(employees, ['currency', 'basic_salary', 'bonus', 'local_service_tax',
                                                 'lunch_allowance'])

        StatutoryDeduction.objects.bulk_update(statutory_deductions, ['local_service_tax'])
        Deduction.objects.bulk_update(non_statutory_deductions, ['sacco', 'damage', 'salary_advance', 'police_fine'])


def delete_all_csv_files():
    CSV.objects.all().delete()

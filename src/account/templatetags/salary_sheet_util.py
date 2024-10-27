from datetime import datetime
from math import floor

from django import template
from django.db.models import Sum

from account.models import Invoice
from employee.models import Employee

register = template.Library()


@register.filter
def to_floor(number):
    return floor(number)


@register.filter
def get_account_number(employee: Employee):
    bank_account = employee.bankaccount_set.filter(default=True).first()
    if bank_account:
        return bank_account.account_number
    return 'bank account number not found'


@register.filter
def _total_by_des_type(employee_salary_set):
    total = 0
    for employee_salary in employee_salary_set:
        total += floor(employee_salary.gross_amount)
    return floor(total)


@register.filter
def _total_bonus(employee_salary_set):
    total = 0
    for employee_salary in employee_salary_set:
        total += floor(employee_salary.festival_bonus)
    return floor(total)


@register.filter
def _total_festival_bonus(employee_festival_bonus_set):
    return floor(employee_festival_bonus_set.aggregate(Sum('amount'))['amount__sum'])

    total = 0
    for employee_festival_bonus in employee_festival_bonus_set:
        total += floor(employee_festival_bonus.amount)
    return floor(total)


@register.filter
def _in_dollar(value):
    return value / 80


@register.filter
def sum_invoice_details(invoice: Invoice, column: str):
    return invoice.invoicedetail_set.all().aggregate(total=Sum(column))['total']

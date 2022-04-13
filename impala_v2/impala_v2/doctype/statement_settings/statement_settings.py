# Copyright (c) 2022, dhinesh and contributors
# For license information, please see license.txt

import frappe
import calendar
from frappe.model.document import Document
from datetime import datetime, date, timedelta
from frappe.utils.data import today
from impala.impala.report.account_recievable_statement.account_recievable_statement import execute

class StatementSettings(Document):
	 def validate(self):
		 if not(self.age_1<self.age_2 and self.age_2<self.age_3 and self.age_3<self.age_4):
			 frappe.throw("age_1 < age_2 < age_3 < age_4")
		
	
def get_statement_values():
	
	statement_settings=frappe.get_doc("Statement Settings")
	customers=frappe.get_list("Customer")
	companys=frappe.get_list("Company")
	if statement_settings.period=='Monthly':
		dates=find_date(statement_settings.date)
		to_date=dates[0]
		from_date=dates[1]
	if(to_date and from_date):
		for company in companys:
			for customer in customers:
				data={"company":company["name"],"customer":customer["name"],"from_date":from_date,"to_date":to_date,"age1":statement_settings.age_1,"age2":statement_settings.age_2,"age3":statement_settings.age_3,"age4":statement_settings.age_4}
				value=execute(frappe._dict(data))
				if(value[1]):
					print("\n\n\n****************\n\n\n")
					print(value[1])
					new_receivable_statement(value[1],data)
					pass
				
				
				

def find_date(sdate):
	sdate=int(sdate)
	today = date.today()
	last_date_to=calendar.monthrange(today.year, today.month)[1]
	print(last_date_to==30)
	print(last_date_to)
	print("1")
	print((today.day==last_date_to and last_date_to<sdate)or(today.day==(sdate)))
	print("2.1")
	if((today.day==last_date_to and last_date_to<sdate)or(today.day==sdate)):
		print("2.2")
		to_date=today.strftime("%Y-%m-%d")
		print("2")
		print(to_date)
		from_date=find_from_date()
		print(from_date)
		return [to_date,from_date]
	return[] 
def find_from_date():
	datea = date.today()
	
	print('3')
	print(datea.day,datea.month)
	if(datea.month-1==0):
		if(datea.day==31):
			from_day_year=str(datea.year)
			from_day_month=str(datea.month)
			from_day_day='01'
		else:
			from_day_year=str(datea.year-1)
			from_day_month='12'
			from_day_day=(datea.day+1)
	else:
		print("4")
		last_date_from=calendar.monthrange(datea.year, datea.month-1)[1]
		print(last_date_from,(datea.day+1>last_date_from))
		if(datea.day+1>last_date_from):
			from_day_year=str(datea.year)
			from_day_month=str(datea.month)
			from_day_day='01'
		else:
			print("5")
			from_day_year=str(datea.year)
			from_day_month=str(datea.month-1)
			from_day_day=str(datea.day+1)
	if(int(from_day_day)<=9):
		from_day_day="0"+from_day_day
	if(int(from_day_month)<=9):
		from_day_month="0"+from_day_month
	
	from_date=from_day_year+"-"+from_day_month+"-"+from_day_day
	return from_date
def new_receivable_statement(value,data):
	receivable_statement=frappe.new_doc("Receivable Statement")
	receivable_statement.company=data["company"]
	receivable_statement.from_date=data["from_date"]
	receivable_statement.to_date=data["to_date"]
	receivable_statement.customer=data["customer"]
	receivable_statement.age_1=data["age1"]
	receivable_statement.age_2=data["age2"]
	receivable_statement.age_3=data["age3"]
	receivable_statement.age_4=data["age4"]
	for val in value:
		receivable_statement.append("statement",
		{
			"no":val["docno"] if 'docno' in val else '',
			"debit":val["debit"] if 'debit'in val else '',
			"credit":val["credit"] if 'credit' in val else '',
			"balance":val["balance"] if 'balance' in val else '',
			"allocation":val["alloc"] if 'alloc' in val else '',
			"description"	:val["doctype"]if 'doctype' in val else '',
			"customer":val["customer"] if 'customer' in val else '',
			"date":val["date"] if 'date' in val else '',
		})
	receivable_statement.save()
	

#!/usr/bin/env python3
import os
import re
import PyPDF2
import pygal

monthly_expense={}
#To get all needed statements in the directory
def get_statements(files):
    boa_statements=[]
    for file in files:
        if file.startswith('eStmt'):
            boa_statements.append(file)
    return boa_statements

#To check the month of the statement from the filename of the statment files
def checkMonth(file):
    check=file.split('-')
    if check[1] == '01':
        month="JAN"
    elif check[1] == '02':
        month="FEB"
    elif check[1] == '03':
        month="MAR"
    elif check[1] == '04':
        month="APR"
    elif check[1] == '05':
        month="MAY"
    elif check[1] == '06':
        month="JUN"
    elif check[1] == '07':
        month="JUL"
    elif check[1] == '08':
        month="AUG"
    elif check[1] == '09':
        month="SEP"
    elif check[1] == '10':
        month="OCT"
    elif check[1] == '11':
        month="NOV"
    else:
        month="DEC"
    return month

#To calculate the total expenses of the checked month
def get_expense(file):
    sum=0
    month=checkMonth(file)
    #print(month)
    pdffile=open('%s/%s'%(directory,file),'rb')
    reader=PyPDF2.PdfFileReader(pdffile)
    pageObj=reader.getPage(0)
    text=pageObj.extractText()
    pattern=re.compile(',')
    checkedText=pattern.sub(r'',text)
    #print(checkedText)
    #print(text)
    regx=re.compile(r'subtractions-(\d+,?\.?\d+)|Checks-(\d+,?\.?\d+)',re.I)
    result=list(regx.findall(checkedText))
    expenses=[]
    for i in result:
        expenses=expenses+list(i)
    for element in expenses:
        if element == '':
            expenses.remove(element)
    expenses.remove('')
    #print(expenses)
    for expense in expenses:
        sum=sum+float(expense)
    #print(sum)
    monthly_expense[month]=sum


directory=input("Location of your statements: ") #To specify the location where the statements are saved
statements=get_statements(os.listdir(directory))

#To check all the statements in the directory
for file in statements:
    get_expense(file)

#To draw the bar chart based on the months of the year
hist=pygal.Bar()
hist.title="Monthly Expenses Of The Year"
hist.x_labels=["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]

#To setdefault values of expenses to '0' if the statements of the months are not available yet
for key in hist.x_labels:
    monthly_expense.setdefault(key,0)

y_values=[monthly_expense['JAN'],monthly_expense['FEB'],monthly_expense['MAR'],monthly_expense['APR'],monthly_expense['MAY'],monthly_expense['JUN'],monthly_expense['JUL'],monthly_expense['AUG'],monthly_expense['SEP'],monthly_expense['OCT'],monthly_expense['NOV'],monthly_expense['DEC']]
hist.x_title="Month"
hist.y_title="Total Expenses"
hist.add('US Dollars',y_values)
hist.render_to_file('monthlyexpense.svg') #Save the figure to a file named monthlyexpense.svg in the current directory

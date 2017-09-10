import pandas as pd
import numpy as np
import os
import xlrd
import re
from app import db, models

TTI_file = '/var/www/otti/data/Texas Transfer Inventory_2016-17.xls'

xl_workbook = xlrd.open_workbook(TTI_file)
sheet_names = xl_workbook.sheet_names()
sheet_names = sheet_names[2:] # Names of institutions begin in third entry

def get_values(row):
    tuple = []
    for i in range(len(row)):
        if row[i].value != '':
            tuple.append(row[i].value)
    return tuple

def find_left_edge(xl_sheet):
    ''' Finds index of left-edge of "Course Guide" field in TTI
    by searching for "Course Guide" in the second row.
    '''
    edge = 0
    for i in range(len(xl_sheet.row(1))):
        if xl_sheet.row(1)[i].value.strip() == 'Course Guide':
            return i
    return None

def end_of_maths(row):
    for entry in row:
        if entry.value.strip() == 'Math Requirements':
            return True
    return False

def get_math_offerings(xl_workbook,sheet_names):
    ''' Populates a Python dict with institution names as keys
    and values as lists of mathematics courses scraped from TTI.'''
    
    dict = {}
    for sheet in sheet_names:
        first = []
        last = []
        xl_sheet = xl_workbook.sheet_by_name(sheet)
        i=2
        left_edge = find_left_edge(xl_sheet)
        course_list = []
        while not end_of_maths(xl_sheet.row(i)):
            row = xl_sheet.row(i)
            values = get_values(row)
            first.append(values[0])
            try:
                last.append(values[1])
            except:
                i += 1
                continue
            i += 1
        course_list = first + last
        dict[sheet]=course_list
    return dict

dict = get_math_offerings(xl_workbook,sheet_names)
df = pd.DataFrame.from_dict(dict,orient='index').transpose()

for sheet_name in df:
    institution_id = models.Institution.query.filter_by(sheet_name=sheet_name).first().id
    for course in df[sheet_name]:
        if course:
            rubric, number = course.split(' ')[:2]
            name = ' '.join(course.split(' ')[2:])
            course = models.Course(name=name,rubric=rubric,number=number,institution_id=institution_id)
            db.session.add(course)

db.session.commit()

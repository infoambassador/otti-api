import pandas as pd
import numpy as np
import os
import xlrd
import re
from otti import db, models

TTI_file = '/var/www/otti/data/Texas Transfer Inventory_2016-17.xls'

xl_workbook = xlrd.open_workbook(TTI_file)
sheet_names = xl_workbook.sheet_names()
sheet_names = sheet_names[2:] # Names of institutions begin in third entry

def get_institution_name(sheet_name):
    ''' Scans first column of the spreadsheet looking for
    a non-empty cell containing the document title. It 
    extracts and formats the title.(Ambiguity is necessary 
    because all titles are in the first column, but not 
    all in the first row.)
    '''
    xl_sheet = xl_workbook.sheet_by_name(sheet_name)
    col = xl_sheet.col(0)
    for entry in col:
        if entry != '':
            return remove_excess_spaces(str(entry.value))
    return None

def remove_excess_spaces(institution_name):
    ''' Scraped institution names are full of spaces. This
    function removes the extra spaces.
    E.g., '  San    Jacinto  College ' --> 'San Jacinto College'
    '''
    split_name = institution_name.split(' ')
    non_empty_entries = [e for e in split_name if e != '']
    institution_name = ' '.join(non_empty_entries)
    return institution_name

def insert_institution(sheet_names):
    for sheet_name in sheet_names:
        institution_name = get_institution_name(sheet_name)
        inst = models.Institution(name=institution_name)
        db.session.add(inst)
    consent = input("Names added. Commit? (Type \"yes\"): ")
    if consent == "yes":
        db.session.commit()
        return "Inserts committed."
    else:
        db.session.close()
        return "Inserts aborted."

# insert_institution(sheet_names)

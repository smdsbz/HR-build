#!/usr/bin/python3
# -*- coding: utf-8 -*-

'   self-made utils for operating .xlsx files based on openpyxl (*nix only) ---- by smdsbz   '

from openpyxl import Workbook, load_workbook
from datetime import datetime
#import os, shutil


######## utils ########

def _read_test():
	# return table header line
	wb = load_workbook('./score-sheets/template.xlsx')
	data = wb.get_sheet_by_name(wb.get_sheet_names()[0])
	return tuple([ content.value for content in data['A2':'M2'][0] ])

def _move_cursor(name='something you have to mess up with'):
	# return the index asked
	# IF no match THEN yield index-number for the next empty row
	wb = load_workbook('./score-sheets/template.xlsx')
	data = wb.get_sheet_by_name(wb.get_sheet_names()[0])
	nameCells = data['A'][0:] # 1: test-use; running: 2
	names = tuple(filter(lambda s: s and s.strip(), [ content.value for content in nameCells ]))  # thx 2 MichealLiao
	#print(names)
	if name in names:
		return names.index(name) + 1 # 2: test-use
	else:
		return len(names) + 1

def newFile(title="测试测试", depart="其他", *, date=str(datetime.now())):
	# "./score-sheets/测试测试 - 2017-01-25 xx.xxxxxxx.xlsx"
	try:
		filename = './score-sheets/' + title + ' - ' + date + '.xlsx'
		wb = load_workbook('./score-sheets/template.xlsx')
		ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
		ws.title = title
		ws['B1'], ws['F1'], ws['J1'] = title, depart, date
		wb.save(filename)
		return 1
	except:
		return 0

def write(src, data):
	try:
		wb = load_workbook(src)
		ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
		cur = str(_move_cursor(data[0]))
		dst = ws['A'+cur:'K'+cur][0]
		map(lambda x, y: x.value = y, [ x, y for x in dst for y in data ])
		wb.save(src)
		return 1
	except:
		return 0

######## test-use ########

if __name__ == '__main__':
	# expecting result in console ==> "姓名\项目"
	print(_read_test())
	# expecting result in console ==> 2
	print("姓名\项目 is at", _move_cursor(name="姓名\\项目"))
	# expecting result in console ==> 3
	print("if no match:", _move_cursor())

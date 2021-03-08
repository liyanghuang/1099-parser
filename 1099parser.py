import pandas as pd
import pdfplumber
import re

with pdfplumber.open("/Users/liyanghuang/Downloads/1099.pdf") as pdf:
	page = pdf.pages[5]
	text = page.extract_text()

symbol_re = re.compile(r'.*\/ Symbol:\s*$')
date_re = re.compile(r'^\d{2}\/\d{2}\/\d{2} .*')

lines = text.split('\n')

i = 0
while i < len(lines):
	symbol_line = lines[i]
	if symbol_re.match(symbol_line):
		print(symbol_line)
		i += 1
		date_line = lines[i]
		while i < len(lines) and not symbol_re.match(date_line):
			if date_re.match(date_line):
				print(date_line)
			i+= 1
			if i < len(lines):
				date_line = lines[i]
		i -= 1
	i += 1

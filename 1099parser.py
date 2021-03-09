import pdfplumber
import re
import csv
from tqdm import tqdm

print('(When entering file paths on windows, use \'/\' in the place of \'\\\')')
pdf_path = input('Enter the file path of the 1099 pdf:\n')

# open up the pdf file, keep trying until user enters valid file
valid_pdf = False
while not valid_pdf:
	try:
		pdf = pdfplumber.open(pdf_path)
		valid_pdf = True
	except FileNotFoundError:
		pdf_path = input('The file entered is not a valid file, please try again:\n')

# open up csv file, use default.csv if nothing is entered
csv_path = input('Enter the file path of the output csv:\n')
if csv_path == '':
	print('Nothing was entered, using default file and location: ./default.csv')
	csv_path = 'default.csv'
valid_csv = False
while not valid_csv:
	try:
		csv_file = open(csv_path, 'w', newline='')
		csv_writer = csv.writer(csv_file, delimiter=',')
		valid_csv = True
	except FileNotFoundError:	
		csv_path = input('The file entered is not a valid file, please try again:\n')

# ask the user if they want to compile multiple transactions into one
# mainly for the 'xxx transactions for xx/xx/xx' lines
compile_multiple = input('Compile multiple transactions? (Y/n):\n').lower()
if compile_multiple == '':
	print('Nothing was entered, using default \'n\'')
	compile_multiple = 'n'
while not (compile_multiple == 'y' or compile_multiple == 'n'):
	compile_multiple = input('Invalid input, try again. Enter \'Y\' or \'n\':\n').lower()

# regex for the symbol line
symbol_re = re.compile(r'.*\/ Symbol:\s*$')
# regex for date line
date_re = re.compile(r'^\d{2}\/\d{2}\/\d{2} .*')
# regex for transaction line
transaction_re = re.compile(r'^\d* transactions for \d{2}\/\d{2}\/\d{2}.*')
# regex for transaction child line
transaction_child_re = re.compile(r'^\d*\.\d* .*')

print('Transforming to csv...')

# write csv headers
csv_writer.writerow(['Security', 'Date sold or disposed', 'Quantity', 'Proceeds/Reported gross or net', 'Date acquired', 'Cost or other basis', 'Accrued mkt disc/Wash sale loss disallowed', 'Gain or loss', 'Additional Information'])

for page in tqdm(pdf.pages):
	# extract each line from each page
	text = page.extract_text()
	lines = text.split('\n')
	i = 0
	while i < len(lines):
		symbol_line = lines[i]
		# attempt to match symbol line which signals start of a security block
		if symbol_re.match(symbol_line):
			# once we found symbol look at next lines to figure out what to do next
			i += 1
			date_line = lines[i]
			while i < len(lines) and not symbol_re.match(date_line):
				# if we are not compiling multiple transactions, we want to write out each one
				if compile_multiple == 'n':
					# attemp to match transaction line to see if this security has multiple transactions
					if transaction_re.match(date_line):
						# if it is, we pull out the number, and the date for all of them
						num_transactions = int(date_line.split(' ')[0])
						date_dis = date_line.split(' ')[3][:8]
						trans_counter = 0
						# next we iterate through to capture all the individual transactions
						while trans_counter < num_transactions:
							i += 1
							date_line = lines[i]
							if transaction_child_re.match(date_line):
								split_date_line = date_line.split(' ')
								accrued_disc = '...' if split_date_line[4] == '...' else ' '.join(split_date_line[4:6])
								additional_info = ' '.join(split_date_line[6:]) if split_date_line[4] == '...' else ' '.join(split_date_line[7:])
								csv_writer.writerow([symbol_line.split(' / ')[0]] + [date_dis] + split_date_line[:4] + [accrued_disc] + [additional_info])
								trans_counter += 1
						# after we are done, we skip to the next symbol line
						while i < len(lines) and not symbol_re.match(date_line):
							i += 1
							if i < len(lines):
								date_line = lines[i]
						continue
				
				# if we are not compiling multiple transactions, just write out the lines that 
				# match the dateline regex which includes compiled transactions
				if date_re.match(date_line):
					split_date_line = date_line.split(' ')
					accrued_disc = '...' if split_date_line[5] == '...' else ' '.join(split_date_line[5:7])
					additional_info = ' '.join(split_date_line[7:]) if split_date_line[5] == '...' else ' '.join(split_date_line[8:])
					csv_writer.writerow([symbol_line.split(' / ')[0]] + split_date_line[:5] + [accrued_disc] +[additional_info] )
				i+= 1
				if i < len(lines):
					date_line = lines[i]
			i -= 1
		i += 1

# close files
csv_file.close()
pdf.close()
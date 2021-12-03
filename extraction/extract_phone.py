import os,sys,codecs,re

def main(dir_, out_path, max_file_no):
	emails = []
	for i in range(max_file_no + 1):
		fileName = os.path.join(dir_,str(i)+'.txt')
		if (i == 0 or i == max_file_no):
			print("File: {0}".format(os.path.abspath(fileName)))
		if (not os.path.exists(fileName)):
			emails.append('')
			continue
		content = codecs.open(fileName, 'r',encoding='utf-8',errors='ignore').readlines()
		for line in content:
			match = re.findall(r'[\d]{3}-[\d]{3}-[\d]{4}', line)
			if len(match) > 0:
				emails.append(match[0].lower().strip())
			else:
				emails.append('')

	with codecs.open(out_path,'w',encoding='utf-8',errors='ignore') as f:
		for email in emails[:-1]:
			f.write(email+'\n')
		if emails[-1]=='':
			f.write('\n')
		else:
			f.write(emails[-1])

if __name__ == '__main__':
	# Get the current working directory
	cwd = os.getcwd()

	# Print the current working directory
	# print("Current working directory: {0}".format(cwd))
	print("\nBegin to process phone, the source is at: {0}".format(os.path.abspath("../data/compiled_bios/")))
	print("The destination is at : {0}".format(os.path.abspath("../data/phones")))
	max_file_no = int(sys.argv[1])
	main('../data/compiled_bios/','../data/phones', max_file_no)
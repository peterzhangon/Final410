import os,codecs,re

def main(dir_,out_path):
	emails = []
	for i in range(len(os.listdir(dir_))-1):
		fileName = os.path.join(dir_,str(i)+'.txt')
		print("File: {0}".format(os.path.abspath(fileName)))
		if (not os.path.exists(fileName)):
			continue
		print("Begin to proess {0}".format(os.path.abspath(os.path.join(dir_,str(i)+'.txt'))))
		content = codecs.open(fileName), 'r',encoding='utf-8',errors='ignore').readline()
		for line in content:
			match = re.findall(r'[\w\.-]+@[\w\.-]+', line)
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
	print("Current working directory: {0}".format(cwd))
	print("Current working directory: {0}".format(os.path.abspath("../data/compiled_bios/")))
	print("Current working directory: {0}".format(os.path.abspath("../data/emails")))
	main('../data/compiled_bios/','../data/emails')

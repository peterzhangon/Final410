import os,codecs,json

def main(base_data_dir,output_dataset_full_corpus,output_meta_data,input_dept_path,uni_path,input_names_path,input_url_path,input_loc_path,input_email_path,input_phone_num,output_unis_filter_file,output_locs_filter_file):
	with open(uni_path,'r') as f:
		unis = f.readlines()

	with open(input_dept_path,'r') as f:
		depts = f.readlines()

	with open(input_names_path,'r') as f:
		names = f.readlines()

	with open(input_url_path,'r') as f:
		urls = f.readlines()

	with codecs.open(input_loc_path,'r',encoding='utf-8',errors='ignore') as f:
		locs = f.readlines()

	with codecs.open(input_email_path,'r',encoding='utf-8',errors='ignore') as f:
		emails = f.readlines()

	with codecs.open(input_phone_num,'r',encoding='utf-8',errors='ignore') as f:
		phones = f.readlines()

	max_len = 15
	max_parts = 3
	non_names = ['curriculum','vitae','bio','professor','assistant',')','(','--','nat','center','sitemap','u.','2002','washington']

	corrected_names = []

	for name in names:
		parts = name.strip().split()
		corrected_name = ''
		for part in parts[:max_parts]:
			if len(part)<=max_len and part.lower() not in non_names and part.title() not in corrected_name.split():
				corrected_name += ' '+part.title()
		corrected_names.append(corrected_name)

	# The real file numbers
	num_bios = len(os.listdir(base_data_dir))-5

	print(len(phones),len(emails),len(corrected_names),len(locs),len(depts),len(unis),num_bios)

	with open(output_dataset_full_corpus,'w') as f1:
		with codecs.open(output_meta_data,'w',encoding='utf-8',errors='ignore') as f2:
			for i in range(num_bios)[:-1]:
				f1.write('[None] '+str(i)+'.txt')
				f1.write('\n')
				if emails[i]=='\n':
					emails[i]='None'
				if phones[i]=='\n':
					phones[i]='None'
				f2.write(str(i)+'.txt'+'\t'
					+unis[i].strip()+'\t'+depts[i].strip()+'\t'+corrected_names[i]+'\t'+urls[i].strip()+'\t'+locs[i].strip()+'\t'+emails[i].strip()+'\t'+phones[i].strip())
				f2.write('\n')

			f1.write('[None] '+str(num_bios-1)+'.txt')
			if emails[num_bios-1]=='\n':
				emails[num_bios-1]='None'
			if phones[num_bios-1]=='\n':
				phones[num_bios-1]='None'
			f2.write(str(num_bios-1)+'.txt'+'\t'
				+unis[num_bios-1].strip()+'\t'+depts[num_bios-1].strip()+'\t'+corrected_names[num_bios-1]+'\t'+urls[num_bios-1].strip()+'\t'+locs[num_bios-1].strip()+'\t'+emails[num_bios-1].strip()+'\t'+phones[num_bios-1].strip())

	unis_dict = {"unis":sorted([uni.strip() for uni in list(set(unis))])}
	all_countries = set()
	all_locs = set()

	for loc in locs:
		country = loc.split('\t')[1]
		all_countries.add(country.strip())
		all_locs.add(loc.replace('\t',', ').strip())

	all_countries = sorted(list(all_countries))
	all_locs = sorted(list(all_locs))
	all_locs = all_countries + all_locs

	locs_dict = {"locs":all_locs}

	json.dump(unis_dict,open(output_unis_filter_file,'w'))
	json.dump(locs_dict,open(output_locs_filter_file,'w'))

if __name__ == '__main__':
	base_data_dir = './data/compiled_bios'
	print("base_data_dir : {0}".format(os.path.abspath(base_data_dir)))
	output_dataset_full_corpus = './data/compiled_bios/dataset-full-corpus.txt'
	print("output_dataset_full_corpus : {0}".format(os.path.abspath(output_dataset_full_corpus)))
	output_meta_data = './data/compiled_bios/metadata.dat'
	print("output_meta_data : {0}".format(os.path.abspath(output_meta_data)))
	input_dept_path = './data/depts'
	print("input_dept_path : {0}".format(os.path.abspath(input_dept_path)))
	uni_path = './data/unis'
	print("uni_path : {0}".format(os.path.abspath(uni_path)))
	input_names_path = './data/names.txt'
	print("input_names_path : {0}".format(os.path.abspath(input_names_path)))
	input_url_path = './data/urls'
	print("input_url_path : {0}".format(os.path.abspath(input_url_path)))
	input_loc_path = './data/location'
	print("input_loc_path : {0}".format(os.path.abspath(input_loc_path)))
	input_email_path = './data/emails'
	print("input_email_path : {0}".format(os.path.abspath(input_email_path)))
	input_phone_num = './data/phones'
	print("input_phone_num : {0}".format(os.path.abspath(input_phone_num)))
	output_unis_filter_file = './data/filter_data/unis.json'
	print("output_unis_filter_file : {0}".format(os.path.abspath(output_unis_filter_file)))
	output_locs_filter_file = './data/filter_data/locs.json'
	print("output_locs_filter_file : {0}".format(os.path.abspath(output_locs_filter_file)))

	main(base_data_dir, output_dataset_full_corpus, output_meta_data, input_dept_path, uni_path, input_names_path, input_url_path, input_loc_path, input_email_path, input_phone_num, output_unis_filter_file, output_locs_filter_file)

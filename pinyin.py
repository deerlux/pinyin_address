#!/usr/bin/env python
#coding=utf-8

def get_pinyin_first_letter(str, dict):		
	try:
		letter = dict[ord(str[0])][0]
	except KeyError:
		letter = str
	return letter
def get_pinyin_first_letters(str,dict):
	import string
	letters = [get_pinyin_first_letter(c,dict) for c in str]
	return string.join(letters,'')
def gbk2utf(str):
	return str.decode('gbk')
def utf2gbk(str):
	return str.encode('gbk')
#if __name__ == '__main__':
#	import cPickle
#	file1 = open("pydb.db",'rb')
#	pinyin_dict = cPickle.load(file1)
#	file1.close()
#	print get_pinyin_first_letters(u'朱镕基',pinyin_dict)

if __name__== '__main__':
	import sys
	import csv
	import getopt
	import cPickle
	import os.path

	prog_path = os.path.dirname(sys.argv[0])
	file1 = open(os.path.join(prog_path,"pydb.db"),'rb')
	pinyin_dict = cPickle.load(file1)
	file1.close()

	try:
		opts,args = getopt.getopt(sys.argv[1:], "i:o:d")
	except getopt.GetoptError, err:
		print str(err)         
		sys.exit(2)
	inverse = False
	for o, a in opts:
		if o == "-i":
			ifilename = a
		elif o =='-o':
			ofilename = a            
		elif o == '-d':
			inverse = True        
	
	if len(sys.argv) >1:
		if len(sys.argv) == 2:
			ifilename = sys.argv[1]
			ofilename = os.path.join(os.path.dirname(sys.argv[1]), \
					os.path.basename(sys.argv[1]).split('.')[0] + '_new.csv')

		cread = csv.reader(file(ifilename, 'rb'), dialect='excel')
		cwrite = csv.writer(file(ofilename,'wb'), dialect ='excel')
		iter = 0
		for row in cread:
			row[1] = gbk2utf(row[1])
			row[3] = gbk2utf(row[3])
			if iter != 0:
				# 如果姓为空则姓改为拼音首字缩写
				if row[3] == "":					
					row[3] = get_pinyin_first_letters(row[1],pinyin_dict)
				# 如果名为空则改为姓的值，再把姓改为名的拼音首字缩写
				elif row[1] == '':
					row[1] = row[3]
					row[3] = get_pinyin_first_letters(row[1],pinyin_dict)
				# 如果两者均不为空，则将名和姓连接，再将姓改为拼音首字缩写
				else:
					if inverse:
						row[1] = row[1]+row[3]
						row[3] = get_pinyin_first_letters(row[1],pinyin_dict)
					else:
						row[1] = row[3]+row[1]
						row[3] = get_pinyin_first_letters(row[1],pinyin_dict)
			row[1]=utf2gbk(row[1])
			row[3]=utf2gbk(row[3])
			cwrite.writerow(row)
			iter = iter + 1	
	else:
		usage=u'''用法:  pinyin.exe -i XXX.csv -o YYY.csv [-d]'''
		print usage

#-*- coding: utf-8 -*-
## 
import re, os, codecs, sys, glob

# path = '/Users/muhammedyidris/git/bootstrapping_classes/data'
# filelist = glob.glob( os.path.join(path, 'nyt_index-2.txt'))

test_cases = []
test_cases_labels = []
doca_protests = eval(open('/Users/muhammedyidris/git/bootstrapping_classes/data/doca_protest_test_cases.txt').read())

print 'Starting doca_protests'
for i in doca_protests:
	path = '/Volumes/MYI_PASS/data/nyt_corpus/data/'+i.strip()
	f = open(path).read()
	head, sep, tail = f.partition('<block class="full_text">')
	head, sep, tail = tail.partition('</block>')
	foo = head.replace('\n', '').replace('<p>', ''). replace('</p>', '').replace('    ', ' ').replace('  ', ' ')
	test_cases.append(foo)
	test_cases_labels.append(1)
	# break
print 'Starting non_protests'

non_protests = open('/Users/muhammedyidris/Dropbox/dissertation/data/preprocessed_source/non_protests.txt').read()
non_protests = non_protests.split('</story>')

for i in non_protests:
	head, sep, tail = i.strip().partition('<source>')
	fook = tail.replace('\n', ' ').replace('<p>', '').replace('</source>', '').replace('  ', ' ')
	test_cases.append(fook)
	test_cases_labels.append(0)
	# break

print 'Writing files...'
# out = open('/Users/muhammedyidris/git/bootstrapping_classes/data/test_cases.txt', 'w+')

for i in test_cases:
	print i.strip()+'\n\n'
	break
# out.close()

# out1 = open('/Users/muhammedyidris/git/bootstrapping_classes/data/test_cases_labels.txt', 'w+')
# print test_cases_labels
# out1.close()

print len(test_cases)
print len(test_cases_labels)
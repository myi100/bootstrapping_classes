#-*- coding: utf-8 -*-
## SVM classifier
import re, os, codecs, sys, glob
import random
import hashlib
import numpy as np
import pylab as pl
import matplotlib.font_manager
from sklearn import svm
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from scipy.stats import itemfreq
from sklearn.metrics import accuracy_score, average_precision_score, confusion_matrix, classification_report
import time

print 'Setting up pipeline...\n'
##################################
##Processing Pipeline
text_clf = Pipeline([('vect', CountVectorizer()),
							('tfidf', TfidfTransformer()),
							('clf', svm.OneClassSVM(nu=0.1, kernel="linear")),
])
##################################

print 'Training classifier...'
##################################
##Training Data
training = open('/Users/muhammedyidris/bootstrapping_classes/prefilter/doca_protest.txt').read()
re_story = re.compile('\#{1,}.END.OF.STORY.[1-9]{1,}.\#{1,}')
training_set = re.split(re_story, training)
training_set_target = np.asarray([1] * len(training_set))
del training_set[-1]
false = open('/Users/muhammedyidris/bootstrapping_classes/prefilter/non_protests.txt').read()
false_set = re.split(re_story, false)
del false_set[-1]


print '-Training-set size: '+str(len(training_set))

train_smpl = [ training_set[i] for i in sorted(random.sample(xrange(len(training_set)), int(len(training_set) * .25))) ]
train_target = np.asarray([1] * len(train_smpl))
test_smpl = list(set(training_set) - set(train_smpl))+false_set
test_target = np.asarray(([1] * (len(test_smpl)-len(false_set))) + ([-1] * len(false_set)))

print '-Training-set training-sample size: '+str(len(train_smpl))
print '-Training-set testing-sample size: '+str(len(test_smpl))

##Test Classifier
_ = text_clf.fit(train_smpl, train_target)
classifier_predicted = text_clf.predict(test_smpl)
accuracy = np.mean(classifier_predicted == test_target)
print '-Classifier accuracy: '+str(accuracy*100)[0:5]+'%'
print '-Confusion matrix:\n'+str(confusion_matrix(test_target, classifier_predicted))+'\nwhere x = true labels; y = predicted labels.\n'
print '-Classification report:\n'+classification_report(test_target, classifier_predicted)+'\n'

#false_negative
# for 
#false_positive
###################################

###################################
##Test Data
path = '/Users/muhammedyidris/bootstrapping_classes/nyt/formatted_nyt'
filelist = glob.glob( os.path.join(path, '*.txt'))

test_set = []
for fullfile in filelist:
	f = open(fullfile).read().split('\n\n\n')
	test_set = test_set + f
	break

print 'Test-set size: '+str(len(test_set))+'\n'
###################################

print 'Classifying test set...'
##################################
#Test Classifier
start_time = time.time()
predicted = text_clf.predict(test_set).astype(np.int64)
elapsed_time = time.time() - start_time
print 'Classification time: '+str(elapsed_time)
print 'Frequency:\n'+str(itemfreq(predicted))+'\n'


p_fileno = 100
positive_cases = open('/Users/muhammedyidris/git/bootstrapping_classes/filtered_nyt/filtered_nyt-'+str(p_fileno)+'.txt', 'w+')
p = 0

k_fileno = 100
keyword_cases = open('/Users/muhammedyidris/git/bootstrapping_classes/filtered_nyt/by_keyword/filtered_nyt_by_keyword-'+str(k_fileno)+'.txt', 'w+')
k = 0

keywords = ['protest', 'protesters', 'protests', 'rights', 'demonstrators', 'demonstration', 'support', 'demonstrations', 'activists', 'opposition', 'arrested', 'crowd', 'fired', 'march', 'hundreds', 'marched', 'protesting', 'organized', 'demand', 'protested', 'organization', 'demonstrated', 'demanding', 'dozens', 'criticized', 'protestors', 'activist', 'protester', 'marchers', 'Demonstrators', 'demands', 'oppose', 'boycott', 'demonstrate', 'organizers', 'casualties', 'anti-government', 'criticizing']


for i in range(0, len(predicted)):
	if predicted[i] == 1:
		if positive_cases.tell() + sys.getsizeof(test_set[i]) > 11141120:
			positive_cases.close()
			p_fileno+=1
			positive_cases = open('/Users/muhammedyidris/git/bootstrapping_classes/filtered_nyt/test/filtered_nyt-'+str(p_fileno)+'.txt', 'w+')
		
		print >> positive_cases, test_set[i]+'\n'
		p+=1

		if any(key in test_set[i][0:300] for key in keywords):
			if keyword_cases.tell() + sys.getsizeof(test_set[i]) > 11141120:
				keyword_cases.close()
				k_fileno+=1
				keyword_cases = open('/Users/muhammedyidris/git/bootstrapping_classes/test/filtered_nyt/by_keyword/filtered_nyt_by_keyword-'+str(k_fileno)+'.txt', 'w+')
			
			print >> keyword_cases, test_set[i]+'\n'
			k+=1



# positive_cases = open('/Users/muhammedyidris/bootstrapping_classes/bootstrap/filtered_nyt.txt', 'w+')
# p = 0
# keyword_cases = open('/Users/muhammedyidris/bootstrapping_classes/boostrap/filtered_nyt_by_keyword.txt', 'w+')
# k = 0
# keywords = ['protest', 'protesters', 'protests', 'rights', 'demonstrators', 'demonstration', 'support', 'demonstrations', 'activists', 'opposition', 'arrested', 'crowd', 'fired', 'march', 'hundreds', 'marched', 'protesting', 'organized', 'demand', 'protested', 'organization', 'demonstrated', 'demanding', 'dozens', 'criticized', 'protestors', 'activist', 'protester', 'marchers', 'Demonstrators', 'demands', 'oppose', 'boycott', 'demonstrate', 'organizers', 'casualties', 'anti-government', 'criticizing']

# for i in range(0, len(predicted)):
# 	if predicted[i] == 1:
# 		print >> positive_cases, test_set[i]+'\n'
# 		p+=1
# 		if any(key in test_set[i][0:300] for key in keywords):
# 			print >> keyword_cases, test_set[i]+'\n'
# 			k+=1

print 'Positive cases: '+str(p)+' ('+str(float(p)/len(test_set) * 100)[0:5]+'% of test-cases.)'
print 'Keyword-filtered cases: '+str(k)+' ('+str((float(k)/p)* 100)[0:4]+'% of positive-cases, '+str((float(k)/len(test_set))* 100)[0:4]+'% of test-cases)\n'
print 'Keywords: '+str(keywords)

###################################
# # corpus['DESCR'] #str description
# # corpus['data'] #list with every element raw text
# # corpus['target'] #numpy.int mapping on to target_names/categories
# # corpus['target_names'] #list of categories
# # corpus['feature_names']


import sys, os, string
import gzip
from bootstrap_assist_9_7 import * 
from multiprocessing import Process


#fpath = '/uusoc/scratch/res/nlp/ruihong/OSI/bootstrap_5_5_18_check_35P_diff_epC_twoSideLoosened_reducedCond_popuModFreqFixed7_2/'
fpath = '/uusoc/scratch/res/nlp/ruihong/OSI/bootstrap_5_5_18_check_35P_diff_epC_twoSideLoosened_reducedCond_popuModFreqFixed7_3/'
fout_popu = open(fpath+'population_bootstrapped', 'w')
fout_reason = open(fpath+'reason_bootstrapped', 'w')
fout_event = open(fpath+'event_bootstrapped', 'w')

#fout_reason_pa = open(fpath+'reason_bootstrapped_phrases', 'a')
#fout_event_pa = open(fpath+'event_bootstrapped_phrases', 'a')

#agents
popu_list_new = {}
reason_list_new = {}
event_list_new = {}
#reason_list_new_p = {}
#event_list_new_p = {}
#reason_list_new_a = {}
#event_list_new_a = {}

popu_list = []
popu_dict = {}
file_popu = open('population_seeds_10.txt')
#file_popu = open('population_seeds_10_2.txt')
#file_popu = open('population_seeds_10_hrl.txt')
#file_popu = open('population_10seeds_20iter.txt')
for line in file_popu:
	if not line: break
	line = line.strip()
	if line != '':
		popu_list.append(line)
		popu_dict[line] = 1
		popu_list_new[line] = 1
		fout_popu.write(line+'\n')
file_popu.close

reason_list = []
reason_dict = {}
#reason_list_p = []
#reason_dict_p = {}
#reason_dict_a = {}

#reason_dict_pa = {}

#pattern_seeds = ['demanding', 'protesting', 'to demand', 'to protest'] #pa
#reason_pattern_seeds = ['to demand', 'to protest'] #pa
reason_pattern_seeds = ['to demand', 'to protest', 'demanding', 'protesting'] #pa
reason_seeds = []
file_reason = open('reason_seeds_freq')
for line in file_reason:
	if not line: break
	line = line.strip()
	if line != '':		
		reason_seeds.append(line)		
file_reason.close


#fout_reason.write('reason seeds:\n')
for seed in reason_pattern_seeds:
	fout_reason.write(seed+'\n')
	reason_list.append(seed)
	reason_dict[seed] = 1

#for pat in pattern_seeds:
#	for reason in reason_seeds:
#		reasonP = pat+' '+reason
#		reason_list.append(reasonP)
#		reason_dict[reasonP] = 1
#		reason_list_new[reasonP] = 1
#		fout_reason.write(reasonP+'\n')
'''fout_reason.write('pattern seeds:\n')
for pat in reason_pattern_seeds:
	reason_list_p.append(pat)
	reason_dict_p[pat] = 1
	fout_reason.write(pat+'\n')
fout_reason.write('arg seeds:\n')
for reason in reason_seeds:
	reason_dict_a[reason] = 1
	fout_reason.write(reason+'\n')'''


	

#at the beginning, empty event_list
event_list = []
event_dict = {}
#event_list_p = []
#event_dict_p = {}
#event_dict_a = {}

#event_dict_pa = {}

'''flist = []
#fin_list = open('Gigaword_v5_afp')
fin_list = open('Gigaword_v5_filelist_cleaned_training')
for line in fin_list:
	if not line: break
	line = line.strip()
	if line != '':
		flist.append(line)
fin_list.close'''

part_size = 16

flist_parts = [] 

i = 0
while i < part_size:
	flist_parts.append([])
	i += 1

flist = []
#fin_list = open('/home/huangrh/data/OSI/bootstrap/Gigaword_v5_afp')
#fin_list = open('/home/huangrh/data/OSI/bootstrap/Gigaword_v5_filelist_cleaned_training')
#fin_list = open('Gigaword_v5_filelist_cleaned_training')
fin_list = open('Gigaword_v5_filelist_cleaned_training_filtered')
#fin_list = open('hrl_english_file.txt')
cycle = 0
for line in fin_list:
	if not line: break
	line = line.strip()
	if line != '':
		flist.append(line)
		flist_parts[cycle].append(line)
		cycle = (cycle + 1) % part_size
fin_list.close

reason_popu_list = []
reason_popu_dict = {}
reason_popu_list_new = {}
#reason_popu_list_p = []
#reason_popu_dict_p = {}
#reason_popu_dict_a = {}
#reason_popu_list_new_p = {}
#reason_popu_list_new_a = {}

popu_modifier_types_values = {}# num, no value
#popu_modifier_types = [] #num, nn, amod, poss, prep_in, prep_at

reason_seed_patt_phrases = {}


iteration_stop = 10

iteration = 0

outfname_event = fpath+'event_sentences_deps'
outfname_reason = fpath+'reason_sentences_deps'
outfname_popu = fpath+'popu_sentences_deps'
outfname_modifier = open(fpath+'modifier_iterations', 'a')

fou_log = open('event_pat_arg', 'w')

fou_logr = open('reason_pat_arg', 'w')

fou_popu_tracking = open('popu_tracking_8', 'w')
fou_reason_seed_patt_phrases = open(fpath+'reason_seed_patt_phrases', 'w')

relF = '/uusoc/scratch/res/nlp/ruihong/OSI/samples/samples_key_lowered'
generalF = '/uusoc/scratch/res/nlp/ruihong/OSI/samples/samples_nokey_lowered'

logf_succ = open('check_logs_18_check_35P_succ_diff_epC_twoSideLoosened_reducedCond_popuModFreqFixed7_2', 'a')
#logf_succ.write('second check:\n')
logf_fail = open('check_logs_18_check_35P_fail_diff_epC_twoSideLoosened_reducedCond_popuModFreqFixed7_2', 'a')
checked = {}
while iteration <= iteration_stop:
	fout_popu.write('****************************************************\n')
	fout_popu.write('iteration '+str(iteration)+':\n')
	fout_reason.write('****************************************************\n')
	fout_reason.write('iteration '+str(iteration)+':\n')
	fout_event.write('****************************************************\n')
	fout_event.write('iteration '+str(iteration)+':\n')
	fou_reason_seed_patt_phrases.write('****************************************************\n')
	fou_reason_seed_patt_phrases.write('iteration '+str(iteration)+':\n')

	#fout_reason_pa.write('****************************************************\n')
	#fout_reason_pa.write('iteration '+str(iteration)+':\n')
	#fout_event_pa.write('****************************************************\n')
	#fout_event_pa.write('iteration '+str(iteration)+':\n')

	##########################################event phrase learning step
	outfname = fpath+'event_sentences_'+str(iteration)
	popuFlag = True
	reasonFlag = True
	eventFlag = False
	#retrieve the sentences
	print 'event sentence retrieval at iteration '+str(iteration)+'...........................................'
	#sentence_retrieval(flist, popu_list, popu_list_new, reason_list, reason_list_new, event_list, event_list_new, popuFlag, reasonFlag, eventFlag, outfname)
	#sentence_retrieval(flist, popu_list, popu_list_new, reason_list_p, reason_dict_a, reason_list_new_p, reason_list_new_a, event_list_p, event_dict_a, event_list_new_p, event_list_new_a, popuFlag, reasonFlag, eventFlag, outfname)
	#dependency parsing
	#print 'dependency parsing at iteration '+str(iteration)+'...........................................'
	#os.system('/uusoc/res/nlp/nlp/Ruihong/makeRoom/stanford_parser/stanford-parser-2011-06-27/lexparser.sh '+outfname +' > '+outfname+'_deps')
	#os.system('/uusoc/res/nlp/nlp/Ruihong/makeRoom/stanford_parser/stanford-parser-2011-06-27/lexparser.sh '+outfname +' >> '+outfname_event)


	processV = []
	i = 0
	while i < part_size:
		processV.append(Process(target=sentence_retrieval, args=(flist_parts[i], popu_list, popu_list_new, reason_list, reason_list_new, event_list, event_list_new, popuFlag, reasonFlag, eventFlag, outfname+'_'+str(i))))


		#.start()
		i += 1
	i = 0
	while i < part_size:
		processV[i].start()
		i += 1
	i = 0
	while i < part_size:
		processV[i].join()
		i += 1	

	#tempOut = open(outfname, 'w')
	tempOut_parts = []

	tempUniqs = {}
	i = 0
	while i < part_size:
		tempIn = open(outfname+'_'+str(i))
		tempOut_parts.append(open(outfname+'_d'+str(i), 'w'))
		for cline in tempIn:
			if not cline: break
			cline = cline.strip()
			if cline != '':
				if not cline in tempUniqs:
					#tempOut.write(cline+'\n\n')
					tempUniqs[cline] = 1
		tempIn.close
		i += 1
	#tempOut.flush()
	#tempOut.close
	sents = tempUniqs.keys()
	cycle = 0
	for csent in sents:
		tempOut_parts[cycle].write(csent+'\n\n')
		cycle = (cycle + 1) % part_size

	#dependency parsing
	print 'dependency parsing at iteration '+str(iteration)+'...........................................'

	processV = []

	i = 0
	while i < part_size:
		tempOut_parts[i].flush()
		tempOut_parts[i].close
		processV.append(Process(target=dep_parsing, args=(outfname+'_d'+str(i), outfname+'_d'+str(i)+'_dep')))
		i += 1
	i = 0

	i = 0
	while i < part_size:
		processV[i].start()
		i += 1
	i = 0
	while i < part_size:
		processV[i].join()
		i += 1	
	tempOut = open(outfname_event, 'a')
	i = 0
	while i < part_size:
		tempIn = open(outfname+'_d'+str(i)+'_dep')
		for line in tempIn:
			if not line: break
			tempOut.write(line)
		tempIn.close
		i += 1
	tempOut.flush()
	tempOut.close
		
	
	#fmerged = open(outfname_event)
	
	#event phrase learning
	#reason_threshold = 5
	#freqency_threshold_event = 10
	#popu_threshold = 2 + iteration
	popu_threshold = 2+iteration/10
	#reason_threshold = 3 + iteration/5
	reason_threshold = 2+iteration/10
	#freqency_threshold_event = 5 + iteration
	freqency_threshold_event = 2
	popu_modifier_types_values = {}
	[event_list_new, reason_phraseD, event_phraseWhole] = event_phrase_learning(outfname_event, event_dict, reason_dict, popu_dict, reason_threshold, freqency_threshold_event, popu_threshold, popu_modifier_types_values, reason_pattern_seeds)

	
	print 'event phrase learning at iteration '+str(iteration) +' done!'
	print 'new event phrases:'

	event_newK_0 = event_list_new.keys()
	print 'event before check: '+str(len(event_newK_0))
	event_check_threshold = 0.5
	#relevancy_check
	lexicon_parts = [] 
	i = 0
	while i < part_size:
		lexicon_parts.append([])
		i += 1
	cycle = 0
	for clex in event_newK_0:
		lexicon_parts[cycle].append(clex)
		cycle = (cycle + 1) % part_size

	processV = []
	i = 0
	while i < part_size:
		processV.append(Process(target=relevancy_check, args=(event_list_new, lexicon_parts[i], relF, generalF, event_check_threshold, 'event', i, checked)))
		#.start()
		i += 1
	i = 0
	while i < part_size:
		processV[i].start()
		i += 1
	i = 0
	while i < part_size:
		processV[i].join()
		i += 1

	logf_succ.write('event second check:\n')
	logf_fail.write('event second check:\n')
	event_newK = []
	i = 0
	while i < part_size:
		logf = open('check_temp7_'+str(i))
		for line in logf:
			if not line: break
			line = line.strip()
			if line != '':
				lineV = line.split('\t')
				if len(lineV) > 1:
					if lineV[0] == 'succ':
						event_newK.append(lineV[1])
						logf_succ.write(line+'\n')
					else:
						logf_fail.write(line+'\n')
		logf.close
		i += 1
	logf_succ.flush()
	logf_fail.flush()

	i = 0
	while i < part_size:
		logf = open('checked_temp7_'+str(i))
		for line in logf:
			if not line: break
			line = line.strip()
			if line != '':
				lineV = line.split('\t')
				if len(lineV) > 1:
					checked[lineV[0]] = lineV[1]
		logf.close					
		i += 1

	print 'checked: '+str(len(checked.keys()))	
	#exit(0)
	#event_newK = relevancy_check(event_list_new, relF, generalF, event_check_threshold, 'event')
	#event_newK = event_list_new.keys()
	print 'event after check: '+str(len(event_newK))
	#tempDict = {}
	for cevent in event_newK:
		event_list.append(cevent)
		event_dict[cevent] = 1
		fout_event.write(cevent+'\t'+str(event_list_new[cevent])+'\n')
		#ckey = cevent+'\t'+str(event_list_new[cevent])
		#cvalueV = event_list_new[cevent].split('\t')
		#cvalue = int(cvalueV[0])
		#tempDict[ckey] = cvalue
		#print cevent
	fout_event.flush()

	'''fout_osi = open(fpath+'event_phrase_learned', 'w')
	items = tempDict.items()
	backitems = [[v[1], v[0]] for v in items]
	backitems.sort()
	i = len(backitems) - 1
	while i >= 0:
		fout_osi.write(backitems[i][1]+'\n')
		i -= 1
	fout_osi.flush()
	fout_osi.close

	exit(0)'''


	fou_reason_seed_patt_phrases.write('from event phrase learning..............................:\n')
	ckeys = reason_phraseD.keys()
	for ckey in ckeys:
		#if not ckey in reason_dict_pa and reason_phraseD[ckey] > 1:
		if not ckey in reason_seed_patt_phrases:
			reason_seed_patt_phrases[ckey] = 1
			fou_reason_seed_patt_phrases.write(ckey+'\t'+str(reason_phraseD[ckey])+'\n')				
				
	fou_reason_seed_patt_phrases.flush()

	
	#exit(0)
	##########################################reason phrase learning step, parallel branch 1
	#save reasons for popu learning
	reason_popu_list = []
	reason_popu_dict = {}
	reason_popu_list_new = {}
	for ele in reason_list:
		reason_popu_list.append(ele)
		reason_popu_dict[ele] = 1
	rkeys = reason_list_new.keys()
	for ckey in rkeys:
		reason_popu_list_new[ckey] = 1
	

	outfname = fpath+'reason_sentences_'+str(iteration)
	popuFlag = True
	reasonFlag = False
	eventFlag = True
	#retrieve the sentences
	print 'reason sentence retrieval at iteration '+str(iteration)+'...........................................'
	#sentence_retrieval(flist, popu_list, popu_list_new, reason_list, reason_list_new, event_list, event_list_new, popuFlag, reasonFlag, eventFlag, outfname)
	#sentence_retrieval(flist, popu_list, popu_list_new, reason_list_p, reason_dict_a, reason_list_new_p, reason_list_new_a, event_list_p, event_dict_a, event_list_new_p, event_list_new_a, popuFlag, reasonFlag, eventFlag, outfname)
	#dependency parsing
	#print 'dependency parsing at iteration '+str(iteration)+'...........................................'
	#os.system('/uusoc/res/nlp/nlp/Ruihong/makeRoom/stanford_parser/stanford-parser-2011-06-27/lexparser.sh '+outfname +' >> '+outfname_reason)



	processV = []
	i = 0
	while i < part_size:
		processV.append(Process(target=sentence_retrieval, args=(flist_parts[i], popu_list, popu_list_new, reason_list, reason_list_new, event_list, event_list_new, popuFlag, reasonFlag, eventFlag, outfname+'_'+str(i))))


		#.start()
		i += 1
	i = 0
	while i < part_size:
		processV[i].start()
		i += 1
	i = 0
	while i < part_size:
		processV[i].join()
		i += 1	

	#tempOut = open(outfname, 'w')
	tempOut_parts = []

	tempUniqs = {}
	i = 0
	while i < part_size:
		tempIn = open(outfname+'_'+str(i))
		tempOut_parts.append(open(outfname+'_d'+str(i), 'w'))
		for cline in tempIn:
			if not cline: break
			cline = cline.strip()
			if cline != '':
				if not cline in tempUniqs:
					#tempOut.write(cline+'\n\n')
					tempUniqs[cline] = 1
		tempIn.close
		i += 1
	#tempOut.flush()
	#tempOut.close
	sents = tempUniqs.keys()
	cycle = 0
	for csent in sents:
		tempOut_parts[cycle].write(csent+'\n\n')
		cycle = (cycle + 1) % part_size

	#dependency parsing
	print 'dependency parsing at iteration '+str(iteration)+'...........................................'

	processV = []

	i = 0
	while i < part_size:
		tempOut_parts[i].flush()
		tempOut_parts[i].close
		processV.append(Process(target=dep_parsing, args=(outfname+'_d'+str(i), outfname+'_d'+str(i)+'_dep')))
		i += 1
	i = 0

	i = 0
	while i < part_size:
		processV[i].start()
		i += 1
	i = 0
	while i < part_size:
		processV[i].join()
		i += 1	
	tempOut = open(outfname_reason, 'a')
	i = 0
	while i < part_size:
		tempIn = open(outfname+'_d'+str(i)+'_dep')
		for line in tempIn:
			if not line: break
			tempOut.write(line)
		tempIn.close
		i += 1
	tempOut.flush()
	tempOut.close
	
	
	#reason phrase learning
	popu_threshold = 0+iteration/10
	#event_threshold = 2 + iteration/5
	event_threshold = 2+iteration/10
	#freqency_threshold_reason = 5 + iteration
	freqency_threshold_reason = 2
	[reason_list_new, event_phraseD, reason_phraseWhole_seed_patt] = reason_phrase_learning(outfname_reason, reason_dict, event_dict, popu_dict, event_threshold, freqency_threshold_reason, popu_threshold, popu_modifier_types_values, reason_pattern_seeds)



	print 'reason phrase learning at iteration '+str(iteration) +' done!'
	print 'new reason phrases:'
	#fout_reason.write('new reason phrases:\n')
	reason_newK_0 = reason_list_new.keys()
	print 'reason before check: '+str(len(reason_newK_0))
	reason_check_threshold = 0.5

	#relevancy_check
	lexicon_parts = [] 
	i = 0
	while i < part_size:
		lexicon_parts.append([])
		i += 1
	cycle = 0
	for clex in reason_newK_0:
		lexicon_parts[cycle].append(clex)
		cycle = (cycle + 1) % part_size

	processV = []
	i = 0
	while i < part_size:
		processV.append(Process(target=relevancy_check, args=(reason_list_new, lexicon_parts[i], relF, generalF, reason_check_threshold, 'reason', i, checked)))
		#.start()
		i += 1
	i = 0
	while i < part_size:
		processV[i].start()
		i += 1
	i = 0
	while i < part_size:
		processV[i].join()
		i += 1

	logf_succ.write('reason second check:\n')
	logf_fail.write('reason second check:\n')
	reason_newK = []
	i = 0
	while i < part_size:
		logf = open('check_temp7_'+str(i))
		for line in logf:
			if not line: break
			line = line.strip()
			if line != '':
				lineV = line.split('\t')
				if len(lineV) > 1:
					if lineV[0] == 'succ':
						reason_newK.append(lineV[1])
						logf_succ.write(line+'\n')
					else:
						logf_fail.write(line+'\n')
		i += 1
	logf_succ.flush()
	logf_fail.flush()

	i = 0
	while i < part_size:
		logf = open('checked_temp7_'+str(i))
		for line in logf:
			if not line: break
			line = line.strip()
			if line != '':
				lineV = line.split('\t')
				if len(lineV) > 1:
					checked[lineV[0]] = lineV[1]
		logf.close					
		i += 1
	#reason_newK = relevancy_check(reason_list_new, relF, generalF, reason_check_threshold, 'reason')
	print 'reason after check: '+str(len(reason_newK))
	for creason in reason_newK:
		reason_list.append(creason)
		reason_dict[creason] = 1
		fout_reason.write(creason+'\t'+str(reason_list_new[creason])+'\n')
		print creason

	fout_reason.flush()

	#exit(0)

	fou_reason_seed_patt_phrases.write('from reason phrase learning......................................:\n')
	ckeys = reason_phraseWhole_seed_patt.keys()
	for ckey in ckeys:
		if not ckey in reason_seed_patt_phrases:
			reason_seed_patt_phrases[ckey] = 1
			fou_reason_seed_patt_phrases.write(ckey+'\t'+str(reason_phraseWhole_seed_patt[ckey])+'\n')		
	fou_reason_seed_patt_phrases.flush()

	#report modifiers
	outfname_modifier.write('iteration '+str(iteration)+':\n')
	items = popu_modifier_types_values.items()
	items.sort()
	i = len(items) - 1
	while i >= 0:
		outfname_modifier.write(items[i][0]+':\n')
		citems = items[i][1].items()
		citems.sort()
		tempStr = ''
		j = len(citems) - 1
		while j >= 0:
			tempStr += citems[j][0]+' '
			j -= 1
		outfname_modifier.write(tempStr+'\n')
		i -= 1
	outfname_modifier.flush()
	#outfname_modifier.close

	##########################################population learning step, parallel branch 2
	outfname = fpath+'popu_sentences_'+str(iteration)
	popuFlag = False
	reasonFlag = True
	eventFlag = True
	#retrieve the sentences
	print 'popu sentence retrieval at iteration '+str(iteration)+'...........................................'
	#sentence_retrieval(flist, popu_list, popu_list_new, reason_popu_list, reason_popu_list_new, event_list, event_list_new, popuFlag, reasonFlag, eventFlag, outfname)
	#sentence_retrieval(flist, popu_list, popu_list_new, reason_popu_list_p, reason_popu_dict_a, reason_popu_list_new_p, reason_popu_list_new_a, event_list_p, event_dict_a, event_list_new_p, event_list_new_a, popuFlag, reasonFlag, eventFlag, outfname)
	#dependency parsing
	#print 'dependency parsing at iteration '+str(iteration)+'...........................................'
	#os.system('/uusoc/res/nlp/nlp/Ruihong/makeRoom/stanford_parser/stanford-parser-2011-06-27/lexparser.sh '+outfname +' >> '+outfname_popu)



	processV = []
	i = 0
	while i < part_size:
		processV.append(Process(target=sentence_retrieval, args=(flist_parts[i], popu_list, popu_list_new, reason_popu_list, reason_popu_list_new, event_list, event_list_new, popuFlag, reasonFlag, eventFlag, outfname+'_'+str(i))))


		#.start()
		i += 1
	i = 0
	while i < part_size:
		processV[i].start()
		i += 1
	i = 0
	while i < part_size:
		processV[i].join()
		i += 1	

	#tempOut = open(outfname, 'w')
	tempOut_parts = []

	tempUniqs = {}
	i = 0
	while i < part_size:
		tempIn = open(outfname+'_'+str(i))
		tempOut_parts.append(open(outfname+'_d'+str(i), 'w'))
		for cline in tempIn:
			if not cline: break
			cline = cline.strip()
			if cline != '':
				if not cline in tempUniqs:
					#tempOut.write(cline+'\n\n')
					tempUniqs[cline] = 1
		tempIn.close
		i += 1
	#tempOut.flush()
	#tempOut.close
	sents = tempUniqs.keys()
	cycle = 0
	for csent in sents:
		tempOut_parts[cycle].write(csent+'\n\n')
		cycle = (cycle + 1) % part_size

	#dependency parsing
	print 'dependency parsing at iteration '+str(iteration)+'...........................................'

	processV = []

	i = 0
	while i < part_size:
		tempOut_parts[i].flush()
		tempOut_parts[i].close
		processV.append(Process(target=dep_parsing, args=(outfname+'_d'+str(i), outfname+'_d'+str(i)+'_dep')))
		i += 1
	i = 0

	i = 0
	while i < part_size:
		processV[i].start()
		i += 1
	i = 0
	while i < part_size:
		processV[i].join()
		i += 1	
	tempOut = open(outfname_popu, 'a')
	i = 0
	while i < part_size:
		tempIn = open(outfname+'_d'+str(i)+'_dep')
		for line in tempIn:
			if not line: break
			tempOut.write(line)
		tempIn.close
		i += 1
	tempOut.flush()
	tempOut.close
	
	
	#popu learning
	#event_dict = {'went onstrike':1, 'went on strike':1, 'began strike':1}
	reason_threshold = 0+iteration/10
	#event_threshold = 2 + iteration/5
	event_threshold = 2+iteration/10
	modifier_threshold = 2+iteration/10
	#freqency_threshold_popu = 10 + iteration
	freqency_threshold_popu = 2
	#popu_list_new = popu_phrase_learning(outfname_popu, event_dict, reason_popu_dict, popu_dict, event_threshold, freqency_threshold_popu, reason_threshold)
	[popu_list_new, event_phraseD, reason_phraseD] = popu_phrase_learning(outfname_popu, event_dict, reason_popu_dict, popu_dict, event_threshold, freqency_threshold_popu, reason_threshold, popu_modifier_types_values, modifier_threshold, reason_pattern_seeds)

		

	print 'popu phrase learning at iteration '+str(iteration) +' done!'
	print 'new popu phrases:'
	popu_newK_0 = popu_list_new.keys()
	print 'popu before check: '+str(len(popu_newK_0))
	#popu_check_threshold = 0.005
	popu_check_threshold = 0.0055

	#relevancy_check
	lexicon_parts = [] 
	i = 0
	while i < part_size:
		lexicon_parts.append([])
		i += 1
	cycle = 0
	for clex in popu_newK_0:
		lexicon_parts[cycle].append(clex)
		cycle = (cycle + 1) % part_size

	processV = []
	i = 0
	while i < part_size:
		processV.append(Process(target=relevancy_check, args=(popu_list_new, lexicon_parts[i], relF, generalF, popu_check_threshold, 'popu', i, checked)))
		#.start()
		i += 1
	i = 0
	while i < part_size:
		processV[i].start()
		i += 1
	i = 0
	while i < part_size:
		processV[i].join()
		i += 1

	logf_succ.write('popu second check:\n')
	logf_fail.write('popu second check:\n')
	popu_newK = []
	i = 0
	while i < part_size:
		logf = open('check_temp7_'+str(i))
		for line in logf:
			if not line: break
			line = line.strip()
			if line != '':
				lineV = line.split('\t')
				if len(lineV) > 1:
					if lineV[0] == 'succ':
						popu_newK.append(lineV[1])
						logf_succ.write(line+'\n')
					else:
						logf_fail.write(line+'\n')
		i += 1
	logf_succ.flush()
	logf_fail.flush()

	i = 0
	while i < part_size:
		logf = open('checked_temp7_'+str(i))
		for line in logf:
			if not line: break
			line = line.strip()
			if line != '':
				lineV = line.split('\t')
				if len(lineV) > 1:
					checked[lineV[0]] = lineV[1]
		logf.close					
		i += 1
	
	#popu_newK = relevancy_check(popu_list_new, relF, generalF, popu_check_threshold, 'popu')
	print 'popu after check: '+str(len(popu_newK))
	for cpopu in popu_newK:
		popu_list.append(cpopu)
		popu_dict[cpopu] = 1
		fout_popu.write(cpopu+'\t'+str(popu_list_new[cpopu])+'\n')
		print cpopu
	print 'new popu learned: '+str(len(popu_newK))
	fout_popu.flush()

	fou_reason_seed_patt_phrases.write('from popu phrase learning......................................:\n')
	ckeys = reason_phraseD.keys()
	for ckey in ckeys:
		if not ckey in reason_seed_patt_phrases:
			reason_seed_patt_phrases[ckey] = 1
			fou_reason_seed_patt_phrases.write(ckey+'\t'+str(reason_phraseD[ckey])+'\n')		
	fou_reason_seed_patt_phrases.flush()


	fou_popu_tracking.write('iteration: '+str(iteration)+'\n')
	ckeys = event_phraseD.keys()
	fou_popu_tracking.write('# of event_phrases: '+str(len(ckeys))+'\n')

	ckeys = reason_phraseD.keys()
	fou_popu_tracking.write('# of reason_phrases: '+str(len(ckeys))+'\n')

	fou_popu_tracking.flush()

	if len(event_newK) == 0 and len(reason_newK) == 0 and len(popu_newK) == 0:
		print 'no new things are learned'
		exit(0)

	iteration += 1








import sys, os, string

import gzip


def dep_parsing(infname, outfname):
	os.system('/uusoc/res/nlp/nlp/Ruihong/makeRoom/stanford_parser/stanford-parser-2011-06-27/lexparser.sh '+infname +' >> '+outfname)

#def sentence_retrieval(flist, popu_list, popu_list_new, reason_list, reason_list_new, event_list, event_list_new, popuFlag, reasonFlag, eventFlag, outfname):
def sentence_retrieval(flist, popu_list, popu_list_new, reason_list, reason_list_new, event_list, event_list_new, popuFlag, reasonFlag, eventFlag, outfname):
	#retrieve sents
	lineN = 0
	longTitle = ''
	uniqs = {}
	foundC = 0
	fou = open(outfname, 'w')
	fpath = '/uusoc/scratch/whoville/research/lalindra/osi/data/hrl_english/'

	popu_found_count = 0

	event_list_new_list = event_list_new.keys()
	reason_list_new_list = reason_list_new.keys()


	for line in flist:
		#if not line: break
		#line = line.strip()
		#print line

		if line != '':
			if line[-3:] == '.gz':
				#cfile = gzip.open(fpath+line)
				cfile = gzip.open(line)
			else:
				#cfile = open(fpath+line)
				cfile = open(line)
			
			cflag = False
			rflag = False
			rrflag = False
			sentC = 0
			#cdoc = ''
			#for cline in cfile:
			#	cdoc += cline+' '
			#clines = cdoc.split('.')
			#for cline in clines:
			for cline in cfile:
				if not cline: break
				cline = cline.strip()
				cline2 = cline.lower()
				flag_popu = True
				flag_reason = True
				#flag_keyword = True
				flag_event = True
				flag_popu_new = False
				flag_reason_new = False
				#flag_keyword = True
				flag_event_new = False
	
				cpopu = ''
				cevent = ''
				creason = ''

				phraseBeg_popu = -1
				phraseBeg_event = -1
				phraseBeg_reason = -1

				if popuFlag:
					flag_popu = False

					for popu in popu_list:
						cpos = cline2.find(popu)
						if cpos != -1 and (cpos == 0 or cline2[cpos-1] == ' ') and (cpos+len(popu) == len(cline2) or string.punctuation.find(cline2[cpos+len(popu)]) != -1 or cline2[cpos+len(popu)] == ' '):
							flag_popu = True
							phraseBeg_popu = cpos
							cpopu = popu
							if cpopu in popu_list_new:
								flag_popu_new = True
							break
				'''for reason in reason_list:
					reasonPos = cline2.find(reason)
					if reasonPos != -1:
						cline2V = cline2[:reasonPos].split()
						if not (len(cline2V) >= 1 and (cline2V[-1] == 'is' or cline2V[-1] == 'are' or cline2V[-1] == 'was' or cline2V[-1] == 'were' or cline2V[-1] == 'been') or len(cline2V) >= 2 and (cline2V[-2] == 'is' or cline2V[-2] == 'are' or cline2V[-2] == 'was' or cline2V[-2] == 'were' or cline2V[-2] == 'been')): 
							flag_reason = True
							break'''

				#regular expression searching
				if reasonFlag:
					if not popuFlag or popuFlag and flag_popu and flag_popu_new:

						flag_reason = False
						for reason in reason_list:
							#if cline2.find(event) != -1:
							reasonPhraseV = reason.split()
							begP = 0
							phraseBeg = 0
							found = True
							i = 0
							while i < len(reasonPhraseV):
								cword = reasonPhraseV[i]
								curP = cline2.find(cword, begP) 
								#if curP != -1:
								if curP != -1 and (curP == 0 or cline2[curP-1] == ' ') and (curP+len(cword) == len(cline2) or string.punctuation.find(cline2[curP+len(cword)]) != -1 or cline2[curP+len(cword)] == ' '):
									if begP > 0:
										segV = cline2[begP:curP].split()
										if len(segV) > 5:
											found = False
											break
									if begP == 0:
										phraseBeg = curP
									begP = curP + len(cword)
			
								else:
									found = False
									break
								i += 1
							if found:
								creason = reason
								cline2V =  cline2[:phraseBeg].split()
								if len(cline2V) > 0 and not (cline2V[-1] == 'is' or cline2V[-1] == 'are' or cline2V[-1] == 'was' or cline2V[-1] == 'were' or cline2V[-1] == 'been'):
									flag_reason = True
									if creason in reason_list_new:
										flag_reason_new = True
									phraseBeg_reason = phraseBeg
								
									break

					elif popuFlag and flag_popu and not flag_popu_new:
						flag_reason = False
						for reason in reason_list_new_list:
							#if cline2.find(event) != -1:
							reasonPhraseV = reason.split()
							begP = 0
							phraseBeg = 0
							found = True
							i = 0
							while i < len(reasonPhraseV):
								cword = reasonPhraseV[i]
								curP = cline2.find(cword, begP) 
								#if curP != -1:
								if curP != -1 and (curP == 0 or cline2[curP-1] == ' ') and (curP+len(cword) == len(cline2) or string.punctuation.find(cline2[curP+len(cword)]) != -1 or cline2[curP+len(cword)] == ' '):
									if begP > 0:
										segV = cline2[begP:curP].split()
										if len(segV) > 5:
											found = False
											break
									if begP == 0:
										phraseBeg = curP
									begP = curP + len(cword)
			
								else:
									found = False
									break
								i += 1
							if found:
								creason = reason
								cline2V =  cline2[:phraseBeg].split()
								if len(cline2V) > 0 and not (cline2V[-1] == 'is' or cline2V[-1] == 'are' or cline2V[-1] == 'was' or cline2V[-1] == 'were' or cline2V[-1] == 'been'):
									flag_reason = True
									if creason in reason_list_new:
										flag_reason_new = True
									phraseBeg_reason = phraseBeg
								
									break


				#simple searching
				'''for event in event_list:
					if cline2.find(event) != -1:
						flag_event = True
						break'''

				#regular expression searching
				if eventFlag:
					if popuFlag and flag_popu and flag_popu_new or reasonFlag and flag_reason and flag_reason_new:
						flag_event = False
						for event in event_list:
							#if cline2.find(event) != -1:
							eventPhraseV = event.split()
							begP = 0
							phraseBeg = 0
							found = True
							i = 0
							while i < len(eventPhraseV):
								cword = eventPhraseV[i]
								curP = cline2.find(cword, begP) 
								#if curP != -1:
								if curP != -1 and (curP == 0 or cline2[curP-1] == ' ') and (curP+len(cword) == len(cline2) or string.punctuation.find(cline2[curP+len(cword)]) != -1 or cline2[curP+len(cword)] == ' '):
									if begP > 0:
										segV = cline2[begP:curP].split()
										if len(segV) > 5:
											found = False
											break
									if begP == 0:
										phraseBeg = curP
									begP = curP + len(cword)
			
								else:
									found = False
									break
								i += 1
							if found:
								cevent = event
								flag_event = True
								if cevent in event_list_new:
									flag_event_new = True
								phraseBeg_event = phraseBeg
								break
					elif popuFlag and flag_popu and not flag_popu_new or reasonFlag and flag_reason and not flag_reason_new:
						flag_event = False
						for event in event_list_new_list:
							#if cline2.find(event) != -1:
							eventPhraseV = event.split()
							begP = 0
							phraseBeg = 0
							found = True
							i = 0
							while i < len(eventPhraseV):
								cword = eventPhraseV[i]
								curP = cline2.find(cword, begP) 
								#if curP != -1:
								if curP != -1 and (curP == 0 or cline2[curP-1] == ' ') and (curP+len(cword) == len(cline2) or string.punctuation.find(cline2[curP+len(cword)]) != -1 or cline2[curP+len(cword)] == ' '):
									if begP > 0:
										segV = cline2[begP:curP].split()
										if len(segV) > 5:
											found = False
											break
									if begP == 0:
										phraseBeg = curP
									begP = curP + len(cword)
			
								else:
									found = False
									break
								i += 1
							if found:
								cevent = event
								flag_event = True
								if cevent in event_list_new:
									flag_event_new = True
								phraseBeg_event = phraseBeg
								break


				#if flag_popu and flag_reason and flag_keyword:
				if flag_popu and flag_reason and flag_event and (flag_popu_new or flag_reason_new or flag_event_new):
				#if flag_popu and flag_reason and flag_event:
				#if flag_popu and flag_reason and flag_event and (flag_popu_new or flag_reason_new or flag_event_new) and phraseBeg_event > phraseBeg_popu:
				#if flag_popu and flag_event and flag_keyword:
				#if flag_reason and flag_event and flag_keyword:
					if len(cline) < 500 and not cline in uniqs:
					#if not cline in uniqs:
						uniqs[cline] = 1
						#fou.write(cline+'\t'+cpopu+'\t'+cevent+'\n\n')
						#print 'found: '+line
						fou.write(cline+'\n\n')
						#fou.flush()
						foundC += 1
						if foundC%10 == 0:
							print str(foundC)
						
						#print line
			
				lineN += 1
		#fou.flush()
	#print 'fileC: '+str(fileC)
	#print 'popu_found_count '+str(popu_found_count)
	fou.flush()
	fou.close
	#flist.close
	print 'foundC: '+str(foundC)

#def event_phrase_learning(outfname, event_dict, reason_dict, popu_dict, reason_threshold, frequency, popu_threshold):
def event_phrase_learning(outfname, event_dict, reason_dict, popu_dict, reason_threshold, frequency, popu_threshold, popu_modifier_types_values, reason_p_seeds):
	fin = open(outfname)
	sent = ''
	posV = []
	empty_lineC = 0
	event_start = ''
	reason_word = ''
	reason_start = ''
	first_arg_feat_dict = {}
	first_arg_feat_dict_popu = {}

	event_phraseWhole = {}
	event_phraseWhole_reasonD = {}
	event_phraseWhole_reasonD_reasonS = {}
	event_phraseWhole_popuD = {}
	event_phraseWhole_p = {}
	event_phraseWhole_p_reasonD = {}
	event_phraseWhole_p_popuD = {}
	event_phraseWhole_a = {}
	event_phraseWhole_a_reasonD = {}
	event_phraseWhole_a_popuD = {}

	event_phraseD = {}#key: phrase_head(without the last word), value: count
	event_phraseL = {}#key: phrase_head(without the last word), value: {}, key: head, value: freq of head
	phraseC = 0

	reason_head_dict = {}
	keys = reason_dict.keys()
	for key in keys:
		keyV = key.split()
		creasonHead = keyV[0]
		if keyV[0] == 'to':
			creasonHead = keyV[1]
		reason_head_dict[creasonHead] = 1
	

	reason_phraseD = {}
	reason_phraseD = {}

	for line in fin:
			if not line: break
			line = line.strip()
			if line == '':
				empty_lineC += 1
				if empty_lineC % 2 == 0:
					uniq_flag = True
					#if not sent in uniq_sentD:
					#	uniq_sentD[sent] = 1
					#	uniq_flag = True 
					#if sent in sent_to_filter and sent_to_filter[sent] > 0:
					#	sent_to_filter[sent] -= 1
					#	uniq_flag = False

					'''sent_to_filterK = sent_to_filter.keys()					
					for ccsent in sent_to_filterK:
						if sent.find(ccsent) != -1:
							uniq_flag = False
							del sent_to_filter[ccsent]
							sent_filterN += 1'''
						
					if event_start != '' and uniq_flag:
						#startP = 0
						#endP = 0
						#key = ''
						reason_startV = reason_start.split('-')
						reason_phrase = reason_startV[0]
						reason_phrase_p = ''
						reason_phrase_a = ''
						#if len(reason_phrase) > 3 and reason_phrase[-3:] != 'ing':
						if not reason_phrase.endswith('ing'):
							reason_phrase = 'to '+reason_phrase
						reason_phrase_o = reason_phrase
						reasonF = False
						reasonComp = False
						if 'dobj'+'______'+reason_start in first_arg_feat_dict:
							#reasonF = True
							#cobj = first_arg_feat_dict['dobj'+'______'+reason_start]
							cobjW = first_arg_feat_dict['dobj'+'______'+reason_start]
							cobjV = cobjW.split('-')
							cobj = cobjW.rstrip('-'+cobjV[-1])
							if 'prt'+'______'+reason_start in first_arg_feat_dict:
								reason_phrase += ' '+first_arg_feat_dict['prt'+'______'+reason_start]
							#reason_phrase_p = reason_phrase							
							reason_phrase += ' '+cobj
							#reason_phrase_a = cobj
							#if reason_phrase in reason_dict:
							#	reasonF = True
							reasonComp = True
							#post modifiers
							'''if 'prep'+'______'+reason_start in first_arg_feat_dict:
								reason_phrase += ' '+first_arg_feat_dict['prep'+'______'+reason_start]
							elif 'xcomp'+'______'+reason_start in first_arg_feat_dict:
								reason_phrase += ' '+first_arg_feat_dict['xcomp'+'______'+reason_start]
							elif 'infmod'+'______'+reason_start in first_arg_feat_dict:
								reason_phrase += ' to '+first_arg_feat_dict['infmod'+'______'+reason_start]
							elif 'amod'+'______'+cobjW in first_arg_feat_dict:
								reason_phrase += ' '+first_arg_feat_dict['amod'+'______'+cobjW]'''

						elif 'prep'+'______'+reason_start in first_arg_feat_dict:
							#reasonF = True
							if 'prt'+'______'+reason_start in first_arg_feat_dict:
								reason_phrase += ' '+first_arg_feat_dict['prt'+'______'+reason_start]
							#reason_phrase_p = reason_phrase							
							reason_phrase += ' '+first_arg_feat_dict['prep'+'______'+reason_start]
							reasonComp = True
							#reason_phrase_a = first_arg_feat_dict['prep'+'______'+reason_start]
							#if reason_phrase in reason_dict:
							#	reasonF = True
						#if reason_phrase != reason_phrase_o:
						if reasonComp:
							#reason_phrase_vec = reason_phrase.split()
							#reason_phrase_p = reason_phrase[:-len(reason_phrase_vec[-1])].strip()
							#reason_phrase_a = reason_phrase_vec[-1]
							#if reason_phrase_p in reason_p_seeds or reason_phrase_p in reason_dict_p and reason_phrase_a in reason_dict_a:
							#	reasonF = True
							reason_phrase = reason_phrase.lower()
							reasonPatF = False	
							for reason_pat in reason_p_seeds:
								if reason_phrase.find(reason_pat) != -1:
									reasonPatF = True
							if reasonPatF or reason_phrase in reason_dict:
								reasonF = True

							if reasonF:
								event_startV = event_start.split('-')
								phrase = event_startV[0]
								phrase_p = ''
								phrase_a = ''
								#phrase_head = event_startV[0]
								#chead = ''
								eventComp = True
								if 'dobj'+'______'+event_start in first_arg_feat_dict:
									#cobj = first_arg_feat_dict['dobj'+'______'+event_start]
									cobjW = first_arg_feat_dict['dobj'+'______'+event_start]
									cobjV = cobjW.split('-')
									cobj = cobjW.rstrip('-'+cobjV[-1])
									if 'prt'+'______'+event_start in first_arg_feat_dict:
										phrase += ' '+first_arg_feat_dict['prt'+'______'+event_start]
									#phrase_p = phrase
									phrase += ' '+cobj
									#phrase_a = cobj
								elif 'prep'+'______'+event_start in first_arg_feat_dict:
									if 'prt'+'______'+event_start in first_arg_feat_dict:
										phrase += ' '+first_arg_feat_dict['prt'+'______'+event_start]
									#phrase_p = phrase
									phrase += ' '+first_arg_feat_dict['prep'+'______'+event_start]
									#phrase_a = first_arg_feat_dict['prep'+'______'+event_start]
								if phrase != event_startV[0]:
									phrase = phrase.lower()
									phrase_vec = phrase.split()
									#phrase_p = phrase[:-len(phrase_vec[-1])].strip()
									#phrase_a = phrase_vec[-1]
									#if True:
									popu_term_found = ''
									if 'nsubj'+'______'+event_start in first_arg_feat_dict:
										wordR = first_arg_feat_dict['nsubj'+'______'+event_start]
										wordRV = wordR.split('-')
										popu_term = wordR.rstrip('-'+wordRV[-1]).lower()
										#popu_term = first_arg_feat_dict['nsubj'+'______'+event_start]
										if popu_term in popu_dict:#check_2
											popu_term_found = popu_term
											if wordR in first_arg_feat_dict_popu:
												#print 'here'
												modifiers = first_arg_feat_dict_popu[wordR].keys()
												for modi in modifiers:	
													cvalue = first_arg_feat_dict_popu[wordR][modi]						

													if not modi in popu_modifier_types_values:
														popu_modifier_types_values[modi] = {}
													if modi == 'num' and cvalue.lower() != 'one' and cvalue.lower() != '1':
														if not 'num' in popu_modifier_types_values[modi]:
															popu_modifier_types_values[modi]['num'] = 1
														else:
															popu_modifier_types_values[modi]['num'] += 1
													else:

														if not cvalue in popu_modifier_types_values[modi]:
															popu_modifier_types_values[modi][cvalue] = 1
														else:
															popu_modifier_types_values[modi][cvalue] += 1
											#else:
											#	continue

											#if True:
											#delayed  until fully checked
											if reasonPatF:
												if not reason_phrase in reason_phraseD:
													reason_phraseD[reason_phrase] = 1
												else:
													reason_phraseD[reason_phrase] += 1
											if not phrase in event_phraseWhole:
												event_phraseWhole[phrase] = 1
												#event_phraseWhole_reasonD[phrase] = {reason_word:1}
												event_phraseWhole_reasonD[phrase] = {reason_phrase:1}
												if popu_term_found != '':
													event_phraseWhole_popuD[phrase] = {popu_term_found:1}
												#event_phraseWhole_popuD[phrase] = {popu_term:1}
												
												#phraseC += 1
												#if phraseC % 100 == 0:
												#	print str(phraseC)
											else:
												event_phraseWhole[phrase] += 1
												event_phraseWhole_reasonD[phrase][reason_phrase] = 1
												if popu_term_found != '':
													if not phrase in event_phraseWhole_popuD:
														event_phraseWhole_popuD[phrase] = {popu_term_found:1}
													else:
														event_phraseWhole_popuD[phrase][popu_term_found] = 1
												#event_phraseWhole_popuD[phrase][popu_term] = 1
											if reasonPatF:
												event_phraseWhole_reasonD_reasonS[phrase] = 1

											'''if not phrase_p in event_phraseWhole_p:
												event_phraseWhole_p[phrase_p] = 1
												#event_phraseWhole_reasonD[phrase] = {reason_word:1}
												event_phraseWhole_p_reasonD[phrase_p] = {reason_phrase:1}
												event_phraseWhole_p_popuD[phrase_p] = {popu_term:1}
												#phraseC += 1
												#if phraseC % 100 == 0:
												#	print str(phraseC)
											else:
												event_phraseWhole_p[phrase_p] += 1
												event_phraseWhole_p_reasonD[phrase_p][reason_phrase] = 1
												event_phraseWhole_p_popuD[phrase_p][popu_term] = 1

											if not phrase_a in event_phraseWhole_a:
												event_phraseWhole_a[phrase_a] = 1
												#event_phraseWhole_reasonD[phrase] = {reason_word:1}
												event_phraseWhole_a_reasonD[phrase_a] = {reason_phrase:1}
												event_phraseWhole_a_popuD[phrase_a] = {popu_term:1}
												#phraseC += 1
												#if phraseC % 100 == 0:
												#	print str(phraseC)
											else:
												event_phraseWhole_a[phrase_a] += 1
												event_phraseWhole_a_reasonD[phrase_a][reason_phrase] = 1
												event_phraseWhole_a_popuD[phrase_a][popu_term] = 1
											'''



							

											#phrase = phrase.lower()
							
											phraseV = phrase.split()					
											phrase_head = phrase.rstrip(phraseV[-1])
											chead = phraseV[-1]
											if not phrase_head in event_phraseD:
												event_phraseD[phrase_head] = 1
												event_phraseL[phrase_head] = {}								
												event_phraseL[phrase_head][chead] = 1
											else:
												event_phraseD[phrase_head] += 1
												if not chead in event_phraseL[phrase_head]:
													event_phraseL[phrase_head][chead] = 1
												else:
													event_phraseL[phrase_head][chead] += 1
											phraseC += 1
											if phraseC % 100 == 0:
												print str(phraseC)
											#fou.write(phrase+'\n')
						

						
							
					sent = ''
					posV = []
					event_start = ''
					reason_word = ''
					reason_start = ''
					first_arg_feat_dict = {}
					first_arg_feat_dict_popu = {}
					
			elif line[0] == '(':
				#parse += oline
				prightB = 0
				rightB = line.find(')')
				while rightB != -1:
					leftB = line.rfind('(', prightB, rightB)
					if leftB == -1:
						break
					if leftB < rightB :
						word = line[leftB+1: rightB]
						pos_word = word.split()
						if len(pos_word) > 1:
							sent += pos_word[1] + ' '
							posV.append(pos_word[0])
						elif len(pos_word) == 1:
							sent += pos_word[0] + ' '
							posV.append(pos_word[0])

					prightB = rightB

					rightB = line.find(')', rightB+1)
			else:
					feat = line
					leftB = feat.find('(')
					rightB = feat.rfind(')')				
					words = feat[leftB+1: rightB]

					featH = feat[:leftB]
					wordLR = words.split(', ')
					if len(wordLR) == 2:		
						#wordL = wordLR[0].split('-')
						wordL = wordLR[0].rstrip("'")
						wordLV = wordL.split('-')
						wordR = wordLR[1].rstrip("'")
						wordRV = wordR.split('-')
						#if wordRV[0] == 'demanding' and featH == 'xcomp':
						#if wordRV[0] == 'demanding' and featH == 'xcomp' or wordRV[0] == 'protesting' and featH == 'xcomp':
						#if (wordRV[0] == 'demanding' or wordRV[0] == 'protesting' or wordRV[0] == 'protest' or wordRV[0] == 'demand') and featH == 'xcomp':
						#if (wordRV[0] == 'threatening' or wordRV[0] == 'seeking' or wordRV[0] == 'claiming' or wordRV[0] == 'urging' or wordRV[0] == 'calling' or wordRV[0] == 'complaining' or wordRV[0] == 'declaring' or wordRV[0] == 'contending' or wordRV[0] == 'expressing' or wordRV[0] == 'press') and featH == 'xcomp':
						#if (wordRV[0] == 'urging' or wordRV[0] == 'seeking' or wordRV[0] == 'seek' or wordRV[0] == 'urge' or wordRV[0] == 'calling' or wordRV[0] == 'mark' or wordRV[0] == 'forcing' or wordRV[0] == 'express' or wordRV[0] == 'expressing' or wordRV[0] == 'press' or wordRV[0] == 'condemning' or wordRV[0] == 'condemn' or wordRV[0] == 'accusing' or wordRV[0] == 'pledging') and featH == 'xcomp':
						#if wordRV[0] in reason_head_dict and featH == 'xcomp':
						if wordRV[0] in reason_head_dict and featH == 'xcomp':

						#if wordRV[0] == 'protesting' and featH == 'xcomp':
						#if wordRV[0] == 'threatening' and featH == 'xcomp':
						#if wordRV[0] == 'fighting' and featH == 'xcomp':
							event_start = wordL#the starting verb
							reason_word = wordRV[0]
							reason_start = wordR

						featHV = featH.split('_')
						featH_o = featH
						#if len(featHV) == 2 and featHV[0] == 'prep':
						if len(featHV) == 2:
							featH = featHV[0]							
						key = featH+'______'+wordL
						#first_arg_feat_dict[key] = wordRV[-1]#phrase ending position
						feedword = wordR.rstrip('-'+wordRV[-1])
						feedwordInd = int(wordRV[-1]) - 1
						posVL = len(posV)

						if featH_o != 'det':
							if not wordL in first_arg_feat_dict_popu:
								first_arg_feat_dict_popu[wordL] = {}
								if not featH_o in first_arg_feat_dict_popu[wordL]:
									first_arg_feat_dict_popu[wordL][featH_o] = feedword
									#if featH_o != 'num':
									#	first_arg_feat_dict_popu[wordL][featH_o][feedword] = 1

						if featHV[0] == 'prep' and len(featHV) == 1 and not key in first_arg_feat_dict and int(wordLV[-1]) < int(wordRV[-1]):
							if feedwordInd < posVL and posV[feedwordInd] != 'CD' and posV[feedwordInd] != 'PRP':
								first_arg_feat_dict[key] = feedword
 
						elif featHV[0] == 'prep' and len(featHV) > 1 and not key in first_arg_feat_dict and int(wordLV[-1]) < int(wordRV[-1]):
							#print featH
							if feedwordInd < posVL and posV[feedwordInd] != 'CD' and posV[feedwordInd] != 'PRP':
								first_arg_feat_dict[key] = featHV[1]  + ' '+ feedword
						elif featH == 'prt'  and not key in first_arg_feat_dict:
							#if feedword != 'on' and feedword != 'since':
							if True:
								first_arg_feat_dict[key] = feedword  
						elif featH == 'dobj'  and not key in first_arg_feat_dict:
							#first_arg_feat_dict[key] = feedword
							if feedwordInd < posVL and posV[feedwordInd] != 'CD' and posV[feedwordInd] != 'PRP':
								first_arg_feat_dict[key] = wordR
						elif featH == 'nsubj' and not key in first_arg_feat_dict:
							#first_arg_feat_dict[key] = feedword.lower()
							first_arg_feat_dict[key] = wordR
						elif featH == 'xcomp' and not key in first_arg_feat_dict:
							first_arg_feat_dict[key] = feedword.lower()
						elif featH == 'infmod' and not key in first_arg_feat_dict:
							first_arg_feat_dict[key] = feedword.lower()
						elif featH == 'amod' and not key in first_arg_feat_dict and int(wordLV[-1]) < int(wordRV[-1]):
							first_arg_feat_dict[key] = feedword.lower()


	fin.close

	#event_list_new_p = {}
	#event_list_new_a = {}	
	event_list_new = {}	

	logf = open('phrase_learning_logs_18_check_35P_diff_epC_twoSideLoosened_reducedCond_popuModFreqFixed7_2', 'a')
	logf.write('event phrase learning:\n')

	#selection based on whole phrases
	items = event_phraseWhole.items()
	backitems = [[v[1], v[0]] for v in items] 
	backitems.sort()
	i = len(backitems) - 1
	print 'dict size: '+str(len(event_dict.keys()))
	for key in event_dict.keys():
		print 'key: '+key
	#while i >= 0 and i >= len(backitems) - 500:
	while i >= 0:
		reasonL = event_phraseWhole_reasonD[backitems[i][1]].keys()
		reasonT = len(reasonL)

		popuT = 0
		popuL = []
		if backitems[i][1] in event_phraseWhole_popuD:
			popuL = event_phraseWhole_popuD[backitems[i][1]].keys()
			popuT = len(popuL)

		#if reasonT > 1:
		cevent = backitems[i][1]
		cfreq = backitems[i][0]
		#if reasonT >= reason_threshold and cfreq >= frequency and not cevent in event_dict and popuT >= popu_threshold:
		if cfreq >= frequency and not cevent in event_dict and (popuT >= popu_threshold and reasonT >= reason_threshold):
		#if cfreq >= frequency:
		#if cfreq >= frequency and not cevent in event_dict and (popuT >= popu_threshold and reasonT >= reason_threshold) and cevent in event_phraseWhole_reasonD_reasonS:
		#if cfreq >= frequency and not cevent in event_dict and (reasonT >= reason_threshold):
		#if cfreq >= frequency and (reasonT >= reason_threshold):
			
			event_list_new[cevent] = str(cfreq)+'\t'+str(reasonT) + '\t'+str(popuT)
			reasons = ''
			for key in reasonL:
				reasons += key+' '
			popuStr = ''
			for cpopu in popuL:
				popuStr += cpopu+'|'
			logf.write('good: '+cevent+'\t'+str(cfreq)+'\t'+str(reasonT) + '\t' + reasons + '\t'+str(popuT)+'\t'+popuStr+'\n')
			#fou.write(.lower()+'\t'+str(backitems[i][0])+'_'+str(reasonT)+'\n')
			#fou.write(backitems[i][1].lower()+'\n')
			#columN += 1		
			#fou.write(backitems[i][1])
			#if columN % lineSize == 0:
			#	fou.write('\n')
			#else:
			#	fou.write('\t')
		else:
			logf.write( 'bad: '+cevent+'\t'+str(cfreq)+'\t'+str(reasonT) + '\t'+str(popuT)+'\n')
		i -= 1

	'''logf.write('patterns:\n')
	items = event_phraseWhole_p.items()
	backitems = [[v[1], v[0]] for v in items] 
	backitems.sort()
	i = len(backitems) - 1
	#while i >= 0 and i >= len(backitems) - 500:
	while i >= 0:
		reasonT = len(event_phraseWhole_p_reasonD[backitems[i][1]].keys())
		popuT = len(event_phraseWhole_p_popuD[backitems[i][1]].keys())
		#if reasonT > 1:
		cevent = backitems[i][1]
		cfreq = backitems[i][0]
		#if reasonT >= reason_threshold and cfreq >= frequency and not cevent in event_dict and popuT >= popu_threshold:
		if cfreq >= frequency and not cevent in event_dict_p and (popuT >= popu_threshold or reasonT >= reason_threshold):
			event_list_new_p[cevent] = str(cfreq)+'\t'+str(reasonT) + '\t'+str(popuT)
			reasons = ''
			for key in event_phraseWhole_p_reasonD[backitems[i][1]].keys():
				reasons += key+' '
			logf.write('good: '+cevent+'\t'+str(cfreq)+'\t'+str(reasonT) + '\t' + reasons + '\t'+str(popuT)+'\n')
			#fou.write(.lower()+'\t'+str(backitems[i][0])+'_'+str(reasonT)+'\n')
			#fou.write(backitems[i][1].lower()+'\n')
			#columN += 1		
			#fou.write(backitems[i][1])
			#if columN % lineSize == 0:
			#	fou.write('\n')
			#else:
			#	fou.write('\t')
		else:
			logf.write( 'bad: '+cevent+'\t'+str(cfreq)+'\t'+str(reasonT) + '\t'+str(popuT)+'\n')
		i -= 1
	#fou.flush()
	#fou.close
	#logf.flush()
	#logf.close
	logf.write('args:\n')
	items = event_phraseWhole_a.items()
	backitems = [[v[1], v[0]] for v in items] 
	backitems.sort()
	i = len(backitems) - 1
	#while i >= 0 and i >= len(backitems) - 500:
	while i >= 0:
		reasonT = len(event_phraseWhole_a_reasonD[backitems[i][1]].keys())
		popuT = len(event_phraseWhole_a_popuD[backitems[i][1]].keys())
		#if reasonT > 1:
		cevent = backitems[i][1]
		cfreq = backitems[i][0]
		#if reasonT >= reason_threshold and cfreq >= frequency and not cevent in event_dict and popuT >= popu_threshold:
		if cfreq >= frequency and not cevent in event_dict_a and (popuT >= popu_threshold or reasonT >= reason_threshold):
			event_list_new_a[cevent] = str(cfreq)+'\t'+str(reasonT) + '\t'+str(popuT)
			reasons = ''
			for key in event_phraseWhole_a_reasonD[backitems[i][1]].keys():
				reasons += key+' '
			logf.write('good: '+cevent+'\t'+str(cfreq)+'\t'+str(reasonT) + '\t' + reasons + '\t'+str(popuT)+'\n')
			#fou.write(.lower()+'\t'+str(backitems[i][0])+'_'+str(reasonT)+'\n')
			#fou.write(backitems[i][1].lower()+'\n')
			#columN += 1		
			#fou.write(backitems[i][1])
			#if columN % lineSize == 0:
			#	fou.write('\n')
			#else:
			#	fou.write('\t')
		else:
			logf.write( 'bad: '+cevent+'\t'+str(cfreq)+'\t'+str(reasonT) + '\t'+str(popuT)+'\n')
		i -= 1'''
	#fou.flush()
	#fou.close
	logf.flush()
	logf.close
	return [event_list_new, reason_phraseD, event_phraseWhole]


#def reason_phrase_learning(outfname, event_dict, reason_dict, popu_dict, reason_threshold, frequency, popu_threshold):
def reason_phrase_learning(outfname, event_dict, reason_dict, popu_dict, reason_threshold, frequency, popu_threshold, popu_modifier_types_values, reason_p_seeds):
	fin = open(outfname)
	sent = ''
	posV = []
	empty_lineC = 0
	event_start = ''
	reason_word = ''
	reason_start = ''
	first_arg_feat_dict = {}
	first_arg_feat_dict_popu = {}

	event_phraseWhole = {}
	event_phraseWhole_seed_patt = {}
	event_phraseWhole_reasonD = {}
	event_phraseWhole_popuD = {}
	'''event_phraseWhole_p = {}
	event_phraseWhole_p_reasonD = {}
	event_phraseWhole_p_popuD = {}
	event_phraseWhole_a = {}
	event_phraseWhole_a_reasonD = {}
	event_phraseWhole_a_popuD = {}'''
	#fou_temp = open('reason_temp', 'w')

	event_phraseD = {}#key: phrase_head(without the last word), value: count
	event_phraseL = {}#key: phrase_head(without the last word), value: {}, key: head, value: freq of head
	phraseC = 0

	
	reason_head_dict = {}
	keys = reason_dict.keys()
	for key in keys:
		keyV = key.split()
		creasonHead = keyV[0]
		if keyV[0] == 'to':
			creasonHead = keyV[1]
		reason_head_dict[creasonHead] = 1
	
	reason_phraseD = {}

	for line in fin:
			if not line: break
			line = line.strip()
			if line == '':
				empty_lineC += 1
				if empty_lineC % 2 == 0:
					uniq_flag = True
					#if not sent in uniq_sentD:
					#	uniq_sentD[sent] = 1
					#	uniq_flag = True 
					#if sent in sent_to_filter and sent_to_filter[sent] > 0:
					#	sent_to_filter[sent] -= 1
					#	uniq_flag = False

					'''sent_to_filterK = sent_to_filter.keys()					
					for ccsent in sent_to_filterK:
						if sent.find(ccsent) != -1:
							uniq_flag = False
							del sent_to_filter[ccsent]
							sent_filterN += 1'''
						
					if event_start != '' and uniq_flag:
						#startP = 0
						#endP = 0
						#key = ''
						reason_startV = reason_start.split('-')
						reason_phrase = reason_startV[0]
						reason_phrase_p = ''
						reason_phrase_a = ''
						reasonF = False
						if 'dobj'+'______'+reason_start in first_arg_feat_dict:
							#reasonF = True
							#cobj = first_arg_feat_dict['dobj'+'______'+reason_start]
							cobjW = first_arg_feat_dict['dobj'+'______'+reason_start]
							cobjV = cobjW.split('-')
							cobj = cobjW.rstrip('-'+cobjV[-1])
							if 'prt'+'______'+reason_start in first_arg_feat_dict:
								reason_phrase += ' '+first_arg_feat_dict['prt'+'______'+reason_start]
							
							#reason_phrase_p = reason_phrase							
							reason_phrase += ' '+cobj
							#reason_phrase_a = cobj
							#if reason_phrase in reason_dict:
							#	reasonF = True
							
						elif 'prep'+'______'+reason_start in first_arg_feat_dict:
							#reasonF = True
							if 'prt'+'______'+reason_start in first_arg_feat_dict:
								reason_phrase += ' '+first_arg_feat_dict['prt'+'______'+reason_start]
							#reason_phrase_p = reason_phrase							
							reason_phrase += ' '+first_arg_feat_dict['prep'+'______'+reason_start]
							#reason_phrase_a = first_arg_feat_dict['prep'+'______'+reason_start]
							#if reason_phrase in reason_dict:
							#	reasonF = True
						if reason_phrase != reason_startV[0]:#phrase form
							#reason_phrase_vec = reason_phrase.split()
							#reason_phrase_p = reason_phrase[:-len(reason_phrase_vec[-1])].strip()
							#reason_phrase_a = reason_phrase_vec[-1]
							#if reason_phrase_p in reason_dict_p and reason_phrase_a in reason_dict_a:
								#fou_temp.write('wierd: '+reason_phrase_a+'\n')
								#ckeys = reason_dict_a.keys()
								#tempStr = ''
								#for ckey in ckeys:
								#	tempStr += ckey+' '
								#fou_temp.write('dict: '+tempStr+'\n')
							reason_phrase = reason_phrase.lower()
							if reason_phrase in reason_dict:
								reasonF = True
							if reasonF:
								event_startV = event_start.split('-')
								phrase = event_startV[0]
								if not phrase.endswith('ing'):
									phrase = 'to '+phrase
								#else:
								#	continue
								phrase_o = phrase
								phrase_p = ''
								phrase_a = ''
								#phrase_head = event_startV[0]
								#chead = ''

								#fou_temp.write('phrase: '+reason_phrase+'\n')
								if 'dobj'+'______'+event_start in first_arg_feat_dict:
									#cobj = first_arg_feat_dict['dobj'+'______'+event_start]
									cobjW = first_arg_feat_dict['dobj'+'______'+event_start]
									cobjV = cobjW.split('-')
									cobj = cobjW.rstrip('-'+cobjV[-1])
									if 'prt'+'______'+event_start in first_arg_feat_dict:
										phrase += ' '+first_arg_feat_dict['prt'+'______'+event_start]								
									#phrase_p = phrase
									phrase += ' '+cobj
									#phrase_a = cobj
									#post modifiers
									'''if 'prep'+'______'+event_start in first_arg_feat_dict:
										phrase += ' '+first_arg_feat_dict['prep'+'______'+event_start]
									elif 'xcomp'+'______'+event_start in first_arg_feat_dict:
										phrase += ' '+first_arg_feat_dict['xcomp'+'______'+event_start]
									elif 'infmod'+'______'+event_start in first_arg_feat_dict:
										phrase += ' to '+first_arg_feat_dict['infmod'+'______'+event_start]
									elif 'amod'+'______'+cobjW in first_arg_feat_dict:
										phrase += ' '+first_arg_feat_dict['amod'+'______'+cobjW]'''

								elif 'prep'+'______'+event_start in first_arg_feat_dict:
									if 'prt'+'______'+event_start in first_arg_feat_dict:
										phrase += ' '+first_arg_feat_dict['prt'+'______'+event_start]
									#phrase_p = phrase
									phrase += ' '+first_arg_feat_dict['prep'+'______'+event_start]
									#phrase_a = first_arg_feat_dict['prep'+'______'+event_start]
								if phrase != phrase_o:
									#phrase_vec = phrase.split()
									#phrase_p = phrase[:-len(phrase_vec[-1])].strip()
									#phrase_a = phrase_vec[-1]
									#if phrase != event_startV[0]:
									popu_term_found = ''
									#if True:
									#if 'nsubj'+'______'+event_start in first_arg_feat_dict and first_arg_feat_dict['nsubj'+'______'+event_start] in popu_dict:
									if 'nsubj'+'______'+reason_start in first_arg_feat_dict:				
										wordR = first_arg_feat_dict['nsubj'+'______'+reason_start]
										wordRV = wordR.split('-')
										popu_term = wordR.rstrip('-'+wordRV[-1]).lower()
										#popu_term = first_arg_feat_dict['nsubj'+'______'+event_start]
										if popu_term in popu_dict:#check_2
											popu_term_found = popu_term
											if wordR in first_arg_feat_dict_popu:
												modifiers = first_arg_feat_dict_popu[wordR].keys()
												'''for modi in modifiers:
													if not modi in popu_modifier_types_values:
														popu_modifier_types_values[modi] = {}
													if modi == 'num':
														if not 'num' in popu_modifier_types_values[modi]:
															popu_modifier_types_values[modi]['num'] = 1
														else:
															popu_modifier_types_values[modi]['num'] += 1
													else:
														cvalue = first_arg_feat_dict_popu[wordR][modi]
														if not cvalue in popu_modifier_types_values[modi]:
															popu_modifier_types_values[modi][cvalue] = 1
														else:
															popu_modifier_types_values[modi][cvalue] += 1'''
											#else:
											#	continue
									if True:
											#delayed until fully checked
											phrase = phrase.lower()
											if not reason_phrase in reason_phraseD:
												reason_phraseD[reason_phrase] = 1
											else:
												reason_phraseD[reason_phrase] += 1

											reasonPatF = False
											for reason_pat in reason_p_seeds:
												if phrase.find(reason_pat) != -1:
													reasonPatF = True
											if not reasonPatF:
												
												if not phrase in event_phraseWhole:
													event_phraseWhole[phrase] = 1
													#event_phraseWhole_reasonD[phrase] = {reason_word:1}
													event_phraseWhole_reasonD[phrase] = {reason_phrase:1}
													#event_phraseWhole_popuD[phrase] = {popu_term:1}
													if popu_term_found != '':
														
														event_phraseWhole_popuD[phrase] = {popu_term_found:1}
													#phraseC += 1
													#if phraseC % 100 == 0:
													#	print str(phraseC)
												else:
													event_phraseWhole[phrase] += 1
													event_phraseWhole_reasonD[phrase][reason_phrase] = 1
													#event_phraseWhole_popuD[phrase][popu_term] = 1
													if popu_term_found != '':
														if not phrase in event_phraseWhole_popuD:
															event_phraseWhole_popuD[phrase] = {popu_term_found:1}
														else:
															event_phraseWhole_popuD[phrase][popu_term_found] = 1
											else:
												if not phrase in event_phraseWhole_seed_patt:
													event_phraseWhole_seed_patt[phrase] = 1
												else:
													event_phraseWhole_seed_patt[phrase] += 1

											'''if not phrase_p in event_phraseWhole_p:
												event_phraseWhole_p[phrase_p] = 1
												#event_phraseWhole_reasonD[phrase] = {reason_word:1}
												event_phraseWhole_p_reasonD[phrase_p] = {reason_phrase:1}
												event_phraseWhole_p_popuD[phrase_p] = {popu_term:1}
												#phraseC += 1
												#if phraseC % 100 == 0:
												#	print str(phraseC)
											else:
												event_phraseWhole_p[phrase_p] += 1
												event_phraseWhole_p_reasonD[phrase_p][reason_phrase] = 1
												event_phraseWhole_p_popuD[phrase_p][popu_term] = 1

											if not phrase_a in event_phraseWhole_a:
												event_phraseWhole_a[phrase_a] = 1
												#event_phraseWhole_reasonD[phrase] = {reason_word:1}
												event_phraseWhole_a_reasonD[phrase_a] = {reason_phrase:1}
												event_phraseWhole_a_popuD[phrase_a] = {popu_term:1}
												#phraseC += 1
												#if phraseC % 100 == 0:
												#	print str(phraseC)
											else:
												event_phraseWhole_a[phrase_a] += 1
												event_phraseWhole_a_reasonD[phrase_a][reason_phrase] = 1
												event_phraseWhole_a_popuD[phrase_a][popu_term] = 1'''

											#phrase = phrase.lower()
							
											phraseV = phrase.split()					
											phrase_head = phrase.rstrip(phraseV[-1])
											chead = phraseV[-1]
											if not phrase_head in event_phraseD:
												event_phraseD[phrase_head] = 1
												event_phraseL[phrase_head] = {}								
												event_phraseL[phrase_head][chead] = 1
											else:
												event_phraseD[phrase_head] += 1
												if not chead in event_phraseL[phrase_head]:
													event_phraseL[phrase_head][chead] = 1
												else:
													event_phraseL[phrase_head][chead] += 1
											phraseC += 1
											if phraseC % 100 == 0:
												print str(phraseC)
											#fou.write(phrase+'\n')
						

						
							
					sent = ''
					posV = []
					event_start = ''
					reason_word = ''
					reason_start = ''
					first_arg_feat_dict = {}
					first_arg_feat_dict_popu = {}
					
			elif line[0] == '(':
				#parse += oline
				prightB = 0
				rightB = line.find(')')
				while rightB != -1:
					leftB = line.rfind('(', prightB, rightB)
					if leftB == -1:
						break
					if leftB < rightB :
						word = line[leftB+1: rightB]
						pos_word = word.split()
						if len(pos_word) > 1:
							sent += pos_word[1] + ' '
							posV.append(pos_word[0])
						elif len(pos_word) == 1:
							sent += pos_word[0] + ' '
							posV.append(pos_word[0])
					prightB = rightB

					rightB = line.find(')', rightB+1)
			else:
					feat = line
					leftB = feat.find('(')
					rightB = feat.rfind(')')				
					words = feat[leftB+1: rightB]

					featH = feat[:leftB]
					wordLR = words.split(', ')
					if len(wordLR) == 2:		
						#wordL = wordLR[0].split('-')
						wordL = wordLR[0].rstrip("'")
						wordLV = wordL.split('-')
						wordR = wordLR[1].rstrip("'")
						wordRV = wordR.split('-')
						#if wordRV[0] == 'demanding' and featH == 'xcomp':
						#if wordRV[0] == 'demanding' and featH == 'xcomp' or wordRV[0] == 'protesting' and featH == 'xcomp':
						#if (wordRV[0] == 'demanding' or wordRV[0] == 'protesting' or wordRV[0] == 'protest' or wordRV[0] == 'demand') and featH == 'xcomp':
						#if (wordRV[0] == 'threatening' or wordRV[0] == 'seeking' or wordRV[0] == 'claiming' or wordRV[0] == 'urging' or wordRV[0] == 'calling' or wordRV[0] == 'complaining' or wordRV[0] == 'declaring' or wordRV[0] == 'contending' or wordRV[0] == 'expressing' or wordRV[0] == 'press') and featH == 'xcomp':
						#if (wordRV[0] == 'urging' or wordRV[0] == 'seeking' or wordRV[0] == 'seek' or wordRV[0] == 'urge' or wordRV[0] == 'calling' or wordRV[0] == 'mark' or wordRV[0] == 'forcing' or wordRV[0] == 'express' or wordRV[0] == 'expressing' or wordRV[0] == 'press' or wordRV[0] == 'condemning' or wordRV[0] == 'condemn' or wordRV[0] == 'accusing' or wordRV[0] == 'pledging') and featH == 'xcomp':
						if wordLV[0] in reason_head_dict and featH == 'xcomp':

						#if wordRV[0] == 'protesting' and featH == 'xcomp':
						#if wordRV[0] == 'threatening' and featH == 'xcomp':
						#if wordRV[0] == 'fighting' and featH == 'xcomp':
							#event_start = wordL#the starting verb
							#reason_word = wordRV[0]
							#reason_start = wordR
							event_start = wordR#the starting verb
							reason_word = wordLV[0]
							reason_start = wordL

						featHV = featH.split('_')
						featH_o = featH
						#if len(featHV) == 2 and featHV[0] == 'prep':
						if len(featHV) == 2:
							featH = featHV[0]
						key = featH+'______'+wordL
						#first_arg_feat_dict[key] = wordRV[-1]#phrase ending position
						feedword = wordR.rstrip('-'+wordRV[-1])
						feedwordInd = int(wordRV[-1]) - 1
						posVL = len(posV)
						if featH_o != 'det':
							if not wordL in first_arg_feat_dict_popu:
								first_arg_feat_dict_popu[wordL] = {}
								if not featH_o in first_arg_feat_dict_popu[wordL]:
									first_arg_feat_dict_popu[wordL][featH_o] = feedword
									#if featH_o != 'num':
									#	first_arg_feat_dict_popu[wordL][featH_o][feedword] = 1


						if featHV[0] == 'prep' and len(featHV) == 1 and not key in first_arg_feat_dict and int(wordLV[-1]) < int(wordRV[-1]):
							if feedwordInd < posVL and posV[feedwordInd] != 'CD' and posV[feedwordInd] != 'PRP':
								first_arg_feat_dict[key] = feedword
 
						elif featHV[0] == 'prep' and len(featHV) > 1 and not key in first_arg_feat_dict and int(wordLV[-1]) < int(wordRV[-1]):
							#print featH
							if feedwordInd < posVL and posV[feedwordInd] != 'CD' and posV[feedwordInd] != 'PRP':
								first_arg_feat_dict[key] = featHV[1]  + ' '+ feedword
						elif featH == 'prt'  and not key in first_arg_feat_dict:
							#if feedword != 'on' and feedword != 'since':
							if True:
								first_arg_feat_dict[key] = feedword  
						elif featH == 'dobj'  and not key in first_arg_feat_dict:
							#first_arg_feat_dict[key] = feedword
							if feedwordInd < posVL and posV[feedwordInd] != 'CD' and posV[feedwordInd] != 'PRP':
								first_arg_feat_dict[key] = wordR
						elif featH == 'nsubj' and not key in first_arg_feat_dict:
							#first_arg_feat_dict[key] = feedword.lower()
							first_arg_feat_dict[key] = wordR
						elif featH == 'xcomp' and not key in first_arg_feat_dict:
							first_arg_feat_dict[key] = feedword.lower()
						elif featH == 'infmod' and not key in first_arg_feat_dict:
							first_arg_feat_dict[key] = feedword.lower()
						elif featH == 'amod' and not key in first_arg_feat_dict and int(wordLV[-1]) < int(wordRV[-1]):
							first_arg_feat_dict[key] = feedword.lower()




	fin.close

	#event_list_new_p = {}
	#event_list_new_a = {}
	event_list_new = {}

	logf = open('phrase_learning_logs_18_check_35P_diff_epC_twoSideLoosened_reducedCond_popuModFreqFixed7_2', 'a')
	logf.write('reason phrase learning:\n')

	items = event_phraseWhole.items()
	backitems = [[v[1], v[0]] for v in items] 
	backitems.sort()
	i = len(backitems) - 1
	#while i >= 0 and i >= len(backitems) - 500:
	while i >= 0:
		reasonT = len(event_phraseWhole_reasonD[backitems[i][1]].keys())
		popuT = 0
		if backitems[i][1] in event_phraseWhole_popuD:
			popuT = len(event_phraseWhole_popuD[backitems[i][1]].keys())
		#if reasonT > 1:
		cevent = backitems[i][1]
		cfreq = backitems[i][0]
		ceventV = cevent.split()
		if len(ceventV[0]) > 3 and ceventV[0][-3:] != 'ing':
			cevent = 'to '+cevent
		#if reasonT >= reason_threshold and cfreq >= frequency and not cevent in event_dict and popuT >= popu_threshold:
		if cfreq >= frequency and not cevent in event_dict and (popuT >= popu_threshold and reasonT >= reason_threshold):
		#if cfreq >= frequency and not cevent in event_dict and (reasonT >= reason_threshold):

			event_list_new[cevent] = str(cfreq)+'\t'+str(reasonT) + '\t'+str(popuT)
			logf.write('good: '+cevent+'\t'+str(cfreq)+'\t'+str(reasonT) + '\t'+str(popuT) + '\n')
			#fou.write(.lower()+'\t'+str(backitems[i][0])+'_'+str(reasonT)+'\n')
			#fou.write(backitems[i][1].lower()+'\n')
			#columN += 1		
			#fou.write(backitems[i][1])
			#if columN % lineSize == 0:
			#	fou.write('\n')
			#else:
			#	fou.write('\t')
		else:
			logf.write( 'bad: '+cevent+'\t'+str(cfreq)+'\t'+str(reasonT) + '\t'+str(popuT)+'\n')
		i -= 1
	'''logf.write('patterns:\n')
	items = event_phraseWhole_p.items()
	backitems = [[v[1], v[0]] for v in items] 
	backitems.sort()
	i = len(backitems) - 1
	#while i >= 0 and i >= len(backitems) - 500:
	while i >= 0:
		reasonT = len(event_phraseWhole_p_reasonD[backitems[i][1]].keys())
		popuT = len(event_phraseWhole_p_popuD[backitems[i][1]].keys())
		#if reasonT > 1:
		cevent = backitems[i][1]
		cfreq = backitems[i][0]
		#if reasonT >= reason_threshold and cfreq >= frequency and not cevent in event_dict and popuT >= popu_threshold:
		pat_seed_flag = False
		for pat_seed in reason_p_seeds:
			if cevent.find(pat_seed) != -1:
				pat_seed_flag = True
		if not pat_seed_flag and cfreq >= frequency and not cevent in event_dict_p and (popuT >= popu_threshold or reasonT >= reason_threshold):
			event_list_new_p[cevent] = str(cfreq)+'\t'+str(reasonT) + '\t'+str(popuT)
			reasons = ''
			for key in event_phraseWhole_p_reasonD[backitems[i][1]].keys():
				reasons += key+' '
			logf.write('good: '+cevent+'\t'+str(cfreq)+'\t'+str(reasonT) + '\t' + reasons + '\t'+str(popuT)+'\n')
			#fou.write(.lower()+'\t'+str(backitems[i][0])+'_'+str(reasonT)+'\n')
			#fou.write(backitems[i][1].lower()+'\n')
			#columN += 1		
			#fou.write(backitems[i][1])
			#if columN % lineSize == 0:
			#	fou.write('\n')
			#else:
			#	fou.write('\t')
		else:
			logf.write( 'bad: '+cevent+'\t'+str(cfreq)+'\t'+str(reasonT) + '\t'+str(popuT)+'\n')
		i -= 1
	#fou.flush()
	#fou.close
	#logf.flush()
	#logf.close
	logf.write('args:\n')
	items = event_phraseWhole_a.items()
	backitems = [[v[1], v[0]] for v in items] 
	backitems.sort()
	i = len(backitems) - 1
	#while i >= 0 and i >= len(backitems) - 500:
	while i >= 0:
		reasonT = len(event_phraseWhole_a_reasonD[backitems[i][1]].keys())
		popuT = len(event_phraseWhole_a_popuD[backitems[i][1]].keys())
		#if reasonT > 1:
		cevent = backitems[i][1]
		cfreq = backitems[i][0]
		#if reasonT >= reason_threshold and cfreq >= frequency and not cevent in event_dict and popuT >= popu_threshold:
		if cfreq >= frequency and not cevent in event_dict_a and (popuT >= popu_threshold or reasonT >= reason_threshold):
			event_list_new_a[cevent] = str(cfreq)+'\t'+str(reasonT) + '\t'+str(popuT)
			reasons = ''
			for key in event_phraseWhole_a_reasonD[backitems[i][1]].keys():
				reasons += key+' '
			logf.write('good: '+cevent+'\t'+str(cfreq)+'\t'+str(reasonT) + '\t' + reasons + '\t'+str(popuT)+'\n')
			#fou.write(.lower()+'\t'+str(backitems[i][0])+'_'+str(reasonT)+'\n')
			#fou.write(backitems[i][1].lower()+'\n')
			#columN += 1		
			#fou.write(backitems[i][1])
			#if columN % lineSize == 0:
			#	fou.write('\n')
			#else:
			#	fou.write('\t')
		else:
			logf.write( 'bad: '+cevent+'\t'+str(cfreq)+'\t'+str(reasonT) + '\t'+str(popuT)+'\n')
		i -= 1'''
	#fou.flush()
	#fou.close
	logf.flush()
	logf.close
	#return event_list_new
	#ckeys = reason_phraseD.keys()
	#tempStr = ''
	#for ckey in ckeys:
	#	tempStr += ckey+' '
	#fou_temp.write('reason_phraseD: '+tempStr+'\n')
	return [event_list_new, reason_phraseD, event_phraseWhole_seed_patt]

#def popu_phrase_learning(outfname, event_dict, reason_dict, popu_dict, event_threshold, freqency_threshold, reason_threshold):
def popu_phrase_learning(outfname, event_dict, reason_dict, popu_dict, event_threshold, freqency_threshold, reason_threshold, popu_modifier_types_values, modifier_threshold, reason_p_seeds):

	fin = open(outfname)

	event_verbArg = {}
	
	eventK = event_dict.keys()
	for key in eventK:
		keyV = key.split()
		creasonHead = keyV[0]
		if keyV[0] == 'to':
			creasonHead = keyV[1]
		event_verbArg[creasonHead] = 1
	'''for line in eventK:
		#if not line: break
		#line = line.strip()
		#if line != '':
		if True:
			#lineV = line.split('\t')
			lineVV = line.split()
			if len(lineVV) > 1:
				eventHead = lineVV[0]
				if eventHead == 'to':
					eventHead = lineVV[1]
				if not eventHead in event_verbArg:
					event_verbArg[eventHead] = {}
				eventArg = lineVV[-1]
				event_verbArg[eventHead][eventArg] = 1'''

	popu_terms = {}
	popu_terms_event = {}
	popu_terms_reason = {}
	popu_terms_reason_reasonS = {}
	popu_terms_modifiers = {}
	popu_nums = {}
	

	'''print 'event_verbArg: '+str(len(event_verbArg.keys()))
	for key in event_verbArg.keys():
		cdictK = event_verbArg[key].keys()
		tempStr = ''
		for ckey in cdictK:
			tempStr += ckey+' '
		print key+'\t'+tempStr'''

	
	event_phraseD = {}
	reason_phraseD = {}

	empty_lineC = 0
	sent = ''
	posV = []
	first_arg_feat_dict_0 = {}
	first_arg_feat_dict = {}
	first_arg_feat_dict_popu = {}
	word_pos = {}

	for line in fin:
			if not line: break
			line = line.strip()
			if line == '':
				empty_lineC += 1
				if empty_lineC % 2 == 0:
					#if 'nsubj' in first_arg_feat_dict and 'dobj' in first_arg_feat_dict:
					if 'nsubj' in first_arg_feat_dict_0:
						verbs = first_arg_feat_dict_0['nsubj'].keys()
						correct_flag = False
						#print 'nsubj found'
						for verb in verbs:
							verbV = verb.split('-')
							verb_word = verbV[0]
							if verb_word in event_verbArg:								
								phrase = verb_word#the event phrase
								phrase_p = ''
								phrase_a = ''
								if 'dobj'+'______'+verb in first_arg_feat_dict:
									#cobj = first_arg_feat_dict['dobj'+'______'+verb]
									cobjW = first_arg_feat_dict['dobj'+'______'+verb]
									cobjV = cobjW.split('-')
									cobj = cobjW.rstrip('-'+cobjV[-1])
									if 'prt'+'______'+verb in first_arg_feat_dict:
										phrase += ' '+first_arg_feat_dict['prt'+'______'+verb]	
									#phrase_p = phrase
									phrase += ' '+cobj
									#phrase_a = cobj

								elif 'prep'+'______'+verb in first_arg_feat_dict:
									if 'prt'+'______'+verb in first_arg_feat_dict:
										phrase += ' '+first_arg_feat_dict['prt'+'______'+verb]
									#phrase_p = phrase
									phrase += ' '+first_arg_feat_dict['prep'+'______'+verb]
									#phrase_a = first_arg_feat_dict['prep'+'______'+verb]
								if phrase != verb_word:
									#phrase_vec = phrase.split()
									#phrase_p = phrase[:-len(phrase_vec[-1])].strip()
									#phrase_a = phrase_vec[-1]

									#if verb in first_arg_feat_dict['dobj']:
									#	arg = first_arg_feat_dict['dobj'][verb]
									#	argV = arg.split('-')
									#	arg_word = argV[0]


									#	if arg_word in event_verbArg[verb_word]:
									#print 'verb_word found'
									phrase = phrase.lower()								
									if phrase in event_dict:#check_1
									#if phrase_p in event_dict_p and phrase_a in event_dict_a:#check_1
											#check reasons/effects too
											#print 'event found'
											reason_phrase_found = ''
											reasonPatF = False
											if 'xcomp' in first_arg_feat_dict_0 and verb in first_arg_feat_dict_0['xcomp']:
												#print 'here xcomp'
												reason = first_arg_feat_dict_0['xcomp'][verb]

												#print 'verb here: '+verb
												#for reason in reasons:
												if True:
													#print 'reason: '+reason 
													reasonV = reason.split('-')
													reason_word = reasonV[0]
													reason_phrase = reason_word
													if not reason_phrase.endswith('ing'):
														reason_phrase = 'to '+reason_phrase
													reason_phrase_o = reason_phrase
													reason_phrase_p = ''
													reason_phrase_a = ''
													#print 'reason_phrase here: '+reason
													if 'dobj'+'______'+reason in first_arg_feat_dict:
														#cobj = first_arg_feat_dict['dobj'+'______'+reason]
														cobjW = first_arg_feat_dict['dobj'+'______'+reason]
														cobjV = cobjW.split('-')
														cobj = cobjW.rstrip('-'+cobjV[-1])
														if 'prt'+'______'+reason in first_arg_feat_dict:
															reason_phrase += ' '+first_arg_feat_dict['prt'+'______'+reason]	
														#reason_phrase_p = reason_phrase							
														reason_phrase += ' '+cobj
														#reason_phrase_a = cobj	
														'''if 'prep'+'______'+reason in first_arg_feat_dict:
															reason_phrase += ' '+first_arg_feat_dict['prep'+'______'+reason]
														elif 'xcomp'+'______'+reason in first_arg_feat_dict:
															reason_phrase += ' '+first_arg_feat_dict['xcomp'+'______'+reason]
														elif 'infmod'+'______'+reason in first_arg_feat_dict:
															reason_phrase += ' to '+first_arg_feat_dict['infmod'+'______'+reason]
														elif 'amod'+'______'+cobjW in first_arg_feat_dict:
															reason_phrase += ' '+first_arg_feat_dict['amod'+'______'+cobjW]	
														'''				

													elif 'prep'+'______'+reason in first_arg_feat_dict:
														if 'prt'+'______'+reason in first_arg_feat_dict:
															reason_phrase += ' '+first_arg_feat_dict['prt'+'______'+reason]
														#reason_phrase_p = reason_phrase	
														reason_phrase += ' '+first_arg_feat_dict['prep'+'______'+reason]
														#reason_phrase_a = first_arg_feat_dict['prep'+'______'+reason]

													if reason_phrase != reason_phrase_o:
														#reason_phrase_vec = reason_phrase.split()
														#reason_phrase_p = reason_phrase[:-len(reason_phrase_vec[-1])].strip()
														#reason_phrase_a = reason_phrase_vec[-1]
														#print 'reason_phrase: '+reason_phrase
														#if reason_phrase in reason_dict:#check_2
														reason_phrase = reason_phrase.lower()
														for reason_pat in reason_p_seeds:
															if reason_phrase.find(reason_pat) != -1:
																reasonPatF = True
														if reasonPatF or reason_phrase in reason_dict:
														#if reason_phrase_p in reason_p_seeds or reason_phrase_p in reason_dict_p and reason_phrase_a in reason_dict_a:#check_2
															#delayed until fully checked
															#if not phrase in event_phraseD:
															#	event_phraseD[phrase] = 1
															#else:
															#	event_phraseD[phrase] += 1
															reason_phrase_found = reason_phrase
															if reasonPatF:
																if not reason_phrase in reason_phraseD:
																	reason_phraseD[reason_phrase] = 1
																else:
																	reason_phraseD[reason_phrase] += 1

											if True:

															if not phrase in event_phraseD:
																event_phraseD[phrase] = 1
															else:
																event_phraseD[phrase] += 1
															popu = first_arg_feat_dict_0['nsubj'][verb]

															if 'prep_of' in first_arg_feat_dict_0 and popu in first_arg_feat_dict_0['prep_of']:
																num = popu
																popu = first_arg_feat_dict_0['prep_of'][num]
																numV = num.split('-')
																num_word = numV[0]
																if not num_word in popu_nums:
																	popu_nums[num_word] = 1
																else:
																	popu_nums[num_word] += 1
															popuV = popu.split('-')
															#popu_word = popuV[0]
															popu_word = popu.rstrip('-'+popuV[-1])
															if popu_word in word_pos and word_pos[popu_word] != 'PRP' and word_pos[popu_word] != 'WP':
																popu_word = popu_word.lower()
																if not popu_word in popu_terms:
																	popu_terms[popu_word] = 1
																else:
																	popu_terms[popu_word] += 1
																if popu in first_arg_feat_dict_popu:
																	if not popu_word in popu_terms_modifiers:
																		popu_terms_modifiers[popu_word] = {}
																	modifiers = first_arg_feat_dict_popu[popu].keys()
																	for modi in modifiers:
																		if modi in popu_modifier_types_values:
																			cunit = modi
																			cform = first_arg_feat_dict_popu[popu][modi]
																			if cunit == 'num' and cform.lower() != 'one' and cform.lower() != '1':
																				#popu_terms_modifiers[popu_word][cunit] = 1
																				popu_terms_modifiers[popu_word][cunit] = popu_modifier_types_values['num']['num']
																			elif first_arg_feat_dict_popu[popu][modi] in popu_modifier_types_values[cunit]:

																				cunit_0 = cunit
																				cunit += '_'+cform

																				popu_terms_modifiers[popu_word][cunit] = popu_modifier_types_values[cunit_0][cform]

																#event_approx = verb_word + ' '+arg_word
																if not popu_word in popu_terms_event:
																	popu_terms_event[popu_word] = {}
																#popu_terms_event[popu_word][event_approx] = 1
																popu_terms_event[popu_word][phrase] = 1
																if not popu_word in popu_terms_reason:
																	popu_terms_reason[popu_word] = {}
																#popu_terms_event[popu_word][event_approx] = 1
																if reason_phrase_found != '':
																	popu_terms_reason[popu_word][reason_phrase_found] = 1
																if reasonPatF:
																	popu_terms_reason_reasonS[popu_word] = 1


															correct_flag = True
															break
							if correct_flag:
								break

										
										

					sent = ''
					posV = []
					first_arg_feat_dict_0 = {}
					first_arg_feat_dict = {}
					first_arg_feat_dict_popu = {}
					word_pos = {}

			elif line[0] == '(':
				#parse += oline
				prightB = 0
				rightB = line.find(')')
				while rightB != -1:
					leftB = line.rfind('(', prightB, rightB)
					if leftB == -1:
						break
					if leftB < rightB :
						word = line[leftB+1: rightB]
						pos_word = word.split()
						if len(pos_word) > 1:
							sent += pos_word[1] + ' '
							posV.append(pos_word[0])
						elif len(pos_word) == 1:
							sent += pos_word[0] + ' '
							posV.append(pos_word[0])
						word_pos[pos_word[1]] = pos_word[0]
					prightB = rightB

					rightB = line.find(')', rightB+1)
			else:
					feat = line
					leftB = feat.find('(')
					rightB = feat.rfind(')')				
					words = feat[leftB+1: rightB]

					featH = feat[:leftB]
					wordLR = words.split(', ')
					if len(wordLR) == 2:
						#prep_of(num, head), nsubj(verb, subj), dobj(verb, obj)
						if featH == 'nsubj' or featH == 'prep_of' or featH == 'xcomp':
						#if featH == 'nsubj' or featH == 'xcomp':
							if not featH in first_arg_feat_dict_0:
								first_arg_feat_dict_0[featH] = {}
							first_arg_feat_dict_0[featH][wordLR[0]] = wordLR[1]
					


						featHV = featH.split('_')
						featH_o = featH
						#if len(featHV) == 2 and featHV[0] == 'prep':
						if len(featHV) == 2:
							featH = featHV[0]

						wordL = wordLR[0].rstrip("'")
						wordLV = wordL.split('-')
						wordR = wordLR[1].rstrip("'")
						wordRV = wordR.split('-')

						key = featH+'______'+wordL
						#first_arg_feat_dict[key] = wordRV[-1]#phrase ending position
						feedword = wordR.rstrip('-'+wordRV[-1])
						feedwordInd = int(wordRV[-1]) - 1
						posVL = len(posV)

						if featH_o != 'det':
							if not wordL in first_arg_feat_dict_popu:
								first_arg_feat_dict_popu[wordL] = {}
								if not featH_o in first_arg_feat_dict_popu[wordL]:
									first_arg_feat_dict_popu[wordL][featH_o] = feedword
									#if featH_o != 'num':
									#	first_arg_feat_dict_popu[wordL][featH_o][feedword] = 1

						if featHV[0] == 'prep' and len(featHV) == 1 and not key in first_arg_feat_dict and int(wordLV[-1]) < int(wordRV[-1]):
							if feedwordInd < posVL and posV[feedwordInd] != 'CD' and posV[feedwordInd] != 'PRP':
								first_arg_feat_dict[key] = feedword
 
						elif featHV[0] == 'prep' and len(featHV) > 1 and not key in first_arg_feat_dict and int(wordLV[-1]) < int(wordRV[-1]):
							#print featH
							if feedwordInd < posVL and posV[feedwordInd] != 'CD' and posV[feedwordInd] != 'PRP':
								first_arg_feat_dict[key] = featHV[1]  + ' '+ feedword
						elif featH == 'prt'  and not key in first_arg_feat_dict:
							#if feedword != 'on' and feedword != 'since':
							if True:
								first_arg_feat_dict[key] = feedword  
						elif featH == 'dobj'  and not key in first_arg_feat_dict:
							#first_arg_feat_dict[key] = feedword
							if feedwordInd < posVL and posV[feedwordInd] != 'CD' and posV[feedwordInd] != 'PRP':
								first_arg_feat_dict[key] = wordR
						#elif featH == 'nsubj' and not key in first_arg_feat_dict:
						#	first_arg_feat_dict[key] = feedword.lower()

						elif featH == 'xcomp' and not key in first_arg_feat_dict:
							first_arg_feat_dict[key] = feedword.lower()
						elif featH == 'infmod' and not key in first_arg_feat_dict:
							first_arg_feat_dict[key] = feedword.lower()
						elif featH == 'amod' and not key in first_arg_feat_dict and int(wordLV[-1]) < int(wordRV[-1]):
							first_arg_feat_dict[key] = feedword.lower()

	fin.close

	'''fou_nums = open('generated_population_nums_eventP247_demand_protest', 'w')
	items = popu_nums.items()
	backitems = [[v[1], v[0]] for v in items]
	backitems.sort()

	i = len(backitems) - 1
	while i >= 0:
		fou_nums.write(backitems[i][1]+'\t'+str(backitems[i][0])+'\n')
		i -= 1
	fou_nums.flush()
	fou_nums.close

	fou_terms = open('generated_population_terms_eventP247_demand_protest', 'w')'''
	
	popu_list_new = {}

	items = popu_terms.items()
	backitems = [[v[1], v[0]] for v in items]
	backitems.sort()

	print 'backitems: '+str(len(backitems))

	logf = open('phrase_learning_logs_18_check_35P_diff_epC_twoSideLoosened_reducedCond_popuModFreqFixed7_2', 'a')
	logf.write('popu phrase learning:\n')
	i = len(backitems) - 1
	while i >= 0:	
		popu_word = backitems[i][1]	
		cfreq = backitems[i][0]	
		eventT = len(popu_terms_event[popu_word].keys())
		reasonT = 0
		if popu_word in popu_terms_reason:
			reasonT = len(popu_terms_reason[popu_word].keys())
		modiT = 0
		modiStr = ''
		numModFlag = False
		avg_count = 0
		all_count = 0
		if popu_word in popu_terms_modifiers:
			if 'num' in popu_terms_modifiers[popu_word]:
				numModFlag = True
			modiK = popu_terms_modifiers[popu_word].keys()		
			modiT = len(modiK)
			for key in modiK:
				modiStr += key+' '
				all_count += popu_terms_modifiers[popu_word][key]
			if modiT > 0:
				avg_count = float(all_count) / float(modiT)

		avg_count_topTwo = 0
		all_count_topTwo = 0

		if popu_word in popu_terms_modifiers:
			items_m = popu_terms_modifiers[popu_word].items()
			if len(items_m) >= 2:
				backitems_m = [[v[1], v[0]] for v in items_m]
				backitems_m.sort()
				all_count_topTwo = backitems_m[-1][0] + backitems_m[-2][0]
				avg_count_topTwo = float(all_count_topTwo) / float(2)

		
		#popu_word
		#j = 0
		#while j < len(popu_word)
		validateF = False
		for char in popu_word:
			if string.ascii_letters.find(char) != -1:
				validateF = True
				break
		#string.ascii_letters
		#print 'freqency_threshold: '+str(freqency_threshold)
		#print 'event_threshold: '+str(event_threshold)			
		#if not popu_word in popu_dict and cfreq >= freqency_threshold and eventT >= event_threshold and validateF and reasonT >= reason_threshold:
		#if not popu_word in popu_dict and cfreq >= freqency_threshold and validateF and (reasonT >= reason_threshold and eventT >= event_threshold) and (modiT >= modifier_threshold and numModFlag):
		#if not popu_word in popu_dict and cfreq >= freqency_threshold and validateF and (reasonT >= reason_threshold and eventT >= event_threshold) and (modiT >= modifier_threshold):
		if not popu_word in popu_dict and cfreq >= freqency_threshold and validateF and (reasonT >= reason_threshold and eventT >= event_threshold) and (modiT >= modifier_threshold and avg_count_topTwo >= 100):
		#if not popu_word in popu_dict and cfreq >= freqency_threshold and validateF and (reasonT >= reason_threshold and eventT >= event_threshold) and (modiT >= modifier_threshold and numModFlag):
		#if not popu_word in popu_dict and cfreq >= freqency_threshold and validateF and (reasonT >= reason_threshold and eventT >= event_threshold) and (modiT >= modifier_threshold and numModFlag) and popu_word in popu_terms_reason_reasonS:
		#if not popu_word in popu_dict and cfreq >= freqency_threshold and validateF and (eventT >= event_threshold) and (modiT >= modifier_threshold and numModFlag):
			popu_list_new[popu_word] = str(backitems[i][0])+'\t'+str(eventT) + '\t'+str(reasonT)+'\t'+str(modiT)
			logf.write( 'good: '+popu_word +'\t'+str(backitems[i][0])+'\t'+str(eventT) + '\t'+str(reasonT)+'\t'+str(modiT)+'\t'+modiStr+'\t'+str(avg_count)+'\t'+str(avg_count_topTwo)+'\n')

		elif not popu_word in popu_dict and validateF:
			logf.write( 'bad: '+ popu_word + '\t'+str(backitems[i][0])+'\t'+str(eventT) + '\t'+str(reasonT)+'\t'+str(modiT)+'\t'+modiStr+'\t'+str(avg_count)+'\t'+str(avg_count_topTwo)+'\n')
		i -= 1
	logf.flush()
	logf.close
	#return popu_list_new
	return [popu_list_new, event_phraseD, reason_phraseD]

def relevancy_check(lexiconD, lexiconL, relF, generalF, threshold, source, part, checked):
	logf = open('check_temp7_'+str(part), 'w')
	tempO = open('checked_temp7_'+str(part), 'w')
	#logf_succ.write('second check:\n')
	#logf_fail = open('check_logs_18_check_35P_fail_diff', 'a')
	#logf_fail.write('second check:\n')
	#lexiconL = lexiconD.keys()
	filtered_lexicon = []
	failed_lexicon = []
	relf = open(relF)
	generalf = open(generalF)
	relCont = []
	generalCont = []
	for line in relf:
		if not line: break
		relCont.append(line)
	relf.close
	for line in generalf:
		if not line: break
		generalCont.append(line)
	generalf.close
	
	for event in lexiconL:
		relC = 0
		generalC = 0
		relC_doc = 0 
		event_0 = event
		event = event.lower()

		if event_0 in checked:
			print 'here1'
			hist = checked[event_0]
			if source == 'reason' or source == 'event':
				histV = hist.split(' ')
				relC = int(histV[0]) 
				generalC = int(histV[1]) 
			elif source == 'popu':
				relC = int(hist)
		#rel_doc_flag = False
		#general_doc_flag = False
		else:
			print 'here2'
			for cline2 in relCont:
							cline2 = cline2.strip()
							if cline2 != '':
								eventPhraseV = event.split()
								begP = 0
								phraseBeg = 0
								found = True
								i = 0
								while i < len(eventPhraseV):
									cword = eventPhraseV[i]
									curP = cline2.find(cword, begP) 
									#if curP != -1:
									if curP != -1 and (curP == 0 or cline2[curP-1] == ' ') and (curP+len(cword) == len(cline2) or string.punctuation.find(cline2[curP+len(cword)]) != -1 or cline2[curP+len(cword)] == ' '):
										if begP > 0:
											segV = cline2[begP:curP].split()
											if len(segV) > 5:
												found = False
												break
										if begP == 0:
											phraseBeg = curP
										begP = curP + len(cword)
			
									else:
										found = False
										break
									i += 1
								if found:
									#cevent = event
									#flag_event = True
									#if cevent in event_list_new:
									#	flag_event_new = True
									#phraseBeg_event = phraseBeg
									relC += 1
									#rel_doc_flag = True
									#break	
							#else:
							#	if rel_doc_flag:
							#		relC_doc += 1
							#	rel_doc_flag = False
								
			if source == 'event' or source == 'reason':				
				for cline2 in generalCont:
						
								cline2 = cline2.strip()
								if cline2 != '':
									eventPhraseV = event.split()
									begP = 0
									phraseBeg = 0
									found = True
									i = 0
									while i < len(eventPhraseV):
										cword = eventPhraseV[i]
										curP = cline2.find(cword, begP) 
										#if curP != -1:
										if curP != -1 and (curP == 0 or cline2[curP-1] == ' ') and (curP+len(cword) == len(cline2) or string.punctuation.find(cline2[curP+len(cword)]) != -1 or cline2[curP+len(cword)] == ' '):
											if begP > 0:
												segV = cline2[begP:curP].split()
												if len(segV) > 5:
													found = False
													break
											if begP == 0:
												phraseBeg = curP
											begP = curP + len(cword)
			
										else:
											found = False
											break
										i += 1
									if found:
										#cevent = event
										#flag_event = True
										#if cevent in event_list_new:
										#	flag_event_new = True
										#phraseBeg_event = phraseBeg
										generalC += 1
										#general_doc_flag = True
										#break
			if source == 'event' or source == 'reason':
				#checked[event_0] = str(relC)+'\t'+str(generalC)
				tempO.write(event_0+'\t'+str(relC)+' '+str(generalC)+'\n')
				tempO.flush()
			elif source == 'popu':
				#checked[event_0] = str(relC)
				tempO.write(event_0+'\t'+str(relC)+'\n')
				tempO.flush()


							
		freqV = lexiconD[event_0].split('\t')
		freq = int(freqV[0])
		relProb = 1
		if relC > 0:
			relProb = round(float(freq) / float(relC), 2)
		relProb += 0.0001

		domainProb = 0
		if relC > 0:
			domainProb = round(float(generalC) / float(relC))
		domainProb -= 0.0001

		#if not ( generalC <= 3*relC or generalC <= 5*relC and relC <= 20 or relC == 0 and generalC <= 5):
		#if generalC <= 3*relC or generalC <= 5*relC and float(freq) >= threshold * float(relC):
                #if (source == 'event' or source == 'reason') and (generalC <= 3*relC or generalC <= 5*relC and relProb >= threshold) or source == 'popu' and relProb >= threshold:	
                #if (source == 'event' or source == 'reason') and (generalC <= 3*relC or generalC <= 5*relC and relProb >= threshold) or source == 'popu' and relProb >= threshold:
                #if (source == 'event' or source == 'reason') and (generalC <= 3*relC) or source == 'popu' and relProb >= threshold:	
                if (source == 'event' or source == 'reason') and (generalC <= 3*relC) or source == 'popu' and freq >= int(threshold * relC):	
                #if (source == 'event' or source == 'reason') and (generalC <= 3*relC or relProb >= threshold) or source == 'popu' and relProb >= threshold:			
                #if (source == 'event' or source == 'reason') and (domainProb <= 3 or domainProb <= 5 and relProb >= threshold) or source == 'popu' and relProb >= threshold:					
			filtered_lexicon.append(event_0)
			logf.write('succ\t'+event_0+'\t'+str(freq)+'\t'+str(relProb)+'\trelC: '+str(relC)+'\trelC_doc: '+str(relC_doc)+'\tgeneralC: '+str(generalC)+'\n')
			#print 'checked: '+event+' success!'
			logf.flush()

		else:
			failed_lexicon.append(event_0)
			logf.write('failed\t'+event_0+'\t'+str(freq)+'\t'+str(relProb)+'\trelC: '+str(relC)+'\trelC_doc: '+str(relC_doc)+'\tgeneralC: '+str(generalC)+'\n')
			#print 'checked: '+event+' failed!'
			logf.flush()

	logf.close
	tempO.close

	#return checked
	#logf_succ.close
	#logf_fail.close

	#return [filtered_lexicon, failed_lexicon]
			 
	
	





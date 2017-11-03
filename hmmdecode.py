import sys
import math
import time
from collections import defaultdict

startTime = time.time()

f = open('hmmmodel.txt','rU')

transition_dict = {}
transition_list = {}
emission_dict = {}
possible_tags = {}

len_of_transition_dict = (int)(f.readline())
# print len_of_transition_dict
for i in range(0, len_of_transition_dict):
	l = f.readline()
	prev, tag, transition_prob = l.split("\t")
	# print prev, tag, transition_prob
	if prev not in transition_dict:
		transition_dict[prev] = {}
		transition_list[prev] = []
	transition_dict[prev][tag] = (float)(transition_prob.strip("\n"))
	
	transition_list[prev].append(tag)

# print transition_dict
# print transition_list

len_of_emission_dict = (int)(f.readline())
# print len_of_emission_dict
for i in range(0, len_of_emission_dict):
	l = f.readline()
	tag, word, emission_prob = l.split("\t")
	#print tag, word, emission_prob
	if tag not in emission_dict:
		emission_dict[tag] = {}
	emission_dict[tag][word] = (float)(emission_prob.strip("\n"))

#read from model all the possible tags for each word
for l in f:
	#list of all possible tags for a word in the training set
	l = l.rstrip()
	slices = l.split(" ")
	#print slices
	len_of_slices = len(slices)
	#print len_of_slices
	w = slices[0]
	#print w
	ls = set()
	for i in range(1, len_of_slices):
		ls.add(slices[i])
	if w not in possible_tags:
		possible_tags[w] = {}
	possible_tags[w] = ls
	
# print transition_dict
# print "\n"
# print emission_dict
# print "\n"
# print possible_tags
# print "\n"



output_file = open("hmmoutput.txt", "w")


#test_file = sys.argv[1]
test_file = open("hmm_test.txt","rU")
# probability_matrix = [[]]
#test_text_file = open("test-text.txt","rU")
for line in test_file:
	line = line.rstrip()
		
	viterbi_prob = {}
	poss_tag_list = defaultdict(list)
	backptr = {}
	poss_tag_list[0] = {"q0"}
	viterbi_prob[0, "q0"] = 0.0
	# print poss_tag_list
	# print viterbi_prob 
	# print "\n"
	words = line.split(" ")
	#print words
	prev_tags = poss_tag_list[0]
	# print prev_tags

	count = 1
	# print words	
	for word in words:
		#print word
		current_tag_list = []
		if possible_tags.has_key(word): #word is in training data
			# print "\nPOSSIBLE TAGS: "
			# print possible_tags[word]
			# print "\n"
			current_tag_list = possible_tags[word]
			# print current_tag_list
		else: #new word which is not present in the training set
			# print "HERE#############"
			for prev_tag in prev_tags:
				# print "\n"
				# print prev_tag
				# for x in transition_list[prev_tag]:
				# 	print x
				# print transition_list[prev_tag]
				if prev_tag in transition_list:
					for ctag in transition_list[prev_tag]: 
						# print ctag  
						if ctag not in current_tag_list:
					# ctag = transition_list[prev_tag]
					# print ctag
							if ctag!='qX':
								# print ctag
								current_tag_list.append(ctag)
							# else: print "hry"
		# print current_tag_list    
					

		# print current_tag_list
		for current_tag in current_tag_list: #consider possible tags one by one
			maxprob = float('-inf')
			maxtag = ""
			#print "hi"
			# print current_tag
			for prev_tag in prev_tags:
				# print prev_tag
				#print "hello"
				if prev_tag in transition_dict:
					if current_tag in transition_dict[prev_tag]:
						p1 = transition_dict[prev_tag][current_tag]
						# print p1
					else: p1 = transition_dict[prev_tag]['qX']
				# else:
				# 	p1 = transition_dict[prev_tag]["qX"]

				if current_tag in emission_dict:
					if word in emission_dict[current_tag]:
						p2 = emission_dict[current_tag][word]
						# print p2
					else: p2 = 1.0
				else: p2 = 1.0

				p3 = viterbi_prob[count-1, prev_tag]
				# print p3
				# print "Hey"
				prob = math.log(p1)+math.log(p2)+(float)(p3) 
				# print prob
				# print maxprob
				if prob > maxprob:
					# print("Greater!")
					maxprob = prob
 					maxtag = prev_tag
 					#print maxprob, maxtag
 			#print word, current_tag, maxprob, maxtag
 			poss_tag_list[count].append(current_tag)
			viterbi_prob[count,current_tag] = maxprob
			backptr[count,current_tag] = maxtag

		prev_tags = poss_tag_list[count]
		count = count+1 

	# print poss_tag_list
	# print "\n"
	# print viterbi_prob
	# print "\n"
	# print backptr


	maxprob = float('-inf')
	maxtag = ''


	len_of_poss_tag_list = len(poss_tag_list) - 1
	# print len_of_poss_tag_list
	#print poss_tag_list[len_of_poss_tag_list]
	for poss_tag in poss_tag_list[len_of_poss_tag_list]: #iterate through the list of possible tags of the last word
		# print poss_tag
		if viterbi_prob[len_of_poss_tag_list,poss_tag] > maxprob:
			maxprob = viterbi_prob[len_of_poss_tag_list,poss_tag]
			maxtag = poss_tag
	#print maxtag

	# print "\nStart Tagging"

	final_tag = {}
	for x in range(len_of_poss_tag_list, 0, -1): #traverse in reverse
		#print x
		#print maxtag
		final_tag[words[x-1]] = maxtag
		maxtag = backptr[x, maxtag]
		#print maxtag
	# print final_tag	
	# print "End Tagging"

	for word in words:
		s = word + "/" + final_tag[word] + " "
		output_file.write(s)
	output_file.write("\n")

elapsedTime = time.time() - startTime
print elapsedTime
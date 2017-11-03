import sys
import math
import os


def count_occurences(tokens):
	occurence_count = {}
	for x in tokens:
		if x in occurence_count:
			occurence_count[x] += 1
		else:
			occurence_count[x] = 1
	return occurence_count

def ngrams(sentence,n):
	n_grams = []
	if n ==1:
		n_grams = sentence
	if n == 2:
		for i in range(len(sentence)-1):
			n_grams.append((sentence[i],sentence[i+1]))
	if n == 3:
		for i in range(len(sentence)-2):
			n_grams.append((sentence[i],sentence[i+1],sentence[i+2]))
	if n == 4:
		for i in range(len(sentence)-3):
			n_grams.append((sentence[i],sentence[i+1],sentence[i+2],sentence[i+3]))
	return n_grams



def brevity_penalty(candidate,references):
	c = 0
	
	for i in candidate:
		c += len(i)


	min_arr = []
	for i in references:
		r = 0
		for j in i:
			r += len(j)
		min_arr.append(abs(r-c))

	r = min(min_arr)

	if r >= c:
		return math.exp(1-r/c)
	else:
		return 1

def modified_precision(candidates,list_of_references,n):
	clip_count = 0
	unclip_count = 0
	for candidate,references in zip(candidates,list_of_references):  #zip each candidate with the list of all its references
		new_counts = {}
		candidate = candidate.split()

		n_gram_cand = ngrams(candidate,n) 

		if len(n_gram_cand) == 0:    #length of candidate is less than the value of n
			continue

		candidate_count = count_occurences(n_gram_cand)
			
		max_count = {}
		for reference in references:
			reference = reference.strip()
			reference = reference.split()
			n_gram_reference = ngrams(reference,n)

			reference_count = count_occurences(n_gram_reference)

			for x in candidate_count:
				try:
					max_count[x] = max(max_count.get(x,0),reference_count[x])
				except:
					max_count[x] = max_count.get(x,0) 
			
		for i in candidate_count:
			new_counts[i] = min(candidate_count[i],max_count[i])

		clip_count += sum(new_counts.values())
		unclip_count += sum(candidate_count.values())  #unclipped candidate words

	modified_prec = float(clip_count)/count_w 
	return modified_prec


def bleu_score(candidate,references):
	weights = [0.25,0.25,0.25,0.25]

	p_n = [] #modified precision score
	brevity_p = brevity_penalty(candidate,references)

	
	references_list = []
	for i in range(len(references[0])): #no of columns
		t = []
		for j in range(len(references)):  #no of rows
			#print [references[j][i]]
			t += [references[j][i]]
			#print temp
		references_list.append(t) #data = list of references for candidate1

	#print "\n"
	for n in range(1,5):
		mod_prec_score = modified_precision(candidate,references_list,n)
		#print temp
		p_n.append(mod_prec_score)


	#print "\n"
	pn_sum = 0
	for w,p in zip(weights,p_n):
		if p!=0:
			pn_sum += (w*math.log(p))

	
	score = brevity_p*math.exp(pn_sum)
	#print score

	return score

candidate_file = sys.argv[1]
reference_file  = sys.argv[2]

f = open(candidate_file,'r')
candidate_contents = f.readlines()

f2 = open('bleu_out.txt','w')

reference_contents = []
paths = []

if os.path.isfile(reference_file):
	f1 = open(reference_file,'r')
	reference_contents.append(f1.readlines())
else:
	for dirpath,dirname,files in os.walk(reference_file):
		for filename in files:
			paths.append(os.path.join(dirpath, filename))

	for path in paths:
		f1 = open(path,'r')
		reference_contents.append(f1.readlines())
		f1.close()


# for i in range(len(candidate_contents)):
# 	candidate_contents[i] = candidate_contents[i].strip()

bleuscore = bleu_score(candidate_contents,reference_contents)
f2.write(str(bleuscore))

f.close()
f2.close()
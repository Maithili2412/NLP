#NB Classifier - Learn
#!/usr/bin/python
import math
import sys
from collections import defaultdict
from string import whitespace
tp = 'TP'
tn = 'TN'
dp = 'DP'
dn = 'DN'

def naive_bayes(i, tru, decep, pos, neg):
    
    for token in data_dict[i]:
        token = token.lower()
        token = token.replace("--", " ")
        token = token.replace(" ","")
        token.translate(None, whitespace)
        if token in stop_words:
            continue
        if token == " " or token == "":
            continue
        if token.isdigit():
            continue

        if len(token) == 1:
            continue

        elif token in learn_dict:
            if(pos and tru):
                if(learn_dict[token][tp] == 0):
                    learn_dict[token][tp] = 1
                else:
                    learn_dict[token][tp] += 1
            elif(pos and decep):
                if(learn_dict[token][dp] == 0):
                    learn_dict[token][dp] = 1
                else:
                    learn_dict[token][dp] += 1
            elif(neg and decep):
                if(learn_dict[token][dn] == 0):
                    learn_dict[token][dn] = 1
                else:
                    learn_dict[token][dn] += 1
            elif(neg and tru):
                if(learn_dict[token][tn] == 0):
                    learn_dict[token][tn] = 1
                else:
                    learn_dict[token][tn] += 1
                    
                
        else:
            learn_dict[token]={}
            learn_dict[token][tp]= 0
            learn_dict[token][tn] = 0
            learn_dict[token][dp] = 0
            learn_dict[token][dn] = 0
            if(pos and tru):
                learn_dict[token][tp] = 1
            elif(pos and decep):
                learn_dict[token][dp] = 1
            elif(neg and decep):
                learn_dict[token][dn] = 1
            elif(neg and tru):
                learn_dict[token][tn] = 1


 
 #-------------------------------------------------------------------------------------------------------------------------------   
    
data_dict = {}

id = set()
paragraphs = [[]]
punc = {',', '.', '{', '}', '(', ')', '!', '\"', '@', '#', '%', '^', '&', '*', ':', ';', '/', '?', '<', '>', '=', '+', '[', ']'}
stop_words = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']

inputfile = sys.argv[1]
in_file = open(inputfile,"r")

#inputfile = open("train-text.txt","rU")
data = in_file.read()
paragraphs = data.split("\n")

for p in paragraphs:

    #print p
    for c in punc:
            if c in p:
                p = p.replace(c, "")
    
    words = p.split(" ")

    id.add(words[0])
    key = words[0]

    word_list = []
    for w in range(1, len(words)):
        #print w
        """
        for c in punc:
            if c in words[w]:
                words[w] = words[w].replace(c, "")
        """

        #print words[w]
        word_list.append(words[w])
        data_dict[key] = word_list
    
   

#read train-labels file
labels_dict = {}

#labelfile = open("train-labels.txt", "rU")
#with open("train-labels.txt", "rU") as labelfile:
labelfile = sys.argv[2]
l_file = open(labelfile,"r")
for line in l_file:
    class_labels = []
    key, TD, PN = line.split()
    #print key, TD, PN
    class_labels.append(TD)
    class_labels.append(PN)
    labels_dict[key] = class_labels

        
#print data_dict
#print
#print labels_dict
#print data_dict["02GRaAeUBioqRjtkICm3"][5]
#-------------------------------------------------------------------------------------------------------------------------------------

no_of_positive_reviews = 0
no_of_negative_reviews = 0
no_of_truthful_reviews = 0
no_of_deceptive_reviews = 0

learn_dict = {}
for i in id:
    if i in data_dict and i in labels_dict:
        if labels_dict[i][0] == "truthful":
            tru = True
            no_of_truthful_reviews += 1
        else:
            tru = False

        if labels_dict[i][0] == "deceptive":
            decep = True
            no_of_deceptive_reviews += 1
        else:
            decep = False

        if labels_dict[i][1] == "positive":
            pos = True
            no_of_positive_reviews += 1
        else:
            pos = False

        if labels_dict[i][1] == "negative":
            neg = True
            no_of_negative_reviews += 1
        else:
            neg = False

        naive_bayes(i, tru, decep, pos, neg)

#print
#print learn_dict
#print "\nno_of_truthful\tno_of_deceptive\t_no_of_positive\tno_of_negative"
#print "\n%d\t%d\t%d\t%d" % (no_of_truthful_reviews, no_of_deceptive_reviews, no_of_positive_reviews, no_of_negative_reviews)
#r = no_of_deceptive_reviews+no_of_negative_reviews+no_of_truthful_reviews+no_of_positive_reviews
#print r


prior_truthful = prior_deceptive = prior_positive = prior_negative = 0.5
p = math.log(0.5)
#print prior_truthful, prior_deceptive, prior_truthful, prior_negative
#print p


unique_word_count = 0
total_word_count = 0
TP_class_count = 0
DP_class_count = 0
TN_class_count = 0
DN_class_count = 0

for h in learn_dict:
    unique_word_count = unique_word_count + 1
    TP_class_count += learn_dict[h][tp]
    DP_class_count += learn_dict[h][dp]
    TN_class_count += learn_dict[h][tn]
    DN_class_count += learn_dict[h][dn]

total_word_count = DP_class_count + TP_class_count + DN_class_count + TN_class_count

#print unique_word_count, total_word_count
#print TP_class_count, DP_class_count, TN_class_count, DN_class_count
#print len(labels_dict)


#smoothing - denominator
tp_den = TP_class_count + unique_word_count
dp_den = DP_class_count + unique_word_count
tn_den = TN_class_count + unique_word_count
dn_den = DN_class_count + unique_word_count


f = open("nbmodel.txt", "w")
#claculating probabilities
for word in learn_dict:

    tp1 = (math.log(learn_dict[word][tp]+1)- math.log(tp_den))
    learn_dict[word][tp] = tp1
   
    dp1 = (math.log(learn_dict[word][dp]+1)- math.log(dp_den))
    learn_dict[word][dp] = dp1
   
    tn1 = (math.log(learn_dict[word][tn]+1)- math.log(tn_den))
    learn_dict[word][tn] = tn1

    dn1 = (math.log(learn_dict[word][dn]+1)- math.log(dn_den))
    learn_dict[word][dn] = dn1


f.write("token TruePositive DeceptivePositive TrueNegative DeceptiveNegative\n")
for h in learn_dict:    
    s = h +'\t'+ str(learn_dict[h][tp]) +'\t'+ str(learn_dict[h][dp])+'\t'+ str(learn_dict[h][tn]) +'\t'+str(learn_dict[h][dn]);
    f.write(s+"\n")
f.close()

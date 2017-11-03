import math
import sys
import string
tp = 'TP'
tn = 'TN'
dp = 'DP'
dn = 'DN'

def predict_class(tp_prob, dp_prob, tn_prob, dn_prob):
    if((tp_prob > dp_prob)and(tp_prob > tn_prob)and(tp_prob > dn_prob)):
        return tp
    elif((dp_prob > tp_prob) and (dp_prob > tn_prob) and (dp_prob > dn_prob)):
        return dp
    elif((tn_prob > tp_prob) and (tn_prob > dp_prob) and (tn_prob > dn_prob)):
        return tn
    else:
        return dn


def write_class(predicted_class, i):
    id = i
    if(predicted_class == tp):
        td = "truthful"
        pn  = "positive"

    elif(predicted_class == dp):
        td = "deceptive"
        pn = "positive"

    elif(predicted_class == tn):
        td = "truthful"
        pn = "negative"

    else:
        td = "deceptive"
        pn = "negative"

    op = id+" "+td+" "+pn
    output_file.write(op+"\n")



model_file = open("nbmodel.txt", "r")
model_dict = {}
model_file.readline()
for line in model_file:
    class_prob = []
    key, PT, PD, NT, ND = line.split("\t")
    #print key, PT, PD, NT, ND
    class_prob.append(PT)
    class_prob.append(PD)
    class_prob.append(NT)
    class_prob.append(ND)
    model_dict[key] = class_prob


output_file = open("nboutput.txt", "w")


#read from test data file
test_dict = {}

test_id = set()
paragraphs = [[]]
punc = {',', '.', '{', '}', '(', ')', '!', '\"', '@', '#', '$', '%', '^', '&', '*', ':', ';', '/', '?', '<', '>', '=', '+', '[', ']'}
stop_words = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']

test_text_file = sys.argv[1]
tt_file = open(test_text_file,"r")
#test_text_file = open("test-text.txt","rU")
test_data = tt_file.read()
paragraphs = test_data.split("\n")

for p in paragraphs:

    #print p
    for c in punc:
        if c in p:
            p = p.replace(c, "")
    words = p.split(" ")

    test_id.add(words[0]) #identifier
    key = words[0]

    word_list = []
    for w in range(1, len(words)):
        #print w
        """
        for c in punc:
            if c in words[w]:
                words[w] = words[w].replace(c,"")
        """
        #print words[w]
        word_list.append(words[w])
        test_dict[key] = word_list
    
    #print

#print test_dict
#print test_id
#print
#print model_dict
if '' in test_id:
    test_id.remove('')


#print len(test_dict)
#process the test_dict
for i in test_id:
    tp_prob = dp_prob = tn_prob = dn_prob = math.log(0.5) #prior probability is 0.5
    for words in test_dict[i]:
        words = words.lower()
        words = words.replace("--", " ")
        words = words.replace(" ", "")
        if words in stop_words:
            continue
        if words == " " or words == "":
            continue
        if words not in model_dict:
            continue
        elif words in model_dict:
            tp_prob += (float)(model_dict[words][0])
            dp_prob += (float)(model_dict[words][1])
            tn_prob += (float)(model_dict[words][2])
            dn_prob += (float)(model_dict[words][3])

        #print words
    #print tp_prob, dp_prob, tn_prob, dn_prob

    predicted_class = predict_class(tp_prob, dp_prob, tn_prob, dn_prob)
    write_class(predicted_class, i)

output_file.close()
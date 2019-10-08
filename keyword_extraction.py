#coding:utf-8
import jieba
jieba.load_userdict("myDictionary.txt")
import jieba.posseg as psg
from collections import Counter
from urllib import request
from urllib.parse import quote
from bs4 import BeautifulSoup
import string
import chardet
import math
import operator; 

s = u''
f = open('3.txt',encoding='UTF-8')       
line = f.readline()  
while line:  
    s=s+line
    line = f.readline()  

f.close()
importantWord=[]
f = open('moreAttentionWord.txt',encoding='UTF-8')
line = f.readline()
while line:
	importantWord.append(line.split("\n")[0])
	line = f.readline()
f.close()

stopWord=[]
f = open('stopwords.txt',encoding='UTF-8')
line = f.readline()
while line:
	stopWord.append(line.split('\n')[0])
	line = f.readline()
f.close()

word=[]
cixing=[]
store=[(x.word,x.flag) for x in psg.cut(s)]
phrasestore=[]
nstore=[]
vstore=[]
sstore=[]
for x in store:
	if x in stopWord:
		continue
	word.append(str(x).split(',')[0].split("'")[1])
	cixing.append(str(x).split(',')[1].split("'")[1])
for i in range(1,len(word)):
	if cixing[i]=='n' and cixing[i-1]=='n' and len(word[i])>1 and len(word[i-1])>1:
		phrasestore.append(word[i-1]+word[i])
	if cixing[i]=='v' and cixing[i-1]=='n' and len(word[i])>1 and len(word[i-1])>1:
		phrasestore.append(word[i-1]+word[i])
	if cixing[i]=='n' and cixing[i-1]=='v' and len(word[i])>1 and len(word[i-1])>1:
		phrasestore.append(word[i-1]+word[i])
	if cixing[i]=='a' and cixing[i-1]=='n' and len(word[i-1])>1:
		phrasestore.append(word[i-1]+word[i])
	if cixing[i]=='d' and cixing[i-1]=='v' and len(word[i-1])>1:
		phrasestore.append(word[i-1]+word[i])
	if cixing[i]=='vn' and cixing[i-1]=='n'and len(word[i])>1 and len(word[i-1])>1:
		phrasestore.append(word[i-1]+word[i])
	if cixing[i]=='n' and cixing[i-1]=='vn' and len(word[i])>1 and len(word[i-1])>1:
		phrasestore.append(word[i-1]+word[i])
	if cixing[i]=='vn' and cixing[i-1]=='v' and len(word[i])>1 and len(word[i-1])>1:
		phrasestore.append(word[i-1]+word[i])
	if cixing[i]=='v' and cixing[i-1]=='vn' and len(word[i])>1 and len(word[i-1])>1:
		phrasestore.append(word[i-1]+word[i])
	if cixing[i]=='a' and cixing[i-1]=='vn' and len(word[i-1])>1:
		phrasestore.append(word[i-1]+word[i])
#把词组数组储存上了nn  nv  vn  an  dv类型的词组

for temp in [(x.word,x.flag) for x in psg.cut(s) if x.flag.startswith('n')]:
    if str(temp).split(',')[0].split("'")[1] in stopWord:
        continue
    nstore.append(str(temp).split(',')[0].split("'")[1])
for temp in [(x.word,x.flag) for x in psg.cut(s) if x.flag.startswith('v')]:
    if str(temp).split(',')[0].split("'")[1] in stopWord:
        continue
    vstore.append(str(temp).split(',')[0].split("'")[1])
for temp in [(x.word,x.flag) for x in psg.cut(s) if x.flag.startswith('x')]:
    if str(temp).split(',')[0].split("'")[1] in stopWord:
        continue
    if len(str(temp).split(',')[0].split("'")[1])>2:
        if '\\' not in str(temp).split(',')[0].split("'")[1]:
            sstore.append(str(temp).split(',')[0].split("'")[1])
for temp in [(x.word,x.flag) for x in psg.cut(s) if x.flag.startswith('l')]:
    if str(temp).split(',')[0].split("'")[1] in stopWord:
        continue
    sstore.append(str(temp).split(',')[0].split("'")[1])





tempn = Counter(nstore).most_common(5)
tempv = Counter(vstore).most_common(2)
temps = Counter(sstore).most_common(4)
tempphrase = Counter(phrasestore).most_common(5)
with open('frequency.txt','w+',encoding='UTF-8') as f:
    for x in tempn:
        if x not in importantWord:
            f.write('{0},{1}\n'.format(x[0],x[1]))
    for x in tempv:
        if x not in importantWord:
            f.write('{0},{1}\n'.format(x[0],x[1]))
    for x in temps:
        if x not in importantWord:
            f.write('{0},{1}\n'.format(x[0],x[1]))
    for x in tempphrase:
        if x not in importantWord:
            f.write('{0},{1}\n'.format(x[0],x[1]))
    for x in importantWord:
    	if x in s:
    		f.write(x.split('\n')[0])
    		f.write(",")
    		f.write(str(s.count(x)))
    		f.write('\n')



print("第一部分完成，接下来准备连上百度文库进行TF-IDF计算")
#分好词接下来存入字典准备连上百度文库进行TF-IDF提取关键词
dictionary = {}  
fr = open("frequency.txt",encoding='UTF-8')
line = fr.readline()
while line:
	dictionary[line.split(',')[0]] = int(line.split(',')[1])
	line = fr.readline()
fr.close()
with open('tfidf_calculation.txt','w+',encoding='UTF-8') as fc:
	for key in dictionary:
	    print(key)
	    url="https://wenku.baidu.com/search?word=%E2%80%9C"+key+"%E2%80%9D&lm=0&od=0&ie=utf-8"
	    s = quote(url,safe=string.printable)
	    if __name__ == "__main__":
	        response = request.urlopen(s)
	        html = response.read()
	        charset = chardet.detect(html)
	        html = html.decode(charset.get('encoding'),'ignore')
	        soup = BeautifulSoup(html,"html.parser")
	        if soup.find("span",class_="nums")==None:
	        	url="https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=utf-8&word=%E2%80%9C"+key+"%E2%80%9D"
	        	s = quote(url,safe=string.printable)
	        	if __name__ == "__main__":
	        		response = request.urlopen(s)
	        		html = response.read()
	        		charset = chardet.detect(html)
	        		html = html.decode(charset.get('encoding'),'ignore')
	        		soup = BeautifulSoup(html,"html.parser")
	        		if soup.find("span",class_="f-lighter lh-22")==None:
	        			dictionary[key]=dictionary[key]*math.log(100000000/(1+100000))
	        			fc.write(key)
	        			fc.write(',')
	        			fc.write(str(dictionary[key]))
	        			fc.write('\n')
	        		else:
	        			dictionary[key]=dictionary[key]*math.log(100000000/(1+int(str(soup.find("span",class_="f-lighter lh-22")).split('共')[1].split('条')[0].replace(',', ''))))
	        			fc.write(key)
	        			fc.write(',')
	        			fc.write(str(dictionary[key]))
	        			fc.write('\n')
	        else:
	        	dictionary[key]=dictionary[key]*math.log(100000000/(1+int(str(soup.find("span",class_="nums")).split('约')[1].split('篇')[0].replace(',', ''))))
	        	fc.write(key)
	        	fc.write(',')
	        	fc.write(str(dictionary[key]))
	        	fc.write('\n')
with open('keyword_prediction.txt','w+',encoding='UTF-8') as fk:
	new_dictionary=sorted(dictionary.items(),key=operator.itemgetter(1),reverse=True)
	flag=0
	for i in range(0,len(new_dictionary)):
		for j in range(0,i):
			if (new_dictionary[i][0] in new_dictionary[j][0]) or (new_dictionary[j][0] in new_dictionary[i][0]):
				flag=1
		if flag==0:
			fk.write(str(new_dictionary[i][0]))
			fk.write('\n')
		flag=0
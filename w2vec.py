# -*- coding: utf-8 -*-

from lxml import etree
from subprocess import call
from nltk.stem.snowball import FrenchStemmer
import unidecode
import commands
import re

#lemmatiseur
stemmer = FrenchStemmer()

# récupération des tweets
tree = etree.parse("littleUnlabeled.xml")

# stockage des messages
messages=[]
for msg in tree.xpath("/root/tweet/message"):
	messages.append(msg.text)

#stopword
fileStopWord=open("stopword.txt","r")
fileLemmatizedStopWord=open("stopwordLematized.txt","w")
lstStopWord = []

for line in fileStopWord :
	#je fais tout ca car unidecode c'est franchement dla merde
	#fuck les accent
	#pourquoi y a pas juste 1 encoding

	line = unicode(line, 'utf-8')
	line = unidecode.unidecode(line)
	if line.find('\n') > 0:
		line = line[0:line.find('\n')]

	line = stemmer.stem(line)
	if line not in lstStopWord :
		lstStopWord.append(line)
		fileLemmatizedStopWord.write(line.encode(encoding='UTF-8',errors='strict')+"\n")

lstStopWord.append("")


# récupérations des mots
hashtags=[]
hashtagsCount=[]

lexique=[]
lexiqueFull=[]
lexiqueFullCount=[]

mots=[]

indexHash = 0
indexMots = 0

v = False
#978
for tweet in messages:

	#tweet = tweet.encode('ascii', 'ignore').decode('ascii')
	# 'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
	if re.match(r'http([^\s]+)', tweet) :
		#test = re.findall('^(http[s]?://([a-zA-Z0-9]+.)+[a-zA-Z0-9]+/[a-zA-Z0-9]+)', tweet)
		test = re.search(r'http([^\s]+)', tweet).group()
		print(test)
		
		tweet = tweet.replace(str(test)," ")
		print(tweet)
		v = True
	if v:
		print(tweet)
		v = False

	tweet = tweet.replace(u"\u00A0", " ")
	tweet = tweet.replace(".", " ")
	tweet = tweet.replace(",", " ")
	tweet = tweet.replace(";", " ")
	tweet = tweet.replace(":", " ")
	tweet = tweet.replace("'", " ")
	#jsuis un terroriste
	tweet = tweet.replace('"', " ")
	tweet = tweet.replace("-", " ")
	tweet = tweet.replace("?", " ")
	tweet = tweet.replace("!", " ")
	tweet = tweet.replace("[", " ")
	tweet = tweet.replace("]", " ")
	tweet = tweet.replace("  ", " ")
	mots = tweet.split(" ")

	lexique.extend(x for x in mots)

mfile=open("lexique.txt","w")


for mot2 in lexique :
	if mot2 :
		mot2 = stemmer.stem(unidecode.unidecode(mot2))
		if mot2 not in lstStopWord :
			if mot2 not in lexiqueFull :
				lexiqueFull.append(mot2)
				lexiqueFullCount.append(1)
			else :
				indexMots = lexiqueFull.index(mot2)
				lexiqueFullCount[indexMots]+=1

for i in range(0,len(lexiqueFull)-1) :
	if lexiqueFullCount[i] > 10 :
		cnt = "\t"+str(lexiqueFullCount[i])+"\n"
		mfile.write(lexiqueFull[i].encode(encoding='UTF-8',errors='strict')+cnt)


mfile.close()

#si on doit refaire les hashtag
"""
mfile2=open("hashtags.txt","w")
for mot in lexiqueFull :
	if re.match('(^|\B)(#[a-zA-Z0-9]+)', mot) :
		if mot.count('#') > 1 :
			for word in re.split("#", mot) :
				if len(word) > 0 :
					word = "#" + word
					word = unidecode.unidecode(word).lower()
					word = re.search('(^|\B)(#[a-zA-Z0-9]+)', word).group()
					if word not in hashtags :
				
						hashtags.append(word)
						hashtagsCount.append(1)
						#mfile2.write(word.encode(encoding='UTF-8',errors='strict')+"\n")
					else :
						indexHash = hashtags.index(word)
						hashtagsCount[indexHash]+=1
		else :
			mot = unidecode.unidecode(mot).lower()
			mot = re.search('(^|\B)(#[a-zA-Z0-9]+)', mot).group()
			if mot not in hashtags :
					
				hashtags.append(mot)
				hashtagsCount.append(1)
				#mfile2.write(mot.encode(encoding='UTF-8',errors='strict')+"\n")

			else :
				indexHash = hashtags.index(mot)
				hashtagsCount[indexHash]+=1

for i in range(0,len(hashtags)-1) :
	if hashtagsCount[i] > 10 :
		cnt = "/"+str(hashtagsCount[i])+"\n"
		mfile2.write(hashtags[i].encode(encoding='UTF-8',errors='strict')+cnt)

mfile2.close()
"""


# si jveux recup les mentions :
# if re.match("(?:^|\s)[＠ @]{1}([^\s#<>[\]|{}]+)", mot) :
# (^|\B)(#[\w\-_]+)
# (^|\B)(#[\w]+)
# word embedings

"""
nomElu = str(nomEluBrut).decode('utf-8')
nomElu = unidecode.unidecode(nomElu).replace("-"," ").lower()
"""
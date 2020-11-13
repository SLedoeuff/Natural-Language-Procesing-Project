# -*- coding: utf-8 -*-

from lxml import etree
from subprocess import call
from nltk.stem.snowball import FrenchStemmer
import commands
import re
import unidecode

# récupération des tweets
tree = etree.parse("unlabeled.xml")

# stockage des messages
messages=[]
for msg in tree.xpath("/root/tweet/message"):
	messages.append(msg.text)

#lemmatiseur
stemmer = FrenchStemmer()


"""
filEmote=open("emote.txt","w")
for mess in messages :
	print(mess)
	if re.search("(?:[\U00010000-\U0010ffff])",mess) :
		test = re.findall("(?:[\U00010000-\U0010ffff])",mess)
		filEmote.write("|".join([k.encode("utf8") for k in test])+"\n")
		print(test)
"""


def Polarite(strTweet):
	#on dégage des trucs useless
	strTweet = strTweet.replace(u"\u00A0", " ")
	strTweet = strTweet.replace(".", " ")
	strTweet = strTweet.replace(",", " ")
	strTweet = strTweet.replace(":", " ")
	strTweet = strTweet.replace(";", " ")
	strTweet = strTweet.replace("-", " ")
	strTweet = strTweet.replace("'", " ")
	strTweet = strTweet.replace('"', " ")
	strTweet = strTweet.replace("  ", " ")
	strTweet = strTweet.replace("?!", " negatst ")
	strTweet = strTweet.replace("??", " negatst ")
	strTweet = strTweet.replace("!!", " negatst ")
	strTweet = strTweet.replace("???", " negatst ")
	strTweet = strTweet.replace("!!!", " negatst ")
	strTweet = strTweet.replace("????", " negatst ")
	strTweet = strTweet.replace("!!!!", " negatst ")
	strTweet = strTweet.replace("?", " ")
	strTweet = strTweet.replace("!", " ")
	strTweet = strTweet.replace(">", " ")
	strTweet = strTweet.replace("<", " ")
	strTweet = strTweet.replace("+", " ")
	strTweet = strTweet.replace("<", " ")
	strTweet = strTweet.replace("&", " ")
	strTweet = strTweet.replace("@", " ")
	strTweet = strTweet.replace("[", " ")
	strTweet = strTweet.replace("]", " ")
	lstMot = strTweet.split(" ")

	#polarite : 0 = neutre, 1 = positif, 2 = negatif, 3 = mixte
	polarite = 0
	nbPositif = 0
	nbNegatif = 0

	#liste de hastags annotés
	hashtagNegatif = ["#rendeznousmelenchon","#jamaismacron","#titaniclepen","#macrongate","#wtf","#sansmoile7mai","#nonaufn","#jamaislepen","#perlimpinpin","#jevoteelledegage","#fhaine","#stopfn7mai","#paslependessayer","#lepenjamais","#pitoyable","#honte","#barrage","#fnjamais","#pasunevoixpourlefn","#7maicontrelepen","#parasite","#toutsaufmacron","#trump","#sortonslepen","#jamaislefn","#dangermacron"]
	hashtagPositif = ["#jevotemacron","#macronpresident","#le7maijevotemacron","#votezmacron","#handicap","#vivelepen","#ecologie"]

	#liste de mots lemmatisés et annotés
	motsPositif = ["calm","symp","coeur","fort","raison","reuss","premi","froid","sang","gagn","excellent","saint","amis","bravo","sauv","defend","meilleur","solut","intelligent","aid","heureux","rassur","solid"]
	motsNegatif = ["negatst","suicid","peur","vid","merd","gross","dommag","hont","perdr","fiscal","meuf","regret","fachospher","insolent","con","null","perdu","dout","mauvais","alert","mort","debil","putain","mensong","agress","constern","gueul","minabl","arrog","parasit","mediocr","trump","naufrag","hyster","delir","ridicul","indign","incompetent","fou","mediocrit","racist","intox","hain","cru","violenc","insult","ferm","marr","drogu","souffr","trist","malheur","perlimpinpin","pauvr","gamin","ko","catastroph","couill","mepr","agressivit","violent","blagu","moqu","plomb","echec","ridiculise","nul","cul","terror","afflig","????","???","??","?!","!!","!!!","!!!!","haineux","danger","uoif"]

	for mot in lstMot:
		#polarite dans les hashtag
		if re.match('(^|\B)(#[a-zA-Z0-9]+)', mot) :
			if mot.count('#') > 1 :
				for word in re.split("#", mot) :
					if len(word) > 0 :
						word = "#" + word
						word = unidecode.unidecode(word).lower()
						word = re.search('(^|\B)(#[a-zA-Z0-9]+)', word).group()
						if word in hashtagNegatif :
							nbNegatif+=1

						if word in hashtagPositif :
							nbPositif+=1

			else :
				mot = unidecode.unidecode(mot).lower()
				mot = re.search('(^|\B)(#[a-zA-Z0-9]+)', mot).group()
				if mot in hashtagNegatif :
					nbNegatif+=1

				if mot in hashtagPositif :
					nbPositif+=1
		else :
			#polarite dans les mots, lemmatisé
			mot = stemmer.stem(unidecode.unidecode(mot))
			if mot in motsNegatif :
				nbNegatif+=1
			elif mot in motsPositif :
				nbPositif+=1

###########################################################################################################
	if nbPositif != 0 and nbNegatif == 0 :
		polarite = 1

	if nbPositif == 0 and nbNegatif != 0 :
		polarite = 2

	if nbPositif != 0 and nbNegatif != 0 :
		if nbNegatif > nbPositif :
			polarite = 2
		elif nbNegatif < nbPositif :
			polarite = 1
		else :
			polarite = 3

	return polarite

# ceci est un test
file=open("polarite.txt","w")
for tweet in messages :
	#print(Polarite(tweet))
	file.write(str(Polarite(tweet)).encode(encoding='UTF-8',errors='strict')+"\n")

import json
import re
import operator
import unidecode

#import codecs


#file = codecs.open("tweets_unlabeled.json",encoding="utf8")

file = open("tweets_unlabeled.json","r",encoding="utf8")
tweets = file.read()
allTweets = json.loads(tweets)["tweet"]
file.close()


hashtag = {}
at = {}
word = {}


for tweet in allTweets:
    tags = re.findall(r'#[\w]+', tweet["message"], re.U)
    ats = re.findall(r'@[\w_]+', tweet["message"], re.U)
    words = re.findall(r'[\w]+', tweet["message"], re.U)

    for k in tags:
        i = unidecode.unidecode(k.lower())
        if (i not in hashtag):
            hashtag[i] = 1
        else:
            hashtag[i]+=1
    
    for k in ats:
        i = unidecode.unidecode(k.lower())
        if (i not in at):
            at[i] = 1
        else:
            at[i]+=1

    for k in words:
        i = unidecode.unidecode(k.lower())
        if (i not in word):
            word[i] = 1
        else:
            word[i]+=1

sortHash = sorted(hashtag.items(), key=operator.itemgetter(1), reverse=True)

sortat = sorted(at.items(), key=operator.itemgetter(1), reverse=True)
sortword = sorted(word.items(), key=operator.itemgetter(1), reverse=True)


file = open("hastag.json","w+",encoding="utf8")
tweetString = json.dumps(sortHash,ensure_ascii=False)
file.write(tweetString)
file.close()

file = open("at.json","w+",encoding="utf8")
tweetString = json.dumps(sortat,ensure_ascii=False)
file.write(tweetString)
file.close()

file = open("word.json","w+",encoding="utf8")
tweetString = json.dumps(sortword,ensure_ascii=False)
file.write(tweetString)
file.close()

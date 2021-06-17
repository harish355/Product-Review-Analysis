import eel
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen as ureq

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential,load_model
import numpy as np
import pandas as pd

print("Test")
eel.init('web')

def review(url):
    my_url=str(url)
    uclient=ureq(my_url)
    page_html=uclient.read()
    uclient.close()

    page_soup1=BeautifulSoup(page_html,"html.parser")
    totpages=page_soup1.find("div",{"class":"_2MImiq _1Qnn1K"})
    totpages=totpages.span.text.strip()
    x=""
    while(totpages[-1]!=" "):
        x=x+totpages[-1]
        totpages=totpages[0:len(totpages)-1]
    x=int(x[::-1].replace(",",""))
    print("pages",x)
    filename="products2.csv"
    headers="productname,review\n"
    f=open(filename,"w",encoding='utf-8')
    f.write(headers)

    for z in range(1,x+1):
        print("Page ",z," Done")
        try:
                my_url=my_url+"&page="+str(z)
                uclient=ureq(my_url)
                page_html=uclient.read()
                uclient.close()
                page_soup=BeautifulSoup(page_html,"html.parser")
                containers=page_soup.findAll("div",{"class":"_27M-vq"})
                pn=page_soup.find("div",{"_2s4DIt _1CDdy2"})
                pn=pn.text
                for cont in containers:
                    review=cont.findAll("div",{"class":""})
                    review=review[0].text
                    #review=cont.findAll("p",{"class":"t-ZTKy"})
                    #review=review[0].text
                    revwords=review.split()
                    if len(revwords)<191:
                        f.write(str(pn.replace(",","/"))+","+str(review.replace(",","/"))+"\n")
        except:
                pass
    tp='IT DIDNT WORK WE BUY NEW IT DIE ON ME DON.T BUY IT: THE VHS WE BUY DID NOT WORK THE MATCHS WERE BORING TOO BORING I KNOW DON.T HOW WWF CAN HAVE A BAD PPV BUT THEY CAN WE BUY NEW IT WAS SO NEW BUT IT DIE ON ME DON.T BUY THIS ON VHS THIS VHS WAS NEW BUT DIDNT PLAY I HAVE NOT SEEN ALL OF THE PPV BUT WHAT I HAVE SEEN IT DIDNT PLAY GOOD NOT GOOD AT ALL IF YOU WANT TO WATCH IT GET ON DVD THAT ALL HAVE TO SAY DON.T BUY THE VHS IF YOU WANT A GOOD PPV BUY HELL IN THE CALL 2012 THAT ONE GOOD i was not happy to have a vhs i buy not work not happy at all it was too old to play good it woods not work i was sad when it did.nt work i woods not buy a wwf vhs for a 2 time the ppv was poor not that fun to watch it the wwf and a bad ppv i want to see a good wwf ppv'
    f.write(str(pn.replace(",","/"))+","+tp+"\n")
    f.close()
    print("Done")

    model=load_model("ai_model")
    data2 = pd.read_csv("products2.csv",encoding='latin-1')
    tokenizer = Tokenizer(num_words=2000, split=' ')
    tokenizer.fit_on_texts(data2['review'])
    X2 = tokenizer.texts_to_sequences(data2['review'])
    X2 = pad_sequences(X2)
    y2=model.predict(X2)
    result=np.argmax(y2,axis=1)
    posrev=np.count_nonzero(result == 1)
    negrev=len(result)-posrev-1
    return round(posrev/(posrev+negrev),2)

@eel.expose
def search(a):
    result=review(a)
    return result*100

# @eel.expose
# def title(a):
#     my_url=str(a)
#     uclient=ureq(my_url)
#     page_html=uclient.read()
#     uclient.close()

#     pageSoup = BeautifulSoup(page_html, "html.parser")
#     containers = pageSoup.find("div", {"class": "_2s4DIt _1CDdy2"})
#     return (containers.text)

eel.start('index.html',size=(1000,600))

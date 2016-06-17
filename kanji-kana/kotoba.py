from lxml import html
import requests
import sys
import re
import urllib
import cgi

menuURLs = []
# get Kanji, Katakana Pairs
# crawl デジタル大辞泉 on コトバンク, 
# to crawl other dictionaries on the website, 
# just change "4032" to the number of キーワード一覧 pages of the dictionary, 
# and change "daijisen" to the dictionary name
for i in range(1,4032):
    menuURLs.append("https://kotobank.jp/dictionary/daijisen/"+str(i))

URLs = []
for menuURL in menuURLs:
    try:
        page = requests.get(menuURL)
        tree = html.fromstring(page.text)
        lastIsSansyou = False
        for result in tree.xpath('//div/div/div/div/section/ul/li/a'):
            URLs.append(result.attrib['href'])
            if len(URLs)%1000 == 0:             
                with open('status.txt','w') as f:
                    f.write("len(URLs): "+str(len(URLs))+"\n")
    except:
        with open('status.txt','w') as f:
            f.write("Error, But Continue\n")
        pass

for url in URLs:
    try:
        page = requests.get("https://kotobank.jp"+url)
        tree = html.fromstring(page.text)
        for result in tree.xpath('//*'):
            if result.tag == "title":
                lp=result.text.find("(")
                rp=result.text.find(")")
                key = result.text[0:lp]
                with open('dictionary.csv','a+') as f:
                    f.write(key+","+result.text[lp+1:rp]+"\n")
                if len(dictionary)%1000 == 0:
                    with open('status.txt','w') as f:
                        f.write("len(dictionary): "+str(len(dictionary))+"\n")
                break
    except:
        with open('status.txt','w') as f:
            f.write("Error, But Continue\n")
        pass
from lxml import html
import requests
import sys
import re
import urllib
import cgi
import json

URLs = []
with open('new_entries_from_20150324_until_20150623.tsv','r') as f:
    lines = f.readlines()
    for line in lines:
        URLs.append(["https://ja.wikipedia.org/wiki/"+line.split()[0],line.split()[0]])
with open('new_entries_from_20150623_until_head.tsv','r') as f:
    lines = f.readlines()
    for line in lines:
        URLs.append(["https://ja.wikipedia.org/wiki/"+line.split()[0],line.split()[0]])
dictionary = {}
loop = 0
for url in URLs:
    # loop+=1
    # if len(dictionary) ==5:
    #     break
    try:
        page = requests.get(url[0])
        tree = html.fromstring(page.text)
        dic = {}
        hasInfo = False
        for result in tree.xpath('//div/div/div/table/tr'):
            children = result.getchildren()
            if len(children) == 2:
                head = children[0].text
                body = []
                if head is not None:
                    grand = children[1].getchildren()
                    for grandchild in grand:
                        if grandchild.tag == "a":
                            if grandchild.text is not None:
                                body.append(grandchild.text)
                if len(body) > 0:
                    dic[head] = body
                    hasInfo = True
        if hasInfo:
            dictionary[url[1]]=dic
            if len(dictionary) % 1000 == 0:
                with open('infoWiki.txt','w') as f:
                    json.dump(dictionary, f, ensure_ascii=False, indent=4).encode('utf8')
            with open('status2.txt','w') as f:
                f.write("len(dictionary): "+str(len(dictionary))+"\n")
    except:
        with open('status2.txt','w') as f:
            f.write("Error, But Continue\n")
        pass
        
with open('infoWiki.txt','w') as f:
    json.dump(dictionary, f, ensure_ascii=False, indent=4).encode('utf8')
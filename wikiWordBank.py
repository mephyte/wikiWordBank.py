import lxml
import requests
from bs4 import BeautifulSoup
import re
import os

filePath = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists('%s\Word' % filePath):
    os.makedirs('%s\Word' % filePath) #Get filepath, if word folder does not
                      #exists then make it
pagesGot = 0 # set to count how many pages scraped
existingWords = []
print 'How many pages to scan?'
timesGet = int(raw_input())

def wordBank():
    global filePath
    alpha = list('abcdefghijklmnopqrstuvwyzx') # make .txt for each letter
    for x in alpha:                            # of alphabet
        with open('%s\Word\%sWords.txt' % (filePath, x), 'w+') as fg:
            con = fg.readlines() #Read all the lines of the file
            con = [y.strip() for y in con] #Strip of u' from unicode
            for m in con: #For every word in line in file, append to words list
                existingWords.append(m.lower())
            newPage()

def postBank(x):
    global filePath
    global pagesGot
    global timesGet
    pagesGot = pagesGot + 1 # Increments by 1 for each page scraped
    for i in x: # For every word on wiki page
        if i not in existingWords: # If word is already not existing
            letter = i[0] #Get first letter of the word
            with open('%s\Word\%sWords.txt' % (filePath ,letter), 'a') as fg:
                fg.write(i) # Write word into appropriate file depending
                fg.write('\n') # on first letter
                fg.close()
                existingWords.append(i) # Add word to existingWords
                print i , ' New'
        elif i in existingWords:
            pass # if word exists then move to next word
    if pagesGot == timesGet:
        raw_input() # Will scrape as many pages as set on first userinput
    else:
        wordBank()

def newPage():
    pContent = []
    global existingWords
    pageRequest = requests.get('https://en.wikipedia.org/wiki/Special:Random')
    soupParser = BeautifulSoup(pageRequest.text, 'lxml')
    getContent = soupParser.find_all('p') #Find all <p> elements on page
    try:
        pContent.append(getContent[0].text.encode('utf-8').lower())
        pContent = ''.join(pContent) #Wiki is not all in unicode
        nContent = re.sub('[^a-zA-Z\s]','',pContent) # RegEx to strip all
        postBank(nContent.split()) # but alphabetic letters
    except: #Sometimes an error happens which I can't figure out why
        newPage()

wordBank()

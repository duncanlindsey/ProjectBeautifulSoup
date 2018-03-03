from bs4 import BeautifulSoup
import requests, re
import numpy as np
import pandas as pd

parentURL = 'http://www.cs.ucl.ac.uk/'
targetURL = 'http://www.cs.ucl.ac.uk/current_students/syllabus/pg/'

def collectSoup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def parseModuleList(soup):
    modules = soup.find_all(title=re.compile('COMP'))
    return modules

def tabulateModules(modules):
    moduleData = []
    for module in modules:
        text = singleSplit(module.contents[0], '-')
        link = parentURL + module.get('href')
        moduleData.append([text[0], text[1], link])
    df = pd.DataFrame(moduleData, columns = ['Code', 'Name', 'Link'])
    return df

def singleSplit(text, delim):
    return (text.partition(delim)[0].strip(), text.partition(delim)[2].strip())

def runScrape():
    soup = collectSoup(targetURL)
    modules = parseModuleList(soup)
    moduleLibrary = tabulateModules(modules)
    print(moduleLibrary)

''' FILE RUN '''

runScrape()

#soup = collectSoup(targetURL)
#modules = parseModuleList(soup)
#for module in modules:
    #print(module.contents[0])
    #print(parentURL + module.get('href'))
#print('%s modules found.' % (len(modules)))
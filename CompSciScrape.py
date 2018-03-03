from bs4 import BeautifulSoup
import requests, re
import numpy as np
import pandas as pd

targetModulesFile = 'TargetModules.csv'

def collectSoup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def parseModuleList(soup, parentURL):
    modules = soup.find_all(title=re.compile('COMP'))
    moduleData = []
    for module in modules:
        text = singleSplit(module.contents[0], '-')
        link = parentURL + module.get('href')
        moduleData.append([text[0].replace('  ',' '), text[1].replace('  ',' '), link])
    df = pd.DataFrame(moduleData, columns = ['Code', 'Module', 'Link'])
    return df

def singleSplit(text, delim):
    return (text.partition(delim)[0].strip(), text.partition(delim)[2].strip())

def identifyLinks(library, targets):
    joined = targets.join(library.set_index('Module'), on = 'Module')
    return joined

def loadCSV(filename):
    df = pd.read_csv(filename)
    return df
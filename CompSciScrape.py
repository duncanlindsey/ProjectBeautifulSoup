from bs4 import BeautifulSoup
import requests, re
import numpy as np
import pandas as pd

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

def parseModuleDetails(soup):
    focus_soup = soup.find(class_='syllabus_page')
    titles = focus_soup.find_all('th')
    values = focus_soup.find_all('td')
    #paragraphs = focus_soup.find_all('div', class_=re.compile('csc'))
    module_details = []
    for i in range(len(titles)):
        module_details.append([titles[i].get_text(), values[i].get_text(' ', strip=True)])
    for header in focus_soup.find_all('div', class_=re.compile('csc-header ')):
        header_text = header.get_text(strip=True)
        body_text = []
        for sibling in header.next_siblings:
            if sibling.name and sibling.name.startswith('h'):
                break
            if sibling.name == 'p':
                body_text.append(sibling.get_text(' ', strip=True))
            if sibling.name == 'ul':
                for bullet in sibling.find_all('li'):
                    body_text.append('- ' + bullet.get_text(' ', strip=True))
        module_details.append([header_text, body_text])
        #header = paragraphs[j].find_all('h1')
        #body = paragraphs[j].find_all(['p','ul'])
        #print(header)
        #print(body)
        #module_details.append([header.text, body.get_text(' ', strip=True)])
        #print(headers[j].text)
        #print(paragraphs[j].text)
    print(module_details)
    

def singleSplit(text, delim):
    return (text.partition(delim)[0].strip(), text.partition(delim)[2].strip())

def joinDataframes(targets, library, onField):
    joined = targets.join(library.set_index(onField), on = onField)
    return joined

def loadCSV(filename):
    df = pd.read_csv(filename)
    return df

soup = collectSoup('http://www.cs.ucl.ac.uk/current_students/syllabus/compgi/compgi09_applied_machine_learning/')
parseModuleDetails(soup)
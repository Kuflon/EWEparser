import requests
from bs4 import BeautifulSoup
import docx
import random

#You can find it on page, F12 -> Networks. Reload page, open first link. Find 'User-Agent'.
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36 Edg/81.0.416.64',
               'Accept': '*/*'}

def get_html(url):
    '''
    Using method get to request page
    '''
    r = requests.get(url, headers=HEADERS)
    return r


def create_url(word):
    '''
    Creating url for the word
    Ex. https://context.reverso.net/translation/english-russian/take+off
    '''
    url = 'https://context.reverso.net/translation/english-russian/'
    url += word
    return url


def get_content(html):
    '''
    Getting content from page, preprocessing data
    '''
    #Make soup with the html
    soup = BeautifulSoup(html, 'html.parser')

    #Get All ENG block with examples
    items = soup.find_all('div', class_='src')

    #That's the word that we have, just for better visualizing
    word = soup.find('input', id='entry').get('value')

    #Make the array of all possible exmaples of the word
    examples = []
    for item in items:
        example = item.select_one("span")
        if example:
            examples.append(example.text.replace('\\n', ''))

    #Returning random example of the word
    return f'{word} - {examples[int(random.uniform(0, len(examples) - 1))]}'


def parse(url):
    '''
    Get the DOM,
    Return the string with "Word - Example"
    '''
    html = get_html(url)

    #if status is ok, well
    if html.status_code == 200:
        str = get_content(html.text)
    else:
        print('Error')
    return str


#Reading file
file = open('wordlist.txt', encoding='utf-8')
wordlist = []
for row in file:
    wordlist.append(row)

answer = []
doc = docx.Document()
for i in range(len(wordlist)):
    #preprocess words for searching
    wordlist[i] = wordlist[i].replace(" ", "+")
    wordlist[i] = wordlist[i].replace("\\n", '')

    #get current url
    url = create_url(wordlist[i])

    #Add current answer
    doc.add_paragraph(parse(url))

doc.save('answer.docx')

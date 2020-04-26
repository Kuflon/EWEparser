import requests
from bs4 import BeautifulSoup
import docx
import random

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36 Edg/81.0.416.64',
               'Accept': '*/*'}

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def create_url(word):
    url = 'https://context.reverso.net/translation/english-russian/'
    url += word
    return url


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='src')
    word = soup.find('input', id='entry').get('value')

    examples = []
    for item in items:
        example = item.select_one("span")
        if example:
            examples.append(example.text.replace('\\n', ''))

    return f'{word} - {examples[int(random.uniform(0, len(examples) - 1))]}'


def parse(url):
    html = get_html(url)
    if html.status_code == 200:
        str = get_content(html.text)
    else:
        print('Error')
    return str


file = open('wordlist.txt', encoding='utf-8')
wordlist = []
for row in file:
    wordlist.append(row)

answer = []
doc = docx.Document()
for i in range(len(wordlist)):
    wordlist[i] = wordlist[i].replace(" ", "+")
    wordlist[i] = wordlist[i].replace("\\n", '')
    url = create_url(wordlist[i])
    doc.add_paragraph(parse(url))
doc.save('answer.docx')

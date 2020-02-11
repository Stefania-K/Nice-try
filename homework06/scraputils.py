import requests
from pprint import pprint as pp
from bs4 import BeautifulSoup as bp

url = 'https://news.ycombinator.com'
r = requests.get('https://news.ycombinator.com/news?p=2')
page = bp(r.content, 'html.parser')

def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    titles = []

    tables = parser.table.find_all('table') # Находим все таблицы
    needed_table = tables[1] # Выбираем нужную.
    tds = needed_table.find_all('td', attrs={'class': 'subtext'}) # Код всех строчек с информацией о новости
    ttls = needed_table.find_all('a', attrs={'class': 'storylink'}) # Код всех заголовков
    for title in ttls: # С
        titles.append(title.text)
    
    for i, td in enumerate(tds):
        tr = td.find_all('a')
        url = ttls[i]['href']
        title = titles[i]
        
        author = td.find('a', attrs={'class': 'hnuser'})
        if author == None:
            author = '--'
        else:
            author = author.text

        nya = list(tr[len(tr) - 1].text) #getting comments
        l = []
        for j, ele in enumerate(nya):
            if ele == '\xa0':
                while j > 0:
                    l.append(nya[j-1])
                    j -= 1
        l.reverse()
        if len(l) > 0:
            st = int(''.join(l))
        else:
            st = 'discuss'
        
        score = td.find('span', attrs={'class': 'score'})
        if score == None:
            score = 0
        else:
            score = list(score.text)
            m = []
            for j, ele in enumerate(score):
                if ele == ' ':
                    while j > 0:
                        m.append(score[j-1])
                        j -= 1
            m.reverse()
            score = int(''.join(m))
        news_list.append({
            'points': score,
            'title': title,
            'author': author,
            'url': url,
            'comments': st
        })
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    more_link = parser.find('a', attrs={'class': 'morelink', 'rel': 'next'})
    more_link = more_link['href']

    return more_link


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = bp(response.content, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

pp(get_news(url, 3)[:3])

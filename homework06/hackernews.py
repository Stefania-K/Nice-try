from bottle import (
    route, run, template, request, redirect
)
from scraputils import get_news
from bd import News, session
from bayes import NaiveBayesClassifier

url = 'https://news.ycombinator.com'

@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()

    new_id = request.query['id']
    label  = request.query['label']

    new = s.query(News).get(new_id)
    new.label = label

    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    news_lst = get_news('https://news.ycombinator.com', 10)
    s = session()
    for i in range(len(news_lst)):
        if len(s.query(News).filter(News.title == news_lst[i]['title'], News.author == news_lst[i]['author']).all()) == 0:
            new_news = News(title = news_lst[i]['title'],
                            author = news_lst[i]['author'],
                            points = news_lst[i]['points'],
                            comments = news_lst[i]['comments'],
                            url = news_lst[i]['url'])
            s.add(new_news)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    pass


if __name__ == "__main__":
    run(host="localhost", port=9998)

s = session()
count = 0
for ele in s.query(News).filter(News.label != None).all():
    count += 1
print(count)

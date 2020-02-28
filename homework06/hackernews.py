from bottle import (
    route, run, template, request, redirect
)
from scraputils import get_news
from bd import News, session
from bayes import NaiveBayesClassifier
import string

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

@route('/recommendations')
def recommendations():
    s = session()
    rows_unlabelled = s.query(News).filter(News.label == None).all()
    X = [clean(row.title).lower() for row in rows_unlabelled]
    
    predictions = model.predict(X)
    rows_good = [rows_unlabelled[i] for i in range(len(rows_unlabelled)) if predictions[i] == 'good']
    rows_maybe = [rows_unlabelled[i] for i in range(len(rows_unlabelled)) if predictions[i] == 'maybe']
    rows_never = [rows_unlabelled[i] for i in range(len(rows_unlabelled)) if predictions[i] == 'never']
    
    return template('recommendations_template', rows_good=rows_good, rows_maybe=rows_maybe, rows_never=rows_never)


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


if __name__ == "__main__":
    s = session()
    rows = s.query(News).filter(News.label != None).all()
    X_train = [clean(row.title).lower() for row in rows]
    y_train = [row.label for row in rows]
    model = NaiveBayesClassifier(alpha=0.05)
    model.fit(X_train, y_train)
    
    run(host="localhost", port=9998)

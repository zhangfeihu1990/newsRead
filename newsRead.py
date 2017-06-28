from flask import Flask
from flask import render_template
from models import News
from mongoalchemy.session import Session
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()
app = Flask(__name__)
bootstrap.init_app(app)
session = Session.connect('runoob')

@app.route('/')
def index():

    #return 'Hello World!'
    news = session.query(News).skip(3).limit(3)
    for n in news:
      print n.title,n.update_time
    return render_template('index.html', news=news)

@app.route('/news/<int:id>')
def getNewsById(id):
  print id
  body = "world news"
  return render_template('news.html', body=body)

if __name__ == '__main__':
    app.run()

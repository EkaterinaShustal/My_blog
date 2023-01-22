from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/articles')
def articles():
    article = Article.query.order_by(Article.date.desc()).all()
    return render_template('articles.html', article=article)


@app.route('/articles/<int:id>')
def articles_detail(id):# put application's code here
    article = Article.query.get(id)
    return render_template('articles_detail.html', article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():  # put application's code here
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/articles')
        except:
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template('create-article.html')


@app.route('/articles/<int:id>/delete')
def articles_delete(id):# put application's code here
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/articles')
    except:
        return 'При удалении статьи произошла ошибка'


@app.route('/articles/<int:id>/update', methods=['POST', 'GET'])
def articles_update(id):  # put application's code here
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/articles')
        except:
            return 'При редактировании статьи произошла ошибка'
    else:
        article = Article.query.get(id)
        return render_template('articles_update.html', article=article)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(port=5577, debug=True)
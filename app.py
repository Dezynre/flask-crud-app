
#DEPENDENCIES
from flask import Flask, request, redirect, render_template, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import os


#CONFIGURATION
app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


#MODELS
class Post(db.Model):
	__tablename__='posts'
	id=db.Column(db.Integer, primary_key=True)
	title=db.Column(db.String(255))
	content=db.Column(db.String(255))

#SERVER INIT
@app.before_first_request
def initialize():
	db.create_all()
	return 0

#ROUTES
@app.route('/')
def index():
	posts=Post.query.all()
	return render_template('index.htm', posts=posts)

@app.route('/create_post')
def create_post():
	return render_template('create_post.htm')

@app.route('/add_post', methods=['POST'])
def add_post():
	title=request.form['title']
	content=request.form['content']
	postX=Post(title=title, content=content)
	db.session.add(postX)
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/post/delete/<int:id>')
def delete(id):
	post=Post.query.filter_by(id=int(id)).first()
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/post/modify/<int:id>', methods=['GET', 'POST'])
def modify(id):
	post=Post.query.filter_by(id=int(id)).first()
	if request.method=='GET':
		return render_template('modify.htm', post=post)
	else:
		post.title=request.form['title']
		post.content=request.form['content']
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('index'))

if __name__=="__main__":
	app.run()
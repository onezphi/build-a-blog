from flask import Flask,render_template,request,redirect,url_for,session

from flask_sqlalchemy import SQLAlchemy
import cgi



app=Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://build-a-blog:blog@localhost:5000/build-a-blog'
app.config['SQLALCHEMY_ECHO']=True
db=SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text(480))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Blog %r>' % self.title

        
@app.route('/base')
def index():
    if request.method == 'GET':
        return render_template('base.html',title='Home Page')

@app.route('/blog')
def blog(): 

    blog_posts=Blog.query.all()

    return render_template('blog.html',posts=blog_posts,title='Blog Page')

@app.route('/newpost')
def newpost():
    return render_template('newpost.html',title='Create new post')

@app.route('/blog/<int:post_id>')
def singlepost(post_id):

   
    entry=Blog.query.filter_by(id=post_id).one()

    return render_template('singlepost.html',entry=entry)
@app.route('/add',methods=['POST'])
def add():

    blog_title = request.form['title']
    blog_body=request.form['body']
    blog_data=Blog(title=blog_title,body=blog_body)
    if blog_title == '':
            return render_template('newpost.html',title='Create new post',err='Please enter a title for your Blog post')
    if blog_body == '':
            return render_template('newpost.html',title='Create new post',err='Please enter the body of your post',blog_title=blog_title)
    else:
        db.session.add(blog_data)
        db.session.commit( )
        post_data=Blog.query.filter_by(title=blog_title).first()
        post_id=post_data.id
        return redirect( url_for('singlepost',post_id=post_id))

if __name__=='__main__':
    app.run(debug=True)
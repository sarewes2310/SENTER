from flask import Flask,render_template,url_for,Markup
import sqlalchemy
import json

app = Flask(__name__)

#
# LIST VARIABEL CSS
#
list_css = [
    '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">',
]

#
# LIST VARIABEL JS
#
list_js = [
    #'<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>',
    #'<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>',
    #'<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>'
    #'<script src="component/asset/head.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>',
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.3/Chart.min.js"></script>',
    #'<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.3/Chart.bundle.min.js"></script>'
]

posts = [
    {
        'author'      : 'Corey Schafer',
        'title'       : 'Blog Post 1',
        'content'     : 'First post content',
        'date_posted' : 'April 20, 2019',
        #'css'         : url_for('static', filename='ujicoba.css')
    },
    {
        'author'      : 'Jane Doe',
        'title'       : 'Blog Post 2',
        'content'     : 'Second post content',
        'date_posted' : 'April 21, 2019',
        #'css'         : url_for('static', filename='ujicoba.css')
    }
]

@app.route("/", methods=['GET','POST'])
@app.route("/home")
def home():
    #dump(render_template("home.html"))
    #print(url_for('static', filename='ujicoba.css'))
    return render_template("home.html",posts = posts,css=url_for('static', filename='ujicoba.css'))


@app.route("/search",methods=['GET','POST'])
def index():
    return render_template("component/body/home.html",list_css = list_css,list_js = list_js)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/user/<username>")
def show_post(username):
    return "User %s" % username


@app.route("/subpath/<path:user_path>")
def show_subpath(user_path):
    return "Path %s" % user_path


@app.route("/ujicoba")
def uji():
    return json.dumps(Markup.escape(render_template("ujicoba.html")))
    #return json.dumps(posts)


@app.route("/ujiTampilan")
def ujiTampilan():
    return render_template("component/body/home.html")

with app.test_request_context():
    print(url_for('show_post',username="John Cena"))
    print(url_for('about'))

if __name__ == '__main__':
    app.run(debug=True)
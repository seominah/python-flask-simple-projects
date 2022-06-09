from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.post


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/post/write', methods=['GET'])
def write_get():
    return render_template('post-view.html')

@app.route('/post/write/<int:num>', methods=['GET', 'POST'])
def post_get_one(num):
    if request.method == 'GET':
        post = db.post.find_one({'num': num})
        return render_template('update-view.html', post = post)
    else:
        post = db.post.find_one({'num': num})
        title_receive = request.form['title_give']
        content_receive = request.form['content_give']
        db.post.update_one({'num':num}, {'$set':{'title': title_receive, 'content': content_receive}})
        return jsonify({'msg': '수정완료!'})

@app.route('/post', methods=['POST'])
def post_post():
    title_receive = request.form['title_give']
    writer_receive = request.form['writer_give']
    content_receive = request.form['content_give']

    post_list = list(db.post.find({}, {'_id': False}))
    count = len(post_list) + 1

    doc = {
        'num': count,
        'title': title_receive,
        'writer': writer_receive,
        'content': content_receive
    }

    db.post.insert_one(doc)
    return jsonify({'msg': '게시글 등록 완료!'})

@app.route('/post', methods=['GET'])
def post_get():
    post_list = list(db.post.find({}, {'_id': False}))
    return jsonify({'posts': post_list})

@app.route('/post/delete', methods=['POST'])
def post_delete():
    num_receive = request.form['num_give']
    db.post.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '게시글 삭제 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)

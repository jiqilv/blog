from flask import Flask, render_template, request, redirect, url_for
from flask import session
app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 将最大请求大小设置为16MB
# 全局变量，用于存储用户输入的文本数据
text_data = ''
# 在全局变量中定义一个用户名和密码
USERNAME = '114514'
PASSWORD = '114514'
app.secret_key = '114514'


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error_msg = 'Invalid username or password'
            return render_template('login.html', error=error_msg)
    else:
        return render_template('login.html')


@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        global text_data
        return render_template('index.html', text_data=text_data)


@app.route('/save_text', methods=['POST'])
def save_text():
    global text_data
    new_post = {}
    new_post['author'] = USERNAME
    new_post['message'] = request.form['text']
    if 'posts' not in session:
        session['posts'] = []
    session['posts'].append(new_post)
    text_data += '{}: {}\n'.format(new_post['author'], new_post['message'])  # 更新全局变量
    return redirect(url_for('show_text'))


@app.route('/show_text')
def show_text():
    return render_template('show_text.html', text_data=text_data)


@app.route('/return_home')
def return_home():
    if session.get('logged_in'):
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()

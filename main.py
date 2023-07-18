from flask import Flask, request, make_response, redirect, render_template

todos = ['TODO 1', 'TODO 2', 'TODO 3']


app = Flask(__name__)


@app.route('/')
def index():
    """
        Gets the user IP and save it on a cookie and redirects the user to 'hello'
    """
    user_ip = request.remote_addr
    
    response = make_response(redirect('hello'))
    response.set_cookie('user_ip',user_ip)

    return response


@app.route('/hello')
def hello():
    """
        Gets the cookie user_ip's value and render the template 'hello.html'
    """
    user_ip = request.cookies.get('user_ip')
    context = {'user_ip' : user_ip, 
               'todos' : todos}
    return render_template('hello.html', **context)

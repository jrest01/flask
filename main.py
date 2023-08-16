from flask import  request, make_response, redirect, render_template, session, url_for, flash
import unittest

from app import create_app
from app.forms import LoginForm

from app.firestore_service import get_users, get_todos

app = create_app()
todos = ['Estudiar', 'Trabajar', 'Ir al gimnasio']


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', error=error)


@app.route('/')
def index():
    """
        Gets the user IP and save it on a cookie and redirects the user to 'hello'
    """
    user_ip = request.remote_addr
    
    response = make_response(redirect('hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello', methods=['GET'])
def hello():
    """
        Gets the cookie user_ip's value and render the template 'hello.html'
    """
    user_ip = session.get('user_ip')
    username = session.get('username')

    context = {'user_ip' : user_ip, 
               'todos' : get_todos(username),
               'username' : username           
    }

    users = get_users()

    for user in users:
        print(user.id)
        print(user.to_dict()['password'])

    return render_template('hello.html', **context)



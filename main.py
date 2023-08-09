from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap4
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import unittest



app = Flask(__name__)
bootstrap = Bootstrap4(app)

app.config['SECRET_KEY'] = 'SUPER SECRET'

todos = ['Estudiar', 'Trabajar', 'Ir al gimnasio']


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


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


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    """
        Gets the cookie user_ip's value and render the template 'hello.html'
    """
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    username = session.get('username')

    context = {'user_ip' : user_ip, 
               'todos' : todos,
               'login_form' : login_form,
               'username' : username           
    }

    if request.method == 'POST':
        

        username = login_form.username.data
        session['username'] = username
        flash('Username succesfull registred')
        return redirect(url_for('index'))

    return render_template('hello.html', **context)



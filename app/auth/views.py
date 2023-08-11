from . import auth
from app.forms import LoginForm
from flask import render_template, request, session, url_for, flash, redirect

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form' : login_form
    }

    if request.method == 'POST':   
        username = login_form.username.data
        session['username'] = username
        flash('Username succesfull registred')
        return redirect(url_for('index'))
    return render_template('login.html', **context)
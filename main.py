import unittest
from flask import  request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user
from app import create_app
from app.forms import TodoForm, TodoDeleteForm, TodoUpdateForm

from app.firestore_service import get_todos, todo_put, todo_delete, todo_update

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


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    """
        Gets the cookie user_ip's value and render the template 'hello.html'
    """
    user_ip = session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()
    todo_delete_form = TodoDeleteForm()
    todo_update_form = TodoUpdateForm()

    context = {'user_ip' : user_ip, 
               'todos' : get_todos(username),
               'username' : username,
               'todo_form' : todo_form,
               'todo_delete_form' : todo_delete_form,
               'todo_update_form' : todo_update_form,
    }

    if request.method == 'POST':
        todo_put(username, todo_form.description.data)

        flash('Task Added Succesfully')
        return redirect(url_for('hello'))

    return render_template('hello.html', **context)


@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    todo_delete(user_id, todo_id)
    
    return redirect(url_for('hello'))

@app.route('/todos/update/<todo_id>/<int:done>', methods = ['POST'])
def update(todo_id, done):
    user_id = current_user.id
    print('DONE', done)
    todo_update(user_id, todo_id, done)

    return redirect(url_for('hello'))

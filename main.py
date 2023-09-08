import unittest
from flask import  request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user
from app import create_app
from app.forms import TodoForm, TodoDeleteForm, TodoStatusUpdate, TodoUpdateButton, TodoUpdateForm

from app.firestore_service import get_todos, todo_put, todo_delete, todo_update, get_todo, todo_update_description

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
    todo_status_update = TodoStatusUpdate()
    todo_update_button = TodoUpdateButton()

    context = {'user_ip' : user_ip, 
               'todos' : get_todos(username),
               'username' : username,
               'todo_form' : todo_form,
               'todo_delete_form' : todo_delete_form,
               'todo_status_update' : todo_status_update,
               'todo_update_button' : todo_update_button,
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
def status(todo_id, done):
    user_id = current_user.id
    print('DONE', done)
    todo_update(user_id, todo_id, done)

    return redirect(url_for('hello'))

@app.route('/setcookie/<todo_id>', methods = ['POST', 'GET'])
def setcookie(todo_id):
   
   resp = make_response( redirect(url_for('updates22')))
   resp.set_cookie('todo_id', todo_id)
   
   return resp

def getcookie():
    todo_id = request.cookies.get('todo_id')
    return todo_id


@app.route('/delete_cookie', methods = ['GET','POST'])
def delete_cookie():
    res = make_response(redirect('hello'))
    res.set_cookie(key='todo_id', expires=0, max_age=0, value='0')
    return res
    

@app.route('/todos/updates/<todo_id>', methods = ['GET','POST'])
#Reemplazar por un controlador que almacene el id en una cookie y redirija a otro controlador que admita el método POST
def updates(todo_id): 
    args=[todo_id]
    return redirect(url_for('setcookie', todo_id=todo_id))
    


@app.route('/todos/updates22', methods = ['GET','POST'])
def updates22():
    user_id = current_user.id
    todo_id = getcookie()
    todo = get_todo(user_id, todo_id)
    todo_update_form = TodoUpdateForm()
    todo_doc = todo.to_dict()
    context = {
        'user_id' : user_id,
        'todo' : todo,
        'todo_update_form': todo_update_form,
        'todo_doc' : todo_doc,
        'todo_id' : todo_id,
    }

    if request.method == 'POST':
        context['new_description'] = todo_update_form.description.data
        print('-*-*'*10)
        print(todo_update_form.description.data)

        return redirect(url_for('update_description', todo_id=todo_id, new_description=todo_update_form.description.data))
    
    return render_template('update.html', **context)




@app.route('/todos/update_description/<todo_id>/<new_description>', methods = ['POST', 'GET'])
def update_description(todo_id, new_description):
    user = current_user.id
    
    todo_update_description(todo_id=todo_id, user_id=user, description=new_description)
    delete_cookie()
    return redirect(url_for('delete_cookie'))

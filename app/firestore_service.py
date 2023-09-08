import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

project_id = 'flask-to-do-list-platzi'

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential, {
    'projectId' : project_id
})

db = firestore.client()


def get_users():
    return db.collection('users').get()


def get_user(user_id):
    return db.collection('users').document(user_id).get()


def user_put(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({'password' : user_data.password})


def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()


def get_todo(user_id, todo_id):
    todo_ref = _get_todo_ref(user_id, todo_id)
    # return todo_ref.get()
    return db.collection('users').document(user_id).collection('todos').document(todo_id).get()


def todo_put(user_id, todo_description):
    todos_ref = db.collection('users').document(user_id).collection('todos')
    todos_ref.add({'description' : todo_description, 'done' : False})


def todo_delete(user_id, todo_id):
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.delete()
    

def todo_update(user_id, todo_id, done):
    todo_done = not bool(done)
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.update({'done': todo_done})
    

def todo_update_description(user_id, todo_id, description):
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.update({'description': description})
    

def _get_todo_ref(user_id, todo_id):
    return db.collection('users').document(user_id).collection('todos').document(todo_id)
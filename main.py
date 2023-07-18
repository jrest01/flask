from flask import Flask, request, make_response, redirect



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
        Gets the cookie user_ip's value
    """
    user_ip = request.cookies.get('user_ip')
    return f"Hello, for IP address is {user_ip}"

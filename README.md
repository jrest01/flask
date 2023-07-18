# Flask Project

Follow the next terminal commands:

```sh
# Create the venv
python -m venv flask-env

# Activate the venv
.\flask-env\Scripts\activate
pip3 install -r requirements.txt

# Declare the variable FLASK_APP (Windows):
set FLASK_APP=main.py

# Declare the variable FLASK_ENV (Windows):
set “FLASK_ENV=development”

#Activate the debug mode:
set FLASK_DEBUG=1

# Run the flask server

flask run

OR

py main.py

# Navigate to:
http://127.0.0.1:5000/flask
```
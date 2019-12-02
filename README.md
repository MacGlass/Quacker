"Quacker" is a twitter clone!

To get "Quacker" started, run the following commands in your terminal: 

1. Create the Python virtual environment:

$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt


2. Set up the database:

(venv) $ createdb warbler
(venv) $ python seed.py


3. Start the server:

(venv) $ flask run



Testing:  

To run a file containing unittests, you can run the command: FLASK_ENV=production python -m unittest <name-of-python-file>


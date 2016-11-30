#!/usr/bin/python
from app import app
app.secret_key = 'password'
app.run(host='0.0.0.0', debug=True)

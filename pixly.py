import os
from flask import Flask

AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']

print(AWS_ACCESS_KEY, AWS_SECRET_KEY);
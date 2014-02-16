#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kuo
#
# Created:     15/02/2014
# Copyright:   (c) kuo 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from flask import Flask

app = Flask(__name__)
from app import views
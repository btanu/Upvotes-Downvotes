from . import main  #import bluerint instance main
from flask import render_template

@main.app_errorhandler(404)
def four_Ow_four(error):
    
    return render_template('fourOwfour.html'), 404
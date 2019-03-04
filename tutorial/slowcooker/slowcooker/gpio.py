import functools
import RPi.GPIO as GPIO
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from slowcooker.db import get_db

bp = Blueprint('gpio', __name__, url_prefix='/gpio')

@bp.route('/test', methods=('POST', 'GET'))
def gpio():
    #if request.method == 'POST':
        #turn on gpio
        return render_template('gpio/test.html')

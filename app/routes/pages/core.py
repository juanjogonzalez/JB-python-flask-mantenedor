from flask import Blueprint, render_template
from flask_login import login_required

core_bp = Blueprint('core', __name__, url_prefix='/')

@core_bp.route('/')
@login_required
def home_route():

    return render_template('pages/home.html')
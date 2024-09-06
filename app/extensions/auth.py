from flask_login import LoginManager

from app.extensions.db import db

#Cargar modelo del usuario
from app.models.auth import User

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login" #hay que crear esta vista
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    try:
        #Query...
        return User.query.filter_by(id = user_id).first()
    except:
        return None
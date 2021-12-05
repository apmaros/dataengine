from flask import Blueprint

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    return 'Login'


@auth_bp.route('/logout')
def logout():
    return 'Logout'

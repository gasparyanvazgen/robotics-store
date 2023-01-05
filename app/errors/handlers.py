from flask import redirect, url_for

def handle_forbidden(error):
    return redirect(url_for('main.login'))

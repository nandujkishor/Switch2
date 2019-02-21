from functools import wraps
from config import Config
from flask_login import current_user
from flask import redirect, url_for

def access(team, level):
    def ac_level_required(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            print(current_user.super(), current_user.data.get('fname'))
            if current_user.super():
                print("Superuser in charge, yeah!")
                return func(*args, **kwargs)
            if current_user.staff == []:
                print("Unauthorized access")
                return redirect(url_for('index'))
            for s in staff:
                if s.get('team') == team:
                    if s.get('level') >= level:
                        return func(*args, **kwargs)
                    else:
                        return redirect(url_for('index'))
            else:
                print("No access for current user")
                return redirect(url_for('index'))
            return func(*args, **kwargs)
        return decorated_view
    return ac_level_required

def get_user_ip(request):
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        s = request.environ['REMOTE_ADDR']
    else:
        s = request.environ['HTTP_X_FORWARDED_FOR']
    return s

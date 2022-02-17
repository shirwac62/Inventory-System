from flask import url_for, session
from flask_login import logout_user
from werkzeug.utils import redirect
from utility.mkblueprint import ProjectBlueprint
blueprint = ProjectBlueprint('/logout', __name__)


@blueprint.route(blueprint.url)
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('/.login'))

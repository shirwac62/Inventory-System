from flask import render_template

from utility.mkblueprint import ProjectBlueprint

blueprint = ProjectBlueprint('home', __name__)


@blueprint.route(blueprint.url, methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='Home')

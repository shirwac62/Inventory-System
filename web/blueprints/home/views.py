from flask import render_template

from utility import blueprint
from utility.mkblueprint import ProjectBlueprint

blueprint = ProjectBlueprint('home', __name__)


@blueprint.route(blueprint.url, methods=['GET','POST'])
# @app.route("/home")
def home():
    # conn = mysql.connect()
    # cursor = conn.cursor()
    # cursor.execute("SELECT COUNT(product_id) FROM product WHERE user_id="+ str(current_user.user_id) +"")
    # products = cursor.fetchone()
    # cursor.execute("SELECT COUNT(location_id) FROM location")
    # locations = cursor.fetchone()
    # cursor.execute("SELECT COUNT(*) FROM productmovement WHERE user_id="+ str(current_user.user_id) +"")
    # movements = cursor.fetchone()
    # sales = 5
    # return render_template('home.html', title='Home', products=products[0], locations=locations[0], sales=sales, movements=movements[0])
    return render_template('home.html', title='Home')

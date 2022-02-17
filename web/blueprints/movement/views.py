from flask import render_template, url_for, flash
from flask_login import login_required
from werkzeug.utils import redirect

from utility.blueprint import ProjectBlueprint
from web.blueprints.movement.forms import AddMovement
from web.blueprints.movement.model import Movement
from web.blueprints.product.model import Product
from web.extensions import save_to_db

blueprint: ProjectBlueprint = ProjectBlueprint("movement", __name__)


@blueprint.route(blueprint.url + "/add/<movement_id>", methods=['GET', 'POST'])
@login_required
def add_movement(movement_id):
    data = Product.query.get(movement_id)
    form = AddMovement()
    if form.validate_on_submit():
        data = Movement()
        form.populate_obj(data)
        save_to_db(data)
        flash('Your Movement has been created', 'success')
        return redirect(url_for('movement.add_movement'))
    return render_template('product/index.html', title='movement', form=form)


@blueprint.route(blueprint.url)
@login_required
def product_movement():
    movements = Movement.query.all()
    return render_template('movement/index.html', title='Movement', movements=movements)

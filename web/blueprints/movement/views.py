from flask import render_template, url_for, flash, request, jsonify
from flask_login import login_required
from werkzeug.utils import redirect

from utility.blueprint import ProjectBlueprint
from web.blueprints.movement.forms import AddMovement
from web.blueprints.movement.model import Movement
from web.blueprints.product.forms import AddProduct
from web.blueprints.product.model import Product
from web.extensions import save_to_db, delete, db

blueprint: ProjectBlueprint = ProjectBlueprint("movement", __name__)


@blueprint.route(blueprint.url + "/add/<product_id>", methods=['GET', 'POST'])
@login_required
def add_movement(product_id):
    data = Product.query.get(product_id)
    form = AddProduct(obj=data)
    mv_data = Movement()
    if form.validate_on_submit():
        mv_data.name = form.productname.data
        mv_data.from_location = form.location.data
        mv_data.to_location = request.form["to_location"]
        mv_data.quantity = form.quantity.data
        save_to_db(mv_data)
        delete(data)
        flash('Your Movement has been created', 'success')
        return redirect(url_for('movement.product_movement'))
    return render_template('movement/add.html', title='movement', form=form, product=Product)


@blueprint.route(blueprint.url + "/edit/<movement_id>", methods=['GET', 'POST'])
@login_required
def edit_movement(movement_id):
    data = Movement.query.get(movement_id)
    form = AddMovement(obj=data)
    # mv_data = Movement()
    if form.validate_on_submit():
        data.name = form.name.data
        data.from_location = form.from_location.data
        data.to_location = request.form["to_location"]
        data.quantity = form.quantity.data
        save_to_db(data)
        flash('Your Movement has been Updated', 'success')
        return redirect(url_for('movement.product_movement'))
    return render_template('movement/edit.html', title='edit_movement', form=form, movement=Movement)


@blueprint.route(blueprint.url + "/delete/<movement_id>", methods=['GET', 'POST'])
@login_required
def delete_movement(movement_id):
    data = Movement.query.get(movement_id)
    form = AddMovement(obj=data)
    if form.validate_on_submit():
        delete(data)
        flash('Your Movement has been Deleted', 'success')
        return redirect(url_for('movement.product_movement'))
    return render_template('movement/delete.html', title="delete_product", form=form, product=Product, data=data)


@blueprint.route(blueprint.url + '/api')
def pub_index():
    print("pub_index  pub_index")
    start = int(request.args.get('start', 0))
    search = request.args.get('search[value]', '')
    print("search: ", search)
    length = int(request.args.get('length', 5))
    if length and int(length) == -1:
        length = db.session.query(Movement.movement_id).count()
    page = (int(start) + int(length)) / int(length)
    data_list = Movement.query.filter(Movement.name.ilike('%' + search + '%')).paginate(page, length, True)
    data = []
    for b in data_list.items:
        row = [b.movement_id, b.name, b.from_location, b.to_location, b.quantity,
               '<a href="{0}"><i class="fa-solid fa-pen-to-square"></i></a>'.format(url_for('movement.edit_movement', movement_id=b.movement_id))+ " " +\
               '<a href="{0}"><i class="fa-solid fa-trash"></i></a>'.format(url_for('movement.delete_movement', movement_id=b.movement_id))]
        data += [row]
    print("data_list.total: ", data_list.total)
    return jsonify({'data': data, "recordsTotal": data_list.total,
                    "recordsFiltered": data_list.total})


@blueprint.route(blueprint.url)
@login_required
def product_movement():
    movements = Movement.query.all()
    return render_template('movement/index.html', title='Movement', movements=movements)

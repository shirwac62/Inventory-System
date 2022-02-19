from flask import render_template, flash, url_for, request, jsonify
from flask_login import login_required
from werkzeug.utils import redirect

from utility.blueprint import ProjectBlueprint
from web.blueprints.product.forms import AddProduct
from web.blueprints.product.model import Product
from web.extensions import save_to_db, db, delete

blueprint = ProjectBlueprint("product", __name__)


@blueprint.route(blueprint.url + "/add", methods=['GET', 'POST'])
@login_required
def add_product():
    form = AddProduct()
    if form.validate_on_submit():
        data = Product()
        form.populate_obj(data)
        save_to_db(data)
        flash('Your product has been created', 'success')
        return redirect(url_for('product.product'))
    return render_template('product/add.html', title='product', form=form)


@blueprint.route(blueprint.url + "/edit/<product_id>", methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    data = Product.query.get(product_id)
    form = AddProduct(obj=data)
    if form.validate_on_submit():
        data.productname = form.productname.data
        data.location = form.location.data
        data.quantity = form.quantity.data
        save_to_db(data)
        flash('Your product has been Updated', 'success')
        return redirect(url_for('product.product'))
    return render_template('product/edit.html', title='edit_product', form=form, product=Product)


@blueprint.route(blueprint.url + "/delete/<product_id>", methods=['GET', 'POST'])
@login_required
def delete_product(product_id):
    data = Product.query.get(product_id)
    form = AddProduct(obj=data)
    if form.validate_on_submit():
        delete(data)
        flash('Your product has been Deleted', 'success')
        return redirect(url_for('product.product'))
    return render_template('product/delete.html', title="delete_product", form=form, product=Product, data=data)


@blueprint.route(blueprint.url + '/api')
def pub_index():
    print("pub_index  pub_index")
    start = int(request.args.get('start', 0))
    search = request.args.get('search[value]', '')
    print("search: ", search)
    length = int(request.args.get('length', 5))
    if length and int(length) == -1:
        length = db.session.query(Product.product_id).count()
    page = (int(start) + int(length)) / int(length)
    data_list = Product.query.filter(Product.productname.ilike('%' + search + '%')).paginate(page, length, True)
    data = []
    for b in data_list.items:
        row = [b.product_id, b.productname, b.location,
               '<a href="{0}" style=" text-decoration: none">Move</a>'.format( url_for('movement.add_movement', product_id=b.product_id)),\
               '<a href="{0}"><i class="fa-solid fa-pen-to-square"></i></a>'.format( url_for('product.edit_product', product_id=b.product_id))+ " " +\
               '<a href="{0}"><i class="fa-solid fa-trash"></i></a>'.format( url_for('product.delete_product', product_id=b.product_id))]
        data += [row]
    print("data_list.total: ", data_list.total)
    return jsonify({'data': data, "recordsTotal": data_list.total,
                    "recordsFiltered": data_list.total})


@blueprint.route(blueprint.url)
@login_required
def product():
    products = Product.query.all()
    return render_template('product/index.html', title='product', products=products)

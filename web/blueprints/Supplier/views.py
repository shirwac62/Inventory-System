from flask import render_template, flash, url_for, request, jsonify
from flask_login import login_required
from werkzeug.utils import redirect

from utility.mkblueprint import ProjectBlueprint
from web.blueprints.Supplier.forms import SupplierForm
from web.blueprints.Supplier.models import Supplier
from web.extensions import save_to_db, delete, db

blueprint = ProjectBlueprint("supplier", __name__)


@blueprint.route(blueprint.url + "/add", methods=['GET', 'POST'])
@login_required
def add_supplier():
    form = SupplierForm()
    if form.validate_on_submit():
        data = Supplier()
        form.populate_obj(data)
        save_to_db(data)
        flash('Your Supplier has been created', 'success')
        return redirect(url_for('supplier.supplier'))
    return render_template('Supplier/add.html', title='Supplier', form=form)


@blueprint.route(blueprint.url + "/edit/<Supplier_Id>", methods=['GET', 'POST'])
@login_required
def edit_supplier(Supplier_Id):
    data = Supplier.query.get(Supplier_Id)
    form = SupplierForm(obj=data)
    if form.validate_on_submit():
        data.First_Name = form.First_Name.data
        data.Last_Name = form.Last_Name.data
        data.Address = form.Address.data
        data.Supplier_Status = form.Supplier_Status.data
        data.Contact_Number = form.Contact_Number.data
        save_to_db(data)
        flash('Your Supplier has been Updated', 'success')
        return redirect(url_for('supplier.supplier'))
    return render_template('Supplier/edit.html', title='edit_supplier', form=form, supplier=Supplier)


@blueprint.route(blueprint.url + "/delete/<Supplier_Id>", methods=['GET', 'POST'])
@login_required
def delete_supplier(Supplier_Id):
    data = Supplier.query.get(Supplier_Id)
    form = SupplierForm(obj=data)
    if form.validate_on_submit():
        delete(data)
        flash('Your Supplier has been Deleted', 'success')
        return redirect(url_for('supplier.supplier'))
    return render_template('Supplier/delete.html', title="delete_supplier", form=form, supplier=Supplier, data=data)


@blueprint.route(blueprint.url + '/api')
def pub_index():
    print("pub_index  pub_index")
    start = int(request.args.get('start', 0))
    search = request.args.get('search[value]', '')
    print("search: ", search)
    length = int(request.args.get('length', 5))
    if length and int(length) == -1:
        length = db.session.query(Supplier.Supplier_Id).count()
    page = (int(start) + int(length)) / int(length)
    data_list = Supplier.query.filter(Supplier.First_Name.ilike('%' + search + '%')).paginate(page, length, True)
    data = []
    for b in data_list.items:
        row = [b.Supplier_Id, b.First_Name, b.Last_Name, b.Address, b.Supplier_Status, b.Contact_Number,
               '<a href="{0}"><i class="fa-solid fa-pen-to-square"></i></a>'.format(
                   url_for('supplier.edit_supplier', Supplier_Id=b.Supplier_Id)) + " " + \
               '<a href="{0}"><i class="fa-solid fa-trash"></i></a>'.format(
                   url_for('supplier.delete_supplier', Supplier_Id=b.Supplier_Id))]
        data += [row]
    print("data_list.total: ", data_list.total)
    return jsonify({'data': data, "recordsTotal": data_list.total,
                    "recordsFiltered": data_list.total})


@blueprint.route(blueprint.url)
@login_required
def supplier():
    suppliers = Supplier.query.all()
    return render_template('Supplier/index.html', title='Supplier', suppliers=suppliers)

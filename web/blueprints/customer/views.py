from flask import render_template, flash, url_for, request, jsonify
from flask_login import login_required
from werkzeug.utils import redirect

from utility.mkblueprint import ProjectBlueprint
from web.blueprints.customer.forms import CustomerForm
from web.blueprints.customer.models import Customer
from web.extensions import save_to_db, db, delete

blueprint = ProjectBlueprint("customer", __name__)


@blueprint.route(blueprint.url + "/add", methods=['GET', 'POST'])
@login_required
def add_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        data = Customer()
        form.populate_obj(data)
        save_to_db(data)
        flash('Your Customer has been created', 'success')
        return redirect(url_for('customer.customer'))
    return render_template('customer/add.html', title='product', form=form)


@blueprint.route(blueprint.url + "/edit/<Customer_Id>", methods=['GET', 'POST'])
@login_required
def edit_customer(Customer_Id):
    data = Customer.query.get(Customer_Id)
    form = CustomerForm(obj=data)
    if form.validate_on_submit():
        data.First_Name = form.First_Name.data
        data.Last_Name = form.Last_Name.data
        data.Address = form.Address.data
        data.Contact_Number = form.Contact_Number.data
        save_to_db(data)
        flash('Your Customer has been Updated', 'success')
        return redirect(url_for('customer.customer'))
    return render_template('customer/edit.html', title='edit_customer', form=form, customer=Customer)


@blueprint.route(blueprint.url + "/delete/<Customer_Id>", methods=['GET', 'POST'])
@login_required
def delete_customer(Customer_Id):
    data = Customer.query.get(Customer_Id)
    form = CustomerForm(obj=data)
    if form.validate_on_submit():
        delete(data)
        flash('Your Customer has been Deleted', 'success')
        return redirect(url_for('customer.customer'))
    return render_template('customer/delete.html', title="delete_customer", form=form, customer=Customer, data=data)


@blueprint.route(blueprint.url + '/api')
def pub_index():
    print("pub_index  pub_index")
    start = int(request.args.get('start', 0))
    search = request.args.get('search[value]', '')
    print("search: ", search)
    length = int(request.args.get('length', 5))
    if length and int(length) == -1:
        length = db.session.query(Customer.Customer_Id).count()
    page = (int(start) + int(length)) / int(length)
    data_list = Customer.query.filter(Customer.First_Name.ilike('%' + search + '%')).paginate(page, length, True)
    data = []
    for b in data_list.items:
        row = [b.Customer_Id, b.First_Name, b.Last_Name, b.Address, b.Contact_Number,
               '<a href="{0}"><i class="fa-solid fa-pen-to-square"></i></a>'.format(url_for('customer.edit_customer', Customer_Id=b.Customer_Id))+ " " +\
               '<a href="{0}"><i class="fa-solid fa-trash"></i></a>'.format(url_for('customer.delete_customer', Customer_Id=b.Customer_Id))]
        data += [row]
    print("data_list.total: ", data_list.total)
    return jsonify({'data': data, "recordsTotal": data_list.total,
                    "recordsFiltered": data_list.total})


@blueprint.route(blueprint.url)
@login_required
def customer():
    customers = Customer.query.all()
    return render_template('customer/index.html', title='Customer', customers=customers)

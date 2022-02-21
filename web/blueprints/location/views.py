from flask import flash, url_for, render_template, jsonify, request
from flask_login import login_required
from sqlalchemy.orm import session
from werkzeug.utils import redirect

from utility.mkblueprint import ProjectBlueprint
from web.blueprints.location.forms import AddLocation
from web.blueprints.location.model import location
from web.extensions import save_to_db, db, delete

# blueprint: ProjectBlueprint = ProjectBlueprint("/add_location", __name__)
blueprint: ProjectBlueprint = ProjectBlueprint("location", __name__)


@blueprint.route(blueprint.url + "/add", methods=['GET', 'POST'])
@login_required
def add_location():
    form = AddLocation()
    if form.validate_on_submit():
        data = location()
        form.populate_obj(data)
        # data.save()
        save_to_db(data)
        flash('Location Added', 'success')
        return redirect(url_for('location.viewlocation'))
    return render_template('location/add.html', title='Location', form=form)


@blueprint.route(blueprint.url + "/edit/<location_id>", methods=['GET', 'POST'])
@login_required
def edit_location(location_id):
    data = location.query.get(location_id)
    form = AddLocation(obj=data)
    if form.validate_on_submit():
        data.name = form.name.data
        data.description = form.description.data
        data.rent = form.rent.data
        flash('Updated!', 'success')
        save_to_db(data)
        return redirect(url_for('location.viewlocation'))
    # return render_template('edit.html', title='Location', form=form)
    return render_template('location/edit.html', title='Location', form=form, locations=location)

@blueprint.route(blueprint.url + "/delete/<location_id>", methods=['GET', 'POST'])
@login_required
def delete_location(location_id):
    data = location.query.get(location_id)
    form = AddLocation(obj=data)
    if form.validate_on_submit():
        delete(data)
        # data.name = form.name.data
        # data.description = form.description.data
        # data.rent = form.rent.data
        flash('Your product has been Deleted', 'success')
        return redirect(url_for('location.viewlocation'))
    return render_template('location/delete.html', title='delete_Location', form=form, locations=location,data=data)


@blueprint.route(blueprint.url + '/api')
def pub_index():
    print("pub_index  pub_index")
    start = int(request.args.get('start', 0))
    search = request.args.get('search[value]', '')
    print("search: ", search)
    length = int(request.args.get('length', 5))
    if length and int(length) == -1:
        length = db.session.query(location.location_id).count()
    page = (int(start) + int(length)) / int(length)
    data_list = location.query.filter(location.name.ilike('%' + search + '%')).paginate(page, length, True)
    data = []
    for b in data_list.items:
        row = [b.location_id, b.name, b.description, b.rent,
               # '<a href="{0}">Edit</a>'.format(url_for('location.edit_location', location_id=b.location_id))
               '<a href="{0}"><i class="fa-solid fa-pen-to-square"></i></a>'.format(url_for('location.edit_location', location_id=b.location_id)) + "  " + \
               '<a href="{0}"><i class="fa-solid fa-trash"></i></a>'.format(url_for('location.delete_location', location_id=b.location_id))]

        data += [row]
    print("data_list.total: ", data_list.total)
    return jsonify({'data': data, "recordsTotal": data_list.total,
                    "recordsFiltered": data_list.total})


@blueprint.route(blueprint.url)
@login_required
def viewlocation():
    locations = location.query.all()
    return render_template('location/index.html', title='Location', locations=locations)

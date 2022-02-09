import datetime
import os

from flask import request, current_app
from flask_login import current_user
from sqlalchemy import text, and_

from utility.util_data import util_copy
from utility.util_default import get_user_branches
from web.extensions import db
from flask import Blueprint


class ProjectBlueprint(Blueprint):
    def __init__(self, blueprint, name):
        super().__init__(blueprint, name, template_folder='templates')

    @property
    def render(self):
        return {
            "title": self.title,
            "url": self.url,
            "blueprint": self.blueprint,
        }

    @property
    def title(self):
        return self.name.replace("_", " ").title()

    @property
    def url(self):
        return '/' + self.name.replace("_", "-")

    @property
    def blueprint(self):
        return self.name.replace(" ", "_").lower()

    def __repr__(self):
        return self.blueprint


def get_one(model, search=None):
    if search is None:
        search = []
    if hasattr(model, 'branch_id'):
        search.append(model.branch_id.in_(get_user_branches()))
    search = and_(*search)
    return model.query.filter(search).first()


def get_all(model, search=None):
    if search is None:
        search = []
    # if hasattr(model, 'branch_id'):
    #     search.append(model.branch_id.in_(get_user_branches()))
    search = and_(*search)
    return model.query.filter(search).all()


def cause_list(model, search=None, orders=None, field='created_on', direction='desc'):
    print(request.args)
    if search is None:
        search = []
    model_columns = int(request.args.get("pram_length", 1))
    for i in range(0, model_columns):
        d = model.filter_column(i, request.args.get("pram_" + str(i), ''))
        if d is not None:
            search.append(d)
    d = model.filter_column(-1, request.args.get("all", ''))
    if d is not None:
        search.append(d)
    start = request.args.get('start', 0)
    length = request.args.get('length', -1)
    order_values = '{0} {1}'.format(field, direction)
    if length and int(length) == -1:
        length = db.session.query(model.id).count()
    page = (int(start) + int(length)) / int(length)
    search = and_(*search)
    data_list = model.query.filter(search)
    if orders:
        data_list = data_list.order_by(*orders).paginate(page, int(length), True)
    else:
        data_list = data_list.order_by(text(order_values)).paginate(page, int(length), True)
    return data_list


def get_request_data(pram_columns):
    data = {}
    for i in range(0, len(pram_columns)):
        value = request.args.get("pram_" + str(i), '')
        if value == '' or value == '0':
            value = None
        data[pram_columns[i]] = value
    return data


def get_request_prams(pram_columns):
    data = []
    for i in range(0, len(pram_columns)):
        print(pram_columns[i])
        pram_columns[i]['value'] = request.args.get("pram_" + str(i), '')
        value = request.args.get(pram_columns[i]['name'], '')
        if value:
            pram_columns[i]['value'] = value
        data.append(pram_columns[i]['value'])
    return pram_columns, data


def get_data(form, pram_columns):
    data = {}
    for i in range(0, len(pram_columns)):
        data["pram_" + str(i)] = form[pram_columns[i]].data
    return data


def get_blueprint_actions(blueprint, rote='index'):
    actions = ''
    if rote == 'index':
        actions = get_url_actions(actions, blueprint, 'edit', '/URL', "fa fa-edit me-2")
        actions = get_url_actions(actions, blueprint, 'detail', '?val=URL', "fa fa-info-circle me-2")
        actions = get_url_actions(actions, blueprint, 'delete', '/URL', "fas fa-trash text-danger fa-1x me-2")
    else:
        actions = get_url_actions(actions, blueprint, 'detail_edit', '/URL', "fa fa-edit m-r-10")
        actions = get_url_actions(actions, blueprint, 'detail_delete', '/URL', "fas fa-trash text-danger m-r-10")
    # edit_blue_print = current_user.has_permission(blueprint + '.edit')
    # if edit_blue_print:
    #     actions += '<span><a href=/' + blueprint + '/edit/URL><i class="fa fa-edit m-r-10"></i></a></span>'
    # actions = get_url_actions(actions, blueprint,  'delete')
    # print_blue_print = current_user.has_permission(blueprint + '.print_document')
    # if print_blue_print:
    #     if url_for(blueprint + '.print_document', val='val'):
    #         actions += '<span><a href=/' + blueprint + '/print/URL><i class="fa fa-print m-r-10"></i></a></span>'
    # detail_blue_print = current_user.has_permission(blueprint + '.detail')
    # if detail_blue_print:
    #     try:
    #         if url_for(blueprint + '.detail', val='val'):
    #             actions += '<span><a href=/' + blueprint + '/detail?val=URL><i class="fa fa-info-circle m-r-10"></i></a></span>'
    #     except Exception as e:
    #         pass
    #         # print(e)
    return actions


def get_url_actions(actions, blueprint, rote, url, icon):
    from flask import url_for
    if current_user.has_permission(blueprint + '.' + rote):
        try:
            url_data = url_for(blueprint + '.' + rote, val='val')
            print("url_data: ", url_data)
            if url_for(blueprint + '.' + rote, val='val'):
                actions += '<span><a href=/' + blueprint.replace("_", "-") + '/' + rote.replace("_",
                                                                                                "-") + url + '><i class="' + icon + '"></i></a></span>'
        except Exception as e:
            pass
    return actions


def file_registration(count_no, file, filename, parent_id, path):
    file_extension = "." + str(filename.rsplit('.', 1)[1])
    file_folder_path = os.path.join(current_app.config.get('UPLOAD_FOLDER'))
    if not os.path.isdir(file_folder_path + "/" + path):
        os.makedirs(file_folder_path + "/" + path)
    original_f_name = filename
    extension = file_extension
    filename = str(datetime.datetime.now().strftime('%Y-%m-%d-%H_%M_%S_%f')) + '(' + str(parent_id) + '-' + str(
        count_no) + ')' + filename
    while return_file_BASE_DIR(path + filename):
        filename = str(datetime.datetime.now().strftime('%Y-%m-%d-%H_%M_%S_%f')) + '(' + str(parent_id) + '-' + str(
            count_no) + ')' + filename
        count_no += 1
    path = path + filename
    file_folder_path = file_folder_path + "/" + path
    file.seek(0)
    file.save(file_folder_path)
    size = os.path.getsize(file_folder_path)
    if float(os.path.getsize(file_folder_path)) < 1.0:
        try:
            os.remove(file_folder_path)
        except Exception as e:
            print(e)
    return extension, filename, original_f_name, path, size, count_no


def return_file_BASE_DIR(filename):
    if filename:
        file_folder_path = str(os.path.join(current_app.config.get('UPLOAD_FOLDER')))
        abs_path = os.path.join(file_folder_path, filename)
        if os.path.isfile(abs_path):
            return abs_path
        return False
    return False


def copy_file_to_destination(file_name, destination_folder):
    destination_folder_path = str(os.path.join(current_app.config.get('STATIC_FOLDER'))) + destination_folder
    if not os.path.isdir(destination_folder_path):
        os.makedirs(destination_folder_path)
    util_copy(return_file_BASE_DIR(file_name), destination_folder_path)
    return '/static' + destination_folder + str(file_name.split("/")[1].strip())

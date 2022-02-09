from flask_wtf import FlaskForm
from jsonpickle import json
from wtforms import SelectField, HiddenField, SelectMultipleField, Form

from utility.util_common import get_request_prams


class FilterForm(Form):

    @property
    def prams(self):
        pram_columns = {}
        max_column = 0
        for x in self:
            column = int(x.render_kw['data-column'])
            if max_column < column:
                max_column = column
            pram_columns[column] = {'name': x.name, 'value': ''}
        for i in range(max_column + 1):
            if pram_columns.get(i, 0) == 0:
                pram_columns[i] = {'name': '', 'value': ''}
        data_dict, data = get_request_prams(pram_columns)
        for x in self:
            x.data = data_dict[int(x.render_kw['data-column'])]['value']
        return data


class ModelForm(FlaskForm):
    """
    wtforms_components exposes ModelForm but their ModelForm does not inherit
    from flask_wtf's Form, but instead WTForm's Form.

    However, in order to get CSRF protection handled by default we need to
    inherit from flask_wtf's Form. So let's just copy his class directly.

    We modified it by removing the format argument so that wtforms_component
    uses its own default which is to pass in request.form automatically.
    """

    def __init__(self, obj=None, prefix='', **kwargs):
        FlaskForm.__init__(
            self, obj=obj, prefix=prefix, **kwargs
        )
        self._obj = obj


def choices_from_dict(source, prepend_blank=True):
    """
    Convert a dict to a format that's compatible with WTForm's choices. It also
    optionally prepends a "Please select one..." value.

    Example:
      # Convert this data structure:
      STATUS = OrderedDict([
          ('unread', 'Unread'),
          ('open', 'Open'),
          ('contacted', 'Contacted'),
          ('closed', 'Closed')
      ])

      # Into this:
      choices = [('', 'Please select one...'), ('unread', 'Unread) ...]

    :param source: Input source
    :type source: dict
    :param prepend_blank: An optional blank item
    :type prepend_blank: bool
    :return: list
    """
    choices = []

    if prepend_blank:
        choices.append(('', 'Please select one...'))

    for key, value in source.items():
        pair = (key, value)
        choices.append(pair)

    return choices


def choices_from_list(source, prepend_blank=True):
    """
    Convert a list to a format that's compatible with WTForm's choices. It also
    optionally prepends a "Please select one..." value.

    Example:
      # Convert this data structure:
      TIMEZONES = (
        'Africa/Abidjan',
        'Africa/Accra',
        'Africa/Addis_Ababa'
      )

      # Into this:
      choices = [('', 'Please select one...'),
                 ('Africa/Abidjan', 'Africa/Abidjan) ...]

    :param source: Input source
    :type source: list or tuple
    :param prepend_blank: An optional blank item
    :type prepend_blank: bool
    :return: list
    """
    choices = []

    if prepend_blank:
        choices.append(('', 'Please select one...'))

    for item in source:
        pair = (item, item)
        choices.append(pair)

    return choices


def form_error_log(form):
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            print(fieldName, errorMessages, err)


class ValidatingSelectField(SelectField):
    """
    Attempt to make an open ended select multiple field that can accept dynamic
    choices added by the browser.
    """

    def pre_validate(self, form):
        print("NonValidatingSelectField: ", self.data)
        if not self.data or self.data == 'None':
            print("Show Error: ", self.data)
            raise ValueError(self.gettext("Invalid choice"))


class NonValidatingSelectField(SelectField):
    """
    Attempt to make an open ended select multiple field that can accept dynamic
    choices added by the browser.
    """

    def pre_validate(self, form):
        pass


class NonValidatingSelectMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        pass


class JSONField(HiddenField):
    def _value(self):
        return json.dumps(self.data) if self.data else ''

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = json.loads(valuelist[0])
            except ValueError:
                raise ValueError('This field contains invalid JSON')
        else:
            self.data = None

    def pre_validate(self, form):
        super().pre_validate(form)
        if self.data:
            try:
                json.dumps(self.data)
            except TypeError:
                raise ValueError('This field contains invalid JSON')


class ListCheckForm(ModelForm):
    custom_data = JSONField()

    def __init__(self, *args, **kwargs):
        super(ListCheckForm, self).__init__(*args, **kwargs)

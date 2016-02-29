# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django import forms

logger = logging.getLogger(__name__)


class ExampleForm(forms.Form):
    input = forms.CharField(label="Some input here")

    def __init__(self, *args, **kwargs):
        super(ExampleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-8'

        self.helper.layout = Layout(
            'input',
            Submit('submit', 'Submit this input', css_class='btn-lg btn-block'),
        )

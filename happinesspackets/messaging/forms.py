# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML
from django import forms
from django.core.urlresolvers import reverse

from .models import Message, BlacklistedEmail

logger = logging.getLogger(__name__)


def validate_email(email):
    if BlacklistedEmail.objects.filter(email=email).count():
        raise forms.ValidationError("We can't send emails to this address.")


class MessageSendForm(forms.ModelForm):
    hp = forms.CharField(label="do not fill", required=False)

    class Meta:
        model = Message
        fields = ['sender_name', 'sender_email', 'recipient_name', 'recipient_email', 'message',
                  'sender_named', 'sender_approved_public', 'sender_approved_public_named']

    def __init__(self, *args, **kwargs):
        super(MessageSendForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-8'

        self.fields['sender_name'].label = 'Name'
        self.fields['sender_email'].label = 'Email'
        self.fields['sender_email'].help_text = "We'll send you a confirmation link before sending your message out."
        self.fields['sender_email'].validators = [validate_email]
        self.fields['recipient_name'].label = 'Name'
        self.fields['recipient_email'].label = 'Email'
        self.fields['recipient_email'].validators = [validate_email]
        self.fields['message'].help_text = 'Writer\'s block? Check out our <a href="%s">message inspiration</a>.' % reverse('messaging:inspiration')
        self.fields['sender_named'].label = 'You can tell the recipient my name and email address.'
        self.fields['sender_approved_public'].label = "I'm OK with you publishing this message publicly."
        self.fields['sender_approved_public_named'].label = "...and you can even include our names publicly."
        self.fields['sender_approved_public_named'].help_text = "Note that we won't publish anything unless the recipient opts in too."

        self.helper.layout = Layout(
            Fieldset('This message is from...', 'sender_name', 'sender_email', 'hp'),
            Fieldset("You're sending some happiness to...", 'recipient_name', 'recipient_email'),
            Fieldset("Your message is...", 'message'),
            Fieldset("Privacy choices", 'sender_named', 'sender_approved_public', 'sender_approved_public_named'),
            HTML("<br>"),
            Submit('submit', 'Send some happiness', css_class='btn-lg centered'),
        )

    def clean(self):
        super(MessageSendForm, self).clean()
        if self.cleaned_data.get('hp'):
            raise forms.ValidationError('')
        if self.cleaned_data.get('sender_approved_public_named') and not self.cleaned_data.get('sender_approved_public'):
            self.add_error('sender_approved_public_named', "If you want us to publish the message including your name, "
                                                           "you must also check 'I'm OK with you publishing this "
                                                           "message publicly'")


class MessageRecipientForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient_approved_public', 'recipient_approved_public_named']

    def __init__(self, *args, **kwargs):
        super(MessageRecipientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-8'

        self.fields['recipient_approved_public'].label = "I'm OK with you publishing this message publicly."
        self.fields['recipient_approved_public_named'].label = "...and you can even include our names publicly."
        self.fields['recipient_approved_public_named'].help_text = "Note that we won't publish anything unless the sender opted in too."

        self.helper.layout = Layout(
            Fieldset("Privacy choices", 'recipient_approved_public', 'recipient_approved_public_named'),
            HTML("<br>"),
            Submit('submit', 'Save privacy choices', css_class='btn-lg centered'),
        )

    def clean(self):
        super(MessageRecipientForm, self).clean()
        if self.cleaned_data.get('recipient_approved_public_named') and not self.cleaned_data.get('recipient_approved_public'):
            self.add_error('recipient_approved_public_named', "If you want us to publish the message including your "
                                                              "name, you must also check 'I'm OK with you publishing "
                                                              "this message publicly'")

from __future__ import unicode_literals

from django.conf.urls import url

from .views import (StartView, MessageSendView, MessageSenderConfirmationSentView, MessageSenderConfirmationView,
                    MessageSenderConfirmedView, MessageRecipientMessageUpdate, FaqView, ArchiveView, BlacklistEmailView)

urlpatterns = [
    url(r'^$', StartView.as_view(), name='start'),
    url(r'^faq/$', FaqView.as_view(), name='faq'),
    url(r'^archive/$', ArchiveView.as_view(), name='archive'),
    url(r'^blacklist-email/(?P<email>[\w\.@\+-]+)/(?P<digest>\w+)/$', BlacklistEmailView.as_view(), name='blacklist_email'),
    url(r'^send/$', MessageSendView.as_view(), name='send'),
    url(r'^send/confirmation-sent/$', MessageSenderConfirmationSentView.as_view(), name='sender_confirmation_sent'),
    url(r'^send/confirmation/(?P<identifier>[\w-]+)/(?P<token>[\w-]+)/$', MessageSenderConfirmationView.as_view(), name='sender_confirm'),
    url(r'^send/confirmed/$', MessageSenderConfirmedView.as_view(), name='sender_confirmed'),
    url(r'^recipient/(?P<identifier>[\w-]+)/(?P<token>[\w-]+)/$', MessageRecipientMessageUpdate.as_view(), name='recipient_message_update'),
]

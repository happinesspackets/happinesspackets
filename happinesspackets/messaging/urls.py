from __future__ import unicode_literals

from django.urls import path, re_path

from .views import (StartView, MessageSendView, MessageSenderConfirmationSentView, MessageSenderConfirmationView,
                    MessageSenderConfirmedView, MessageRecipientMessageUpdate, FaqView, ArchiveView, BlacklistEmailView)

app_name = "messaging"

urlpatterns = [
    path('', StartView.as_view(), name='start'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('archive/', ArchiveView.as_view(), name='archive'),
    re_path(r'^blacklist-email/(?P<email>[\w\.@\+-]+)/(?P<digest>\w+)/$', BlacklistEmailView.as_view(), name='blacklist_email'),
    path('send/', MessageSendView.as_view(), name='send'),
    path('send/confirmation-sent/', MessageSenderConfirmationSentView.as_view(), name='sender_confirmation_sent'),
    re_path(r'^send/confirmation/(?P<identifier>[\w-]+)/(?P<token>[\w-]+)/$', MessageSenderConfirmationView.as_view(), name='sender_confirm'),
    path('send/confirmed/', MessageSenderConfirmedView.as_view(), name='sender_confirmed'),
    re_path(r'^recipient/(?P<identifier>[\w-]+)/(?P<token>[\w-]+)/$', MessageRecipientMessageUpdate.as_view(), name='recipient_message_update'),
]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from oslove.utils.misc import readable_random_token
from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel

logger = logging.getLogger(__name__)


class ExampleModel(TimeStampedModel):
    STATUS = Choices(
        ('draft', 'concept'),
        ('rejected', 'afgewezen'),
        ('final', 'definitief'),
    )

    identifier = models.CharField(max_length=255, db_index=True)
    status = models.CharField(choices=STATUS, default=STATUS.draft, max_length=255)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk or force_insert:
            self.identifier = readable_random_token(alphanumeric=True)
            while ExampleModel.objects.filter(identifier=self.identifier).count():
                self.identifier = readable_random_token(alphanumeric=True)  # pragma: no cover
        return super(ExampleModel, self).save(force_insert, force_update, using, update_fields)

# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from utils import get_profile

def user_set_profile(sender, **kwargs):
    user = kwargs['instance']
    try:
        profile = get_profile(user.username)
        profile.user = user
        models.Model.save(profile)
    except Exception, e:
        pass
models.signals.post_save.connect(user_set_profile, sender=User, dispatch_uid='djtools.models')

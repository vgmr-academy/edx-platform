from __future__ import unicode_literals
from django.db import models
from mongoengine import *
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User
from microsite_configuration.models import (
    Microsite,
    MicrositeOrganizationMapping,
    MicrositeTemplate
)

class MicrositeDetail(TimeStampedModel):
    name = models.CharField(max_length=250,unique=True)
    logo = models.CharField(max_length=250)
    language_code = models.CharField(max_length=250, null=True)
    color_code = models.CharField(max_length=250)

    class Meta(object):
        verbose_name = 'Microsite Details'
        verbose_name_plural = 'Microsite Details'

    @classmethod
    def save_details(cls,details):
        if cls.objects.filter(name=details['name']).exists():
            return {'success':False,
                    'error_msg':'Microsite Already exists.'}
        else:
            micro_details = cls(name=details['name'],
                                logo=details['logo'],
                                language_code=details['language_code'],
                                color_code=details['color'])
        try:
            micro_details.save()
            return {'success':True,
                    'error_msg':''}
        except Exception as error:
            return {'success':False,
                    'error_msg': str(error)}

    @classmethod
    def get_details(cls,microsite_id):
        if cls.objects.filter(id=microsite_id).exists():
            return {'data': cls.objects.get(id=microsite_id),
                    'error_msg':''}
        else:
            return {'data': '',
                    'error_msg':'The requested Microsite does not exist.'}

    @classmethod
    def get_name(cls,microsite_id):
        return cls.objects.get(id=microsite_id).name

    @classmethod
    def update_details(cls,microsite_id, microsite_details):
        microsite = cls.objects.get(id=microsite_id)
        microsite.name = microsite_details['name']
	if microsite_details['logo'] != '':
	    microsite.logo = microsite_details['logo'].name
        if 'language' in microsite_details:
            microsite.language_code = microsite_details['language']
        microsite.color_code = microsite_details['color']
        try:
            microsite.save()
            return {'data': cls.objects.get(id=microsite_id),
                    'error_msg':''}
        except:
            return {'data': '',
                    'error_msg':'The requested Microsite does not exist.'}

class MicrositeAdminManager(TimeStampedModel):
    class Meta(object):
        db_table = "microsite_admin_manager"
        
    user = models.ForeignKey(User)
    microsite = models.ForeignKey(Microsite)


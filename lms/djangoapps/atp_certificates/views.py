#!/usr/bin/env python
# -*- coding: utf-8 -*-

from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey
import json
from openedx.core.djangolib.markup import HTML
from edxmako.shortcuts import render_to_response,render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from courseware.courses import get_course_by_id
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from course_progress.helpers import get_overall_progress
from lms.djangoapps.grades.new.course_grade import CourseGradeFactory
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from student.models import User,CourseEnrollment
from django.http import JsonResponse,HttpResponse
from microsite_configuration.microsite import is_request_in_microsite,get_all_orgs
from utils import generate_html
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
import datetime

import logging
log = logging.getLogger(__name__)

@login_required
def atp_check_certificate(request,course_id):
    log.info("atp_check_certificate start: "+str(datetime.datetime.now().strftime("%s")))
    context = {}
    try:
        user = request.user
        username = user.username
        course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
        course = get_course_by_id(course_key)
        is_passed = CourseGradeFactory().create(user, course).passed
        if is_passed:
            certificate_url = '/api/atp/generate/certificate/'+course_id+'/'
        else:
            certificate_url = ''
        context['course_id'] = course_id
        context['username'] = username
        context['passed'] = is_passed
        context['certificate_url'] = certificate_url
        context['microsite'] = is_request_in_microsite()
        context['status'] = True

    except:
        context['status'] = False
        context['message'] = 'Error'

    log.info("atp_check_certificate end: "+str(datetime.datetime.now().strftime("%s")))
    return JsonResponse(context)

@login_required
def atp_generate_certificate(request,course_id):
    log.info("atp_generate_certificate start: "+str(datetime.datetime.now().strftime("%s")))
    context = {}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    user = request.user
    username = user.username
    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
    course = get_course_by_id(course_key)
    categorie = course.categ
    course_factory = CourseGradeFactory().get_persisted(user, course)
    is_passed = course_factory.passed
    courseoverview = CourseOverview.get_from_id(course_key)
    course_title = courseoverview.display_name_with_default
    score = str(course_factory.percent * 100)+'%'
    url = 'https://'+settings.FEATURES['LMS_BASE']

    if configuration_helpers.get_value('logo_couleur') :
        logo_path = configuration_helpers.get_value('logo_couleur')
    else:
        logo_path = '/media/certificates/images/logo-amundi.jpg'
    if configuration_helpers.get_value('amundi_brand') and configuration_helpers.get_value('amundi_brand')=="true":
        amundi_academy = '/media/certificates/images/logo-amundi-academy.jpg'
    else:
        amundi_academy=''
    course_img_path = courseoverview.image_urls['raw']
    course_img_path = url+course_img_path
    template_path = '/certificates/template.html'
    certif_img_path = url+'/media/certificates/images/tampon.png'


    #return HttpResponse(pdf)
    return generate_html(
        username,score,course_img_path,template_path,
        course_title,categorie,certif_img_path,
        logo_path,amundi_academy,course.language
    )
    #return response

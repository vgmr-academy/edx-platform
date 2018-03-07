# -*- coding: utf-8 -*-
import json
import logging
import os.path
import os
import time
import base64
from io import BytesIO

from opaque_keys.edx.keys import CourseKey

from util.json_request import JsonResponse
from django.http import Http404, HttpResponseServerError,HttpResponse
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers

from xmodule.modulestore.django import modulestore
from course_api.blocks.api import get_blocks
from courseware.models import StudentModule
from course_api.blocks.views import BlocksInCourseView,BlocksView
from lms.djangoapps.course_blocks.api import get_course_blocks
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from courseware.courses import get_course_by_id
from student.models import *
from django.contrib.auth.models import User

from student.models import UserPreprofile

from django.core.mail import EmailMessage

from lms.djangoapps.grades.new.course_grade import CourseGradeFactory

from xlwt import *

from django.conf import settings

import sys

log = logging.getLogger(__name__)

class course_grade():

	def __init__(self,course_id,course_key=None,request=None):

		self.course_id = course_id
		self.course_key = course_key
		self.request = request

	def get_titles(self):

		if self.course_key is None:
			self.course_key = SlashSeparatedCourseKey.from_deprecated_string(self.course_id)


		#get all course structure
		course_usage_key = modulestore().make_course_usage_key(self.course_key)
		blocks = get_blocks(self.request,course_usage_key,depth='all',requested_fields=['display_name','children'])
		_root = blocks['root']
		blocks_overviews = []
		#return unit title and component root
		try:
			children = blocks['blocks'][_root]['children']
			for z in children:
				child = blocks['blocks'][z]
				try:
					sub_section = child['children']
					for s in sub_section:
						sub_ = blocks['blocks'][s]
						vertical = sub_['children']
						try:
							for v in vertical:
								unit = blocks['blocks'][v]
								w = {}
								w['id'] = unit['id']
								w['display_name'] = unit['display_name']
								try:
									w['children'] = unit['children']
								except:
									pass
								blocks_overviews.append(w)
						except:
							pass
				except:
					pass
		except:
			pass

		studentmodule = StudentModule.objects.raw("SELECT id,course_id,module_id FROM courseware_studentmodule WHERE course_id = %s AND max_grade IS NOT NULL AND grade <= max_grade GROUP BY module_id ORDER BY created", [self.course_id])

		title = []

		for n in studentmodule:

			usage_key = n.module_state_key
			_current = get_blocks(self.request,usage_key,depth='all',requested_fields=['display_name'])
			root = _current['root']

			unit_name = ''

			for over in blocks_overviews:
				if str(root) in over.get('children'):
					unit_name = over.get('display_name')


			q = {
				"title":_current['blocks'][root]['display_name'],
				"root":root,
				'unit':unit_name
			}
			title.append(q)


		return title


	def _user(self,user_id):
		course_key = SlashSeparatedCourseKey.from_deprecated_string(self.course_id)
		course_block = StudentModule.objects.all().filter(student_id=user_id,course_id=course_key,max_grade__isnull=False)
		course_grade = []

		for n in course_block:
			q = {}
			usage_key = n.module_state_key
			block_name = get_blocks(self.request,usage_key,depth='all',requested_fields=['display_name'])
			root = block_name['root']
			display_name = block_name['blocks'][root]['display_name']
			q['earned'] = n.grade
			q['possible'] = n.max_grade
			q['display_name'] = display_name
			q['root'] = root
			course_grade.append(q)

		return course_grade


	def export(self,sended_email):
                reload(sys)
                sys.setdefaultencoding('utf8')

		log.warning("Start Task grade reports course_id : "+str(self.course_id) )
		course_key = CourseKey.from_string(self.course_id)
		course = get_course_by_id(course_key)
		course_enrollement = CourseEnrollment.objects.filter(course_id=course_key)

		#prepare xls
		header = [
			"id","email","first name","last name","level 1","level 2","level 3","level 4"
		]

		title = self.get_titles()

		for n in title:
			header.append(n.get('unit')+' - '+n.get('title'))

		header.append('total grade (in %)')

		filename = '{}_grades_reports.xls'.format(self.course_id).replace('+','_')

		wb = Workbook(encoding='utf-8')
		sheet = wb.add_sheet('Users')

		for i, head in enumerate(header):
			sheet.write(0,i,head)

		j = 0

		for i in range(len(course_enrollement)):

			j = j + 1

			user=course_enrollement[i].user
			course_grade = CourseGradeFactory().create(user, course)

			user_id = user.id
			email = user.email
			first_name = user.first_name
			last_name = user.last_name

			try:
				pre = UserPreprofile.objects.get(email=email)
				_lvl = [pre.level_1,pre.level_2,pre.level_3,pre.level_4]
			except:
				_lvl = ["","","",""]

			final_grade = course_grade.percent * 100

			_user_blocks = self._user(user_id)

			sheet.write(j, 0, user_id)
			sheet.write(j, 1, email)
			sheet.write(j, 2, first_name)
			sheet.write(j, 3, last_name)
			sheet.write(j, 4, _lvl[0])
			sheet.write(j, 5, _lvl[1])
			sheet.write(j, 6, _lvl[2])
			sheet.write(j, 7, _lvl[3])

			k = 8

			for val in title:
				_grade = 0
				for block in _user_blocks:

					if block.get('root') == val.get('root'):
						_grade = block.get('earned')


				sheet.write(j, k, _grade)

				k = k + 1

			sheet.write(j, k, final_grade)

		output = BytesIO()
		wb.save(output)
		_files_values = output.getvalue()

		log.warning("End Task grade reports course_id : "+str(self.course_id))


		#sending mail
		log.warning("send grade reports course_id : "+str(filename))
		log.warning("email : "+str(sended_email))

                if course.language == "fr":
                    subject = "Résultats des participants du module {}".format(course.display_name_with_default_escaped)
	            text_content = "Veuillez trouver en pièce attachée les résultats des participants pour le module{}.\n A noter que si votre campagne de formation est toujours en cours, ce fichier constitue un état statistique intermédiaire.".format(course.display_name_with_default_escaped)
		if course.language == "en":
		    subject = "grades report for {}".format(course.display_name_with_default_escaped)
		    text_content = "Please, find attached the score report for {}.\n Remember that if your training campaign is still in progress, this file is an intermediate statistical status.".format(course.display_name_with_default_escaped)
		from_email=configuration_helpers.get_value('email_from_address', settings.DEFAULT_FROM_EMAIL)
		to = sended_email
		mimetype='application/vnd.ms-excel'
		fail_silently=False
		_data = _files_values
		#_encoded = base64.b64encode(wb)

		_email = EmailMessage(subject, text_content, from_email, [to])
		_email.attach(filename, _data, mimetype=mimetype)
		_email.send(fail_silently=fail_silently)

		log.warning("end send grade reports course_id : "+str(filename))

		context = {
			"filename" : filename
		}

		return context



	def get_xls(self):

		context = {
			"status": False,
			'filepath': None
		}

		folder_path = '/edx/var/edxapp/grades/'
		filename = '{}_grades_reports.xls'.format(self.course_id).replace('+','_')
		filepath = folder_path+filename

		if os.path.isfile(filepath):
			context['status'] = True,
			context['filepath'] = filepath
			context['time'] = time.ctime(os.path.getmtime(filepath))

		return context

	def download_xls(self,filename):

		full_path = '/edx/var/edxapp/grades/'+filename
		_file = open(full_path,'r')
		_content = _file.read()
		response = HttpResponse(_content, content_type="application/vnd.ms-excel")
		response['Content-Disposition'] = "attachment; filename="+filename
		os.remove(full_path)
		return response

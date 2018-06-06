from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import JsonResponse

from edxmako.shortcuts import render_to_response
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from xmodule.modulestore.django import modulestore

from course_progress.models import StudentCourseProgress
from course_progress.helpers import get_overall_progress

import logging
from pprint import pformat
log = logging.getLogger()


@login_required
def get_user_overvall_course_progress(user,course_id):
    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
    overall_progress = get_overall_progress(user, course_id)
    return {'overall_progress': overall_progress}



@login_required
@ensure_csrf_cookie
@require_http_methods(["GET"])
def get_overall_course_progress(request):
    """
    Description: This view kept for fetching the overall course progress.

    Request Parameters:
        course_id: course ID for which progress needs to be calculated.
        student_id: Student for which progress needs to be calculated.

    Returns:
        json response

    Assumes the course_id is in a valid format.

    Author: Naresh Makwana
    """
    course_id = request.GET.get('course_id')
    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)

    overall_progress = get_overall_progress(request.user.id, course_key)

    return JsonResponse({'overall_progress': overall_progress})

@login_required
@ensure_csrf_cookie
@require_http_methods(["GET"])
def get_completion_status(request):
    """
    Description: To check completion status of the section/chapter.

    Request Parameters:
        course_id: course ID string.

    Returns:
        json response

    Assumes the course_id is in a valid format.

    Author: Naresh Makwana
    """
    # Set initial value to progress
    progress= {}
    completion_status = {}

    # Get course id and convert it to course key
    course_id = request.GET.get('course_id')
    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)

    # Get the student course completion progress
    try:
        student_course_progress = StudentCourseProgress.objects.get(student=request.user.id, course_id=course_key)
        progress = student_course_progress.progress
    except StudentCourseProgress.DoesNotExist:
        pass

    # Prepare completion status dictionary
    sequential_id = request.GET.get('sequential_id')
    sequential_progress=progress.get(sequential_id,[])['progress']
    for block_id in progress.get(sequential_id,[])['children']:
        completion_status.update({block_id:progress.get(block_id,[])['progress']})

    # Return the JSON resposne
    return JsonResponse({'completion_status': completion_status})

def has_passed(module_id, course_progress):
    """
    Author: Naresh Makwana
    """
    module_progress = course_progress.get(module_id, {})

    return int(module_progress.get('progress', 0)) == 100

def get_course_progress(student, course_key):
    progress = {}

    try:
        course_progress = StudentCourseProgress.objects.get(student=student.id, course_id=course_key)
        progress = course_progress.progress
    except StudentCourseProgress.DoesNotExist:
        pass

    return progress

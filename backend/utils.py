from dateutil import parser
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q

from .models import *


def collide(can_id, int_id, cur_start, cur_end):
    candidate = Candidate.objects.get(id=can_id)
    interviewer = Candidate.objects.get(id=int_id)

    cur_start = parser.parse(cur_start).time()
    cur_end = parser.parse(cur_end).time()

    time_filter = Q(start_time__range=[cur_start, cur_end]) | Q(
        end_time__range=[cur_start, cur_end])

    candidate_objs = Interview.objects.filter(candidate_name__name=candidate.name).filter(time_filter)
    interviewer_objs = Interview.objects.filter(interviewer_name__name=interviewer.name).filter(time_filter)

    objs = candidate_objs | interviewer_objs

    if objs.exists():
        return True
    return False


def send_confirmation(candidate_name, interviewer_name, start, end, date, recipient_list):
    subject = f'{candidate_name} X {interviewer_name}'
    message = f'Hi {candidate_name}, Your interview is scheduled from {start} to {end} on {date}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = recipient_list
    send_mail(subject, message, email_from, recipient_list)

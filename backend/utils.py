from .models import *
from dateutil import parser


def collide(can_id, int_id, cur_start, cur_end):
    can = Candidate.objects.get(id=can_id)
    int = Candidate.objects.get(id=int_id)
    cur_start = parser.parse(cur_start)
    cur_end = parser.parse(cur_end)

    Inte = Interview.objects.filter(candidate_name__name=can.name, interviewer_name__name=int.name)
    if Inte.exists():
        Inte = Inte[0]
    if (Inte.start_time < cur_start.time() < Inte.end_time) or (Inte.start_time < cur_end.time() < Inte.end_time) or (
            cur_start.time() <= Inte.start_time and cur_end.time() >= Inte.end_time):
        return False
    return True

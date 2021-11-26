from rest_framework import serializers

from .models import Interview


class InterviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interview
        fields = ('id','candidate_name',
                  'interviewer_name',
                  'resume',
                  'start_date',
                  'end_date',
                  'start_time',
                  'end_time',)

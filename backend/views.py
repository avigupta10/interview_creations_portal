from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from .serializers import InterviewSerializer
from .utils import *


@api_view(['GET'])
def api_details(request):
    """
    :param request:
    :return:
    """
    objs = Interview.objects.all()
    details = {
        'View Interview': 'http://127.0.0.1:8000/api/interviews',
        'Create Interview': 'http://127.0.0.1:8000/api/schedule-interview',
        'Update Interview': [
            f'http://127.0.0.1:8000/api/reschedule-interview/{key.id}' for key in objs
        ],

    }
    return Response(details)


class InterviewDetails(ListAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer


class ScheduleInterview(APIView):
    serializer_class = InterviewSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            candidate_id = serializer.data.get('candidate_name')
            interviewer_id = serializer.data.get('interviewer_name')

            try:
                candidate_name = Candidate.objects.get(id=candidate_id)
                interviewer_name = Interviewer.objects.get(id=interviewer_id)
            except Interviewer.DoesNotExist:
                return Response({'error': 'No Such User Exist'}, status=status.HTTP_400_BAD_REQUEST)

            resume = request.FILES.get('resume')
            date = serializer.data.get('date')
            start_time = serializer.data.get('start_time')
            end_time = serializer.data.get('end_time')
            if not collide(candidate_id, interviewer_id, start_time, end_time):
                form, created = Interview.objects.update_or_create(candidate_name=candidate_name,
                                                                   interviewer_name=interviewer_name,
                                                                   resume=resume,
                                                                   date=date,
                                                                   start_time=start_time,
                                                                   end_time=end_time,
                                                                   )

                send_confirmation(candidate_name.name, interviewer_name.name, start_time, end_time, date,
                                  [candidate_name.email, interviewer_name.email])

                return Response(InterviewSerializer(form).data, status=status.HTTP_201_CREATED)
            return Response({'error': 'Candidate and interviewer is already booked for this time range'},
                            status=status.HTTP_400_BAD_REQUEST)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReScheduleInterview(APIView):
    serializer_class = InterviewSerializer

    def get(self, request, key):
        """
        :param request:
        :param key:
        :return:
        """
        obj = Interview.objects.get(id=key)
        data = InterviewSerializer(obj).data
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, key):
        """
        :param request:
        :param key:
        :return:
        """
        try:
            obj = Interview.objects.get(id=key)
        except Interview.DoesNotExist:
            return Response({'error': 'No Such User Exist'}, status=status.HTTP_400_BAD_REQUEST)
        if True:
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                candidate_id = serializer.data.get('candidate_name')
                interviewer_id = serializer.data.get('interviewer_name')

                try:
                    candidate_name = Candidate.objects.get(id=candidate_id)
                    interviewer_name = Interviewer.objects.get(id=interviewer_id)
                except Interviewer.DoesNotExist:
                    return Response({'error': 'No Such User Exist'}, status=status.HTTP_400_BAD_REQUEST)
                obj.candidate_name = candidate_name
                obj.interviewer_name = interviewer_name
                obj.resume = request.FILES['resume']
                obj.date = serializer.data.get('date')
                obj.start_time = serializer.data.get('start_time')
                obj.end_time = serializer.data.get('end_time')
                if not collide(candidate_id, interviewer_id, serializer.data.get('start_time'),
                               serializer.data.get('end_time')):
                    obj.save(update_fields=['candidate_name',
                                            'interviewer_name',
                                            'resume',
                                            'date',
                                            'start_time',
                                            'end_time', ])

                    send_confirmation(candidate_name.name, interviewer_name.name, serializer.data.get('start_time'),
                                      serializer.data.get('end_time'), serializer.data.get('date'),
                                      [candidate_name.email, interviewer_name.email])

                    return Response(InterviewSerializer(obj).data, status=status.HTTP_200_OK)
                return Response({'error': 'Candidate and interviewer is already booked for this time range'},
                                status=status.HTTP_400_BAD_REQUEST)

            print(serializer.errors)
            return Response({'error': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import *
urlpatterns = [
    path('', api_details),
    path('interviews', InterviewDetails.as_view()),
    path('schedule-interview', ScheduleInterview.as_view()),
    path('reschedule-interview/<int:key>', ReScheduleInterview.as_view()),
]
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
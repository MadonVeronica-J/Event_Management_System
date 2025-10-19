"""
URL configuration for eventorganizer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('participant_logout',views.participant_logout,name='participant_logout'),
    path('generate_certificates/<int:event_id>/',views.generate_certificates,name='generate_certificates'),
    path('pending_events',views.pending_events,name='pending_events'),
    path('disapproved_events',views.disapproved_events,name='disapproved_events'),
    path('my_events',views.my_events,name='my_events'),
    path('upcoming_events',views.upcoming_events,name='upcoming_events'),
    path('attended_events',views.attended_events,name='attended_events'),
    path('upload_certificate_template/<int:event_id>/',views.upload_certificate_template,name='upload_certificate_template'),
    path('check_venue',views.check_venue_availability,name='check_venue'),
    path('event_participants/<int:event_id>/',views.event_participants,name='event_participants'),
    path('mark_attendance/<int:event_id>/',views.mark_attendance,name='mark_attendance'),
    path('approved_events',views.approved_events,name='approved_events'),
    path('share_event/<int:event_id>/',views.share_event,name='share_event'),
    path('',views.participant_login, name = 'participant_login'),
    path('participant_dashboard',views.participant_dashboard, name = 'participant_dashboard'),
    path('request_event',views.request_event_approval,name='request_event'),
    path('organizer_logout',views.organizer_logout,name='organizer_logout'),
    path('organizer_dashboard',views.organizer_dashboard,name='organizer_dashboard'),
    path('organizer_login',views.organizer_login,name='organizer_login'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
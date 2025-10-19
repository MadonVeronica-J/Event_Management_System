from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
from django.conf import settings
from django.utils.timezone import now
from .models import Event, Department, Notification, EventParticipant, Venue

def organizer_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user and user.role == "organizer":
            login(request, user)
            return redirect("organizer_dashboard")  
        else:
            messages.error(request, "Invalid organizer credentials.")

    return render(request, "login.html", {"role": "Organizer"})

def participant_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user and user.role == "participant":
            login(request, user)
            return redirect("participant_dashboard")  
        else:
            messages.error(request, "Invalid participant credentials.")

    return render(request, "login.html", {"role": "Participant"})

@login_required
def organizer_dashboard(request):
    events = Event.objects.filter(organizer=request.user)
    new_status_events = events.filter(status__in=['Approved', 'Disapproved'], notified=False)

    for event in new_status_events:
        event.notified = True
        event.save()

    return render(request, 'organizer_dashboard.html', {'events': events, 'new_status_events': new_status_events})

def organizer_logout(request):
    logout(request)
    return redirect('organizer_login')

def participant_logout(request):
    logout(request)
    return redirect('participant_login')

def request_event_approval(request):
    venues = Venue.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        date = request.POST.get('date')
        venue_id = request.POST.get('venue_id')
        venue = get_object_or_404(Venue,id=venue_id)
        Event.objects.create(
            name=name,
            description=description,
            organizer=request.user,
            date=date,
            venue=venue,
            status='pending'
        )

        redirect("organizer_dashboard")

    return render(request, 'request_event.html',{"venues": venues})


@login_required
def approved_events(request):
    organizer = request.user
    events = Event.objects.filter(organizer=organizer, status="approved").order_by("-created_at")
    return render(request, "approved_events.html", {"events": events})

def pending_events(request):
    events = Event.objects.filter(status="Pending", organizer=request.user).order_by("-created_at")
    return render(request, "pending_events.html", {"events": events})

def disapproved_events(request):
    events = Event.objects.filter(status="Disapproved", organizer=request.user).order_by("-created_at")
    return render(request, "disapproved_events.html", {"events": events})

@login_required
def share_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user, status="approved")
    departments = Department.objects.all()

    if request.method == "POST":
        selected_department_ids = request.POST.getlist("departments")
        selected_departments = Department.objects.filter(id__in=selected_department_ids)
        event.department.set(selected_departments)

        participants = CustomUser.objects.filter(department__in=selected_departments, role="participant")
        for participant in participants:
            if not EventParticipant.objects.filter(event=event, participant=participant).exists():
           
                Notification.objects.create(user=participant, message=f"You can participate in {event}")
                EventParticipant.objects.create(event=event, participant=participant)
            
        redirect("approved_events")

    return render(request, "share_event.html", {"event": event, "departments": departments})

@login_required
def participant_dashboard(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "participant_dashboard.html", {"notifications": notifications})

@login_required
def event_participants(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = EventParticipant.objects.filter(event=event)
    return render(request, "event_participants.html",{"event": event, "participants": participants})

@login_required
def mark_attendance(request, event_id):
    
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("status_"):  # Check if it's an attendance field
                participant_id = key.split("_")[1]  # Extract the participant ID
                status = value  # Get the selected status
                
                # Update the attendance record
                EventParticipant.objects.filter(participant_id=participant_id, event_id=event_id).update(status=status)

        redirect("approved_events")

    participants = EventParticipant.objects.filter(event_id=event_id)
    return render(request, "mark_attendance.html", {"participants": participants})

def check_venue_availability(request):
    venues = Venue.objects.all()
    message = None  # Default message

    if request.method == "POST":
        venue_id = request.POST.get("venue")
        event_date = request.POST.get("date")

        # Check if the selected venue is already booked on the given date
        is_booked = Event.objects.filter(venue_id=venue_id, date=event_date, status="approved").exists()

        if is_booked:
            message = "This venue is already booked on the selected date."
        else:
            message = "This venue is available."

    return render(request, "check_venue.html", {"venues": venues, "message": message})

@login_required
def upload_certificate_template(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST" and request.FILES.get("certificate_template"):
        event.certificate_template = request.FILES["certificate_template"]
        event.save()
        return redirect("approved_events")  # Redirect to approved events page

    return render(request, "upload_certificate_template.html", {"event": event})

def attended_events(request):
    attended = EventParticipant.objects.filter(participant=request.user, status="Present").select_related("event")
    return render(request, "attended_events.html", {"attended_events": attended})

def upcoming_events(request):
    upcoming = Event.objects.filter(date__gte=now()).order_by("date")
    return render(request,"upcoming_events.html",{"upcoming_events": upcoming})

def my_events(request):
    return render(request,"my_events.html")

def generate_certificates(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    present_participants = EventParticipant.objects.filter(event=event, status="Present")

    if not event.certificate_template:
        return HttpResponse("❌ No certificate template uploaded for this event.")

    template_path = event.certificate_template.path  # Organizer's uploaded template
    font_path = "static/fonts/arial.ttf"  # Change to your font file path
    output_dir = "media/certificates"

    os.makedirs(output_dir, exist_ok=True)
    
    for participant in present_participants:
        img = Image.open(template_path)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, 50)  # Adjust size as needed
        
        # Position text dynamically (adjust coordinates as per template)
        name_position = (500, 300)
        event_position = (500, 400)
        dept_position = (500, 500)

        draw.text(name_position, participant.participant.username, fill="black", font=font)
        draw.text(event_position, event.name, fill="black", font=font)
        draw.text(dept_position, participant.participant.department.name, fill="black", font=font)

        # Save the certificate
        cert_filename = f"{participant.participant.username}_{event.id}.png"
        cert_path = os.path.join(output_dir, cert_filename)
        img.save(cert_path)

        # Store the certificate path in the database (optional)
        participant.certificate = f"certificates/{cert_filename}"
        participant.save()

    return HttpResponse("✅ Certificates Generated Successfully.")
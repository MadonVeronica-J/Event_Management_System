from django.core.mail import send_mail
from django.conf import settings

def send_event_request_email(admin_email, organizer, event):
    subject = "New Event Approval Request"
    message = f"Organizer {organizer} has requested approval for the event: {event.name}.\n\nDescription: {event.description}\nDate: {event.date}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [admin_email])

def send_event_status_email(organizer_email, event, status):
    subject = f"Your Event '{event.name}' has been {status}"
    message = f"Dear Organizer,\n\nYour event '{event.name}' has been {status} by the admin.\n\nDate: {event.date}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [organizer_email])

def send_event_shared_email(participants_emails, event):
    subject = f"New Event Available: {event.name}"
    message = f"Dear Participant,\n\nA new event '{event.name}' is available for registration.\nDate: {event.date}\nVenue: {event.venue.name}\n\nLog in to your account to register."
    send_mail(subject, message, settings.EMAIL_HOST_USER, participants_emails)
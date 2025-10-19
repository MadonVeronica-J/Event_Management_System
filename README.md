# Event Management System

A role-based web application built using **Python Django**, designed to simplify college and organizational event coordination.  
It provides separate dashboards for **Admins**, **Event Organizers**, and **Participants**, enabling smooth event planning, approval, participation, and certificate distribution.

---

## Features

### Admin
- Adds Event Organizers and Participants.
- Approves or disapproves events requested by organizers.
- Manages overall event and user activities.

### Event Organizer
- Plans and requests new events for admin approval.
- Checks venue availability before submitting an event request.
- Shares approved events with specific departments.
- Marks participant attendance and uploads certificate templates.
- Automatically generates and sends participation certificates to attendees.

### Participants
- View approved events shared with their department.
- Register for available events.
- Receive dashboard notifications when selected or invited to events.
- Access and download certificates after attendance is marked.

---

## Technologies Used
- **Frontend:** HTML, CSS, JavaScript, Bootstrap  
- **Backend:** Python (Django Framework)  
- **Database:** SQLite  
- **Certificate Generation:** PIL  
- **Version Control:** Git & GitHub  

---

## Additional Features
- Department-based participant selection  
- Venue management and booking validation  
- Certificate generation with participant details  
- Dashboard notifications for all user roles  

---

## Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/event-management-system.git
cd event-management-system
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create Superuser
```bash
python manage.py createsuperuser
```

### 6️⃣ Run the Server
```bash
python manage.py runserver
```

Then open http://127.0.0.1:8000/ in your browser.

## Workflow Summary

1. Organizer → Requests event → Admin reviews and approves.
2. Organizer → Shares approved event → Notifies eligible participants.
3. Participants → Register → Attend → Receive certificate via dashboard.


## Author

### Madon Veronica
Aspiring Software Developer | Passionate about building scalable, user-centric applications.

🌐 Portfolio<br>
📫 Email: madon.veronica73@gmail.com


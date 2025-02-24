from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Attendance, Subject
from datetime import date
import json



@login_required
def student_dashboard(request):
    student = request.user.studentprofile
    subjects = Subject.objects.all()
    today = date.today()

    # Attendance Data
    attendance_data = []
    total_hours_attended_today = 0
    total_hours_attended_till_now = 0
    total_hours_attended_current_month = 0

    for subject in subjects:
        total_attended = Attendance.objects.filter(student=student, subject=subject, is_present=True).count()
        attended_this_month = Attendance.objects.filter(student=student, subject=subject, is_present=True, date__month=today.month, date__year=today.year).count()
        attended_today = Attendance.objects.filter(student=student, subject=subject, is_present=True, date=today).count()

        total_classes = subject.total_hours
        attendance_percentage = (total_attended / total_classes) * 100 if total_classes > 0 else 0

        attendance_data.append({
            'subject': subject.name,
            'hours_attended': total_attended,
            'attendance_percentage': round(attendance_percentage, 2)
        })

        total_hours_attended_today += attended_today
        total_hours_attended_till_now += total_attended
        total_hours_attended_current_month += attended_this_month

    context = {
    'attendance_data': json.dumps(attendance_data),  # Convert Python dict to JSON string
    'total_hours_attended_today': total_hours_attended_today,
    'total_hours_attended_till_now': total_hours_attended_till_now,
    'total_hours_attended_current_month': total_hours_attended_current_month,
    }

    return render(request, 'edu/stu_dashboard.html', context)

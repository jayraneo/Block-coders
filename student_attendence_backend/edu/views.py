
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.timezone import now
from .models import Attendance, StudentProfile, Subject

@login_required
def student_dashboard(request):
    # Get the logged-in student's profile
    student = StudentProfile.objects.get(user=request.user)

    # Get the current month and year
    today = now().date()
    month, year = today.month, today.year

    # Query total hours attended per subject
    attendance_data = Attendance.objects.filter(
        student=student,
        date__year=year,
        date__month=month
    ).values('subject__id', 'subject__name').annotate(total_hours=Sum('hours_attended'))

    # Convert to lists for JavaScript
    labels = []
    data = []  # Total hours attended
    percentages = []  # Attendance percentage

    for entry in attendance_data:
        subject_id = entry['subject__id']
        subject_name = entry['subject__name']
        total_hours_attended = entry['total_hours']

        # Get total required hours for the subject from Subject model
        subject = Subject.objects.get(id=subject_id)
        total_subject_hours = subject.total_hours  # Fixed total hours

        # Calculate attendance percentage
        attendance_percentage = (total_hours_attended / total_subject_hours) * 100 if total_subject_hours > 0 else 0

        # Append data for the frontend
        labels.append(subject_name)
        data.append(total_hours_attended)
        percentages.append(round(attendance_percentage, 2))  # Round to 2 decimal places

    return render(request, "edu/stu_dashboard.html", {
        "labels": labels,
        "data": data,  # For bar chart
        "percentages": percentages  # For pie chart
    })


@login_required
def teacher_dashboard(request):
    return render(request, 'edu/tchr_dashboard.html')

@login_required
def stu_add(request):
    return render(request, 'edu/new_stu_details.html')
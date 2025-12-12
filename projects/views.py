from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.templatetags.static import static

from .models import BlockedIP
from .forms import ContactForm
from .models import Project, Education, Certificate, Resume
import markdown

def home(request):
    projects = Project.objects.all()
    education = Education.objects.all()
    certificates = Certificate.objects.all()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent successfully! I will get back to you soon.')
            return redirect('home')
    else:
        form = ContactForm()

    context = {
        'projects': projects,
        'education': education,
        'certificates': certificates,
        'form': form
    }
    return render(request, 'projects/home.html', context)


# ... keep project_detail view as it is ...
def project_detail(request, pk):
    # (Existing code...)
    project = get_object_or_404(Project, pk=pk)
    readme_html = markdown.markdown(
        project.readme_content,
        extensions=['fenced_code', 'codehilite', 'toc']
    )
    return render(request, 'projects/detail.html', {'project': project, 'readme_html': readme_html})



def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    #markdown text to HTML
    readme_html = markdown.markdown(
        project.readme_content,
        extensions=['fenced_code','codehilite','toc']
    )
    return render(request, 'projects/detail.html', {
        'project': project,
        'readme_html': readme_html
    })


def resume_view(request):
    # Get the active resume
    resume = Resume.objects.filter(is_active=True).first()

    if resume:
        # Redirect to the file URL
        return redirect(static('projects/resume.pdf'))
    else:
        # Fallback if no resume is uploaded
        messages.error(request, "Resume not found.")
        return redirect('home')

def api_status(request):
    return JsonResponse({
        "status": "online",
        "developer": "Shithij",
        "stack": ["Django", "Python", "Tailwind"],
        "message": "Welcome to the API. Yes, I built this endpoint just for you."
    })


def admin_honeypot(request):
    if request.method == "POST":
        # 1. Get the hacker's IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # 2. Ban them immediately
        if not BlockedIP.objects.filter(ip_address=ip).exists():
            BlockedIP.objects.create(
                ip_address=ip,
                reason="Caught in Honeypot Trap"
            )
            print(f"TRAP TRIGGERED! Banned IP: {ip}")

        # 3. Show the Lockdown Screen
        return render(request, 'blocked_hacker.html', status=403)

    # If it's a GET request, show a fake login page
    # We use the built-in admin login template so it looks 100% real
    return render(request, 'admin/login.html', {'title': 'Log in | Django site admin'})
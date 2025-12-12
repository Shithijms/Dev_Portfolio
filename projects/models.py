from tokenize import blank_re

from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    technology = models.CharField(max_length=100,blank=True)
    github_url = models.URLField()
    readme_content = models.TextField(blank=True,help_text="Markdown content from github")
    imported_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-imported_at']

class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.institution

class Certificate(models.Model):
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    date_earned = models.DateField()
    link = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

class Resume(models.Model):
    name = models.CharField(max_length=100, default="My Resume")
    pdf_file = models.FileField(upload_to='resumes/')
    is_active = models.BooleanField(default=False, help_text="If checked, this will be the resume users see.")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # If we are marking this as active, unmark all others
        if self.is_active:
            Resume.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"

class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField()
    reason = models.CharField(max_length=200, default="Honeypot Triggered")
    banned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Banned: {self.ip_address}"
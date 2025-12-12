from django.db.models.signals import post_save
from django.dispatch import receiver
from admin_honeypot.models import LoginAttempt
from .models import BlockedIP

@receiver(post_save, sender=LoginAttempt)
def ban_hacker(sender, instance, created, **kwargs):
    """
    If a login attempt is recorded in the honeypot,
    immediately add that IP to the BlockedIP table.
    """
    if created:
        ip = instance.ip_address
        # Only ban if not already banned
        if not BlockedIP.objects.filter(ip_address=ip).exists():
            BlockedIP.objects.create(
                ip_address=ip,
                reason=f"Attempted login with user: {instance.username}"
            )
            print(f" UNAUTHORISED USER ATTEMPTED TO LOGIN AND BANNED: {ip}")

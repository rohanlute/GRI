from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """
    Minimal email utilities: keep only user-created account email logic.
    """

    @staticmethod
    def send_email(recipient, subject, message, html_template=None, context=None):
        """Send an email to a user or raw email address.

        recipient: User object or email string
        subject: Email subject
        message: Plain text fallback body
        html_template: Optional HTML template path
        context: Optional template context
        """
        recipient_email = getattr(recipient, 'email', recipient)

        if not recipient_email:
            logger.warning("EmailService.send_email skipped because recipient email is missing.")
            return False

        try:
            html_content = None
            if html_template:
                html_content = render_to_string(html_template, context or {})

            email = EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@localhost'),
                to=[recipient_email],
            )

            if html_content:
                email.attach_alternative(html_content, "text/html")

            email.send(fail_silently=False)
            return True

        except Exception:
            logger.exception("Failed to send email to %s", recipient_email)
            return False


    @staticmethod
    def build_user_created_context(user, login_url=None):
        """Build the email payload for newly created users."""
        full_name = (
            getattr(user, 'get_full_name', lambda: '')() or
            getattr(user, 'full_name', None) or
            getattr(user, 'username', '') or
            'there'
        ).strip()

        company_name = getattr(getattr(user, 'company', None), 'company_name', None)
        role_name = getattr(getattr(user, 'role', None), 'role_name', None)

        if not login_url:
            login_url = f"{getattr(settings, 'SITE_URL', '').rstrip('/')}{'/accounts/login/'}"

        subject = "Your account has been created"

        message = f"""Hello {full_name},

Your account has been created successfully.

You can now log in with the credentials shared by the administrator.

Login URL: {login_url}
Username: {getattr(user, 'username', '')}
Email: {getattr(user, 'email', '')}
Company: {company_name or 'N/A'}
Role: {role_name or 'N/A'}

If you did not expect this email, please contact your administrator.

Regards,
GRI Team
"""

        return {
            'subject': subject,
            'message': message,
            'user': user,
            'full_name': full_name,
            'login_url': login_url,
            'company_name': company_name,
            'role_name': role_name,
        }


    @staticmethod
    def send_user_created_email(user, login_url=None):
        """Send the user creation notification email."""
        if not user:
            logger.warning("send_user_created_email called without a user instance.")
            return False

        if not getattr(user, 'email', None):
            logger.warning(
                "User creation email skipped for %s because no email address is set.",
                getattr(user, 'username', user),
            )
            return False

        context = EmailService.build_user_created_context(user, login_url=login_url)

        return EmailService.send_email(
            recipient=user,
            subject=context['subject'],
            message=context['message'],
            html_template='emails/accounts/user_created.html',
            context=context,
        )

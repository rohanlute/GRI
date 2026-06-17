from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.accounts.mixins import SuperAdminRequiredMixin


class NotificationListView(
    LoginRequiredMixin,
    SuperAdminRequiredMixin,
    TemplateView
):

    login_url = 'accounts:login'

    template_name = 'applications/notification_list.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['page_title'] = 'Notification Master'

        return context
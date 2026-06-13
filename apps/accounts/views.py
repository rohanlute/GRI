from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import SuperAdminRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (ListView,CreateView,UpdateView,DetailView)
from django.db import transaction
from django.db.models import Q
from .forms import UserCreateForm
from .models import User
from apps.accounts.models import Role
from apps.companies.models import Company


# -----------------------------------------------
# ============= LOGIN ===========================
# -----------------------------------------------

class LoginView(View):

    template_name = 'base/login.html'

    def get(self, request):
        return render(request,self.template_name)

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            user.is_online = True
            user.save()
            return redirect('accounts:dashboard')

        messages.error(request,'Invalid Username or Password')

        return render(request,self.template_name)


# -----------------------------------------------
# ============= LOGOUT ==========================
# -----------------------------------------------

class LogoutView(View):

    def get(self, request):
        request.user.is_online = False
        request.user.save()

        logout(request)

        messages.success(request,'Logged out successfully')

        return redirect('accounts:login')
    
# -----------------------------------------------
# ============= DASHBOARD =======================
# -----------------------------------------------

class DashboardView(LoginRequiredMixin,TemplateView):

    login_url = 'accounts:login'

    template_name = ('dashboard/dashboard.html')

    def get_context_data(self,**kwargs):

        context = super().get_context_data(**kwargs)

        context['user'] = (self.request.user)

        return context


# -----------------------------------------------
# ============= USER LIST =======================
# -----------------------------------------------

class UserListView(LoginRequiredMixin,SuperAdminRequiredMixin,ListView):

    model = User

    template_name = ('accounts/user_management/user_list.html')

    context_object_name = 'users'

    def get_queryset(self):

        queryset = User.objects.select_related('role', 'company').filter(
            role__role_code='SUPERADMIN'
        ).order_by('-id')

        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search) |
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(mobile_number__icontains=search) |
                Q(employee_code__icontains=search) |
                Q(department__icontains=search) |
                Q(company__company_name__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        users = context.get('users')

        if users is not None and hasattr(users, 'count'):
            context['total_users_count'] = users.count()
            context['active_users_count'] = users.filter(is_active=True).count()

        return context

# ============= USER LIST =======================

class UserCreateView(LoginRequiredMixin,SuperAdminRequiredMixin,CreateView):

    model = User

    form_class = UserCreateForm

    template_name = ('accounts/user_management/user_create.html')

    success_url = reverse_lazy('accounts:user_list')

    

    def form_valid(self, form):

        user = form.save(commit=False)

        if self.request.FILES.get('profile_image'):
            user.profile_image = self.request.FILES.get('profile_image')

        user.set_password(form.cleaned_data['password'])

        role = Role.objects.get(role_code='SUPERADMIN')

        company_name = (self.request.POST.get('companyname') or '').strip()
        company = Company.objects.filter(
            Q(company_code__iexact=company_name) |
            Q(company_name__iexact=company_name)
        ).first()

        if company is None:
            company = Company.objects.order_by('id').first()

        if company is None:
            form.add_error(None, 'Please create a company before creating a user.')
            return self.form_invalid(form)

        user.role = role

        user.company = company

        user.is_company_user = False

        user.save()

        messages.success(
            self.request,
            'User created successfully.'
        )

        return redirect(
            self.success_url
        )

    def form_invalid(self, form):

        print(form.errors)

        return super().form_invalid(form)
    

class UserUpdateView(LoginRequiredMixin,SuperAdminRequiredMixin,UpdateView):

    model = User

    form_class = UserCreateForm

    template_name = ('accounts/user_management/user_create.html')

    success_url = reverse_lazy('accounts:user_list')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['page_title'] = 'Edit User'

        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['password'].required = False
        form.fields['confirm_password'].required = False
        return form

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save(commit=False)

            if self.request.FILES.get('profile_image'):
                user.profile_image = self.request.FILES.get('profile_image')

            password = (form.cleaned_data.get('password') or '').strip()
            if password:
                user.set_password(password)

            user.save()

        messages.success(self.request, 'User updated successfully.')
        return redirect(self.success_url)


class UserDetailView(LoginRequiredMixin,SuperAdminRequiredMixin,DetailView):

    model = User

    template_name = ('accounts/user_management/user_view.html')

    context_object_name = 'user_obj'

class UserDeleteView(LoginRequiredMixin,SuperAdminRequiredMixin,View):
    login_url = 'accounts:login'
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('accounts:user_list')
    
# -----------------------------------------------
# ============= Department =======================
# -----------------------------------------------

class DepartmentListView(LoginRequiredMixin,SuperAdminRequiredMixin,TemplateView):

    login_url = 'accounts:login'

    template_name = ('accounts/department/department_list.html')

# ================= Department Create ==============
class DepartmentCreateView(LoginRequiredMixin,SuperAdminRequiredMixin,TemplateView):

    login_url = 'accounts:login'

    template_name = ('accounts/department/department_create.html')

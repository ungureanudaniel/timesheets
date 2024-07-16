from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
from .models import UserProfile

User = get_user_model()

#==============user registration view============
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # access the registration form
        if form.is_valid():
            # fetch username and email from form
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            
            # Check if user already exists
            try:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists. Please choose a different username.')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email address already exists. Please use a different email.')
                else:
                    user = form.save()

                    # Notify admins and supervisors via email
                    subject = 'New User Access Request'
                    html_message = render_to_string('registration/registration_notice_email.html', {
                        'username': user.username,
                        'email': user.email,
                    })
                    plain_message = strip_tags(html_message)
                    admins = User.objects.filter(groups__name='ADMIN').values_list('email', flat=True)
                    supervisors = User.objects.filter(groups__name='SUPERVISOR').values_list('email', flat=True)
                    recipients = list(admins) + list(supervisors)
                    
                    send_mail(
                        subject,
                        plain_message,
                        settings.EMAIL_HOST_USER,  # Sender's email address
                        recipients,
                        html_message=html_message,
                    )
                    
                    # success message
                    messages.success(request, 'Registration successful. Your account is pending approval.')

                    # redirect the user to login into the profile page with newly created credentials, but with an inactive account
                    return render(request, 'registration/profile.html')
            except Exception as e:
                print(e)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

#==============user login view==============
class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        return reverse('profile', args=[user.username])

#==============user profile view============
@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    if user.is_approved:
        context = {
            'user': user,
            'is_approved': user.is_approved,
        }
    else:
        context = {
            'user': user,
            'message': 'Account not approved! Wait for approval.'
        }
    
    return render(request, 'registration/profile.html', context)

#============user profile editing====================
class ProfileEditView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'registration/profile_updater.html'
    context_object_name = 'user'
    pk_url_kwarg = 'pk'  # If using 'id', change this to 'id_url_kwarg = 'id' 
    fields = ['bio', 'avatar']

    def get_object(self, queryset=None):
        return self.request.user  # Return the current logged-in user object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data here if needed
        return context
#==============password change view=====================
@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password has been successfully updated.')
            return redirect('profile')  # Replace 'profile' with your actual profile URL name
    else:
        form = PasswordChangeForm(user=request.user)
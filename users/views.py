from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
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
        form = CustomUserCreationForm(request.POST)#access the registration form
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
            except Exception as e:
                print(e)
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
            #  success message
            messages.success(request, 'Registration successful. Your account is pending approval.')

            # redirect the user to login into the profile page with newly creation credentials, but with inactve account
            return render(request, 'registration/profile.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
#==============user profile view============
@login_required
def profile(request):
    user=request.user
    if user.is_approved:
        return render(request, 'registration/profile.html', {'user': user})
    else:
        return render(request, 'registration/profile.html', {'user': user, 'message': 'Account not approved! Wait for approval.'})
    context = {
        'user': request.user  # This will pass the logged-in user's information to the template
    }
    return render(request, 'registration/profile.html', context)
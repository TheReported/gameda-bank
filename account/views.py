from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from bank_account.models import BankAccount
from card.models import Card

from .forms import ProfileEditForm, UserEditForm, UserRegistrationForm
from .models import Profile
from .utils import Status


@login_required
def activity(request):
    accounts = BankAccount.active.filter(user=request.user)
    cards = Card.active.filter(user=request.user)
    return render(
        request,
        'account/dashboard.html',
        {'section': 'dashboard', 'accounts': accounts, 'cards': cards},
    )


def show_main(request):
    return render(request, 'base.html', {'section': 'base'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form}
    )


@login_required
@require_POST
def discharge(request, code):
    user = get_object_or_404(User, code=code, status=Status.ACTIVE)
    user.status = Status.DISCHARGE
    user.save()
    messages.success(request, 'You have discharge your bank account successfully')
    return redirect('bank_account:display')

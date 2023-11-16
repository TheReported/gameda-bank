from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from bank_account.models import BankAccount
from card.models import Card
from transaction.models import Transaction

from .forms import ProfileEditForm, UserEditForm, UserRegistrationForm
from .models import Profile


def show_main(request):
    if request.user.is_authenticated:
        return redirect('activity')

    return render(request, 'additional_content.html', {'section': 'base'})


@login_required
def activity(request):
    bank_accounts = BankAccount.active.filter(user=request.user)
    rich_bank_account = bank_accounts.first()
    cards = []
    transactions = []

    for bank_account in bank_accounts:
        transaction = Transaction.objects.filter(Q(sender=bank_account.code) | Q(cac=bank_account))
        transactions.extend(transaction)
        cards.extend(bank_account.cards.all())

    most_payments_card = (
        Card.objects.filter(payments_card__ccc__in=cards)
        .annotate(num_payments=Count('payments_card'))
        .order_by('-num_payments')
        .first()
    )

    return render(
        request,
        'account/dashboard.html',
        {
            'section': 'dashboard',
            'bank_account': rich_bank_account,
            'card': most_payments_card,
        },
    )


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
def discharge(request):
    request.user.is_active = False
    request.user.save()
    messages.success(request, 'You have discharge your account successfully')
    return redirect('main')

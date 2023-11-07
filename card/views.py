from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from bank_account.models import BankAccount
from payment.models import Payment

from .forms import CardForm
from .models import Card


@login_required
def detail(request, id):
    payments = Payment.objects.filter(id=id)
    return render(
        request,
        'card/detail.html',
        {'section': 'cards', 'payments': payments},
    )


@login_required
def display_card(request):
    cards = Card.objects.filter(user=request.user)
    return render(
        request,
        'display_card.html',
        {'section': 'cards', 'cards': cards},
    )


@login_required
def create(request):
    if request.method == 'POST':
        card_form = CardForm(request.POST)
        if card_form.is_valid():
            card = card_form.save(commit=False)
            card.user = request.user
            card.save()
            messages.success(request, "You have created a Card successfully")
            return redirect('card:display')

        else:
            messages.error(request, "There has been an error creating your card")
    else:
        card_form = CardForm()
    return render(request, "card/create.html", {'section': 'cards', "card_form": card_form})


@login_required
def create_done(request):
    return render(
        request,
        'card/done.html',
        {'section': 'cards'},
    )

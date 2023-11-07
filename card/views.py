from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from account.status import ACTIVE
from payment.models import Payment

from .forms import CardEditForm, CardForm
from .models import Card


@login_required
def detail(request, id):
    card = get_object_or_404(Card, id=id)
    payments = Payment.objects.filter(ccc=card.id)
    return render(
        request,
        'card/detail.html',
        {'section': 'cards', 'payments': payments, 'card': card},
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


@login_required
def edit(request, id):
    card = get_object_or_404(Card, id=id, status=ACTIVE)
    if request.method == 'POST':
        card_edit_form = CardEditForm(instance=card, data=request.POST)
        if card_edit_form.is_valid():
            card_edit_form.save()
            messages.success(request, 'You have edited your card successfully.')
            return redirect('card:display')
        messages.error(request, 'There has been an error editing your card.')
    else:
        card_edit_form = CardEditForm(instance=card)
    return render(
        request,
        'card/edit.html',
        {'section': 'cards', 'card_edit_form': card_edit_form, 'card': card},
    )

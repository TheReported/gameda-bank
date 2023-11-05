from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from bank_account.models import BankAccount

from .forms import CardForm
from .models import Card


@login_required
def card_detail(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    return render(request, "card/detail.html", {"card": card})


@login_required
def display_card(request):
    cards = Card.objects.filter(user=request.user)
    return render(
        request,
        'display_card.html',
        {'section': 'cards', 'cards': cards},
    )


@login_required
def create_card(request):
    bank_account = BankAccount.objects.filter(user=request.user).first()
    cards = Card.objects.filter(bank_account=bank_account)
    if request.method == "POST":
        card_form = CardForm(request.POST)
        if card_form.is_valid():
            card_form.save()
            messages.success(request, "You have created a Card successfully")
        else:
            messages.error(request, "There has been an error creating your card")
    else:
        card_form = CardForm()

    return render(
        request, "card/create.html", {'section': 'cards', "card_form": card_form, "cards": cards}
    )

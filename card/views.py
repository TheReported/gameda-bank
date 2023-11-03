from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from forms import CardForm
from models import Card


def card_detail(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    return render(request, "card_detail.html", {"card": card})


def create_card(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return HttpResponse("Su tarjeta ha sido creada satisfactoriamente")
    else:
        form = CardForm()

    return render(request, '', {'form': form})

from .models import Category
from .forms import CategoryForm, FlashcardForm
import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Flashcard
from .forms import TestCardForm

def index(request):
    return  render(request, 'flashcards/index.html')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_categories')
    else:
        form = CategoryForm()
    return render(request, 'flashcards/add_category.html', {'form': form})


def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'flashcards/list_categories.html', {'categories': categories})


def add_card(request):
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_cards')
        else:
            return render(request, 'flashcards/add_card.html', {'form':form})
    else:
        form = FlashcardForm()
    return render(request, 'flashcards/add_card.html', {'form': form})


def list_cards(request):
    cards = Flashcard.objects.select_related('category').all()
    return render(request, 'flashcards/list_cards.html', {'cards': cards})

def test_card(request):
    if request.method == 'POST':
        form = TestCardForm(request.POST)
        if form.is_valid():
            card_id = form.cleaned_data['card_id']
            user_translation = form.cleaned_data['user_translation']

            try:
                card = Flashcard.objects.get(id=card_id)
            except Flashcard.DoesNotExist:
                return HttpResponse("Ошибка: карточка не найдена.")

            if user_translation.lower() == card.translation.lower():
                return render(request, 'flashcards/test_card_result.html', {
                    'is_correct': True,
                    'card': card
                })
            else:
                return render(request, 'flashcards/test_card_result.html', {
                    'is_correct': False,
                    'card': card
                })
        else:
            return render(request, 'flashcards/test_card.html', {
                'form': form,
                'card_word': None
            })

    else:
        cards_count = Flashcard.objects.count()
        if cards_count == 0:
            return HttpResponse("Нет карточек для тренировки.")

        random_index = random.randint(0, cards_count - 1)
        card = Flashcard.objects.all()[random_index]

        form = TestCardForm(initial={'card_id': card.id})
        return render(request, 'flashcards/test_card.html', {
            'form': form,
            'card_word': card.word
        })

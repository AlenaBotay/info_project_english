from .models import Category
import re
from django import forms
from .models import Flashcard

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def clean_name(self):
        data = self.cleaned_data['name'].strip()
        if len(data) < 3:
            raise forms.ValidationError("Название категории должно содержать минимум 3 символа.")
        return data

RE_ENGLISH = re.compile(r'^[A-Za-z\s]+$')
RE_RUSSIAN = re.compile(r'^[А-Яа-яЁё\s]+$')

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['category', 'word', 'translation', 'meaning']

    def clean_word(self):
        data = self.cleaned_data['word'].strip()
        if not data:
            raise forms.ValidationError("Слово не может быть пустым.")
        if not RE_ENGLISH.match(data):
            raise forms.ValidationError("Поле «Слово» должно содержать только английские буквы.")
        return data

    def clean_translation(self):
        data = self.cleaned_data['translation'].strip()
        if not data:
            raise forms.ValidationError("Перевод не может быть пустым.")
        if not RE_RUSSIAN.match(data):
            raise forms.ValidationError("Поле «Перевод» должно содержать только русские буквы.")
        return data

class TestCardForm(forms.Form):
    card_id = forms.IntegerField(widget=forms.HiddenInput())
    user_translation = forms.CharField(label="Ваш перевод", max_length=100)

    def clean_user_translation(self):
        data = self.cleaned_data['user_translation'].strip()
        if not data:
            raise forms.ValidationError("Введите хотя бы один символ.")
        return data

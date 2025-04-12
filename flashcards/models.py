from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Flashcard(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='flashcards')
    word = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    meaning = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.word} - {self.translation}"

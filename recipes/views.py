from django.shortcuts import render

from recipes.models import Recipe

def home_page(request):
    recipe = Recipe.objects.first()
    return render(request, 'recipes/home.html', {'recipe': recipe})

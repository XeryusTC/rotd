import datetime
from django.shortcuts import render

from recipes.models import Recipe

def todays_recipe(day=datetime.date.today()):
    try:
        target = (day.month * day.day + day.year) % \
            Recipe.objects.filter(add_date__lt=datetime.date.today()).count()
        return Recipe.objects.all()[target]
    except:
        pass

def home_page(request):
    recipe = todays_recipe()
    return render(request, 'recipes/home.html', {'recipe': recipe})

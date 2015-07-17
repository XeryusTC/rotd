from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db.utils import IntegrityError

from recipes.models import Recipe

class RecipeModelTests(TestCase):
    def test_recipe_has_name(self):
        r = Recipe(name='test') # Should not raise exception

    def test_recipe_name_required(self):
        r = Recipe.objects.create(name='')
        with self.assertRaises(ValidationError):
            r.full_clean()

    def test_recipe_name_is_unique(self):
        r1 = Recipe.objects.create(name='test recipe')
        r1.save()
        with self.assertRaises(IntegrityError):
            r2 = Recipe.objects.create(name='test recipe')

    def test_string_representation(self):
        recipe = Recipe.objects.create(name='test recipe')
        self.assertEquals(str(recipe), 'test recipe')

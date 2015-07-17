from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db.utils import IntegrityError

from recipes.models import Recipe

class RecipeModelTests(TestCase):
    def create_minimal_recipe(self, **kwargs):
        values = {'name': 'Test recipe', 'description': 'test description'}
        values.update(kwargs)
        return Recipe(**values)

    def test_recipe_has_name_and_description(self):
        self.create_minimal_recipe() # Should not raise exception

    def test_recipe_name_required(self):
        r = self.create_minimal_recipe(name='')
        with self.assertRaises(ValidationError):
            r.full_clean()

    def test_recipe_description_required(self):
        r = self.create_minimal_recipe(description='')
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

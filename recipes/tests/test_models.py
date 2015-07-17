from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db.utils import IntegrityError

from recipes.models import Recipe
from recipes import factories

class RecipeModelTests(TestCase):
    def test_recipe_has_name_and_description(self):
        Recipe.objects.create(name='Test recipe',
                description='Recipe description')

    def test_recipe_name_required(self):
        r = factories.RecipeFactory(name='')
        with self.assertRaises(ValidationError):
            r.full_clean()

    def test_recipe_description_required(self):
        r = factories.RecipeFactory(description='')
        with self.assertRaises(ValidationError):
            r.full_clean()

    def test_recipe_name_is_unique(self):
        r1 = factories.RecipeFactory(name='Test recipe')
        r1.save()
        with self.assertRaises(IntegrityError):
            r2 = factories.RecipeFactory(name='Test recipe')

    def test_string_representation(self):
        recipe = factories.RecipeFactory(name='test recipe')
        self.assertEquals(str(recipe), 'test recipe')

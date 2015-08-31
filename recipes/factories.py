import datetime
import factory

class RecipeFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'recipes.Recipe'

    name = factory.Sequence(lambda n: 'Recipe %d' % n)
    description = factory.Sequence(
        lambda n: 'Some description %d' %n)

    @factory.post_generation
    def post(obj, create, extracted, **kwargs):
        if not extracted:
            obj.add_date = datetime.date.today() - datetime.timedelta(days=1)

class IngredientFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'recipes.Ingredient'

    name = factory.Sequence(lambda n: 'Ingredient %d' % n)

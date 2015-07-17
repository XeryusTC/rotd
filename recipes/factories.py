import factory

class RecipeFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'recipes.Recipe'

    name = factory.Sequence(lambda n: 'Recipe %d' % n)
    description = factory.Sequence(
        lambda n: 'Some description %d' %n)

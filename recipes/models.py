# -*- coding: utf-8 -*-
# ROTD suggest a recipe to cook for dinner, changing the recipe every day.
# Copyright © 2015 Xeryus Stokkel

# ROTD is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.

# ROTD is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.

# You should have received a copy of the GNU General Public License
# along with ROTD.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from django.template.defaultfilters import slugify

class Recipe(models.Model):
    name = models.CharField(max_length=64, blank=False, default='',
            unique=True)
    description = models.TextField(default='')
    add_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(default='', unique=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super(Recipe, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('recipes:recipe', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    GRAM  = 'gr'
    LITRE = 'cL'
    CLOVE = 'co'
    TYPE_CHOICES = (
            (GRAM, 'gram'),
            (LITRE, 'centiliter'),
            (CLOVE, 'teen'),
        )

    name = models.CharField(max_length=64, blank=False, default='')
    used_in = models.ManyToManyField(Recipe, blank=True,
            through='IngredientUsage', related_name='ingredient_set')
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, blank=True)

    def __str__(self):
        if self.type == '':
            return self.name
        else:
            return "{name} ({type})".format(name=self.name,
                    type=self.get_type_display())

class IngredientUsage(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    quantity = models.IntegerField()

    def __str__(self):
        return "{qty} {name}".format(qty=self.quantity,
                name=self.ingredient.name)

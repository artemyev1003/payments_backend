from django.db import models
from django.utils.translation import gettext_lazy as _


class Item(models.Model):
    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')

        ordering = ['name']

    name = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'))
    price = models.IntegerField(_('price'), default=0)  # in cents

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)

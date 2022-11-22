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
        return '{0:.2f}'.format(self.price / 100)


class Order(models.Model):
    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    description = models.TextField(_('description'))

    def __str__(self):
        return 'Order ({})'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='order_item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.item.price * self.quantity


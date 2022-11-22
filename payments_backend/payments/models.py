from django.db import models
from django.utils.translation import gettext_lazy as _


class Item(models.Model):
    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')

        ordering = ['name']

    name = models.CharField(_('name'), max_length=255)
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

    name = models.CharField(_('name'), max_length=255, null=True)
    description = models.TextField(_('description'), null=True)
    items = models.ManyToManyField(Item, through='OrderItem')

    def __str__(self):
        return 'Order ({})'.format(self.name)

    @property
    def get_total_cost(self):
        return sum(oi.get_cost for oi in self.orderitem_set.all())

    @property
    def get_display_total_cost(self):
        return '{0:.2f}'.format(self.get_total_cost / 100)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    @property
    def get_cost(self):
        return self.item.price * self.quantity

    @property
    def get_display_cost(self):
        return '{0:.2f}'.format(self.get_cost / 100)


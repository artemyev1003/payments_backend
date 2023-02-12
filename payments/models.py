from django.db import models
from django.utils.translation import gettext_lazy as _


class Item(models.Model):

    class Currency(models.TextChoices):
        USD = 'usd'
        RUB = 'rub'

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'))
    price = models.IntegerField(_('price'), default=0)  # in cents / kopecks
    currency = models.CharField(_('currency'), max_length=20,
                                choices=Currency.choices, default=Currency.USD)

    def __str__(self):
        return self.name

    def get_display_price(self):
        return '{0:.2f}'.format(self.price / 100)

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ['name']


class Discount(models.Model):
    name = models.CharField(_('name'), max_length=255, null=True)
    percent_off = models.DecimalField(_('percent off'), max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('discount')
        verbose_name_plural = _('discounts')
        ordering = ['name']


class Tax(models.Model):
    name = models.CharField(_('name'), max_length=255, null=True)
    percentage = models.DecimalField(_('percentage'), max_digits=6, decimal_places=4)
    inclusive = models.BooleanField(_('inclusive'), default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('tax')
        verbose_name_plural = _('taxes')
        ordering = ['name']


class Order(models.Model):

    class Currency(models.TextChoices):
        USD = 'usd'
        RUB = 'rub'

    name = models.CharField(_('name'), max_length=255, null=True)
    description = models.TextField(_('description'), null=True)
    items = models.ManyToManyField(Item, through='OrderItem', verbose_name=_('items'))
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, blank=True,
                                 null=True, verbose_name=_('discount'))
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, blank=True,
                            null=True, verbose_name=_('tax'))
    currency = models.CharField(_('currency'), max_length=20,
                                choices=Currency.choices, default=Currency.USD)

    def __str__(self):
        return self.name

    @property
    def get_total_cost(self):
        return sum(oi.get_cost for oi in self.orderitem_set.all())

    @property
    def get_display_total_cost(self):
        return '{0:.2f}'.format(self.get_total_cost / 100)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ['name']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('order'))
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name=_('item'))
    quantity = models.PositiveIntegerField(_('quantity'), default=1)

    def __str__(self):
        return '{}'.format(self.id)

    @property
    def get_cost(self):
        return self.item.price * self.quantity

    @property
    def get_display_cost(self):
        return '{0:.2f}'.format(self.get_cost / 100)

    class Meta:
        verbose_name = _('ordered item')
        verbose_name_plural = _('ordered items')

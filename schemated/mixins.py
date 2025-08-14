from django.db import models

class PricingMixin(models.Model):
    """Mixin that provides pricing-related fields for models."""
    class Meta:
        abstract = True
        
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    delivery = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_price = kwargs.get('total_price', 0.0)
        self.taxes = kwargs.get('taxes', 0.0)
        self.delivery = kwargs.get('delivery', False)
    
    def get_total_with_taxes(self):
        """Calculate total price including taxes."""
        return self.total_price + self.taxes
    
    def get_final_price(self):
        """Calculate final price including taxes and delivery if applicable."""
        total = self.get_total_with_taxes()
        if hasattr(self, 'delivery_fee') and self.delivery:
            total += getattr(self, 'delivery_fee', 0)
        return total
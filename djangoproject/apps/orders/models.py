from django.db import models, transaction
import datetime
from apps.items.models import Product



def generate_order_id():
    today_str = datetime.date.today().strftime('%Y%m%d')
    last_order = Order.objects.filter(created_at__date=datetime.date.today()).order_by('id').last()
    if last_order:
        try:
            last_number = int(last_order.order_id.split('-')[-1])
        except:
            last_number = 0
    else:
        last_number = 0
    new_number = last_number + 1
    return f'ORD{today_str}-{new_number:03d}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Shipped', 'Shipped'),
        ('Done', 'Done'),
        ('Canceled', 'Canceled'),
    ]

    order_id = models.CharField(max_length=20, unique=True, default=generate_order_id)
    product = models.ForeignKey('items.Product', on_delete=models.CASCADE, related_name="orders")

    # Informasi pembeli
    buyer_name = models.CharField(max_length=100, default="Unknown")
    buyer_phone = models.CharField(max_length=20, default="-")
    buyer_gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female')],
        default='Other'
    )
    buyer_age = models.PositiveIntegerField(default=0)

    # 🟢 Tambahan untuk wilayah
    city = models.CharField(max_length=100, default="-")   # Kota/Kecamatan
    region = models.CharField(max_length=100, default="-") # Kabupaten/Daerah
    address = models.TextField(default="-")

    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    proof_image = models.ImageField(upload_to='bukti_transfer/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        """Kurangi stok saat order dibuat."""
        is_new = self._state.adding
        self.total_price = self.product.price * self.quantity

        if is_new:
            # Order baru => kurangi stok produk
            self.product.reduce_stock(self.quantity)
        else:
            # Jika order diedit => sesuaikan stok
            old_order = Order.objects.get(pk=self.pk)
            diff_qty = self.quantity - old_order.quantity
            if diff_qty != 0:
                self.product.reduce_stock(diff_qty)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} - {self.buyer_name} ({self.status})"


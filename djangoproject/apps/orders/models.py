from django.db import models
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


# ========================
# ORDER MODEL
# ========================
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Shipped', 'Shipped'),
        ('Done', 'Done'),
        ('Canceled', 'Canceled'),
    ]

    order_id = models.CharField(max_length=20, unique=True, default=generate_order_id)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    buyer_name = models.CharField(max_length=100, default="Unknown")  # default buyer_name
    buyer_phone = models.CharField(max_length=20, default="-")        # default kosong
    buyer_gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        default='Other'   # kasih default
    )
    buyer_birth = models.DateField(default=datetime.date.today)  # default hari ini (biar nggak error)
    address = models.TextField(default="-")                      # alamat kosong
    quantity = models.PositiveIntegerField(default=1)            # minimal 1
    total_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    proof_image = models.ImageField(upload_to='bukti_transfer/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # hitung total harga otomatis
        self.total_price = self.product.price * self.quantity

        # jika order sudah dibayar/done → update stok & sold
        if self.status in ['Paid', 'Done']:
            if self.product.stock >= self.quantity:
                self.product.stock -= self.quantity
                self.product.sold += self.quantity
                self.product.save()
            else:
                raise ValueError("Stok produk tidak cukup!")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} - {self.buyer_name} ({self.status})"

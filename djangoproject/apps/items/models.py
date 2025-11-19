from django.db import models

class Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='produk/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    ram = models.CharField(max_length=50, blank=True, null=True)
    memory = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    def reduce_stock(self, quantity: int):
        """Kurangi stok & tambahkan jumlah produk terjual."""
        if self.stock >= quantity:
            self.stock -= quantity
            self.sold += quantity
            self.save()
        else:
            raise ValueError(f"Stok tidak cukup untuk {self.name}. Tersisa {self.stock}")

    def __str__(self):
        return f"{self.name} ({self.ram}/{self.memory}) - Stok: {self.stock}, Terjual: {self.sold}"

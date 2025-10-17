from django import forms
from apps.items.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['sold']  # Exclude the sold field since it's tracked separately
        
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}), 
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'min': '0'}),
        }
        
        labels = {
            'name': 'Nama Produk',
            'image': 'Gambar Produk',
            'description': 'Deskripsi Produk',
            'price': 'Harga (IDR)',
            'stock': 'Stok Awal',
            'ram': 'RAM',
            'memory': 'Memori Internal',
            'color': 'Warna',
          
        }
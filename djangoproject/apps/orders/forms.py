from django import forms
from .models import Order
from apps.items.models import Product


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['buyer_name', 'buyer_gender', 'buyer_age', 'region', 'quantity', 'buyer_phone', 'address', 'quantity','city']
        exclude = ['order_id', 'product', 'total_price', 'status', 'proof_image', 'created_at']
        
    def __init__(self, *args, **kwargs):
        # Ambil produk agar bisa atur batas quantity sesuai stok
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        
        # Set batas maksimum quantity berdasarkan stok produk
        if self.product:
            self.fields['quantity'].widget.attrs.update({
                'max': self.product.stock,
                'min': 1
            })
        
        # Tambahkan kelas Tailwind untuk styling form
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.NumberInput, forms.EmailInput, forms.DateInput)):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition'
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition'
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition',
                    'rows': 3
                })
            
            # Tambahkan placeholder
            placeholders = {
                'buyer_name': 'Masukkan nama lengkap Anda',
                'buyer_age': 'Masukkan umur Anda',
                'region': 'Masukkan nama kecamatan',
                'city': 'Masukkan nama kabupaten/kota',
                 'address': 'Masukkan detail alamat',
                 'buyer_phone':'082314678220',
                'quantity': f'Masukkan jumlah (maks: {self.product.stock if self.product else 10})'
            }
            if field_name in placeholders:
                field.widget.attrs.update({'placeholder': placeholders[field_name]})

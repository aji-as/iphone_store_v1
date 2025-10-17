from django import forms
from .models import Order
from apps.items.models import Product


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['buyer_name', 'buyer_phone', 'buyer_gender', 'buyer_birth', 'address', 'quantity']
        exclude = ['order_id', 'product', 'total_price', 'status', 'proof_image', 'created_at']
        
    def __init__(self, *args, **kwargs):
        # Accept product as a parameter to set the initial value
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        
        # Set quantity max value based on product stock
        if self.product:
            self.fields['quantity'].widget.attrs.update({
                'max': self.product.stock,
                'min': 1
            })
        
        # Add Tailwind classes to form fields
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
            
            # Add placeholders
            placeholders = {
                'buyer_name': 'Masukkan nama lengkap Anda',
                'buyer_phone': 'Masukkan nomor telepon Anda',
                'address': 'Masukkan alamat lengkap Anda',
                'quantity': f'Masukkan jumlah (maks: {self.product.stock if self.product else 10})'
            }
            if field_name in placeholders:
                field.widget.attrs.update({'placeholder': placeholders[field_name]})


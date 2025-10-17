project_name/
│
├── project_name/              # folder utama project (settings)
│   ├── __init__.py
│   ├── settings.py            # konfigurasi project
│   ├── urls.py                # routing global
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                      # kumpulan aplikasi (dibuat manual agar rapi)
│   ├── products/              # app untuk produk
│   │   ├── models.py          # tabel Product
│   │   ├── views.py           # view product (list/detail)
│   │   ├── urls.py            # routing khusus produk
│   │   └── templates/products/
│   │       └── ...
│   │
│   ├── orders/                # app untuk pesanan
│   │   ├── models.py          # tabel Order
│   │   ├── views.py           # checkout, status pesanan
│   │   ├── urls.py
│   │   └── templates/orders/
│   │       └── ...
│   │
│   ├── buyers/                # app untuk pembeli
│   │   ├── models.py          # tabel Buyer
│   │   ├── views.py           # profil, registrasi
│   │   ├── urls.py
│   │   └── templates/buyers/
│   │       └── ...
│   │
│   └── dashboard/             # app untuk seller
│       ├── views.py           # CRUD produk, kelola pesanan
│       ├── urls.py
│       └── templates/dashboard/
│           └── ...
│
├── static/                    # file statis (css, js, img)
├── media/                     # upload (gambar produk, bukti transfer)
├── templates/                 # template global (base.html dll)
└── manage.py

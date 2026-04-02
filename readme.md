src/
│
├── app/
│   ├── main.py
│   └── dependencies.py
│
├── modules/
│   ├── product/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   ├── controllers.py
│   │   └── cache.py
|   |
|   ├── auth/
|   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   ├── controllers.py
│   │   └── security.py     //JWT w hashing
│
├── infrastructure/
│   ├── database/
│   ├── cache/
│   ├── http/              //httpx requests
│   ├── storage/
│   └── external/
│
├── ai/
└── tests/
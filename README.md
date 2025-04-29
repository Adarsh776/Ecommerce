# ShopEzy - E-commerce Platform

ShopEzy is a modern e-commerce platform built with Django, featuring a responsive design and comprehensive product management system.

## Features

- 🛍️ **Product Management**
  - Product categories and subcategories
  - Product variants with different attributes
  - Digital and physical products support
  - Product images and descriptions

- 🔍 **Search & Navigation**
  - Advanced product search
  - Category-based browsing
  - Product filtering

- 👤 **User Management**
  - User registration and authentication
  - User profiles
  - Order history

- 🛒 **Shopping Features**
  - Shopping cart
  - Wishlist
  - Product reviews and ratings
  - Secure checkout process

- 💳 **Payment Integration**
  - Multiple payment methods
  - Secure payment processing
  - Order tracking

## Tech Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (Development), PostgreSQL (Production)
- **Authentication**: Django Authentication System
- **Payment Processing**: Integration with major payment gateways

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Adarsh776/Ecommerce
cd Ecommerce
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

```
shopezzy/
├── coreapp/              # Main application
│   ├── models.py         # Database models
│   ├── views.py          # View logic
│   ├── urls.py           # URL routing
│   └── admin.py          # Admin interface
├── authentication/       # User authentication
├── orderapp/            # Order management
├── templates/           # HTML templates
├── static/              # Static files
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   └── img/            # Images
└── manage.py           # Django management script
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django Documentation
- Bootstrap for frontend components
- Font Awesome for icons

## Contact

Adarsh S - [@yourtwitter](https://twitter.com/yourtwitter)
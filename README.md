README.md

# E-Commerce Flask Application

This is a simple e-commerce web application built using Flask. The application allows managing products, categories, and a shopping cart system. It includes both admin and user functionalities for a seamless experience.

---

## **Features**
1. **Product Management**:
   - Add, edit, and delete products.
   - Products have fields: `name`, `price`, `description`, `image_url`, and `category`.

2. **Category Management**:
   - Products are grouped into categories.
   - Categories can be added and selected for products.

3. **Shopping Cart**:
   - Add products to the cart.
   - Increase or decrease product quantities in the cart.
   - Clear all products from the cart.

4. **User Interface**:
   - User-friendly navigation with Bootstrap.
   - Separate admin panel for managing products.

---

## **Technologies Used**
- **Backend**: Flask, Flask-SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript (with Fetch API)
- **Styling**: Bootstrap 4
- **Migrations**: Flask-Migrate (for database version control)

---

## **Setup Instructions**

### **1. Clone the repository**
```bash
git clone https://github.com/Ahmed120112/ecommerce-products-flask.git
cd ecommerce-flask

2. Create a virtual environment

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Initialize the database

If the database does not exist or needs to be reset:

rm e_commerce.db  # Remove the old database (optional)
flask db init     # Initialize migrations
flask db migrate  # Create migrations for the database
flask db upgrade  # Apply migrations

5. Run the application

python app.py

The application will be available at: http://127.0.0.1:8080

Project Structure

ecommerce-flask/
│
├── app.py               # Main application file
├── models.py            # Database models
├── requirements.txt     # Python dependencies
├── migrations/          # Flask-Migrate files for database migrations
├── templates/           # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── products.html    # Product listing template
│   ├── admin_products.html  # Admin product management template
│
├── static/              # Static files
│   ├── css/             # Custom stylesheets
│   ├── js/              # JavaScript files
│
├── e_commerce.db        # SQLite database file
└── README.md            # Project documentation

Endpoints

1. User Endpoints

Method	Endpoint	Description
GET	/	View all products.
GET	/category/<int:category_id>	View products by category.
POST	/add_to_cart	Add product to cart.
POST	/increase_quantity	Increase product quantity in cart.
POST	/decrease_quantity	Decrease product quantity in cart.
POST	/clear_cart	Clear the cart.

2. Admin Endpoints

Method	Endpoint	Description
GET	/admin/products	Manage products.
POST	/admin/products/add	Add a new product.
POST	/admin/products/update/<int:product_id>	Update a product.
POST	/admin/products/delete/<int:product_id>	Delete a product.

Key Files

1. models.py

Defines the database models:
	•	Product: Represents the products with fields: id, name, price, description, image_url, category_id.
	•	Category: Represents the product categories with fields: id, name.
	•	Cart: Represents the shopping cart items.

2. app.py

The main Flask application file that handles:
	•	Routes for user and admin functionalities.
	•	Database initialization and management.
	•	API endpoints for CRUD operations and cart functionality.

3. HTML Templates

	•	base.html: Base template with navigation.
	•	products.html: Displays all products or products by category.
	•	admin_products.html: Admin panel for managing products.

Example Usage

Adding a Product

	1.	Go to /admin/products.
	2.	Fill out the product form (name, price, description, image URL, and category).
	3.	Click “Add Product”.

Shopping Cart

	1.	Go to the homepage (/).
	2.	Click “Add to Cart” on any product.
	3.	Open the cart sidebar using the “View Cart” button.
	4.	Increase/decrease quantity or clear the cart.

Troubleshooting

1. Database Locked Error

If you encounter database is locked:
	•	Ensure no other processes are accessing the database.
	•	Use SQLite in single-thread mode: sqlite:///e_commerce.db?check_same_thread=False.

2. Internal Server Error (500)

	•	Check the logs in the terminal for detailed error messages.
	•	Ensure all required fields are provided in the form.

3. JavaScript Errors

	•	Open the browser’s Developer Tools (F12) and check the Console and Network tabs for errors.

Future Improvements

	1.	User authentication system.
	2.	Enhanced cart features (e.g., checkout, payment integration).
	3.	Improved UI/UX with animations.
	4.	Support for multiple languages.

License

This project is licensed under the MIT License.

---

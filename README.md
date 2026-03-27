# Construction Materials E-Commerce Platform

This is a comprehensive e-commerce web application built using Django, designed specifically for buying and selling construction materials. The platform supports two primary user roles: Buyers and Sellers, allowing seamless management of products, wishlists, and shopping carts.

## Features

*   **User Authentication & Management:**
    *   Secure Signup, Login, and Logout functionality.
    *   Password management (Forgot Password, OTP verification, Reset Password, Change Password).
    *   User Profiles with customizable avatars and details.
*   **Dual User Roles:**
    *   **Buyers:** Browse products, add items to cart or wishlist, and proceed to checkout.
    *   **Sellers:** Add, edit, manage, and delete their own construction material products.
*   **Product Management:**
    *   Wide range of supported categories including Cement, Bricks, Rebars, Concrete Bricks, Concrete Block, Soil, and Patthar.
    *   Sellers can specify product details, brand/company (e.g., UltraTech, Jindal, Trishul), pricing, descriptions, and upload product images.
    *   Individual product detail pages.
*   **Shopping Experience:**
    *   **Cart System:** Users can add products to their cart, update quantities, and view total prices.
    *   **Wishlist:** Save products for later viewing and easy access.
    *   **Checkout Process:** Integrated order placement workflow.
*   **Responsive Design:**
    *   Built with HTML templates ensuring a smooth experience across different devices.

## Technology Stack

*   **Backend:** Python, Django Web Framework
*   **Database:** SQLite (default for development)
*   **Frontend:** HTML, CSS, JavaScript (Django Templates)
*   **Media Management:** Built-in Django capabilities for handling images (User Profiles & Product Images).

## Project Structure

*   `myenv/`: Contains the Python virtual environment.
*   `myproject/`: The main Django project directory containing configuration (`settings.py`, `urls.py`).
    *   `myapp/`: The core Django application containing models, views, and logic.
        *   `models.py`: Defines the database schema (`User`, `Product`, `Wishlist`, `Cart`).
        *   `views.py`: Contains the application logic for all routes.
        *   `urls.py`: Maps URLs to their respective views.
        *   `templates/`: Contains all HTML templates for rendering the frontend.

## How to Run Locally

1. **Activate the Virtual Environment:**
   ```bash
   # On Windows
   myenv\Scripts\activate
   ```
2. **Navigate to the Project Directory:**
   ```bash
   cd myenv/myproject
   ```
3. **Apply Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
   The site will be available at `http://127.0.0.1:8000/`.

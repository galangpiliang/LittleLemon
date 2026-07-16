# Little Lemon Restaurant API 🌻

This repository contains the backend REST API for the **Little Lemon Restaurant**, built using **Django**, **Django REST Framework (DRF)**, and **Djoser**.

---

## 📓 Project Origin

This project was developed as the final peer-graded assessment for the **Meta APIs Course** on **Coursera**.

> ⚠️ **Important Notice for Reviewers & Readers:**  
> Per the official course instructions, the local SQLite database (`db.sqlite3`) and a `notes.txt` file containing testing credentials have been deliberately committed and included in this repository. This allows peer reviewers to test user groups and roles immediately without manual configuration.

---

## 🚅 Key Features Implemented

The API supports full role-based access control (RBAC) across four distinct user groups:

* **Admin:** Manage user groups, add categories, and create menu items.
* **Managers:** Assign users to the delivery crew, assign orders, and update the "Item of the Day".
* **Delivery Crew:** Access assigned orders and update order delivery statuses.
* **Customers:** Register, authenticate via tokens, browse menu items (with pagination, filtering, and sorting), manage a shopping cart, and place orders.

---

## 🔌 Tech Stack

* **Framework:** Django & Django REST Framework (DRF)
* **Authentication:** Djoser (Token-based authentication)
* **Database:** SQLite
* **Environment Management:** Pipenv

---

## 🏠 Local Setup Instructions

To run and test this API locally, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/galangpiliang/LittleLemon.git
cd LittleLemon
```

### 2. Install dependencies and activate the virtual environment

Ensure you have `pipenv` installed.

```bash
pipenv install
pipenv shell
```

### 3. Run database migrations

If making database updates:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Start the development server

```bash
python manage.py runserver
```

The API will be accessible locally at:

```
http://127.0.0.1:8000/
```

---

## 🧪 Testing & User Credentials

To test features such as ordering, sorting, and user role separation, refer to the **`notes.txt`** file in the root directory.

It contains pre-configured credentials for:

* **Admin/Superuser account**
* **Manager account**
* **Delivery Crew account**
* **Customer account**

You can use these credentials to log in via the browsable API or through an API client such as **Insomnia** or **Postman**.
# Transportation Management System (Django)

This Django-based web application allows a transportation company to manage trips, ticket bookings, payments, and user roles (Admin, Staff, Driver, Passenger).

## Key Features

-  **Role-Based Login**: Admin, Staff, Driver, and Passenger dashboards.
-  **Trip Booking**: Passengers can book seats with automatic seat availability check.
-  **Payments**: Each ticket has an associated payment entry.
-  **Notifications**: Passengers get notified upon successful booking.
-  **Staff/Driver/Admin Views**: Access-specific pages for data and actions.
-  **API Endpoints**: Exposed REST APIs for tickets, trips, and notifications.

## Project Structure

```bash
transport_system/
├── core/                # Main app with models, views, forms, APIs
├── templates/           # HTML templates for each role and page
├── static/              # Static files (CSS, JS, etc.)
├── manage.py            # Django project runner
├── db.sqlite3           # Database 
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation

| Role      | Abilities                                     |
| --------- | --------------------------------------------- |
| Admin     | View revenue reports, all data access         |
| Staff     | View all trips, tickets, and payments         |
| Driver    | View assigned trips, report trip status       |
| Passenger | Search trips, book tickets, get notifications |

API Endpoints
POST /api/book-ticket/ → Book a ticket (auth required)
GET /api/my-tickets/ → Passenger's ticket history
GET /api/trips/ → List of available trips
GET /api/my-notifications/ → View booking notifications

Future Improvements:
Real-time bus tracking via GPS
OTP/email verification
Payment gateway integration

To run this project:
Clone the repo--
git clone https://github.com/SomayaElgendy/transportation-system.git
cd transportation-system

Create and activate virtual environment--
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On macOS/Linux

Run pip install -r requirements.txt

Apply migrations and create a superuser--
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

Launch the dev server with python manage.py runserver
Visit http://127.0.0.1:8000

Run tests--
python manage.py test

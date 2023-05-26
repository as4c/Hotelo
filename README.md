# Hotel Booking Django App

This is a Django web application for hotel booking. It provides users with the ability to book hotels, check hotel availability, manage check-in and checkout, view hotel details, write reviews, and process online payments using the Stripe API.

## Features

- User Authentication: Users can register, log in, and manage their accounts.
- Book a New Hotel: Users can search for hotels, select dates, and make bookings.
- Check Hotel Availability: Users can check the availability of hotels for specific dates.
- Check-in and Checkout: Users can manage their check-in and checkout dates.
- Hotel Detail Description: Users can view detailed information about hotels, including amenities, room types, and location.
- Write Hotel Rating Reviews: Users can write and submit reviews/ratings for hotels they have stayed in.
- Online Booking with Stripe: Integrated Stripe payment API for secure online payment processing.

## Installation

1. Clone the repository:
'''
git clone https://github.com/as4c/Hotelo.git
'''

2. Change into the project directory:
3. Create a virtual environment:
'''
python3 -m venv env
'''

4. Activate the virtual environment:
- For Linux/Mac:
  ```
  source env/bin/activate
  ```

- For Windows:
  ```
  .\env\Scripts\activate
  ```

- For Linux/Mac:
  ```
  source env\bin\activate
  ```

5. Install the required dependencies:
'''
pip instatll -r requirements.txt
'''

6. Set up the database:


7. Run the development server:
'''
python manage.py migrate
'''



8. Open your web browser and visit `http://localhost:8000` to access the application.

## Configuration

Before running the app, make sure to configure the following settings:

- Database Configuration: Update the database settings in the `settings.py` file.
- Stripe API Configuration: Set up your Stripe API keys in the `settings.py` file.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature/fix:
'''
git checkout -b feature/my-feature
'''


3. Make your changes and commit them:

git commit -m "Add new feature"

css


4. Push the changes to your forked repository:

git push origin feature/my-feature

csharp


5. Open a pull request on the original repository.

## License

This project is licensed under the [MIT License](LICENSE).
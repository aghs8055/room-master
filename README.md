# Room Master

Room Master is a project that allows managers to efficiently manage rooms and their reservations, while providing users with the flexibility to reserve a room according to their preferences.

## Features

- User Registration and Login: Users can sign up and log in to the website, enabling them to access the reservation system.
- Request Creation: Regular users can create reservation requests with specified dates or times.
- Request Modification: Users have the ability to edit or delete their requests before they are approved or denied.
- User Upgrade: Django administrators can upgrade a regular user to a manager role.
- Room Management: Managers can create, edit, or delete rooms within the system.
- Request Approval: Managers can view user requests and approve or deny them based on availability.
- Error Handling: Managers receive appropriate error messages or warnings when approving requests, ensuring smooth operations.
- Reservation Check: Managers can check the reservations for a specific room in different time slots.

## Technologies Used

- Django web framework
- PostgreSQL database
- Docker containerization

## Requirements

- Docker 23.0.1 or higher
- Docker Compose 2.16.0 or higher
- Python 3.8.10 or higher
- pip 23.0.1 or higher

## Installation (Development)

1. Clone the repository:
```
git clone https://gitlab.com/aghs8055/ticketer.git
```

2. Install the necessary Python libraries:
```
pip install -r requirements.txt
```

3. Start the Docker container and run the application:

```
make up
```

The Makefile provides the following commands for convenience:

- make up: start application in docker containers
- make down: stops application
- make restart: restarts application
- make refresh-database: refreshes the project database
- make lint: runs the linter for the application
- make help: displays the available commands
- make create-superuser: create a super user in database

## Contact

If you have any questions, comments, or feedback, please feel free to contact us at aghs8055@gmail.com. We are always happy to hear from our users and improve our product based on their needs.
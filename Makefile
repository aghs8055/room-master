help:
	@echo "Usage: make <command>"
	@echo "make lint"
	@echo "       Lint the code"
	@echo "make up"
	@echo "       Start environment."
	@echo "make down"
	@echo "       Stop environment."
	@echo "make restart"
	@echo "       Restart environment."
	@echo "make refresh-database"
	@echo "       Refresh database."
	@echo "make create-superuser"
	@echo "       Create a superuser in database."

lint:
	@pycodestyle --max-line-length=120 --exclude=venv,"**/migrations/*.py" .

up:
	@docker compose up --build -d

down:
	@docker compose down

restart:
	@docker compose down
	@docker compose up --build -d

refresh-database:
	@docker compose down --volumes

create-superuser:
	@docker compose exec web python manage.py createsuperuser

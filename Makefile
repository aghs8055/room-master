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
	@docker compose --env-file .env.dev up --build -d

down:
	@docker compose --env-file .env.dev down

restart:
	@docker compose --env-file .env.dev down
	@docker compose --env-file .env.dev up --build -d

refresh-database:
	@docker compose --env-file .env.dev down --volumes

create-superuser:
	@docker compose --env-file .env.dev exec web python manage.py createsuperuser

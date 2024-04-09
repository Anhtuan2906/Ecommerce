run:
	@echo "Running server..."
	python3 manage.py runserver 0.0.0.0:8000

reset-db:
	@echo "Resetting database..."
	rm -rf */__pycache__
	rm -rf media/products
	rm -rf db.sqlite3

	mkdir media/products
	python3 manage.py makemigrations customers
	python3 manage.py makemigrations store
	python3 manage.py migrate
	@echo "Database reset complete."

superuser:
	@echo "Creating superuser..."
	python3 manage.py createsuperuser

p_up:
	#create all services listed in docker compose file with docker
	@docker compose up -d

p_down:
	#delete all services listed in docker compose file
	@docker compose down

db_up:
	#create a database from the db server
	@docker exec -it escrowx-postgres createdb --username=root --owner=root escrowx_db

db_down:
	#delete a database from the db server
	@docker exec -it escrowx-postgres dropdb --username=root escrowx_db

run: 
	# run the django server
	@python manage.py runserver

migration:
	@python manage.py makemigrations

migrate:
	@python manage.py migrate

create_app:
	@python manage.py startapp $(name)

build_image:
	#build project file to a docker image
	@docker build -t escrowx:latest .
# ==============
# VOA Project Makefile
# ==============

min:
	docker compose -f docker-compose.min.yml up --build

full:
	docker compose -f docker-compose.full.yml up --build

down:
	docker compose -f docker-compose.full.yml down -v
	docker compose -f docker-compose.min.yml down -v

rebuild:
	docker compose -f docker-compose.full.yml down -v
	docker compose -f docker-compose.min.yml down -v
	docker system prune -af
	docker compose -f docker-compose.full.yml up --build

ps:
	docker ps

clean:
	docker system prune -af

# Set the default command to list all available recipes
default:
    @just --list

# Start all services in the background
up:
    docker compose up -d

# Stop and remove all containers, networks, and volumes
down:
    docker compose down

# Stop and remove everything, including volumes (destructive)
clean:
    docker compose down -v

# View real-time logs (e.g., 'just logs' or 'just logs web')
logs service="":
    docker compose logs -f {{service}}

# Rebuild all containers (or a specific one like 'just build web')
build service="":
    docker compose build {{service}}

# Restart services
restart service="":
    docker compose restart {{service}}

# Check the status of your containers
ps:
    docker compose ps

# SSH/Drop into a shell inside the web container (defaults to root)
shell user="root":
    docker compose exec --user {{user}} web sh

# --- Alembic Database Migrations ---

# Generate a new migration script (e.g., just migration "add_users_table")
migration message:
    docker compose exec --user root web alembic revision --autogenerate -m "{{message}}"

# Run all pending migrations to bring the DB up to date
migrate:
    docker compose exec --user root web alembic upgrade head

# Rollback the last applied migration
rollback:
    docker compose exec --user root web alembic downgrade -1

# View the current migration history
history:
    docker compose exec --user root web alembic history --verbose

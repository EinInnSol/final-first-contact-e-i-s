#!/bin/bash
set -e

# Wait for database to be ready
echo "Waiting for database to be ready..."
while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
  echo "Database is unavailable - sleeping"
  sleep 1
done

echo "Database is ready!"

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Create demo data if in demo mode
if [ "$DEMO_MODE" = "true" ]; then
    echo "Creating demo data..."
    python -c "
import asyncio
from app.database import get_db
from app.models import create_demo_data

async def main():
    async for db in get_db():
        await create_demo_data(db)
        break

asyncio.run(main())
"
fi

# Start the application
echo "Starting First Contact EIS Backend..."
exec "$@"

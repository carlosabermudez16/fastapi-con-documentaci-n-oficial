

1. uv run python src/app/scripts/create_db_and_tables.py -> creación de tablas
2. uv run alembic revision --autogenerate -m "add config ondelete hero" -> migración para actualizar de relaciones y tablas
3. uv run alembic upgrade head -> confirmar cambios en db
4. uv run main.py -> ejecución de aplicación

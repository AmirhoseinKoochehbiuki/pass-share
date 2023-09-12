echo "Waiting for Postgresql to start..."
./wait-for db:5432

echo "Migrating the Database..."
python3 manage.py migrate

echo "starting API server..."
python3 manage.py runserver 0.0.0.0:8000
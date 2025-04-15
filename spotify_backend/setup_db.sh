#!/bin/bash

# Kiểm tra và tạo user PostgreSQL với quyền CREATEDB
echo "Creating PostgreSQL user 'spotify_user'..."
sudo -u postgres psql -c "DO \$\$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'spotify_user') THEN CREATE USER spotify_user WITH PASSWORD '123456' CREATEDB; END IF; END \$\$;" || {
    echo "Failed to create PostgreSQL user."
    exit 1
}

# Kiểm tra và tạo database spotify_db
echo "Creating database 'spotify_db'..."
if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw "spotify_db"; then
    sudo -u postgres psql -c "CREATE DATABASE spotify_db OWNER spotify_user;" || {
        echo "Failed to create database 'spotify_db'."
        exit 1
    }
else
    echo "Database 'spotify_db' already exists."
fi

# Kích hoạt virtual environment (nằm ngoài spotify_backend)
echo "Activating virtual environment..."
if [ -d "../myenv" ]; then
    source ../myenv/bin/activate || {
        echo "Failed to activate virtual environment."
        exit 1
    }
else
    echo "Virtual environment 'myenv' not found at '../myenv'. Please check the path."
    exit 1
fi

# Di chuyển vào thư mục project (đã ở trong spotify_backend, không cần cd nữa)
echo "Already in project directory: $(pwd)"

# Tạo migration files
echo "Generating migrations..."
python manage.py makemigrations || {
    echo "Failed to generate migrations."
    exit 1
}

# Áp dụng migrations
echo "Applying migrations..."
python manage.py migrate || {
    echo "Failed to apply migrations."
    exit 1
}

echo "Database setup completed successfully!"
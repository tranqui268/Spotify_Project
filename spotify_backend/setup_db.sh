#!/bin/bash

# Đặt biến môi trường cho thư mục project
PROJECT_DIR="/home/nhatqui/Spotify_Project/spotify_backend"
VENV_DIR="../myenv"

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

# Di chuyển vào thư mục project
cd "$PROJECT_DIR" || {
    echo "Failed to change directory to $PROJECT_DIR."
    exit 1
}

# Kích hoạt virtual environment
echo "Activating virtual environment..."
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate" || {
        echo "Failed to activate virtual environment."
        exit 1
    }
else
    echo "Virtual environment '$VENV_DIR' not found. Creating new virtual environment..."
    python3 -m venv "$VENV_DIR" || {
        echo "Failed to create virtual environment."
        exit 1
    }
    source "$VENV_DIR/bin/activate" || {
        echo "Failed to activate newly created virtual environment."
        exit 1
    }
    # Cài đặt các gói phụ thuộc từ requirements.txt
    echo "Installing dependencies..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt || {
            echo "Failed to install dependencies from requirements.txt."
            exit 1
        }
    else
        echo "requirements.txt not found. Installing basic dependencies..."
        pip install django djangorestframework djangorestframework-simplejwt django-filters drf-yasg cloudinary django-cloudinary-storage django-cors-headers django-seed psycopg2-binary || {
            echo "Failed to install basic dependencies."
            exit 1
        }
        echo "django-cors-headers" >> requirements.txt
        echo "django-seed==0.2.2" >> requirements.txt  # Sử dụng phiên bản tương thích
    fi
fi

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

# Tạo user admin duy nhất
echo "Creating admin user..."
python manage.py shell < create_admin.py || {
    echo "Failed to create admin user."
    exit 1
}

# Seed dữ liệu mẫu
echo "Seeding sample data..."
python manage.py seed_data --number 20 || {
    echo "Failed to seed sample data with django-seed. Using manual seed instead..."
    python seed_data.py || {
        echo "Failed to seed data manually."
        exit 1
    }
}

echo "Database setup completed successfully!"
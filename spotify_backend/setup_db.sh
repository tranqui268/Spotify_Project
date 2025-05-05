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

# Seed dữ liệu mẫu
echo "Seeding sample data..."
python manage.py seed_data --number 20 || {
    echo "Failed to seed sample data. Using manual seed instead..."
    python manage.py shell -c "from django.utils import timezone; from accounts.models import CustomUser; from music.models import Artist, Genre, Album, Song, Playlist; import random; from datetime import datetime, timedelta; admin_user, _ = CustomUser.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True, 'is_premium': True}); admin_user.set_password('adminpassword123'); admin_user.save(); for i in range(5): username=f'user{i+1}'; email=f'user{i+1}@example.com'; user, _ = CustomUser.objects.get_or_create(username=username, defaults={'email': email, 'is_premium': random.choice([True, False]), 'premium_expiry': timezone.now() + timedelta(days=30) if random.choice([True, False]) else None}); user.set_password('password123'); user.save(); genres=['Pop', 'Rock', 'Jazz', 'Hip-Hop', 'Classical']; for g in genres: Genre.objects.get_or_create(name=g, defaults={'description': f'{g} genre'}); for i in range(3): Artist.objects.get_or_create(name=f'Artist {i+1}', defaults={'bio': f'Bio of Artist {i+1}', 'verified': random.choice([True, False]), 'monthly_listeners': random.randint(1000, 1000000), 'profile_picture': f'spotify/artist_profile_{i+1}.jpg'}); artists=Artist.objects.all(); genres=Genre.objects.all(); for i in range(5): Album.objects.get_or_create(title=f'Album {i+1}', artist=random.choice(artists), defaults={'genre': random.choice(genres), 'total_song': random.randint(5, 15), 'release_date': datetime(2025, random.randint(1, 12), random.randint(1, 28)), 'cover_image': f'spotify/album_cover_{i+1}.jpg'}); albums=Album.objects.all(); for i in range(10): Song.objects.get_or_create(title=f'Song {i+1}', artist=random.choice(artists), defaults={'album': random.choice(albums), 'genre': random.choice(genres), 'duration': timedelta(minutes=random.randint(2, 5), seconds=random.randint(0, 59)), 'release_date': datetime(2025, random.randint(1, 12), random.randint(1, 28)), 'total_plays': random.randint(0, 100000), 'song_image': f'spotify/song_image_{i+1}.jpg', 'audio_file': f'spotify/audio_{i+1}.mp3', 'video_file': f'spotify/video_{i+1}.mp4'}); users=CustomUser.objects.all(); songs=Song.objects.all(); for i in range(3): playlist=Playlist.objects.create(name=f'Playlist {i+1}', user=random.choice(users), is_public=random.choice([True, False])); selected_songs=random.sample(list(songs), random.randint(3, 5)); playlist.songs.set(selected_songs); print('Data seeding completed!')" || {
        echo "Failed to seed data manually."
        exit 1
    }
}

echo "Database setup completed successfully!"
from django.core.management.base import BaseCommand
from django_seed import Seed
from accounts.models import CustomUser
from music.models import Artist, Genre, Album, Song, Playlist

class Command(BaseCommand):
    help = 'Seed the database with sample data using django-seed'

    def add_arguments(self, parser):
        parser.add_argument('--number', default=10, type=int, help='Number of records to create for each model')

    def handle(self, *args, **kwargs):
        number = kwargs['number']
        seeder = Seed.seeder()

        # Seed CustomUser
        seeder.add_entity(CustomUser, number, {
            'username': lambda x: seeder.faker.user_name(),
            'email': lambda x: seeder.faker.email(),
            'is_premium': lambda x: seeder.faker.boolean(),          
            'password': lambda x: 'password123',
        })

        # Seed Genre
        seeder.add_entity(Genre, 5, {
            'name': lambda x: seeder.faker.word(),
            'description': lambda x: seeder.faker.sentence(),
        })

        # Seed Artist (bỏ qua profile_picture)
        seeder.add_entity(Artist, number, {
            'name': lambda x: seeder.faker.name(),
            'bio': lambda x: seeder.faker.text(),
            'verified': lambda x: seeder.faker.boolean(),
            'monthly_listeners': lambda x: seeder.faker.random_int(min=1000, max=1000000),
            'profile_picture': 'https://res.cloudinary.com/dhis8yzem/image/upload/v1746455024/music_tsgdjp.jpg',  # Đặt giá trị None để bỏ qua
        })

        # Seed Album
        seeder.add_entity(Album, number, {
            'title': lambda x: seeder.faker.sentence(nb_words=3),
            'artist': lambda x: seeder.faker.random_element(elements=Artist.objects.all()),
            'genre': lambda x: seeder.faker.random_element(elements=Genre.objects.all()),
            'total_song': lambda x: seeder.faker.random_int(min=5, max=15),
            'release_date': lambda x: seeder.faker.date_this_year(),
            'cover_image': 'https://res.cloudinary.com/dhis8yzem/image/upload/v1746455024/music_tsgdjp.jpg',  # Bỏ qua CloudinaryField
        })

        # Seed Song
        seeder.add_entity(Song, number, {
            'title': lambda x: seeder.faker.sentence(nb_words=2),
            'artist': lambda x: seeder.faker.random_element(elements=Artist.objects.all()),
            'album': lambda x: seeder.faker.random_element(elements=Album.objects.all()),
            'genre': lambda x: seeder.faker.random_element(elements=Genre.objects.all()),
            'duration': lambda x: seeder.faker.random_int(min=120, max=300),
            'release_date': lambda x: seeder.faker.date_this_year(),
            'total_plays': lambda x: seeder.faker.random_int(min=0, max=100000),
            'song_image': 'https://res.cloudinary.com/dhis8yzem/image/upload/v1746455024/music_tsgdjp.jpg',  # Bỏ qua CloudinaryField
            'audio_file': lambda x: None,  # Bỏ qua CloudinaryField
            'video_file': lambda x: None,  # Bỏ qua CloudinaryField
        })

        # Thực thi seeder
        inserted_pks = seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {number} records for each model'))

        # Seed Playlist
        users = CustomUser.objects.all()
        songs = Song.objects.all()
        for i in range(number):
            playlist = Playlist.objects.create(
                name=f'Playlist {i+1}',
                user=seeder.faker.random_element(elements=users),
                is_public=seeder.faker.boolean(),
            )
            selected_songs = seeder.faker.random_elements(elements=songs, length=seeder.faker.random_int(min=3, max=5))
            playlist.songs.set(selected_songs)
            self.stdout.write(self.style.SUCCESS(f'Created playlist: Playlist {i+1}'))
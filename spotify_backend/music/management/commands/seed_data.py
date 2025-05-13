from django.core.management.base import BaseCommand
from django_seed import Seed
from accounts.models import CustomUser
from music.models import Artist, Genre, Album, Song, Playlist

class Command(BaseCommand):
    help = 'Seed database with manually curated music data'

    def handle(self, *args, **kwargs):
        # 1. Tạo thể loại
        genres = [
            {'name': 'Pop', 'description': 'Nhạc Pop'},
            {'name': 'R&B', 'description': 'Rhythm and Blues'},
            {'name': 'Hip-Hop', 'description': 'Nhạc Hip-Hop'},
            {'name': 'Rock', 'description': 'Nhạc Rock'},
            {'name': 'Electronic', 'description': 'Nhạc điện tử'},
        ]
        for genre in genres:
            Genre.objects.create(**genre)

        # 2. Tạo nghệ sĩ
        artists = [
            {
                'name': 'Sơn Tùng M-TP',
                'bio': 'Ca sĩ nhạc pop Việt Nam',
                'verified': True,
                'monthly_listeners': 15000000,
                'profile_picture': 'https://i.scdn.co/image/ab676161000051745a79a6ca8c60e4ec1440be53'
            },
            {
                'name': 'HIEUTHUHAI',
                'bio': 'Rapper Việt Nam',
                'verified': True,
                'monthly_listeners': 71000000,
                'profile_picture': 'https://i.scdn.co/image/ab6761610000517421942907035a43a2d118c55c'
            },
            {
                'name': 'buitruonglinh',
                'bio': 'Rapper Việt Nam',
                'verified': True,
                'monthly_listeners': 15000000,
                'profile_picture': 'https://i.scdn.co/image/ab676161000051749adfc46417bb7d546b4ab3dd'
            },
            {
                'name': 'SOOBIN',
                'bio': 'Ca sĩ nhạc pop Việt Nam',
                'verified': True,
                'monthly_listeners': 71000000,
                'profile_picture': 'https://i.scdn.co/image/ab676161000051744bf18316dd0bd42ea5f9f8ec'
            },
            {
                'name': 'Da LAB',
                'bio': 'Nhóm nhạc pop Việt Nam',
                'verified': True,
                'monthly_listeners': 15000000,
                'profile_picture': 'https://i.scdn.co/image/ab6761610000517462c092ca08054a8ce883ef7e'
            },
            {
                'name': 'Vũ.',
                'bio': 'Ca sĩ nhạc pop Việt Nam',
                'verified': True,
                'monthly_listeners': 71000000,
                'profile_picture': 'https://i.scdn.co/image/ab676161000051742d7150aa7e90e9a85610ab3d'
            },
            {
                'name': 'tlinh',
                'bio': 'Rapper Việt Nam',
                'verified': True,
                'monthly_listeners': 15000000,
                'profile_picture': 'https://i.scdn.co/image/ab67616100005174230e62752ca87da1d85d0445'
            },
            {
                'name': 'Vũ Cát Tường',
                'bio': 'Ca sĩ nhạc pop Việt Nam',
                'verified': True,
                'monthly_listeners': 71000000,
                'profile_picture': 'https://i.scdn.co/image/ab676161000051741a459d6adcd9e8bceba2a5e4'
            },
            {
                'name': 'Kai Đinh',
                'bio': 'Ca sĩ nhạc pop Việt Nam',
                'verified': True,
                'monthly_listeners': 15000000,
                'profile_picture': 'https://i.scdn.co/image/ab676161000051743f32f0c12f127b02af3f684c'
            },
            {
                'name': 'Dương Domic',
                'bio': 'Ca sĩ nhạc pop Việt Nam',
                'verified': True,
                'monthly_listeners': 71000000,
                'profile_picture': 'https://i.scdn.co/image/ab67616100005174352d5672d70464e67c3ae963'
            },
            
        ]
        artist_objs = {artist['name']: Artist.objects.create(**artist) for artist in artists}

        # 3. Tạo album
        albums = [
            {
                'title': 'm-tp M-TP',
                'artist': artist_objs['Sơn Tùng M-TP'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'total_song': 3,
                'release_date': '2021-05-20',
                'cover_image': 'https://i.scdn.co/image/ab67616d00001e02794744c57c9f35db88249842'
            },
            {
                'title': 'Ai Cũng Phải Bắt Đầu Từ Đâu Đó',
                'artist': artist_objs['HIEUTHUHAI'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'total_song': 3,
                'release_date': '2020-02-21',
                'cover_image': 'https://i.scdn.co/image/ab67616d00001e02c006b0181a3846c1c63e178f'
            },
            {
                'title': 'Từng Ngày Như Mãi Mãi',
                'artist': artist_objs['buitruonglinh'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'total_song': 3,
                'release_date': '2021-05-20',
                'cover_image': 'https://i.scdn.co/image/ab67616d00001e02fe0cbef064f18008462d29ef'
            },
            {
                'title': 'BẬT NÓ LÊN',
                'artist': artist_objs['SOOBIN'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'total_song': 0,
                'release_date': '2020-02-21',
                'cover_image': 'https://i.scdn.co/image/ab67616d00001e028bdbdf691a5b791a5afb515b'
            },
            {
                'title': 'Da LAB Instrumental',
                'artist': artist_objs['Da LAB'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'total_song': 0,
                'release_date': '2021-05-20',
                'cover_image': 'https://i.scdn.co/image/ab67616d00001e0243fab536a52200d784c3cb8a'
            },
            {
                'title': 'Bảo Tàng Của Nuối Tiếc',
                'artist': artist_objs['Vũ.'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'total_song': 0,
                'release_date': '2020-02-21',
                'cover_image': 'https://i.scdn.co/image/ab67616d00001e02be066d7fd668d8a0672b1245'
            },
            {
                'title': 'ái (live at GENfest 23)',
                'artist': artist_objs['tlinh'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'total_song': 0,
                'release_date': '2021-05-20',
                'cover_image': 'https://i.scdn.co/image/ab67616d00001e02a17404597ce43b116d0456bf'
            },
            {
                'title': 'Trạm Không Gian Số 0 (Unplugged)',
                'artist': artist_objs['Vũ Cát Tường'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'total_song': 0,
                'release_date': '2020-02-21',
                'cover_image': 'https://i.scdn.co/image/ab67616d00001e02949bb9a16826218b205488ae'
            },
            {
                'title': 'Sài Gòn thanh xuân',
                'artist': artist_objs['Kai Đinh'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'total_song': 0,
                'release_date': '2021-05-20',
                'cover_image': 'https://i.scdn.co/image/ab67616d00001e0278873f6bd214ac4a99df1b90'
            },
            {
                'title': 'Dữ Liệu Quý',
                'artist': artist_objs['Dương Domic'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'total_song': 0,
                'release_date': '2020-02-21',
                'cover_image': 'https://i.scdn.co/image/ab67616d00001e02aa8b2071efbaa7ec3f41b60b'
            },
            
        ]
        album_objs = {album['title']: Album.objects.create(**album) for album in albums}

        # 4. Tạo bài hát
        songs = [
            {
                'title': 'Cơn Mưa Ngang Qua',
                'artist': artist_objs['Sơn Tùng M-TP'],
                'album': album_objs['m-tp M-TP'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'duration': 288,
                'release_date': '2021-05-20',
                'total_plays': 150000000,
                'song_image': 'https://i.scdn.co/image/ab67616d00001e02794744c57c9f35db88249842',
                'audio_file': 'https://res.cloudinary.com/dpzt1mkbh/video/upload/v1744629130/ConMuaNgangQua-SonTungMTP-1142953_tezia4.mp3',
                'video_file': None
            },
            {
                'title': 'Anh Sai Rồi',
                'artist': artist_objs['Sơn Tùng M-TP'],
                'album': album_objs['m-tp M-TP'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'duration': 252,
                'release_date': '2020-08-21',
                'total_plays': 1800000000,
                'song_image': 'https://i.scdn.co/image/ab67616d00001e02794744c57c9f35db88249842',
                'audio_file': 'https://res.cloudinary.com/dpzt1mkbh/video/upload/v1744620656/AnhSaiRoi-SonTungMTP-2647024_khmtgm.mp3',
                'video_file': None
            },
            {
                'title': 'Nắng Ấm Xa Dần',
                'artist': artist_objs['Sơn Tùng M-TP'],
                'album': album_objs['m-tp M-TP'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'duration': 188,
                'release_date': '2020-08-21',
                'total_plays': 1800000000,
                'song_image': 'https://i.scdn.co/image/ab67616d00001e02794744c57c9f35db88249842',
                'audio_file': 'https://res.cloudinary.com/dpzt1mkbh/video/upload/v1744629165/NangAmXaDan-SonTungMTP-2697291_a68rzt.mp3',
                'video_file': None
            },
            {
                'title': 'Không Thể Say',
                'artist': artist_objs['HIEUTHUHAI'],
                'album': album_objs['Ai Cũng Phải Bắt Đầu Từ Đâu Đó'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'duration': 228,
                'release_date': '2021-05-20',
                'total_plays': 150000000,
                'song_image': 'https://i.scdn.co/image/ab67616d00001e02c006b0181a3846c1c63e178f',
                'audio_file': 'https://res.cloudinary.com/dpzt1mkbh/video/upload/v1747025397/KhongTheSay-HIEUTHUHAI-9293024_if3ohq.mp3',
                'video_file': None
            },
            {
                'title': 'Exit Sign',
                'artist': artist_objs['HIEUTHUHAI'],
                'album': album_objs['Ai Cũng Phải Bắt Đầu Từ Đâu Đó'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'duration': 201,
                'release_date': '2020-08-21',
                'total_plays': 1800000000,
                'song_image': 'https://i.scdn.co/image/ab67616d00001e02c006b0181a3846c1c63e178f',
                'audio_file': 'https://res.cloudinary.com/dpzt1mkbh/video/upload/v1747025397/ExitSign-HIEUTHUHAI-11966367_jahhx1.mp3',
                'video_file': None
            },
            {
                'title': 'Siêu Sao',
                'artist': artist_objs['HIEUTHUHAI'],
                'album': album_objs['Ai Cũng Phải Bắt Đầu Từ Đâu Đó'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'duration': 186,
                'release_date': '2020-08-21',
                'total_plays': 1800000000,
                'song_image': 'https://i.scdn.co/image/ab67616d00001e02c006b0181a3846c1c63e178f',
                'audio_file': 'https://res.cloudinary.com/dpzt1mkbh/video/upload/v1747025396/SieuSao-HIEUTHUHAI-11966363_ds8tmu.mp3',
                'video_file': None
            },
            {
                'title': 'Từng Ngày Như Mãi Mãi',
                'artist': artist_objs['buitruonglinh'],
                'album': album_objs['Từng Ngày Như Mãi Mãi'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'duration': 213,
                'release_date': '2021-05-20',
                'total_plays': 150000000,
                'song_image': 'https://i.scdn.co/image/ab67616d00001e02fe0cbef064f18008462d29ef',
                'audio_file': 'https://res.cloudinary.com/dpzt1mkbh/video/upload/v1747025397/TungNgayNhuMaiMai-buitruonglinh-16755997_m4qfi4.mp3',
                'video_file': None
            },
            {
                'title': 'Em Ơi Là Em',
                'artist': artist_objs['buitruonglinh'],
                'album': album_objs['Từng Ngày Như Mãi Mãi'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'duration': 187,
                'release_date': '2020-08-21',
                'total_plays': 1800000000,
                'song_image': 'https://i.scdn.co/image/ab67616d00001e02fe0cbef064f18008462d29ef',
                'audio_file': 'https://res.cloudinary.com/dpzt1mkbh/video/upload/v1747025407/EmOiLaEm-buitruonglinhKieuChiBMZ-16952662_giakla.mp3',
                'video_file': None
            },
            {
                'title': 'Vì Điều Gì',
                'artist': artist_objs['buitruonglinh'],
                'album': album_objs['Từng Ngày Như Mãi Mãi'],
                'genre': Genre.objects.filter(name='Pop').first(),
                'duration': 153,
                'release_date': '2020-08-21',
                'total_plays': 1800000000,
                'song_image': 'https://i.scdn.co/image/ab67616d00001e02fe0cbef064f18008462d29ef',
                'audio_file': 'https://res.cloudinary.com/dpzt1mkbh/video/upload/v1747025404/j469h2qi1y_xqecwl.mp3',
                'video_file': None
            },
        ]
        for song in songs:
            Song.objects.create(**song)

        # 5. Tạo người dùng
        users = [
            {'username': 'admin123', 'email': 'admin123@example.com', 'is_superuser': True, 'is_premium': True, 'password': 'admin123'},
            {'username': 'user', 'email': 'user@example.com', 'is_superuser': False, 'is_premium': False, 'password': 'user123'},
        ]
        # Kiểm tra và chỉ tạo người dùng nếu username chưa tồn tại
        user_objs = []
        for user in users:
            if not CustomUser.objects.filter(username=user['username']).exists():
                user_objs.append(CustomUser.objects.create_user(**user))

        # Thêm người dùng mặc định nếu danh sách user_objs trống
        if not user_objs:
            default_user = {'username': 'default_user', 'email': 'default_user@example.com', 'is_superuser': False, 'is_premium': False, 'password': 'default123'}
            # Kiểm tra sự tồn tại của username trước khi tạo người dùng mặc định
            if not CustomUser.objects.filter(username=default_user['username']).exists():
                user_objs.append(CustomUser.objects.create_user(**default_user))

        # Kiểm tra số lượng người dùng trong user_objs trước khi sử dụng
        if len(user_objs) < 2:
            while len(user_objs) < 2:
                default_user = {
                    'username': f'default_user_{len(user_objs)}',
                    'email': f'default_user_{len(user_objs)}@example.com',
                    'is_superuser': False,
                    'is_premium': False,
                    'password': 'default123'
                }
                if not CustomUser.objects.filter(username=default_user['username']).exists():
                    user_objs.append(CustomUser.objects.create_user(**default_user))

        # 6. Tạo playlist
        playlists = [
            {
                'name': 'Top Hits Việt Nam',
                'user': user_objs[0],
                'is_public': True,
                'songs': Song.objects.filter(artist__name='Sơn Tùng M-TP')
            },
            {
                'name': 'Rap Việt',
                'user': user_objs[1],
                'is_public': True,
                'songs': Song.objects.filter(artist__name='HIEUTHUHAI')
            },
        ]
        for playlist in playlists:
            pl = Playlist.objects.create(name=playlist['name'], user=playlist['user'], is_public=playlist['is_public'])
            pl.songs.set(playlist['songs'])

        self.stdout.write(self.style.SUCCESS('Đã tạo dữ liệu mẫu thành công!'))
    def add_arguments(self, parser):
        parser.add_argument('--number', default=10, type=int, help='Number of records to create for each model')

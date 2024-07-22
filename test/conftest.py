# tests/conftest.py
import pytest
from app import create_app
from db import db
from models import ArtistModel, RecordModel, UserModel
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def headers(app):
    with app.app_context():
        user = UserModel(username='testuser', password='testpass', name='John Doe', email='fake@fake.com')
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=user.id)
        return {'Authorization': f'Bearer {access_token}'}

@pytest.fixture
def artist(app):
    with app.app_context():
        artist = ArtistModel(name='Test Artist')
        db.session.add(artist)
        db.session.commit()
        db.session.refresh(artist)  # Refresh to ensure it's attached
        return artist

@pytest.fixture
def record(app, artist):
    with app.app_context():
        record = RecordModel(
            name='Test Record',
            artist_id=artist.id,
            year=2022,
            format='Vinyl'
        )
        db.session.add(record)
        db.session.commit()
        db.session.refresh(record)  # Refresh to ensure it's attached
        return record

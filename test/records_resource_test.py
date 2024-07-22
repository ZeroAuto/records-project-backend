# tests/test_records_resource.py
import pytest
from models import ArtistModel, UserModel, UserRecordModel
from db import db

def test_add_record(client, headers, record):
    response = client.post(f'/record/add/{record.id}', headers=headers)
    assert response.status_code == 200

def test_find_record_by_name_and_artist(client, headers, record):
    with client.application.app_context():
        artist = db.session.query(ArtistModel).filter_by(id=record.artist_id).first()
        response = client.get('/record/find', query_string={'name': record.name, 'artist': artist.name}, headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == record.name
        assert data['artist_name'] == artist.name

def test_get_record(client, record):
    response = client.get(f'/record/{record.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == record.name
#
def test_delete_record(client, headers, record):
    response = client.delete(f'/record/{record.id}', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Record deleted'
#
def test_update_record(client, headers, record, artist):
    updated_data = {
        'name': 'Updated Record',
        'year': 2023,
        'format': 'CD',
        'artist': 'Updated Artist'
    }
    response = client.put(f'/record/{record.id}', json=updated_data, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Updated Record'
    assert data['year'] == 2023
    assert data['format'] == 'CD'
    assert data['artist_id'] != artist.id
#
def test_search_records(client, headers, record):
    response = client.get('/record', query_string={'text': 'Test'}, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0

def test_user_records(client, headers, record):
    user_record = UserRecordModel(user_id=1, record_id=record.id)
    db.session.add(user_record)
    db.session.commit()

    response = client.get('/record/user', query_string={'text': 'Test'}, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0

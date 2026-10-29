"""
Unit and integration tests for Station creation, capacity management, and lookup (PB-06, PB-07).
"""
import pytest

def test_list_stations(client):
    res = client.get('/api/stations')
    assert res.status_code == 200
    stations = res.get_json()
    assert len(stations) >= 2
    assert any(s['station_name'] == 'Station Alpha' for s in stations)

def test_get_station_by_id(client):
    res = client.get('/api/stations/1')
    assert res.status_code == 200
    data = res.get_json()
    assert data['station_name'] == 'Station Alpha'
    assert data['capacity'] == 5

    res_404 = client.get('/api/stations/999')
    assert res_404.status_code == 404

def test_get_station_bicycles(client):
    res = client.get('/api/stations/1/bicycles')
    assert res.status_code == 200
    bikes = res.get_json()
    assert len(bikes) >= 1
    assert all(b['status'] == 'Available' for b in bikes)

def test_create_station_admin(client, admin_token):
    payload = {
        'station_name': 'Station Gamma',
        'location': 'Location C',
        'capacity': 10
    }
    res = client.post(
        '/api/stations',
        headers={'Authorization': f'Bearer {admin_token}'},
        json=payload
    )
    assert res.status_code == 201
    station = res.get_json()
    assert station['station_name'] == 'Station Gamma'
    assert station['capacity'] == 10

def test_create_station_unauthorized(client, user1_token):
    payload = {
        'station_name': 'Unauthorized Station',
        'location': 'Nowhere',
        'capacity': 5
    }
    res = client.post(
        '/api/stations',
        headers={'Authorization': f'Bearer {user1_token}'},
        json=payload
    )
    assert res.status_code == 403

def test_update_and_delete_station(client, admin_token):
    # Create station first
    create_res = client.post(
        '/api/stations',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={'station_name': 'Station Delta', 'location': 'Location D', 'capacity': 4}
    )
    station_id = create_res.get_json()['station_id']

    # Update station
    up_res = client.put(
        f'/api/stations/{station_id}',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={'station_name': 'Station Delta Renovated', 'location': 'Location D-New', 'capacity': 8}
    )
    assert up_res.status_code == 200
    assert up_res.get_json()['station_name'] == 'Station Delta Renovated'

    # Delete station
    del_res = client.delete(
        f'/api/stations/{station_id}',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert del_res.status_code == 200

    # Ensure deleted
    get_res = client.get(f'/api/stations/{station_id}')
    assert get_res.status_code == 404


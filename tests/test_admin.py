"""
Unit and integration tests for Admin operations and Owner verification (PB-04, PB-05).
"""
import pytest

def test_admin_dashboard_metrics(client, admin_token):
    res = client.get('/api/admin/dashboard', headers={'Authorization': f'Bearer {admin_token}'})
    assert res.status_code == 200
    data = res.get_json()
    assert 'users' in data
    assert 'bicycles' in data
    assert 'stations' in data
    assert 'rentals' in data
    assert 'payments' in data
    assert data['users']['total_customers'] >= 2

def test_admin_dashboard_unauthorized(client, user1_token):
    res = client.get('/api/admin/dashboard', headers={'Authorization': f'Bearer {user1_token}'})
    assert res.status_code == 403

def test_admin_list_users(client, admin_token):
    res = client.get('/api/admin/users', headers={'Authorization': f'Bearer {admin_token}'})
    assert res.status_code == 200
    users = res.get_json()
    assert len(users) >= 2
    assert any(u['email'] == 'user1@test.com' for u in users)

def test_admin_list_owners(client, admin_token):
    res = client.get('/api/admin/owners', headers={'Authorization': f'Bearer {admin_token}'})
    assert res.status_code == 200
    owners = res.get_json()
    assert len(owners) >= 2

def test_admin_approve_and_reject_owner(client, admin_token):
    # Approve owner 2
    res = client.post(
        '/api/admin/owners/2/status',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={'status': 'Approved'}
    )
    assert res.status_code == 200
    assert res.get_json()['approval_status'] == 'Approved'

    # Reject owner 2
    res = client.post(
        '/api/admin/owners/2/status',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={'status': 'Rejected'}
    )
    assert res.status_code == 200
    assert res.get_json()['approval_status'] == 'Rejected'

    # Invalid status
    res = client.post(
        '/api/admin/owners/2/status',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={'status': 'InvalidStatus'}
    )
    assert res.status_code == 400


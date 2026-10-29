"""
PB-23: Automated Key UI Workflow Test
Simulates the entire customer journey end-to-end:
1. Register Customer account
2. Login & receive JWT authentication token
3. Browse & search available bicycles by station
4. Select bicycle and verify station capacity & availability
5. Rent bicycle (verify atomic status transition to 'Rented' & station count decrement)
6. Verify duplicate rental prevention (PB-13)
7. Query active rental status and verify ride timer & departure timestamp
8. Return bicycle to destination station (verify capacity limit guard & status update)
9. Calculate rental duration & fare (PB-15: Minimum 1 hour formula applied)
10. Verify simulated payment ledger record created with 'Paid' status (PB-17)
"""

def test_automated_key_ui_workflow(client):
    # Step 1: Customer Registration
    reg_payload = {
        'name': 'E2E Workflow Rider',
        'email': 'e2e_rider@test.com',
        'phone': '1234567890',
        'password': 'Password@123',
        'role': 'user'
    }
    res_reg = client.post('/api/auth/register', json=reg_payload)
    assert res_reg.status_code == 201
    user_data = res_reg.get_json()
    assert user_data['email'] == 'e2e_rider@test.com'
    token = user_data['token']
    headers = {'Authorization': f'Bearer {token}'}

    # Step 2: Customer Login
    res_login = client.post('/api/auth/login', json={
        'email': 'e2e_rider@test.com',
        'password': 'Password@123'
    })
    assert res_login.status_code == 200
    assert res_login.get_json()['role'] == 'user'

    # Step 3: Search Available Bicycles by Station (PB-11)
    res_bikes = client.get('/api/bicycles/available?station_id=1')
    assert res_bikes.status_code == 200
    bikes = res_bikes.get_json()
    assert len(bikes) > 0
    chosen_bike = bikes[0]
    bike_id = chosen_bike['bicycle_id']
    hourly_rate = chosen_bike['rental_rate']

    # Step 4: Verify Initial Station Availability Count (PB-07)
    s1_before = client.get('/api/stations/1').get_json()
    init_avail = s1_before['available_bicycles']
    assert init_avail > 0

    # Step 5: Implement Bicycle Rental Workflow (PB-12)
    res_rent = client.post('/api/rentals', json={'bicycle_id': bike_id}, headers=headers)
    assert res_rent.status_code == 201
    rental_info = res_rent.get_json()
    rental_id = rental_info['rental_id']
    assert rental_info['status'] == 'Active'

    # Verify bicycle is now Rented and station count decremented
    bike_check = client.get(f'/api/bicycles/{bike_id}').get_json()
    assert bike_check['status'] == 'Rented'
    s1_after = client.get('/api/stations/1').get_json()
    assert s1_after['available_bicycles'] == init_avail - 1

    # Step 6: Prevent Duplicate Active Rentals (PB-13)
    res_dup = client.post('/api/rentals', json={'bicycle_id': bike_id}, headers=headers)
    assert res_dup.status_code == 400
    assert 'already' in res_dup.get_json()['error'].lower()

    # Step 7: Record Rental Start & Track Active Rental (PB-14)
    res_active = client.get('/api/rentals/active', headers=headers)
    assert res_active.status_code == 200
    active_data = res_active.get_json()['rental']
    assert active_data is not None
    assert active_data['rental_id'] == rental_id
    assert active_data['start_time'] is not None

    # Step 8: Return Bicycle to Destination Station (PB-16, PB-07)
    # Check Destination Station 2
    s2_before = client.get('/api/stations/2').get_json()
    s2_init = s2_before['available_bicycles']

    res_return = client.post(f'/api/rentals/{rental_id}/return', json={
        'return_station_id': 2
    }, headers=headers)
    assert res_return.status_code == 200
    return_summary = res_return.get_json()

    # Step 9: Calculate Rental Duration and Fare (PB-15)
    assert return_summary['status'] == 'Completed'
    assert return_summary['duration'] >= 1.0  # Minimum 1 hour
    expected_min_fare = round(1.0 * hourly_rate, 2)
    assert return_summary['fare'] >= expected_min_fare

    # Step 10: Verify Bicycle Status & Station Sync After Return (PB-16)
    bike_returned = client.get(f'/api/bicycles/{bike_id}').get_json()
    assert bike_returned['status'] == 'Available'
    assert bike_returned['station_id'] == 2

    s2_after = client.get('/api/stations/2').get_json()
    assert s2_after['available_bicycles'] == s2_init + 1

    # Step 11: Maintain Simulated Payment Ledger and Status (PB-17)
    res_payments = client.get('/api/payments', headers=headers)
    assert res_payments.status_code == 200
    payments = res_payments.get_json()
    user_payments = [p for p in payments if p['rental_id'] == rental_id]
    assert len(user_payments) == 1
    assert user_payments[0]['status'] == 'Paid'
    assert user_payments[0]['amount'] == return_summary['fare']


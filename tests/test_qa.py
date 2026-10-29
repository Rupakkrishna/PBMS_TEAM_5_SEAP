"""
PB-21 & PB-22: Test QA, Code Coverage & Cyclomatic Complexity endpoints
"""

def test_qa_backlog_endpoint(client):
    res = client.get('/api/qa/backlog')
    assert res.status_code == 200
    data = res.get_json()
    assert data['total_tasks'] == 24
    assert data['total_story_points'] == 97
    assert len(data['tasks']) == 24

    # Test filtering by sprint
    res_sprint1 = client.get('/api/qa/backlog?sprint=1')
    assert res_sprint1.status_code == 200
    assert len(res_sprint1.get_json()['tasks']) == 5

def test_qa_complexity_endpoint(client):
    res = client.get('/api/qa/complexity')
    assert res.status_code == 200
    data = res.get_json()
    assert 'modules' in data
    assert data['total_functions_analyzed'] > 50
    assert data['average_complexity'] < 10.0

def test_qa_coverage_endpoint(client):
    res = client.get('/api/qa/coverage')
    assert res.status_code == 200
    data = res.get_json()
    assert 'aggregate_coverage_percentage' in data
    assert 'modules' in data

def test_qa_run_workflow_endpoint(client):
    res = client.post('/api/qa/run-workflow')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert len(data['trace']) >= 8

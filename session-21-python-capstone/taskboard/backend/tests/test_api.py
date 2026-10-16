"""API tests for TaskBoard. 13 tests across 8 endpoints, all against the SQLite test database from conftest.py."""

SAMPLE = {"title": "Deploy application", "description": "Helm upgrade to the dev cluster", "priority": "HIGH", "assignee": "Nishant"}


def test_health_is_up(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}


def test_ready_checks_database(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "READY"}


def test_root_points_to_docs(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "TaskBoard API"
    assert body["docs"] == "/docs"


def test_metrics_are_prometheus_formatted(client):
    client.get("/health")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "# HELP" in response.text
    assert "http_requests_total" in response.text


def test_list_tasks_starts_empty(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task_returns_201_with_defaults(client):
    response = client.post("/api/tasks", json=SAMPLE)
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Deploy application"
    assert body["priority"] == "HIGH"
    assert body["status"] == "TODO"
    assert body["assignee"] == "Nishant"
    assert "created_at" in body


def test_create_task_rejects_invalid_priority(client):
    response = client.post("/api/tasks", json={**SAMPLE, "priority": "URGENT"})
    assert response.status_code == 422


def test_create_task_rejects_empty_title(client):
    response = client.post("/api/tasks", json={**SAMPLE, "title": ""})
    assert response.status_code == 422


def test_get_task_by_id_and_404(client):
    created = client.post("/api/tasks", json=SAMPLE).json()
    found = client.get(f"/api/tasks/{created['id']}")
    assert found.status_code == 200
    assert found.json()["title"] == SAMPLE["title"]
    assert client.get("/api/tasks/9999").status_code == 404


def test_update_task_is_partial(client):
    created = client.post("/api/tasks", json=SAMPLE).json()
    response = client.put(f"/api/tasks/{created['id']}", json={"status": "IN_PROGRESS"})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "IN_PROGRESS"
    assert body["title"] == SAMPLE["title"]
    assert body["priority"] == "HIGH"
    assert client.put("/api/tasks/9999", json={"status": "DONE"}).status_code == 404


def test_delete_task_then_404(client):
    created = client.post("/api/tasks", json=SAMPLE).json()
    assert client.delete(f"/api/tasks/{created['id']}").status_code == 204
    assert client.get(f"/api/tasks/{created['id']}").status_code == 404
    assert client.delete(f"/api/tasks/{created['id']}").status_code == 404


def test_stats_count_by_status(client):
    client.post("/api/tasks", json=SAMPLE)
    client.post("/api/tasks", json={**SAMPLE, "status": "IN_PROGRESS"})
    client.post("/api/tasks", json={**SAMPLE, "status": "DONE"})
    client.post("/api/tasks", json={**SAMPLE, "status": "DONE"})
    stats = client.get("/api/tasks/stats").json()
    assert stats == {"total": 4, "todo": 1, "inProgress": 1, "done": 2}


def test_list_tasks_filters_by_status_newest_first(client):
    client.post("/api/tasks", json={**SAMPLE, "title": "first"})
    client.post("/api/tasks", json={**SAMPLE, "title": "second", "status": "DONE"})
    client.post("/api/tasks", json={**SAMPLE, "title": "third"})
    titles = [t["title"] for t in client.get("/api/tasks").json()]
    assert titles == ["third", "second", "first"]
    done = client.get("/api/tasks", params={"status": "DONE"}).json()
    assert [t["title"] for t in done] == ["second"]

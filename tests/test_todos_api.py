# AC-5: Backend unit tests cover todo list contract and CRUD API behavior
# AC-8: Frontend-visible todo states depend on contract-aligned API behavior

def test_get_todos_returns_bare_array_with_contract_fields(client):
    resp = client.get("/api/todos")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    for todo in body:
        assert set(todo.keys()) == {"id", "title", "completed"}
        assert isinstance(todo["title"], str)
        assert isinstance(todo["completed"], bool)


def test_post_todos_creates_todo_from_title_only(client):
    resp = client.post("/api/todos", json={"title": "Buy milk"})
    assert resp.status_code == 201
    body = resp.json()
    assert set(body.keys()) == {"id", "title", "completed"}
    assert body["title"] == "Buy milk"
    assert body["completed"] is False


def test_patch_todo_updates_completed_with_boolean(client):
    created = client.post("/api/todos", json={"title": "Walk dog"}).json()
    resp = client.patch(f"/api/todos/{created['id']}", json={"completed": True})
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == created["id"]
    assert body["title"] == "Walk dog"
    assert body["completed"] is True


def test_delete_todo_removes_item_and_returns_success(client):
    created = client.post("/api/todos", json={"title": "Tidy desk"}).json()
    resp = client.delete(f"/api/todos/{created['id']}")
    assert resp.status_code == 200
    assert resp.json() == {"success": True}


def test_get_todos_when_empty_returns_visible_empty_state_payload(client):
    resp = client.get("/api/todos")
    assert resp.status_code == 200
    assert resp.json() == []

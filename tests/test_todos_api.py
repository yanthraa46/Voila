# AC-4: Todo items persist across refresh/restart and backend CRUD contract stays stable

from app.database import Base, SessionLocal, engine
from app.models.todo import Todo


def _reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_get_todos_returns_bare_array(client):
    _reset_db()

    response = client.get("/api/todos")

    assert response.status_code == 200
    assert response.json() == []


def test_get_todos_returns_bare_array_of_todo_objects(client):
    _reset_db()
    with SessionLocal() as db:
        todo = Todo(title="Write tests", completed=False)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        todo_id = str(todo.id)

    response = client.get("/api/todos")

    assert response.status_code == 200
    assert response.json() == [{"id": todo_id, "title": "Write tests", "completed": False}]


def test_post_todos_accepts_title_and_returns_created_todo(client):
    _reset_db()

    response = client.post("/api/todos", json={"title": "New todo"})

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "New todo"
    assert body["completed"] is False
    assert "id" in body


def test_patch_todo_accepts_completed_and_returns_updated_todo(client):
    _reset_db()
    with SessionLocal() as db:
        todo = Todo(title="Finish docs", completed=False)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        todo_id = str(todo.id)

    response = client.patch(f"/api/todos/{todo_id}", json={"completed": True})

    assert response.status_code == 200
    assert response.json() == {"id": todo_id, "title": "Finish docs", "completed": True}


def test_patch_todo_accepts_completed_and_persists_update(client):
    _reset_db()
    with SessionLocal() as db:
        todo = Todo(title="Finish docs", completed=False)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        todo_id = str(todo.id)

    response = client.patch(f"/api/todos/{todo_id}", json={"completed": True})

    assert response.status_code == 200
    with SessionLocal() as db:
        updated = db.get(Todo, todo_id)
    assert updated is not None
    assert updated.completed is True


def test_delete_todo_returns_success_true(client):
    _reset_db()
    with SessionLocal() as db:
        todo = Todo(title="Remove me", completed=False)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        todo_id = str(todo.id)

    response = client.delete(f"/api/todos/{todo_id}")

    assert response.status_code == 200
    assert response.json() == {"success": True}


def test_post_todos_rejects_missing_title_with_422(client):
    _reset_db()

    response = client.post("/api/todos", json={})

    assert response.status_code == 422


def test_post_todos_rejects_empty_title_with_422(client):
    _reset_db()

    response = client.post("/api/todos", json={"title": ""})

    assert response.status_code == 422


def test_patch_todo_rejects_missing_completed_with_422(client):
    _reset_db()
    with SessionLocal() as db:
        todo = Todo(title="Need completion", completed=False)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        todo_id = str(todo.id)

    response = client.patch(f"/api/todos/{todo_id}", json={})

    assert response.status_code == 422


def test_patch_todo_rejects_invalid_completed_type_with_422(client):
    _reset_db()
    with SessionLocal() as db:
        todo = Todo(title="Need completion", completed=False)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        todo_id = str(todo.id)

    response = client.patch(f"/api/todos/{todo_id}", json={"completed": "yes"})

    assert response.status_code == 422


def test_patch_todo_returns_404_for_missing_todo(client):
    _reset_db()

    response = client.patch("/api/todos/00000000-0000-0000-0000-000000000000", json={"completed": True})

    assert response.status_code == 404


def test_delete_todo_returns_404_for_missing_todo(client):
    _reset_db()

    response = client.delete("/api/todos/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404

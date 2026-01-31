from sqlmodel import Session, select
from typing import List, Optional
from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..models.user import User

def create_todo(session: Session, todo: TodoCreate, user_id: int) -> Todo:
    """Create a new todo for a user."""
    # Convert TodoCreate to Todo model
    todo_dict = todo.dict()
    db_todo = Todo(**todo_dict)

    # Ensure the todo is linked to the user
    db_todo.user_id = user_id

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def get_todos_by_user(session: Session, user_id: int, completed: Optional[bool] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> List[Todo]:
    """Get all todos for a specific user."""
    query = select(Todo).where(Todo.user_id == user_id)

    if completed is not None:
        query = query.where(Todo.completed == completed)

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    todos = session.exec(query).all()
    return todos

def get_todo_by_id_and_user(session: Session, todo_id: int, user_id: int) -> Optional[Todo]:
    """Get a specific todo by its ID and user ID."""
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    todo = session.exec(statement).first()
    return todo

def update_todo(session: Session, todo_id: int, todo_update: TodoUpdate, user_id: int) -> Optional[Todo]:
    """Update a specific todo for a user."""
    db_todo = get_todo_by_id_and_user(session, todo_id, user_id)
    if not db_todo:
        return None

    # Update the todo with the new values
    todo_data = todo_update.dict(exclude_unset=True)
    for field, value in todo_data.items():
        setattr(db_todo, field, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def delete_todo(session: Session, todo_id: int, user_id: int) -> bool:
    """Delete a specific todo for a user."""
    db_todo = get_todo_by_id_and_user(session, todo_id, user_id)
    if not db_todo:
        return False

    session.delete(db_todo)
    session.commit()
    return True

def toggle_todo_completion(session: Session, todo_id: int, user_id: int) -> Optional[Todo]:
    """Toggle the completion status of a specific todo for a user."""
    db_todo = get_todo_by_id_and_user(session, todo_id, user_id)
    if not db_todo:
        return None

    db_todo.completed = not db_todo.completed
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo
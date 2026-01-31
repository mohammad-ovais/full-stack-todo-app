from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from ..database.database import get_session
from ..middleware.auth_middleware import get_current_user_id
from ..models.todo import Todo, TodoCreate, TodoUpdate, TodoRead
from ..models.user import User
from ..services.todo_service import (
    create_todo, get_todos_by_user, get_todo_by_id_and_user,
    update_todo, delete_todo, toggle_todo_completion
)

router = APIRouter()

@router.get("/{user_id}/tasks", response_model=List[TodoRead])
def get_tasks(
    user_id: int,
    completed: Optional[bool] = Query(None),
    limit: Optional[int] = Query(None),
    offset: Optional[int] = Query(None),
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Get all todos for the specified user."""
    # Verify that the authenticated user is requesting their own todos
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own todos"
        )

    todos = get_todos_by_user(session, user_id, completed, limit, offset)
    return todos


@router.post("/{user_id}/tasks", response_model=TodoRead)
def create_task(
    user_id: int,
    todo: TodoCreate,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Create a new todo for the specified user."""
    # Verify that the authenticated user is creating todos for themselves
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create todos for yourself"
        )

    db_todo = create_todo(session, todo, user_id)
    return db_todo


@router.get("/{user_id}/tasks/{id}", response_model=TodoRead)
def get_task(
    user_id: int,
    id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Get a specific todo by ID for the specified user."""
    # Verify that the authenticated user is requesting their own todo
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own todos"
        )

    db_todo = get_todo_by_id_and_user(session, id, user_id)
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return db_todo


@router.put("/{user_id}/tasks/{id}", response_model=TodoRead)
def update_task(
    user_id: int,
    id: int,
    todo_update: TodoUpdate,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Update a specific todo by ID for the specified user."""
    # Verify that the authenticated user is updating their own todo
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own todos"
        )

    db_todo = update_todo(session, id, todo_update, user_id)
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return db_todo


@router.delete("/{user_id}/tasks/{id}")
def delete_task(
    user_id: int,
    id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Delete a specific todo by ID for the specified user."""
    # Verify that the authenticated user is deleting their own todo
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own todos"
        )

    success = delete_todo(session, id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return {"message": "Todo deleted successfully"}


@router.patch("/{user_id}/tasks/{id}/complete", response_model=TodoRead)
def toggle_complete_task(
    user_id: int,
    id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a specific todo by ID for the specified user."""
    # Verify that the authenticated user is toggling their own todo
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only modify your own todos"
        )

    db_todo = toggle_todo_completion(session, id, user_id)
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return db_todo
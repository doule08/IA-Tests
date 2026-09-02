import React, { useState } from 'react';
import { Check, Edit2, Trash2, X, Save } from 'lucide-react';
import { Todo, TodoUpdate } from '../types/todo';

interface TodoItemProps {
  todo: Todo;
  onToggleComplete: (id: string, isCompleted: boolean) => Promise<void>;
  onUpdateTodo: (id: string, updateData: TodoUpdate) => Promise<void>;
  onDeleteTodo: (id: string) => Promise<void>;
}

export const TodoItem: React.FC<TodoItemProps> = ({
  todo,
  onToggleComplete,
  onUpdateTodo,
  onDeleteTodo,
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || '');
  const [isDeleting, setIsDeleting] = useState(false);

  const handleSave = async () => {
    if (!editTitle.trim()) return;
    await onUpdateTodo(todo.id, {
      title: editTitle.trim(),
      description: editDescription.trim() ? editDescription.trim() : null,
    });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    setIsEditing(false);
  };

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await onDeleteTodo(todo.id);
    } catch {
      setIsDeleting(false);
    }
  };

  return (
    <div className={`todo-item ${todo.is_completed ? 'completed' : ''} ${isDeleting ? 'deleting' : ''}`}>
      <div className="todo-item-checkbox">
        <button
          type="button"
          className={`checkbox-btn ${todo.is_completed ? 'checked' : ''}`}
          onClick={() => onToggleComplete(todo.id, !todo.is_completed)}
          aria-label={todo.is_completed ? "Marquer non terminée" : "Marquer terminée"}
        >
          {todo.is_completed && <Check size={14} />}
        </button>
      </div>

      <div className="todo-item-content">
        {isEditing ? (
          <div className="edit-form">
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              className="form-control edit-input"
              autoFocus
            />
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              placeholder="Description optionnelle..."
              className="form-control edit-textarea"
              rows={2}
            />
          </div>
        ) : (
          <div>
            <h3 className="todo-title">{todo.title}</h3>
            {todo.description && <p className="todo-description">{todo.description}</p>}
          </div>
        )}
      </div>

      <div className="todo-item-actions">
        {isEditing ? (
          <>
            <button
              onClick={handleSave}
              className="action-btn save-btn"
              title="Enregistrer"
            >
              <Save size={16} />
            </button>
            <button
              onClick={handleCancel}
              className="action-btn cancel-btn"
              title="Annuler"
            >
              <X size={16} />
            </button>
          </>
        ) : (
          <>
            <button
              onClick={() => setIsEditing(true)}
              className="action-btn edit-btn"
              title="Modifier"
            >
              <Edit2 size={16} />
            </button>
            <button
              onClick={handleDelete}
              className="action-btn delete-btn"
              title="Supprimer"
              disabled={isDeleting}
            >
              <Trash2 size={16} />
            </button>
          </>
        )}
      </div>
    </div>
  );
};

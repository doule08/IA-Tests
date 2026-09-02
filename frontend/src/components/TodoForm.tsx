import React, { useState } from 'react';
import { PlusCircle } from 'lucide-react';
import { TodoCreate } from '../types/todo';

interface TodoFormProps {
  onAddTodo: (todo: TodoCreate) => Promise<void>;
  isLoading: boolean;
}

export const TodoForm: React.FC<TodoFormProps> = ({ onAddTodo, isLoading }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [showDescription, setShowDescription] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    await onAddTodo({
      title: title.trim(),
      description: description.trim() ? description.trim() : null,
    });

    setTitle('');
    setDescription('');
    setShowDescription(false);
  };

  return (
    <form className="todo-form" onSubmit={handleSubmit}>
      <div className="form-input-group">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Ajouter une nouvelle tâche..."
          className="form-control"
          disabled={isLoading}
          required
        />
        <button
          type="button"
          onClick={() => setShowDescription(!showDescription)}
          className="btn-toggle-desc"
          title="Ajouter une description"
        >
          {showDescription ? '- Description' : '+ Description'}
        </button>
        <button
          type="submit"
          disabled={isLoading || !title.trim()}
          className="btn btn-primary"
        >
          <PlusCircle size={18} />
          <span>Ajouter</span>
        </button>
      </div>

      {showDescription && (
        <div className="form-description-wrapper">
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Description détaillée (optionnelle)..."
            className="form-control textarea-control"
            rows={2}
            disabled={isLoading}
          />
        </div>
      )}
    </form>
  );
};

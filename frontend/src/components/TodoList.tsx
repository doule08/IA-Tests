import React from 'react';
import { Loader2, Inbox } from 'lucide-react';
import { Todo, TodoUpdate, FilterStatus } from '../types/todo';
import { TodoItem } from './TodoItem';

interface TodoListProps {
  todos: Todo[];
  isLoading: boolean;
  filterStatus: FilterStatus;
  onToggleComplete: (id: string, isCompleted: boolean) => Promise<void>;
  onUpdateTodo: (id: string, updateData: TodoUpdate) => Promise<void>;
  onDeleteTodo: (id: string) => Promise<void>;
}

export const TodoList: React.FC<TodoListProps> = ({
  todos,
  isLoading,
  filterStatus,
  onToggleComplete,
  onUpdateTodo,
  onDeleteTodo,
}) => {
  if (isLoading && todos.length === 0) {
    return (
      <div className="list-loading">
        <Loader2 className="animate-spin" size={32} />
        <p>Chargement de vos tâches...</p>
      </div>
    );
  }

  if (todos.length === 0) {
    return (
      <div className="list-empty">
        <Inbox size={48} className="empty-icon" />
        <p className="empty-title">
          {filterStatus === 'all'
            ? 'Aucune tâche pour le moment'
            : filterStatus === 'active'
            ? 'Aucune tâche en cours'
            : 'Aucune tâche terminée'}
        </p>
        <p className="empty-subtitle">
          {filterStatus === 'all'
            ? 'Ajoutez votre première tâche ci-dessus !'
            : 'Changez de filtre pour voir d\'autres tâches.'}
        </p>
      </div>
    );
  }

  return (
    <div className="todo-list">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggleComplete={onToggleComplete}
          onUpdateTodo={onUpdateTodo}
          onDeleteTodo={onDeleteTodo}
        />
      ))}
    </div>
  );
};

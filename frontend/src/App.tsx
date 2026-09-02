import React, { useEffect, useState, useCallback } from 'react';
import { Todo, TodoCreate, TodoUpdate, FilterStatus } from './types/todo';
import { todoApi } from './services/api';
import { Header } from './components/Header';
import { TodoForm } from './components/TodoForm';
import { TodoFilter } from './components/TodoFilter';
import { TodoList } from './components/TodoList';

export const App: React.FC = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [filterStatus, setFilterStatus] = useState<FilterStatus>('all');
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Charger la liste des todos depuis l'API
  const loadTodos = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await todoApi.getTodos();
      setTodos(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur de connexion à l\'API');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadTodos();
  }, [loadTodos]);

  // Ajouter un Todo
  const handleAddTodo = async (todoData: TodoCreate) => {
    try {
      const newTodo = await todoApi.createTodo(todoData);
      setTodos((prev) => [newTodo, ...prev]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors de la création de la tâche');
    }
  };

  // Basculer l'état de complétion
  const handleToggleComplete = async (id: string, isCompleted: boolean) => {
    try {
      const updated = await todoApi.updateTodo(id, { is_completed: isCompleted });
      setTodos((prev) => prev.map((t) => (t.id === id ? updated : t)));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors de la modification');
    }
  };

  // Modifier un Todo (titre, description)
  const handleUpdateTodo = async (id: string, updateData: TodoUpdate) => {
    try {
      const updated = await todoApi.updateTodo(id, updateData);
      setTodos((prev) => prev.map((t) => (t.id === id ? updated : t)));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors de la mise à jour');
    }
  };

  // Supprimer un Todo
  const handleDeleteTodo = async (id: string) => {
    try {
      await todoApi.deleteTodo(id);
      setTodos((prev) => prev.filter((t) => t.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors de la suppression');
    }
  };

  // Filtrer les todos selon le statut sélectionné
  const filteredTodos = todos.filter((todo) => {
    if (filterStatus === 'active') return !todo.is_completed;
    if (filterStatus === 'completed') return todo.is_completed;
    return true;
  });

  const completedCount = todos.filter((t) => t.is_completed).length;

  return (
    <div className="app-container">
      <Header totalCount={todos.length} completedCount={completedCount} />

      <TodoForm onAddTodo={handleAddTodo} isLoading={isLoading} />

      {error && (
        <div className="error-banner">
          <span>⚠️ {error}</span>
          <button onClick={loadTodos} className="btn-toggle-desc">
            Réessayer
          </button>
        </div>
      )}

      <TodoFilter currentFilter={filterStatus} onFilterChange={setFilterStatus} />

      <TodoList
        todos={filteredTodos}
        isLoading={isLoading}
        filterStatus={filterStatus}
        onToggleComplete={handleToggleComplete}
        onUpdateTodo={handleUpdateTodo}
        onDeleteTodo={handleDeleteTodo}
      />
    </div>
  );
};

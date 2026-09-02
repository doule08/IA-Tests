import { Todo, TodoCreate, TodoUpdate, FilterStatus } from '../types/todo';

const API_BASE_URL = '/api/v1/todos';

/**
 * Service pour consommer l'API RESTful FastAPI ToDo List.
 */
export const todoApi = {
  /**
   * Récupère la liste des Todos avec filtrage optionnel.
   */
  async getTodos(filterStatus?: FilterStatus): Promise<Todo[]> {
    let url = `${API_BASE_URL}/`;
    if (filterStatus === 'active') {
      url += '?is_completed=false';
    } else if (filterStatus === 'completed') {
      url += '?is_completed=true';
    }

    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Erreur lors de la récupération des tâches (${response.status})`);
    }
    return response.json();
  },

  /**
   * Récupère une tâche par son ID.
   */
  async getTodoById(id: string): Promise<Todo> {
    const response = await fetch(`${API_BASE_URL}/${id}`);
    if (!response.ok) {
      throw new Error(`Tâche introuvable avec l'ID ${id}`);
    }
    return response.json();
  },

  /**
   * Crée une nouvelle tâche ToDo.
   */
  async createTodo(todoData: TodoCreate): Promise<Todo> {
    const response = await fetch(`${API_BASE_URL}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(todoData),
    });

    if (!response.ok) {
      throw new Error(`Impossible de créer la tâche (${response.status})`);
    }
    return response.json();
  },

  /**
   * Met à jour une tâche ToDo existante.
   */
  async updateTodo(id: string, todoData: TodoUpdate): Promise<Todo> {
    const response = await fetch(`${API_BASE_URL}/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(todoData),
    });

    if (!response.ok) {
      throw new Error(`Impossible de mettre à jour la tâche (${response.status})`);
    }
    return response.json();
  },

  /**
   * Supprime une tâche ToDo.
   */
  async deleteTodo(id: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/${id}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error(`Impossible de supprimer la tâche (${response.status})`);
    }
  },
};

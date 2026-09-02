/**
 * Entité Todo retournée par l'API REST FastAPI.
 */
export interface Todo {
  id: string;
  title: string;
  description: string | null;

  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * Données requises pour créer un Todo.
 */
export interface TodoCreate {
  title: string;
  description?: string | null;
  is_completed?: boolean;
}

/**
 * Données requises pour mettre à jour un Todo.
 */
export interface TodoUpdate {
  title?: string;
  description?: string | null;
  is_completed?: boolean;
}

/**
 * Statuts de filtrage de la liste de Todos.
 */
export type FilterStatus = 'all' | 'active' | 'completed';

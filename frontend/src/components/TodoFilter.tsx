import React from 'react';
import { FilterStatus } from '../types/todo';

interface TodoFilterProps {
  currentFilter: FilterStatus;
  onFilterChange: (filter: FilterStatus) => void;
}

export const TodoFilter: React.FC<TodoFilterProps> = ({ currentFilter, onFilterChange }) => {
  return (
    <div className="filter-container">
      <button
        className={`filter-btn ${currentFilter === 'all' ? 'active' : ''}`}
        onClick={() => onFilterChange('all')}
      >
        Toutes
      </button>
      <button
        className={`filter-btn ${currentFilter === 'active' ? 'active' : ''}`}
        onClick={() => onFilterChange('active')}
      >
        En cours
      </button>
      <button
        className={`filter-btn ${currentFilter === 'completed' ? 'active' : ''}`}
        onClick={() => onFilterChange('completed')}
      >
        Terminées
      </button>
    </div>
  );
};

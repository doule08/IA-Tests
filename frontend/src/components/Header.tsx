import React from 'react';
import { CheckSquare, ListTodo } from 'lucide-react';

interface HeaderProps {
  totalCount: number;
  completedCount: number;
}

export const Header: React.FC<HeaderProps> = ({ totalCount, completedCount }) => {
  const activeCount = totalCount - completedCount;

  return (
    <header className="app-header">
      <div className="header-brand">
        <div className="brand-icon">
          <ListTodo size={28} />
        </div>
        <div>
          <h1 className="brand-title">ToDo Manager</h1>
          <p className="brand-subtitle">FastAPI + React TypeScript</p>
        </div>
      </div>

      <div className="stats-badges">
        <div className="badge badge-active">
          <span className="badge-count">{activeCount}</span>
          <span className="badge-label">en cours</span>
        </div>
        <div className="badge badge-completed">
          <CheckSquare size={16} />
          <span className="badge-count">{completedCount}</span>
          <span className="badge-label">terminées</span>
        </div>
      </div>
    </header>
  );
};

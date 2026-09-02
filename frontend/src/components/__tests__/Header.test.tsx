import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Header } from '../Header';

describe('Header Component', () => {
  it('renders application title and subtitle correctly', () => {
    render(<Header totalCount={5} completedCount={2} />);

    expect(screen.getByText('ToDo Manager')).toBeInTheDocument();
    expect(screen.getByText('FastAPI + React TypeScript')).toBeInTheDocument();
  });

  it('calculates and displays active and completed task badges', () => {
    render(<Header totalCount={10} completedCount={3} />);

    // Total: 10, Completed: 3 -> Active: 7
    expect(screen.getByText('7')).toBeInTheDocument();
    expect(screen.getByText('en cours')).toBeInTheDocument();

    expect(screen.getByText('3')).toBeInTheDocument();
    expect(screen.getByText('terminées')).toBeInTheDocument();
  });
});

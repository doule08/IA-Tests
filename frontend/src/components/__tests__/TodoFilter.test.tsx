import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { TodoFilter } from '../TodoFilter';

describe('TodoFilter Component', () => {
  it('renders all filter buttons and highlights active filter', () => {
    const handleFilterChange = vi.fn();
    render(<TodoFilter currentFilter="active" onFilterChange={handleFilterChange} />);

    const allBtn = screen.getByRole('button', { name: 'Toutes' });
    const activeBtn = screen.getByRole('button', { name: 'En cours' });
    const completedBtn = screen.getByRole('button', { name: 'Terminées' });

    expect(allBtn).toBeInTheDocument();
    expect(activeBtn).toBeInTheDocument();
    expect(completedBtn).toBeInTheDocument();

    expect(activeBtn).toHaveClass('active');
    expect(allBtn).not.toHaveClass('active');
    expect(completedBtn).not.toHaveClass('active');
  });

  it('triggers onFilterChange callback when a filter button is clicked', () => {
    const handleFilterChange = vi.fn();
    render(<TodoFilter currentFilter="all" onFilterChange={handleFilterChange} />);

    const completedBtn = screen.getByRole('button', { name: 'Terminées' });
    fireEvent.click(completedBtn);

    expect(handleFilterChange).toHaveBeenCalledTimes(1);
    expect(handleFilterChange).toHaveBeenCalledWith('completed');
  });
});

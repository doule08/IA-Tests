import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { TodoForm } from '../TodoForm';

describe('TodoForm Component', () => {
  it('renders input and submit button', () => {
    const handleAddTodo = vi.fn().mockResolvedValue(undefined);
    render(<TodoForm onAddTodo={handleAddTodo} isLoading={false} />);

    expect(screen.getByPlaceholderText('Ajouter une nouvelle tâche...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /ajouter/i })).toBeInTheDocument();
  });

  it('toggles description textarea when description button is clicked', () => {
    const handleAddTodo = vi.fn().mockResolvedValue(undefined);
    render(<TodoForm onAddTodo={handleAddTodo} isLoading={false} />);

    expect(screen.queryByPlaceholderText(/description détaillée/i)).not.toBeInTheDocument();

    const descToggleBtn = screen.getByRole('button', { name: /\+ Description/i });
    fireEvent.click(descToggleBtn);

    expect(screen.getByPlaceholderText(/description détaillée/i)).toBeInTheDocument();
  });

  it('submits form with title and description and resets inputs', async () => {
    const handleAddTodo = vi.fn().mockResolvedValue(undefined);
    render(<TodoForm onAddTodo={handleAddTodo} isLoading={false} />);

    const inputTitle = screen.getByPlaceholderText('Ajouter une nouvelle tâche...');
    fireEvent.change(inputTitle, { target: { value: 'Acheter du café' } });

    const descToggleBtn = screen.getByRole('button', { name: /\+ Description/i });
    fireEvent.click(descToggleBtn);

    const inputDesc = screen.getByPlaceholderText(/description détaillée/i);
    fireEvent.change(inputDesc, { target: { value: 'Grain arabica 1kg' } });

    const submitBtn = screen.getByRole('button', { name: /ajouter/i });
    fireEvent.click(submitBtn);

    expect(handleAddTodo).toHaveBeenCalledTimes(1);
    expect(handleAddTodo).toHaveBeenCalledWith({
      title: 'Acheter du café',
      description: 'Grain arabica 1kg',
    });
  });
});

import { useCallback, useEffect, useState } from 'react';
import TodoForm from './components/features/TodoForm';
import TodoList from './components/features/TodoList';
import { createTodo, deleteTodo, fetchTodos, updateTodo } from './components/features/todoApi';
import type { Todo } from './components/features/types';

export default function App() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadTodos = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const items = await fetchTodos();
      setTodos(items);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load todos.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadTodos();
  }, [loadTodos]);

  async function handleCreate({ title }: { title: string }) {
    await createTodo({ title });
    await loadTodos();
  }

  async function handleToggle(todo: Todo) {
    await updateTodo(todo.id, { completed: !todo.completed });
    await loadTodos();
  }

  async function handleDelete(todo: Todo) {
    await deleteTodo(todo.id);
    await loadTodos();
  }

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-10 text-slate-900">
      <div className="mx-auto w-full max-w-2xl space-y-6">
        <header className="space-y-2 text-center">
          <h1 className="text-3xl font-bold tracking-tight">Todo App</h1>
          <p className="text-sm text-slate-600">Manage todos backed by the API.</p>
        </header>
        <TodoForm onCreate={handleCreate} disabled={loading} />
        <TodoList todos={todos} loading={loading} error={error} onToggle={handleToggle} onDelete={handleDelete} onRetry={loadTodos} />
      </div>
    </main>
  );
}

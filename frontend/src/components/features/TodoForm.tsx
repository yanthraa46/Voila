import { useState } from 'react';
import type { FormEvent } from 'react';
import type { TodoCreateInput } from './types';

interface TodoFormProps {
  onCreate: (input: TodoCreateInput) => Promise<void> | void;
  disabled?: boolean;
}

export default function TodoForm({ onCreate, disabled = false }: TodoFormProps) {
  const [title, setTitle] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedTitle = title.trim();
    if (!trimmedTitle) {
      setError('Please enter a todo title.');
      return;
    }

    setError(null);
    setIsSubmitting(true);
    try {
      await onCreate({ title: trimmedTitle });
      setTitle('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create todo.');
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
      <div>
        <label htmlFor="todo-title" className="mb-1 block text-sm font-medium text-slate-700">
          Todo title
        </label>
        <input
          id="todo-title"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          placeholder="Add a new todo"
          className="w-full rounded-xl border border-slate-300 px-3 py-2 text-slate-900 outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200 disabled:cursor-not-allowed disabled:bg-slate-100"
          disabled={disabled || isSubmitting}
        />
      </div>
      {error ? <p className="text-sm text-red-600">{error}</p> : null}
      <button
        type="submit"
        disabled={disabled || isSubmitting}
        className="inline-flex items-center justify-center rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800 focus:ring-2 focus:ring-slate-400 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {isSubmitting ? 'Adding…' : 'Add todo'}
      </button>
    </form>
  );
}

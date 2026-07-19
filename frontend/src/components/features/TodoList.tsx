import type { Todo } from './types';

interface TodoListProps {
  todos: Todo[];
  loading: boolean;
  error: string | null;
  onToggle: (todo: Todo) => Promise<void> | void;
  onDelete: (todo: Todo) => Promise<void> | void;
  onRetry: () => void;
}

export default function TodoList({ todos, loading, error, onToggle, onDelete, onRetry }: TodoListProps) {
  if (loading) {
    return (
      <div className="space-y-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
        {[0, 1, 2].map((item) => (
          <div key={item} className="h-16 animate-pulse rounded-xl bg-slate-100" />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-red-700 shadow-sm">
        <p className="font-medium">Unable to load todos.</p>
        <p className="mt-1 text-sm">{error}</p>
        <button type="button" onClick={onRetry} className="mt-3 rounded-xl bg-red-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-red-500 focus:ring-2 focus:ring-red-300">
          Retry
        </button>
      </div>
    );
  }

  if (!todos.length) {
    return (
      <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-8 text-center shadow-sm">
        <p className="text-base font-medium text-slate-900">No todos yet</p>
        <p className="mt-1 text-sm text-slate-600">Create your first todo to get started.</p>
      </div>
    );
  }

  return (
    <ul className="space-y-3">
      {todos.map((todo) => (
        <li key={todo.id} className="flex items-center justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <label className="flex items-center gap-3">
            <input type="checkbox" checked={todo.completed} onChange={() => onToggle(todo)} className="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" />
            <span className={todo.completed ? 'text-slate-500 line-through' : 'text-slate-900'}>{todo.title}</span>
          </label>
          <button type="button" onClick={() => onDelete(todo)} className="rounded-xl border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50 focus:ring-2 focus:ring-slate-300">
            Delete
          </button>
        </li>
      ))}
    </ul>
  );
}

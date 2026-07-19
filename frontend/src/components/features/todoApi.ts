import type { Todo, TodoCreateInput, TodoId, TodoUpdateInput } from './types';

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? '';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with status ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export function fetchTodos(): Promise<Todo[]> {
  return request<Todo[]>('/api/todos');
}

export function createTodo(input: TodoCreateInput): Promise<Todo> {
  return request<Todo>('/api/todos', {
    method: 'POST',
    body: JSON.stringify({ title: input.title }),
  });
}

export function updateTodo(id: TodoId, input: TodoUpdateInput): Promise<Todo> {
  return request<Todo>(`/api/todos/${id}`, {
    method: 'PATCH',
    body: JSON.stringify({ completed: input.completed }),
  });
}

export function deleteTodo(id: TodoId): Promise<void> {
  return request<void>(`/api/todos/${id}`, {
    method: 'DELETE',
  });
}

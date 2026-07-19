export type TodoId = string | number;

export type Todo = {
  id: TodoId;
  title: string;
  completed: boolean;
};

export type TodoCreateInput = {
  title: string;
};

export type TodoUpdateInput = {
  completed: boolean;
};

// Custom hook for user management
// Provides easy access to user CRUD operations

import { useApi, useMutation } from './use-api';
import { UsersService } from '../services/users-service';
import { User, RegisterUserRequest, UpdateUserRequest } from '../types/api';

export function useUsers() {
  return useApi<User[]>({
    apiFunc: () => UsersService.list(),
    immediate: true,
  });
}

export function useUser(id: number) {
  return useApi<User>({
    apiFunc: () => UsersService.get(id),
    immediate: true,
    deps: [id],
  });
}

export function useCurrentUser() {
  return useApi<User>({
    apiFunc: () => UsersService.me(),
    immediate: true,
  });
}

export function useCreateUser() {
  return useMutation<User, RegisterUserRequest>({
    mutationFn: (data) => UsersService.register(data),
  });
}

export function useUpdateUser() {
  return useMutation<User, { id: number; data: UpdateUserRequest }>({
    mutationFn: ({ id, data }) => UsersService.update(id, data),
  });
}

export function useDeleteUser() {
  return useMutation<void, number>({
    mutationFn: (id) => UsersService.delete(id),
  });
}

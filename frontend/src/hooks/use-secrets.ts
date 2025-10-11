// Custom hook for secrets management
// Provides easy access to secrets CRUD operations

import { useApi, useMutation } from './use-api';
import { SecretsService } from '../services/secrets-service';
import { Secret, CreateSecretRequest, UpdateSecretRequest } from '../types/api';

export function useSecrets() {
  return useApi<Secret[]>({
    apiFunc: () => SecretsService.list(),
    immediate: true,
  });
}

export function useSecret(id: number) {
  return useApi<Secret>({
    apiFunc: () => SecretsService.get(id),
    immediate: true,
    deps: [id],
  });
}

export function useCreateSecret() {
  return useMutation<Secret, CreateSecretRequest>({
    mutationFn: (data) => SecretsService.create(data),
  });
}

export function useUpdateSecret() {
  return useMutation<Secret, { id: number; data: UpdateSecretRequest }>({
    mutationFn: ({ id, data }) => SecretsService.update(id, data),
  });
}

export function useDeleteSecret() {
  return useMutation<void, number>({
    mutationFn: (id) => SecretsService.delete(id),
  });
}

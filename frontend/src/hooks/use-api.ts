// Custom React hook for API calls
// Provides loading states, error handling, and automatic re-fetching

import { useState, useEffect, useCallback } from 'react';
import { ApiError } from '../types/api';

interface UseApiOptions<T> {
  // Function that returns a promise
  apiFunc: () => Promise<T>;
  // Should fetch on mount
  immediate?: boolean;
  // Dependencies to trigger refetch
  deps?: any[];
}

interface UseApiResult<T> {
  data: T | null;
  error: ApiError | null;
  isLoading: boolean;
  refetch: () => Promise<void>;
  reset: () => void;
}

export function useApi<T>(options: UseApiOptions<T>): UseApiResult<T> {
  const { apiFunc, immediate = true, deps = [] } = options;
  
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<ApiError | null>(null);
  const [isLoading, setIsLoading] = useState(immediate);

  const fetchData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await apiFunc();
      setData(result);
      return result;
    } catch (err: any) {
      const apiError: ApiError = {
        message: err.message || 'An error occurred',
        status: err.status,
        code: err.code,
        details: err.details,
      };
      setError(apiError);
      throw apiError;
    } finally {
      setIsLoading(false);
    }
  }, [apiFunc]);

  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setIsLoading(false);
  }, []);

  useEffect(() => {
    if (immediate) {
      fetchData();
    }
  }, deps);

  return {
    data,
    error,
    isLoading,
    refetch: fetchData,
    reset,
  };
}

// Mutation hook for create/update/delete operations
interface UseMutationOptions<TData, TVariables> {
  mutationFn: (variables: TVariables) => Promise<TData>;
  onSuccess?: (data: TData) => void;
  onError?: (error: ApiError) => void;
}

interface UseMutationResult<TData, TVariables> {
  mutate: (variables: TVariables) => Promise<TData | undefined>;
  data: TData | null;
  error: ApiError | null;
  isLoading: boolean;
  reset: () => void;
}

export function useMutation<TData, TVariables = void>(
  options: UseMutationOptions<TData, TVariables>
): UseMutationResult<TData, TVariables> {
  const { mutationFn, onSuccess, onError } = options;
  
  const [data, setData] = useState<TData | null>(null);
  const [error, setError] = useState<ApiError | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const mutate = useCallback(async (variables: TVariables) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await mutationFn(variables);
      setData(result);
      onSuccess?.(result);
      return result;
    } catch (err: any) {
      const apiError: ApiError = {
        message: err.message || 'An error occurred',
        status: err.status,
        code: err.code,
        details: err.details,
      };
      setError(apiError);
      onError?.(apiError);
      throw apiError;
    } finally {
      setIsLoading(false);
    }
  }, [mutationFn, onSuccess, onError]);

  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setIsLoading(false);
  }, []);

  return {
    mutate,
    data,
    error,
    isLoading,
    reset,
  };
}

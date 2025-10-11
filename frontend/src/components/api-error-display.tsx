// API Error Display Component
// Shows user-friendly error messages

import { Alert, AlertDescription, AlertTitle } from './ui/alert';
import { Button } from './ui/button';
import { AlertCircle, RefreshCw, XCircle } from 'lucide-react';
import { ApiError } from '../types/api';

interface ApiErrorDisplayProps {
  error: ApiError;
  onRetry?: () => void;
  className?: string;
}

export function ApiErrorDisplay({ error, onRetry, className }: ApiErrorDisplayProps) {
  const getErrorIcon = () => {
    switch (error.code) {
      case 'UNAUTHORIZED':
      case 'FORBIDDEN':
        return <XCircle className="h-4 w-4" />;
      case 'NETWORK_ERROR':
      case 'TIMEOUT':
        return <RefreshCw className="h-4 w-4" />;
      default:
        return <AlertCircle className="h-4 w-4" />;
    }
  };

  const getErrorTitle = () => {
    switch (error.code) {
      case 'UNAUTHORIZED':
        return 'Authentication Required';
      case 'FORBIDDEN':
        return 'Access Denied';
      case 'NOT_FOUND':
        return 'Not Found';
      case 'RATE_LIMIT':
        return 'Rate Limit Exceeded';
      case 'SERVER_ERROR':
        return 'Server Error';
      case 'NETWORK_ERROR':
        return 'Network Error';
      case 'TIMEOUT':
        return 'Request Timeout';
      default:
        return 'Error';
    }
  };

  const getErrorDescription = () => {
    // Use custom message if available
    if (error.message) {
      return error.message;
    }

    // Default messages based on error code
    switch (error.code) {
      case 'UNAUTHORIZED':
        return 'Please log in to access this resource.';
      case 'FORBIDDEN':
        return 'You do not have permission to perform this action.';
      case 'NOT_FOUND':
        return 'The requested resource was not found.';
      case 'RATE_LIMIT':
        return 'Too many requests. Please wait a moment and try again.';
      case 'SERVER_ERROR':
        return 'An error occurred on the server. Please try again later.';
      case 'NETWORK_ERROR':
        return 'Unable to connect to the server. Please check your internet connection.';
      case 'TIMEOUT':
        return 'The request took too long to complete. Please try again.';
      default:
        return 'An unexpected error occurred.';
    }
  };

  const canRetry = ['NETWORK_ERROR', 'TIMEOUT', 'SERVER_ERROR'].includes(error.code || '');

  return (
    <Alert variant="destructive" className={className}>
      <div className="flex items-start gap-3">
        {getErrorIcon()}
        <div className="flex-1">
          <AlertTitle>{getErrorTitle()}</AlertTitle>
          <AlertDescription className="mt-1">
            {getErrorDescription()}
            {error.details && (
              <details className="mt-2">
                <summary className="text-xs cursor-pointer">Technical Details</summary>
                <pre className="mt-1 text-xs bg-destructive/10 p-2 rounded overflow-auto">
                  {JSON.stringify(error.details, null, 2)}
                </pre>
              </details>
            )}
          </AlertDescription>
          {onRetry && canRetry && (
            <Button
              variant="outline"
              size="sm"
              onClick={onRetry}
              className="mt-3"
            >
              <RefreshCw className="mr-2 h-3 w-3" />
              Retry
            </Button>
          )}
        </div>
      </div>
    </Alert>
  );
}

// Compact version for inline display
interface ApiErrorInlineProps {
  error: ApiError;
  className?: string;
}

export function ApiErrorInline({ error, className }: ApiErrorInlineProps) {
  return (
    <div className={`text-sm text-destructive flex items-center gap-2 ${className}`}>
      <AlertCircle className="h-4 w-4" />
      <span>{error.message || 'An error occurred'}</span>
    </div>
  );
}

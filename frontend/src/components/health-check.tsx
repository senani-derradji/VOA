// Health Check Component
// Displays API connection status

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Activity, CheckCircle, XCircle, RefreshCw } from 'lucide-react';
import { HealthService } from '../services/health-service';
import { API_CONFIG } from '../config/api';

export function HealthCheck() {
  const [status, setStatus] = useState<'checking' | 'healthy' | 'unhealthy'>('checking');
  const [lastChecked, setLastChecked] = useState<Date | null>(null);
  const [healthData, setHealthData] = useState<any>(null);

  const checkHealth = async () => {
    setStatus('checking');
    try {
      const data = await HealthService.check();
      setHealthData(data);
      setStatus('healthy');
      setLastChecked(new Date());
    } catch (error) {
      console.error('Health check failed:', error);
      setStatus('unhealthy');
      setLastChecked(new Date());
    }
  };

  useEffect(() => {
    checkHealth();
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = () => {
    switch (status) {
      case 'healthy':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'unhealthy':
        return <XCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Activity className="h-5 w-5 text-yellow-500 animate-pulse" />;
    }
  };

  const getStatusBadge = () => {
    switch (status) {
      case 'healthy':
        return <Badge className="bg-green-500/10 text-green-600 border-green-500/20">Healthy</Badge>;
      case 'unhealthy':
        return <Badge className="bg-red-500/10 text-red-600 border-red-500/20">Unhealthy</Badge>;
      default:
        return <Badge className="bg-yellow-500/10 text-yellow-600 border-yellow-500/20">Checking...</Badge>;
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {getStatusIcon()}
            <CardTitle>API Health Status</CardTitle>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={checkHealth}
            disabled={status === 'checking'}
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${status === 'checking' ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
        </div>
        <CardDescription>Connection to FastAPI backend</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-sm">Status</span>
          {getStatusBadge()}
        </div>
        
        <div className="flex items-center justify-between">
          <span className="text-sm">API URL</span>
          <code className="text-xs bg-muted px-2 py-1 rounded">{API_CONFIG.baseURL}</code>
        </div>

        {lastChecked && (
          <div className="flex items-center justify-between">
            <span className="text-sm">Last Checked</span>
            <span className="text-xs text-muted-foreground">
              {lastChecked.toLocaleTimeString()}
            </span>
          </div>
        )}

        {healthData && (
          <div className="flex items-center justify-between">
            <span className="text-sm">Response</span>
            <code className="text-xs bg-muted px-2 py-1 rounded">
              {JSON.stringify(healthData).substring(0, 50)}...
            </code>
          </div>
        )}

        {status === 'unhealthy' && (
          <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
            <p className="text-sm text-red-600 dark:text-red-400">
              Cannot connect to API. Make sure the backend is running on {API_CONFIG.baseURL}
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

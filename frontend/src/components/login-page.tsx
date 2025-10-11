import { useState } from 'react';
import { useAuth } from '../lib/auth-context';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Shield, Lock } from 'lucide-react';
import { toast } from 'sonner@2.0.3';

export function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!username || !password) {
      toast.error('Please enter both username and password');
      return;
    }

    setIsLoading(true);
    
    try {
      await login(username, password);
      toast.success('Login successful!');
    } catch (error: any) {
      // Show specific error message from API
      const errorMessage = error?.message || error?.details?.detail || 'Login failed. Please check your credentials.';
      toast.error(errorMessage);
      
      // If network error, show additional help
      if (error?.code === 'NETWORK_ERROR' || error?.code === 'TIMEOUT') {
        toast.error('Cannot connect to server. Make sure the backend is running on http://localhost:8000');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-gradient-to-br from-background via-background to-muted p-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-xl bg-primary/10 mb-4">
            <Shield className="w-8 h-8 text-primary" />
          </div>
          <h1 className="mb-2">VOA: Vaulity Ops</h1>
          <p className="text-muted-foreground">Secure Secrets Management Platform</p>
        </div>

        {/* Login Card */}
        <Card>
          <CardHeader>
            <CardTitle>Sign In</CardTitle>
            <CardDescription>Enter your credentials to access the dashboard</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  type="text"
                  placeholder="Enter username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  disabled={isLoading}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="Enter password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={isLoading}
                />
              </div>

              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? (
                  <>
                    <Lock className="mr-2 h-4 w-4 animate-spin" />
                    Signing in...
                  </>
                ) : (
                  <>
                    <Lock className="mr-2 h-4 w-4" />
                    Sign In
                  </>
                )}
              </Button>
            </form>

            {/* Demo Credentials */}
            <div className="mt-6 p-3 bg-muted rounded-lg">
              <p className="text-sm mb-2">Demo Credentials:</p>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• <span className="font-mono">admin</span> - Full access</li>
                <li>• <span className="font-mono">developer</span> - Secrets only</li>
                <li>• <span className="font-mono">viewer</span> - Read-only</li>
              </ul>
              <p className="text-xs text-muted-foreground mt-2">Password: any value</p>
            </div>
          </CardContent>
        </Card>

        <p className="text-center text-xs text-muted-foreground mt-4">
          Protected by enterprise-grade encryption
        </p>
      </div>
    </div>
  );
}

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Label } from './ui/label';
import { Badge } from './ui/badge';
import { useAuth } from '../lib/auth-context';
import { User, Shield, LogOut, Clock } from 'lucide-react';
import { Separator } from './ui/separator';

export function ProfilePage() {
  const { user, logout } = useAuth();

  const getRoleColor = (role?: string) => {
    switch (role) {
      case 'admin':
        return 'destructive';
      case 'developer':
        return 'default';
      case 'viewer':
        return 'secondary';
      default:
        return 'outline';
    }
  };

  const getRolePermissions = (role?: string) => {
    switch (role) {
      case 'admin':
        return [
          'Full access to all secrets',
          'Create, read, update, and delete secrets',
          'Manage user accounts',
          'View audit logs',
          'Access all environments',
        ];
      case 'developer':
        return [
          'Full access to secrets',
          'Create, read, update, and delete secrets',
          'Access development and staging environments',
          'Limited production access',
        ];
      case 'viewer':
        return [
          'Read-only access to secrets',
          'View secret metadata',
          'Cannot modify or delete secrets',
          'Limited to assigned environments',
        ];
      default:
        return [];
    }
  };

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1>Profile Settings</h1>
        <p className="text-muted-foreground">Manage your account settings and preferences</p>
      </div>

      {/* User Info Card */}
      <Card>
        <CardHeader>
          <CardTitle>Account Information</CardTitle>
          <CardDescription>Your user details and role</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center gap-4">
            <div className="flex items-center justify-center w-16 h-16 rounded-full bg-primary/10">
              <User className="w-8 h-8 text-primary" />
            </div>
            <div>
              <p className="font-mono">{user?.username}</p>
              <div className="flex items-center gap-2 mt-1">
                <Badge variant={getRoleColor(user?.role)} className="gap-1">
                  <Shield className="h-3 w-3" />
                  {user?.role}
                </Badge>
              </div>
            </div>
          </div>

          <Separator />

          <div className="grid gap-4">
            <div>
              <Label>User ID</Label>
              <div className="mt-1 p-2 bg-muted rounded font-mono">{user?.id}</div>
            </div>

            <div>
              <Label>Username</Label>
              <div className="mt-1 p-2 bg-muted rounded font-mono">{user?.username}</div>
            </div>

            <div>
              <Label>Role</Label>
              <div className="mt-1 p-2 bg-muted rounded capitalize">{user?.role}</div>
            </div>

            <div>
              <Label>Account Status</Label>
              <div className="mt-1">
                <Badge variant="outline" className="gap-1">
                  <Clock className="h-3 w-3" />
                  Active
                </Badge>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Permissions Card */}
      <Card>
        <CardHeader>
          <CardTitle>Role Permissions</CardTitle>
          <CardDescription>What you can do with your current role</CardDescription>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2">
            {getRolePermissions(user?.role).map((permission, index) => (
              <li key={index} className="flex items-start gap-2">
                <div className="mt-1 w-1.5 h-1.5 rounded-full bg-primary flex-shrink-0" />
                <span className="text-sm">{permission}</span>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>

      {/* Security Settings */}
      <Card>
        <CardHeader>
          <CardTitle>Security Settings</CardTitle>
          <CardDescription>Manage your account security</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="p-4 bg-muted/50 rounded-lg border border-dashed">
            <h4 className="mb-2">Change Password</h4>
            <p className="text-sm text-muted-foreground mb-3">
              This feature will be available in a future update.
            </p>
            <Button variant="outline" disabled>
              Change Password
            </Button>
          </div>

          <div className="p-4 bg-muted/50 rounded-lg border border-dashed">
            <h4 className="mb-2">Two-Factor Authentication</h4>
            <p className="text-sm text-muted-foreground mb-3">
              Enable 2FA for additional security (coming soon).
            </p>
            <Button variant="outline" disabled>
              Enable 2FA
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Session Management */}
      <Card>
        <CardHeader>
          <CardTitle>Session Management</CardTitle>
          <CardDescription>Manage your active sessions</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
            <div>
              <p>Current Session</p>
              <p className="text-sm text-muted-foreground">Active now</p>
            </div>
            <Button variant="destructive" onClick={logout}>
              <LogOut className="mr-2 h-4 w-4" />
              Sign Out
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* API Information */}
      <Card>
        <CardHeader>
          <CardTitle>API Integration</CardTitle>
          <CardDescription>Integration details for developers</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="p-3 bg-muted rounded-lg">
            <p className="text-sm mb-1">Base URL</p>
            <code className="text-xs text-muted-foreground">https://api.vaulityops.com/api/v1/</code>
          </div>
          <div className="p-3 bg-muted rounded-lg">
            <p className="text-sm mb-1">Authentication</p>
            <code className="text-xs text-muted-foreground">Bearer {'{'}access_token{'}'}</code>
          </div>
          <p className="text-xs text-muted-foreground">
            All API requests require authentication using JWT tokens.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}

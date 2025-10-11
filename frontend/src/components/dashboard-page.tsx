import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Key, Users, Activity, TrendingUp } from 'lucide-react';
import { secretsApi, usersApi, Secret, User } from '../lib/api';
import { useAuth } from '../lib/auth-context';
import { Badge } from './ui/badge';
import { HealthCheck } from './health-check';

export function DashboardPage() {
  const { user } = useAuth();
  const [secrets, setSecrets] = useState<Secret[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [secretsData, usersData] = await Promise.all([
        secretsApi.list(),
        user?.role === 'admin' ? usersApi.list() : Promise.resolve([]),
      ]);
      setSecrets(secretsData);
      setUsers(usersData);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const statCards = [
    {
      title: 'Total Secrets',
      value: secrets.length,
      description: 'Across all environments',
      icon: Key,
      color: 'text-blue-500',
    },
    ...(user?.role === 'admin' ? [{
      title: 'Total Users',
      value: users.length,
      description: 'Active users',
      icon: Users,
      color: 'text-green-500',
    }] : []),
    {
      title: 'Production Secrets',
      value: secrets.filter(s => s.env === 'production').length,
      description: 'Live environment',
      icon: Activity,
      color: 'text-red-500',
    },
    {
      title: 'Recent Activity',
      value: '24h',
      description: 'Last sync',
      icon: TrendingUp,
      color: 'text-purple-500',
    },
  ];

  const recentSecrets = secrets.slice(0, 5);

  const getEnvColor = (env: string) => {
    switch (env) {
      case 'production':
        return 'destructive';
      case 'staging':
        return 'default';
      case 'development':
        return 'secondary';
      default:
        return 'outline';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1>Dashboard Overview</h1>
        <p className="text-muted-foreground">Welcome back, {user?.username}</p>
      </div>

      {/* Health Check */}
      <HealthCheck />

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat, index) => (
          <Card key={index}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm">{stat.title}</CardTitle>
              <stat.icon className={`h-4 w-4 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl">{stat.value}</div>
              <p className="text-xs text-muted-foreground mt-1">
                {stat.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Recent Secrets */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Recent Secrets</CardTitle>
            <CardDescription>Latest added secrets across all environments</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="text-muted-foreground">Loading...</div>
            ) : (
              <div className="space-y-3">
                {recentSecrets.map((secret) => (
                  <div
                    key={secret.id}
                    className="flex items-center justify-between p-3 rounded-lg border bg-card"
                  >
                    <div className="flex items-center gap-3">
                      <div className="flex items-center justify-center w-8 h-8 rounded bg-primary/10">
                        <Key className="w-4 h-4 text-primary" />
                      </div>
                      <div>
                        <p className="font-mono">{secret.name}</p>
                        <p className="text-sm text-muted-foreground">
                          Owner ID: {secret.owner_id}
                        </p>
                      </div>
                    </div>
                    <Badge variant={getEnvColor(secret.env)}>
                      {secret.env}
                    </Badge>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Environment Distribution */}
      <Card>
        <CardHeader>
          <CardTitle>Environment Distribution</CardTitle>
          <CardDescription>Secrets organized by environment</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4">
            <div className="p-4 rounded-lg bg-green-500/10 border border-green-500/20">
              <div className="text-2xl text-green-600 dark:text-green-400">
                {secrets.filter(s => s.env === 'development').length}
              </div>
              <p className="text-sm text-muted-foreground mt-1">Development</p>
            </div>
            <div className="p-4 rounded-lg bg-yellow-500/10 border border-yellow-500/20">
              <div className="text-2xl text-yellow-600 dark:text-yellow-400">
                {secrets.filter(s => s.env === 'staging').length}
              </div>
              <p className="text-sm text-muted-foreground mt-1">Staging</p>
            </div>
            <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/20">
              <div className="text-2xl text-red-600 dark:text-red-400">
                {secrets.filter(s => s.env === 'production').length}
              </div>
              <p className="text-sm text-muted-foreground mt-1">Production</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

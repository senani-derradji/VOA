import { useEffect, useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from './ui/table';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from './ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from './ui/select';
import { Badge } from './ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Plus, Eye, EyeOff, Pencil, Trash2, Search } from 'lucide-react';
import { secretsApi, Secret } from '../lib/api';
import { toast } from 'sonner@2.0.3';
import { useAuth } from '../lib/auth-context';
import { Textarea } from './ui/textarea';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from './ui/alert-dialog';

export function SecretsPage() {
  const { user } = useAuth();
  const [secrets, setSecrets] = useState<Secret[]>([]);
  const [filteredSecrets, setFilteredSecrets] = useState<Secret[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [envFilter, setEnvFilter] = useState<string>('all');
  
  // Modals
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [showEditDialog, setShowEditDialog] = useState(false);
  const [showViewDialog, setShowViewDialog] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [selectedSecret, setSelectedSecret] = useState<Secret | null>(null);
  
  // Form state
  const [formData, setFormData] = useState({
    name: '',
    value: '',
    env: 'development' as Secret['env'],
  });

  const [showValue, setShowValue] = useState(false);

  useEffect(() => {
    loadSecrets();
  }, []);

  useEffect(() => {
    filterSecrets();
  }, [secrets, searchQuery, envFilter]);

  const loadSecrets = async () => {
    setIsLoading(true);
    try {
      const data = await secretsApi.list();
      setSecrets(data);
    } catch (error) {
      toast.error('Failed to load secrets');
    } finally {
      setIsLoading(false);
    }
  };

  const filterSecrets = () => {
    let filtered = secrets;

    if (searchQuery) {
      filtered = filtered.filter(s =>
        s.name.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    if (envFilter !== 'all') {
      filtered = filtered.filter(s => s.env === envFilter);
    }

    setFilteredSecrets(filtered);
  };

  const handleCreate = async () => {
    if (!formData.name || !formData.value) {
      toast.error('Please fill in all fields');
      return;
    }

    try {
      await secretsApi.create({
        ...formData,
        owner_id: user?.id || 1,
      });
      toast.success('Secret created successfully');
      setShowCreateDialog(false);
      resetForm();
      loadSecrets();
    } catch (error) {
      toast.error('Failed to create secret');
    }
  };

  const handleUpdate = async () => {
    if (!selectedSecret) return;

    try {
      await secretsApi.update(selectedSecret.id, formData);
      toast.success('Secret updated successfully');
      setShowEditDialog(false);
      resetForm();
      loadSecrets();
    } catch (error) {
      toast.error('Failed to update secret');
    }
  };

  const handleDelete = async () => {
    if (!selectedSecret) return;

    try {
      await secretsApi.delete(selectedSecret.id);
      toast.success('Secret deleted successfully');
      setShowDeleteDialog(false);
      setSelectedSecret(null);
      loadSecrets();
    } catch (error) {
      toast.error('Failed to delete secret');
    }
  };

  const openEditDialog = (secret: Secret) => {
    setSelectedSecret(secret);
    setFormData({
      name: secret.name,
      value: secret.value,
      env: secret.env,
    });
    setShowEditDialog(true);
  };

  const openViewDialog = async (secret: Secret) => {
    try {
      const data = await secretsApi.get(secret.id);
      setSelectedSecret(data);
      setShowViewDialog(true);
    } catch (error) {
      toast.error('Failed to load secret details');
    }
  };

  const openDeleteDialog = (secret: Secret) => {
    setSelectedSecret(secret);
    setShowDeleteDialog(true);
  };

  const resetForm = () => {
    setFormData({
      name: '',
      value: '',
      env: 'development',
    });
    setSelectedSecret(null);
  };

  const getEnvBadge = (env: string) => {
    switch (env) {
      case 'production':
        return <Badge variant="destructive">{env}</Badge>;
      case 'staging':
        return <Badge variant="default">{env}</Badge>;
      case 'development':
        return <Badge variant="secondary">{env}</Badge>;
      default:
        return <Badge variant="outline">{env}</Badge>;
    }
  };

  const canEdit = user?.role === 'admin' || user?.role === 'developer';
  const canView = true;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1>Secrets Management</h1>
          <p className="text-muted-foreground">Manage your application secrets securely</p>
        </div>
        {canEdit && (
          <Button onClick={() => setShowCreateDialog(true)}>
            <Plus className="mr-2 h-4 w-4" />
            Add Secret
          </Button>
        )}
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle>Filters</CardTitle>
          <CardDescription>Search and filter secrets</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search by name..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-9"
                />
              </div>
            </div>
            <Select value={envFilter} onValueChange={setEnvFilter}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Environment" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Environments</SelectItem>
                <SelectItem value="development">Development</SelectItem>
                <SelectItem value="staging">Staging</SelectItem>
                <SelectItem value="production">Production</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Secrets Table */}
      <Card>
        <CardHeader>
          <CardTitle>Secrets ({filteredSecrets.length})</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="text-center py-8 text-muted-foreground">Loading secrets...</div>
          ) : filteredSecrets.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">No secrets found</div>
          ) : (
            <div className="border rounded-lg">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>ID</TableHead>
                    <TableHead>Name</TableHead>
                    <TableHead>Environment</TableHead>
                    <TableHead>Owner ID</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredSecrets.map((secret) => (
                    <TableRow key={secret.id}>
                      <TableCell className="font-mono">{secret.id}</TableCell>
                      <TableCell className="font-mono">{secret.name}</TableCell>
                      <TableCell>{getEnvBadge(secret.env)}</TableCell>
                      <TableCell>{secret.owner_id}</TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end gap-2">
                          {canView && (
                            <Button
                              variant="ghost"
                              size="icon"
                              onClick={() => openViewDialog(secret)}
                            >
                              <Eye className="h-4 w-4" />
                            </Button>
                          )}
                          {canEdit && (
                            <>
                              <Button
                                variant="ghost"
                                size="icon"
                                onClick={() => openEditDialog(secret)}
                              >
                                <Pencil className="h-4 w-4" />
                              </Button>
                              <Button
                                variant="ghost"
                                size="icon"
                                onClick={() => openDeleteDialog(secret)}
                              >
                                <Trash2 className="h-4 w-4 text-destructive" />
                              </Button>
                            </>
                          )}
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Create Dialog */}
      <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Create New Secret</DialogTitle>
            <DialogDescription>
              Add a new secret to your vault. Endpoint: POST /api/v1/secrets/create
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="create-name">Name</Label>
              <Input
                id="create-name"
                placeholder="e.g., DB_PASSWORD"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="font-mono"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="create-value">Value</Label>
              <Textarea
                id="create-value"
                placeholder="Enter secret value..."
                value={formData.value}
                onChange={(e) => setFormData({ ...formData, value: e.target.value })}
                className="font-mono"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="create-env">Environment</Label>
              <Select
                value={formData.env}
                onValueChange={(value) => setFormData({ ...formData, env: value as Secret['env'] })}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="development">Development</SelectItem>
                  <SelectItem value="staging">Staging</SelectItem>
                  <SelectItem value="production">Production</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowCreateDialog(false)}>
              Cancel
            </Button>
            <Button onClick={handleCreate}>Create Secret</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Edit Dialog */}
      <Dialog open={showEditDialog} onOpenChange={setShowEditDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Secret</DialogTitle>
            <DialogDescription>
              Update secret details. Endpoint: PUT /api/v1/secrets/{'{'}secret_id{'}'}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="edit-name">Name</Label>
              <Input
                id="edit-name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="font-mono"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="edit-value">Value</Label>
              <Textarea
                id="edit-value"
                value={formData.value}
                onChange={(e) => setFormData({ ...formData, value: e.target.value })}
                className="font-mono"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="edit-env">Environment</Label>
              <Select
                value={formData.env}
                onValueChange={(value) => setFormData({ ...formData, env: value as Secret['env'] })}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="development">Development</SelectItem>
                  <SelectItem value="staging">Staging</SelectItem>
                  <SelectItem value="production">Production</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowEditDialog(false)}>
              Cancel
            </Button>
            <Button onClick={handleUpdate}>Update Secret</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* View Dialog */}
      <Dialog open={showViewDialog} onOpenChange={setShowViewDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Secret Details</DialogTitle>
            <DialogDescription>
              Viewing decrypted secret. Endpoint: GET /api/v1/secrets/{'{'}secret_id{'}'}
            </DialogDescription>
          </DialogHeader>
          {selectedSecret && (
            <div className="space-y-4">
              <div className="space-y-2">
                <Label>Name</Label>
                <div className="p-2 bg-muted rounded font-mono">{selectedSecret.name}</div>
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label>Value (Decrypted)</Label>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowValue(!showValue)}
                  >
                    {showValue ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </Button>
                </div>
                <div className="p-2 bg-muted rounded font-mono">
                  {showValue ? selectedSecret.value : '••••••••••••••••'}
                </div>
              </div>
              <div className="space-y-2">
                <Label>Environment</Label>
                <div>{getEnvBadge(selectedSecret.env)}</div>
              </div>
              <div className="space-y-2">
                <Label>Owner ID</Label>
                <div className="p-2 bg-muted rounded">{selectedSecret.owner_id}</div>
              </div>
            </div>
          )}
          <DialogFooter>
            <Button onClick={() => { setShowViewDialog(false); setShowValue(false); }}>
              Close
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation */}
      <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This will permanently delete the secret "{selectedSecret?.name}". This action cannot be undone.
              <br />
              <span className="text-xs text-muted-foreground mt-2">
                Endpoint: DELETE /api/v1/secrets/{'{'}secret_id{'}'}
              </span>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete} className="bg-destructive text-destructive-foreground">
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}

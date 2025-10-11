import { Home, Key, Users, FileText, User, Moon, Sun, LogOut, Shield } from 'lucide-react';
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
  SidebarFooter,
} from './ui/sidebar';
import { useAuth } from '../lib/auth-context';
import { useTheme } from '../lib/theme-provider';
import { Button } from './ui/button';
import { Separator } from './ui/separator';

interface AppSidebarProps {
  currentPage: string;
  onNavigate: (page: string) => void;
}

export function AppSidebar({ currentPage, onNavigate }: AppSidebarProps) {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  const mainItems = [
    {
      title: 'Dashboard',
      icon: Home,
      page: 'dashboard',
      roles: ['admin', 'developer', 'viewer'],
    },
    {
      title: 'Secrets',
      icon: Key,
      page: 'secrets',
      roles: ['admin', 'developer', 'viewer'],
    },
    {
      title: 'Users',
      icon: Users,
      page: 'users',
      roles: ['admin'],
    },
    {
      title: 'Audit Logs',
      icon: FileText,
      page: 'logs',
      roles: ['admin'],
      disabled: true,
    },
  ];

  // No bottom items - Sign Out is in the footer now

  const canAccess = (roles?: string[]) => {
    if (!roles) return true;
    return roles.includes(user?.role || '');
  };

  return (
    <Sidebar>
      <SidebarHeader className="p-4">
        <div className="flex items-center gap-2">
          <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-primary text-primary-foreground">
            <Shield className="w-5 h-5" />
          </div>
          <div>
            <p className="font-mono">VOA</p>
            <p className="text-xs text-muted-foreground">Vaulity Ops</p>
          </div>
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {mainItems.map((item) => {
                if (!canAccess(item.roles)) return null;
                
                return (
                  <SidebarMenuItem key={item.page}>
                    <SidebarMenuButton
                      onClick={() => !item.disabled && onNavigate(item.page)}
                      isActive={currentPage === item.page}
                      disabled={item.disabled}
                    >
                      <item.icon className="w-4 h-4" />
                      <span>{item.title}</span>
                      {item.disabled && (
                        <span className="ml-auto text-xs text-muted-foreground">Soon</span>
                      )}
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>


      </SidebarContent>

      <SidebarFooter className="p-4 space-y-2">
        <Separator />
        
        {/* User Info */}
        <div className="flex items-center gap-2 pt-2">
          <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary/10">
            <User className="w-4 h-4 text-primary" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm truncate">{user?.username}</p>
            <p className="text-xs text-muted-foreground capitalize">{user?.role}</p>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleTheme}
            className="h-8 w-8 shrink-0"
            title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {theme === 'dark' ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </Button>
        </div>

        {/* Sign Out Button */}
        <Button
          variant="outline"
          className="w-full justify-start"
          onClick={logout}
        >
          <LogOut className="mr-2 h-4 w-4" />
          Sign Out
        </Button>
      </SidebarFooter>
    </Sidebar>
  );
}

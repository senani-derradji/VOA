import { useState } from 'react';
import { SidebarProvider, SidebarInset, SidebarTrigger } from './ui/sidebar';
import { AppSidebar } from './app-sidebar';
import { Separator } from './ui/separator';
import { Breadcrumb, BreadcrumbItem, BreadcrumbList, BreadcrumbPage } from './ui/breadcrumb';
import { DashboardPage } from './dashboard-page';
import { SecretsPage } from './secrets-page';
import { UsersPage } from './users-page';
import { ProfilePage } from './profile-page';

export function AppLayout() {
  const [currentPage, setCurrentPage] = useState('dashboard');

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <DashboardPage />;
      case 'secrets':
        return <SecretsPage />;
      case 'users':
        return <UsersPage />;
      case 'logs':
        return (
          <div className="text-center py-16 text-muted-foreground">
            <h2>Audit Logs</h2>
            <p>Coming soon...</p>
          </div>
        );
      default:
        return <DashboardPage />;
    }
  };

  const getPageTitle = () => {
    switch (currentPage) {
      case 'dashboard':
        return 'Dashboard';
      case 'secrets':
        return 'Secrets';
      case 'users':
        return 'Users';
      case 'logs':
        return 'Audit Logs';
      default:
        return 'Dashboard';
    }
  };

  return (
    <SidebarProvider>
      <AppSidebar currentPage={currentPage} onNavigate={setCurrentPage} />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator orientation="vertical" className="mr-2 h-4" />
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem>
                <BreadcrumbPage>{getPageTitle()}</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </header>
        <div className="flex flex-1 flex-col gap-4 p-4 md:p-6 lg:p-8">
          {renderPage()}
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}

import { AuthProvider, useAuth } from './lib/auth-context';
import { ThemeProvider } from './lib/theme-provider';
import { LoginPage } from './components/login-page';
import { AppLayout } from './components/app-layout';
import { Toaster } from './components/ui/sonner';

function AppContent() {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <LoginPage />;
  }

  return <AppLayout />;
}

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <div className="size-full">
          <AppContent />
          <Toaster />
        </div>
      </AuthProvider>
    </ThemeProvider>
  );
}
import { useState, useCallback, useEffect } from 'react';
import { LandingPage } from '@/components/LandingPage';
import { Dashboard } from '@/components/Dashboard';
import { ServerDetails } from '@/components/ServerDetails';
import { CreateServerForm } from '@/components/CreateServerForm';
import type { CloudServer } from '@/services/types';

type View =
  | { name: 'landing' }
  | { name: 'dashboard' }
  | { name: 'create' }
  | { name: 'details'; serverId: string };

function App() {
  const [view, setView] = useState<View>({ name: 'landing' });
  const [servers, setServers] = useState<CloudServer[]>([]);

  const navigate = useCallback((v: View) => {
    setView(v);
    window.scrollTo({ top: 0, behavior: 'instant' });
  }, []);

  useEffect(() => {
    const onPop = () => {
      const hash = window.location.hash;
      if (hash === '#dashboard') setView({ name: 'dashboard' });
      else if (hash === '#create') setView({ name: 'create' });
      else if (hash.startsWith('#servers/')) {
        const id = hash.split('/')[1];
        setView({ name: 'details', serverId: id });
      } else setView({ name: 'landing' });
    };
    window.addEventListener('hashchange', onPop);
    onPop();
    return () => window.removeEventListener('hashchange', onPop);
  }, []);

  const handleNavigate = useCallback((v: View) => {
    if (v.name === 'landing') window.location.hash = '';
    else if (v.name === 'dashboard') window.location.hash = '#dashboard';
    else if (v.name === 'create') window.location.hash = '#create';
    else if (v.name === 'details') window.location.hash = `#servers/${v.serverId}`;
    navigate(v);
  }, [navigate]);

  const handleServersChange = useCallback((s: CloudServer[]) => {
    setServers(s);
  }, []);

  return (
    <div className="min-h-screen bg-ink-950 text-ink-100">
      {view.name === 'landing' && <LandingPage onEnter={() => handleNavigate({ name: 'dashboard' })} />}
      {view.name === 'dashboard' && (
        <Dashboard
          servers={servers}
          onServersChange={handleServersChange}
          onNavigate={handleNavigate}
        />
      )}
      {view.name === 'create' && (
        <CreateServerForm
          onCreated={(id) => handleNavigate({ name: 'details', serverId: id })}
          onBack={() => handleNavigate({ name: 'dashboard' })}
        />
      )}
      {view.name === 'details' && (
        <ServerDetails
          serverId={view.serverId}
          onBack={() => handleNavigate({ name: 'dashboard' })}
        />
      )}
    </div>
  );
}

export default App;

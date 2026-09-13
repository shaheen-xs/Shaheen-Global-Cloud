import { useState, useEffect, useCallback } from 'react';
import {
  Cloud, Server, Plus, Activity, Cpu, HardDrive, MemoryStick,
  Loader2, AlertCircle, RefreshCw, MoreVertical, Play, Square,
  Trash2, ArrowRight, Zap,
} from 'lucide-react';
import { Navigation } from './Navigation';
import { ServerList } from './ServerList';
import { serverService } from '@/services/serverService';
import type { CloudServer, ServerStatus } from '@/services/types';

interface DashboardProps {
  servers: CloudServer[];
  onServersChange: (servers: CloudServer[]) => void;
  onNavigate: (view: { name: 'dashboard' } | { name: 'create' } | { name: 'details'; serverId: string } | { name: 'landing' }) => void;
}

export function Dashboard({ servers, onServersChange, onNavigate }: DashboardProps) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  const fetchServers = useCallback(async (silent = false) => {
    if (!silent) {
      setRefreshing(true);
    }
    try {
      const data = await serverService.list();
      onServersChange(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load servers');
      if (servers.length === 0) {
        onServersChange([]);
      }
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [onServersChange, servers.length]);

  useEffect(() => {
    fetchServers();
    const interval = setInterval(() => fetchServers(true), 10000);
    return () => clearInterval(interval);
  }, [fetchServers]);

  const handleAction = async (server: CloudServer, action: 'start' | 'stop' | 'restart' | 'delete') => {
    setActionLoading(`${server.id}-${action}`);
    try {
      if (action === 'delete') {
        await serverService.delete(server.id);
      } else {
        await serverService[action](server.id);
      }
      await fetchServers(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : `Failed to ${action} server`);
    } finally {
      setActionLoading(null);
    }
  };

  const stats = {
    total: servers.length,
    running: servers.filter((s) => s.status === 'running').length,
    provisioning: servers.filter((s) => s.status === 'provisioning').length,
    stopped: servers.filter((s) => s.status === 'stopped').length,
    totalCpu: servers.filter((s) => s.status === 'running').reduce((sum, s) => sum + s.cpu_cores, 0),
    totalMemory: servers.filter((s) => s.status === 'running').reduce((sum, s) => sum + s.memory_mb, 0),
    totalDisk: servers.filter((s) => s.status === 'running').reduce((sum, s) => sum + s.disk_gb, 0),
  };

  return (
    <div className="min-h-screen bg-ink-950">
      <Navigation
        onLogoClick={() => onNavigate({ name: 'landing' })}
        onNavigate={(v) => onNavigate(v === 'dashboard' ? { name: 'dashboard' } : { name: 'landing' })}
      />

      <div className="pt-20 pb-12 px-6 max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">Cloud Console</h1>
            <p className="text-sm text-ink-400 mt-1">Manage your virtual infrastructure</p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => fetchServers()}
              disabled={refreshing}
              className="btn-secondary flex items-center gap-2"
            >
              <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
              Refresh
            </button>
            <button
              onClick={() => onNavigate({ name: 'create' })}
              className="btn-primary flex items-center gap-2"
            >
              <Plus className="w-4 h-4" />
              New Server
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { icon: Server, label: 'Total Servers', value: stats.total, sub: `${stats.running} running` },
            { icon: Cpu, label: 'Total vCPU', value: stats.totalCpu, sub: 'cores active' },
            { icon: MemoryStick, label: 'Total Memory', value: `${(stats.totalMemory / 1024).toFixed(1)} GB`, sub: 'RAM allocated' },
            { icon: HardDrive, label: 'Total Storage', value: `${stats.totalDisk} GB`, sub: 'disk provisioned' },
          ].map((stat) => (
            <div key={stat.label} className="glass-card p-5">
              <div className="flex items-center justify-between mb-3">
                <div className="w-9 h-9 rounded-lg bg-ink-800/60 flex items-center justify-center">
                  <stat.icon className="w-4 h-4 text-ink-300" strokeWidth={1.5} />
                </div>
                <span className="text-xs text-ink-500">{stat.sub}</span>
              </div>
              <div className="text-2xl font-bold text-white">{stat.value}</div>
              <div className="text-xs text-ink-400 mt-0.5">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Error Banner */}
        {error && (
          <div className="glass-card border-red-500/20 bg-red-500/5 p-4 mb-6 flex items-start gap-3 animate-fade-in">
            <AlertCircle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm text-red-300">{error}</p>
            </div>
            <button onClick={() => setError(null)} className="text-ink-500 hover:text-ink-300">
              <span className="text-xs">Dismiss</span>
            </button>
          </div>
        )}

        {/* Server List */}
        {loading ? (
          <div className="space-y-3">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="glass-card p-6">
                <div className="flex items-center gap-4">
                  <div className="skeleton w-10 h-10 rounded-lg" />
                  <div className="flex-1 space-y-2">
                    <div className="skeleton h-4 w-48" />
                    <div className="skeleton h-3 w-32" />
                  </div>
                  <div className="skeleton h-8 w-24 rounded-xl" />
                </div>
              </div>
            ))}
          </div>
        ) : servers.length === 0 ? (
          <EmptyState onCreate={() => onNavigate({ name: 'create' })} />
        ) : (
          <ServerList
            servers={servers}
            onSelect={(id) => onNavigate({ name: 'details', serverId: id })}
            onAction={handleAction}
            actionLoading={actionLoading}
          />
        )}
      </div>
    </div>
  );
}

function EmptyState({ onCreate }: { onCreate: () => void }) {
  return (
    <div className="glass-card p-16 text-center">
      <div className="w-16 h-16 rounded-2xl bg-ink-800/60 flex items-center justify-center mx-auto mb-6">
        <Cloud className="w-8 h-8 text-ink-400" strokeWidth={1.5} />
      </div>
      <h3 className="text-lg font-semibold text-white mb-2">No servers yet</h3>
      <p className="text-sm text-ink-400 mb-6 max-w-sm mx-auto">
        Provision your first virtual machine to get started with Shaheen Global Cloud.
      </p>
      <button onClick={onCreate} className="btn-primary inline-flex items-center gap-2">
        <Plus className="w-4 h-4" />
        Create Your First Server
      </button>
    </div>
  );
}

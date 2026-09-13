import { useState, useEffect, useCallback } from 'react';
import {
  ArrowLeft, Server, Cpu, MemoryStick, HardDrive, Globe,
  Play, Square, RotateCcw, Trash2, Loader2, AlertCircle,
  Clock, Activity, Network, Copy, Check,
} from 'lucide-react';
import { Navigation } from './Navigation';
import { serverService } from '@/services/serverService';
import type { CloudServer, Job, ServerStatus } from '@/services/types';

interface ServerDetailsProps {
  serverId: string;
  onBack: () => void;
}

const statusConfig: Record<ServerStatus, { label: string; badge: string; dot: string }> = {
  running: { label: 'Running', badge: 'badge-success', dot: 'bg-emerald-400' },
  stopped: { label: 'Stopped', badge: 'badge-neutral', dot: 'bg-ink-500' },
  provisioning: { label: 'Provisioning', badge: 'badge-warning', dot: 'bg-amber-400 animate-pulse' },
  error: { label: 'Error', badge: 'badge-error', dot: 'bg-red-400' },
  deleting: { label: 'Deleting', badge: 'badge-warning', dot: 'bg-amber-400 animate-pulse' },
};

export function ServerDetails({ serverId, onBack }: ServerDetailsProps) {
  const [server, setServer] = useState<CloudServer | null>(null);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState(false);
  const [copied, setCopied] = useState<string | null>(null);

  const fetchServer = useCallback(async () => {
    try {
      const [s, j] = await Promise.all([
        serverService.get(serverId),
        serverService.listJobs().catch(() => []),
      ]);
      setServer(s);
      setJobs(j.filter((job) => job.server_id === serverId));
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load server');
    } finally {
      setLoading(false);
    }
  }, [serverId]);

  useEffect(() => {
    fetchServer();
    const interval = setInterval(fetchServer, 5000);
    return () => clearInterval(interval);
  }, [fetchServer]);

  const handleAction = async (action: 'start' | 'stop' | 'restart' | 'delete') => {
    setActionLoading(true);
    try {
      if (action === 'delete') {
        await serverService.delete(serverId);
        onBack();
        return;
      }
      await serverService[action](serverId);
      await fetchServer();
    } catch (err) {
      setError(err instanceof Error ? err.message : `Failed to ${action} server`);
    } finally {
      setActionLoading(false);
    }
  };

  const copyToClipboard = (text: string, key: string) => {
    navigator.clipboard.writeText(text);
    setCopied(key);
    setTimeout(() => setCopied(null), 2000);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-ink-950">
        <Navigation onLogoClick={onBack} onNavigate={() => onBack()} />
        <div className="pt-20 pb-12 px-6 max-w-5xl mx-auto">
          <div className="glass-card p-8 space-y-4">
            <div className="skeleton h-8 w-48" />
            <div className="skeleton h-4 w-full" />
            <div className="skeleton h-4 w-3/4" />
            <div className="skeleton h-32 w-full" />
          </div>
        </div>
      </div>
    );
  }

  if (error && !server) {
    return (
      <div className="min-h-screen bg-ink-950">
        <Navigation onLogoClick={onBack} onNavigate={() => onBack()} />
        <div className="pt-20 pb-12 px-6 max-w-5xl mx-auto">
          <div className="glass-card p-12 text-center">
            <AlertCircle className="w-10 h-10 text-red-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-white mb-2">Unable to load server</h3>
            <p className="text-sm text-ink-400 mb-6">{error}</p>
            <button onClick={onBack} className="btn-secondary">Back to Dashboard</button>
          </div>
        </div>
      </div>
    );
  }

  if (!server) return null;

  const status = statusConfig[server.status];

  return (
    <div className="min-h-screen bg-ink-950">
      <Navigation onLogoClick={onBack} onNavigate={() => onBack()} />

      <div className="pt-20 pb-12 px-6 max-w-5xl mx-auto">
        <button onClick={onBack} className="btn-ghost flex items-center gap-2 mb-6 -ml-2">
          <ArrowLeft className="w-4 h-4" />
          Back to Dashboard
        </button>

        {error && (
          <div className="glass-card border-red-500/20 bg-red-500/5 p-4 mb-6 flex items-start gap-3 animate-fade-in">
            <AlertCircle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
            <p className="text-sm text-red-300">{error}</p>
          </div>
        )}

        {/* Header */}
        <div className="glass-card p-6 mb-6">
          <div className="flex items-start justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="relative">
                <div className="w-14 h-14 rounded-2xl bg-ink-800/60 flex items-center justify-center">
                  <Server className="w-7 h-7 text-ink-300" strokeWidth={1.5} />
                </div>
                <div className={`absolute -bottom-0.5 -right-0.5 w-4 h-4 rounded-full ${status.dot} border-2 border-ink-900`} />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">{server.name}</h1>
                <p className="text-sm text-ink-400 font-mono">{server.hostname}</p>
              </div>
            </div>
            <span className={status.badge}>{status.label}</span>
          </div>
        </div>

        {/* Action Bar */}
        <div className="flex items-center gap-2 mb-6">
          {server.status === 'running' && (
            <button
              onClick={() => handleAction('stop')}
              disabled={actionLoading}
              className="btn-secondary flex items-center gap-2"
            >
              {actionLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Square className="w-4 h-4" />}
              Stop
            </button>
          )}
          {(server.status === 'stopped' || server.status === 'error') && (
            <button
              onClick={() => handleAction('start')}
              disabled={actionLoading}
              className="btn-primary flex items-center gap-2"
            >
              {actionLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
              Start
            </button>
          )}
          <button
            onClick={() => handleAction('restart')}
            disabled={actionLoading || server.status !== 'running'}
            className="btn-secondary flex items-center gap-2"
          >
            <RotateCcw className="w-4 h-4" />
            Restart
          </button>
          <button
            onClick={() => handleAction('delete')}
            disabled={actionLoading}
            className="btn-secondary flex items-center gap-2 text-red-400 hover:bg-red-500/10 hover:border-red-500/30"
          >
            <Trash2 className="w-4 h-4" />
            Delete
          </button>
        </div>

        {/* Specs Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          {[
            { icon: Cpu, label: 'vCPU Cores', value: server.cpu_cores },
            { icon: MemoryStick, label: 'Memory', value: server.memory_mb >= 1024 ? `${(server.memory_mb / 1024).toFixed(1)} GB` : `${server.memory_mb} MB` },
            { icon: HardDrive, label: 'Disk', value: `${server.disk_gb} GB` },
            { icon: Globe, label: 'Region', value: server.region },
          ].map((spec) => (
            <div key={spec.label} className="glass-card p-5">
              <spec.icon className="w-5 h-5 text-ink-400 mb-3" strokeWidth={1.5} />
              <div className="text-xl font-bold text-white">{spec.value}</div>
              <div className="text-xs text-ink-500 mt-0.5">{spec.label}</div>
            </div>
          ))}
        </div>

        {/* Network Info */}
        <div className="glass-card p-6 mb-6">
          <h2 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
            <Network className="w-4 h-4 text-ink-400" />
            Network
          </h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs text-ink-500">IPv4 Address</span>
              <div className="flex items-center gap-2">
                <span className="text-sm font-mono text-white">{server.ipv4 || 'Not assigned'}</span>
                {server.ipv4 && (
                  <button onClick={() => copyToClipboard(server.ipv4!, 'ipv4')} className="text-ink-500 hover:text-ink-300">
                    {copied === 'ipv4' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  </button>
                )}
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-ink-500">IPv6 Address</span>
              <div className="flex items-center gap-2">
                <span className="text-sm font-mono text-white">{server.ipv6 || 'Not assigned'}</span>
                {server.ipv6 && (
                  <button onClick={() => copyToClipboard(server.ipv6!, 'ipv6')} className="text-ink-500 hover:text-ink-300">
                    {copied === 'ipv6' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  </button>
                )}
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-ink-500">Image</span>
              <span className="text-sm text-white">{server.image}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-ink-500">Plan</span>
              <span className="text-sm text-white capitalize">{server.plan}</span>
            </div>
          </div>
        </div>

        {/* Job History */}
        <div className="glass-card p-6">
          <h2 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
            <Activity className="w-4 h-4 text-ink-400" />
            Job History
          </h2>
          {jobs.length === 0 ? (
            <p className="text-sm text-ink-500 py-4 text-center">No jobs yet</p>
          ) : (
            <div className="space-y-2">
              {jobs.map((job) => (
                <div key={job.id} className="flex items-center gap-3 py-2 border-b border-ink-800/50 last:border-0">
                  <Clock className="w-3.5 h-3.5 text-ink-500 shrink-0" />
                  <span className="text-sm text-white capitalize">{job.job_type}</span>
                  <span className={`badge ${job.status === 'completed' ? 'badge-success' : job.status === 'failed' ? 'badge-error' : 'badge-warning'}`}>
                    {job.status}
                  </span>
                  <span className="text-xs text-ink-500 flex-1 truncate">{job.message}</span>
                  <span className="text-xs text-ink-600 shrink-0">
                    {new Date(job.created_at).toLocaleString()}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Metadata */}
        <div className="glass-card p-6 mt-6">
          <h2 className="text-sm font-semibold text-white mb-4">Metadata</h2>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs text-ink-500">Server ID</span>
              <button onClick={() => copyToClipboard(server.id, 'id')} className="flex items-center gap-2">
                <span className="text-sm font-mono text-ink-300">{server.id.slice(0, 8)}...</span>
                {copied === 'id' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-ink-500" />}
              </button>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-ink-500">Created</span>
              <span className="text-sm text-ink-300">{new Date(server.created_at).toLocaleString()}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-ink-500">Last Updated</span>
              <span className="text-sm text-ink-300">{new Date(server.updated_at).toLocaleString()}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

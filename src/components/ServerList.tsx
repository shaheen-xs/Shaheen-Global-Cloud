import { useState, useRef, useEffect } from 'react';
import {
  Server, MoreVertical, Play, Square, Trash2, ArrowRight,
  Cpu, MemoryStick, HardDrive, Globe, Loader2,
} from 'lucide-react';
import type { CloudServer, ServerStatus } from '@/services/types';

interface ServerListProps {
  servers: CloudServer[];
  onSelect: (id: string) => void;
  onAction: (server: CloudServer, action: 'start' | 'stop' | 'restart' | 'delete') => void;
  actionLoading: string | null;
}

const statusConfig: Record<ServerStatus, { label: string; badge: string; dot: string }> = {
  running: { label: 'Running', badge: 'badge-success', dot: 'bg-emerald-400' },
  stopped: { label: 'Stopped', badge: 'badge-neutral', dot: 'bg-ink-500' },
  provisioning: { label: 'Provisioning', badge: 'badge-warning', dot: 'bg-amber-400 animate-pulse' },
  error: { label: 'Error', badge: 'badge-error', dot: 'bg-red-400' },
  deleting: { label: 'Deleting', badge: 'badge-warning', dot: 'bg-amber-400 animate-pulse' },
};

export function ServerList({ servers, onSelect, onAction, actionLoading }: ServerListProps) {
  const [menuOpen, setMenuOpen] = useState<string | null>(null);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const onClick = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuOpen(null);
      }
    };
    document.addEventListener('mousedown', onClick);
    return () => document.removeEventListener('mousedown', onClick);
  }, []);

  return (
    <div className="space-y-3">
      {servers.map((server) => {
        const status = statusConfig[server.status];
        const isLoading = actionLoading?.startsWith(server.id);

        return (
          <div
            key={server.id}
            className="glass-card-hover p-5 group cursor-pointer animate-fade-in"
            onClick={() => onSelect(server.id)}
          >
            <div className="flex items-center gap-4">
              {/* Status icon */}
              <div className="relative shrink-0">
                <div className="w-11 h-11 rounded-xl bg-ink-800/60 flex items-center justify-center">
                  <Server className="w-5 h-5 text-ink-300" strokeWidth={1.5} />
                </div>
                <div className={`absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 rounded-full ${status.dot} border-2 border-ink-900`} />
              </div>

              {/* Server info */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3 mb-1">
                  <h3 className="text-sm font-semibold text-white truncate">{server.name}</h3>
                  <span className={status.badge}>{status.label}</span>
                </div>
                <div className="flex items-center gap-4 text-xs text-ink-500">
                  <span className="flex items-center gap-1">
                    <Globe className="w-3 h-3" />
                    {server.region}
                  </span>
                  <span className="flex items-center gap-1">
                    <Cpu className="w-3 h-3" />
                    {server.cpu_cores} vCPU
                  </span>
                  <span className="flex items-center gap-1">
                    <MemoryStick className="w-3 h-3" />
                    {server.memory_mb >= 1024 ? `${(server.memory_mb / 1024).toFixed(1)} GB` : `${server.memory_mb} MB`}
                  </span>
                  <span className="flex items-center gap-1">
                    <HardDrive className="w-3 h-3" />
                    {server.disk_gb} GB
                  </span>
                  {server.ipv4 && (
                    <span className="font-mono text-ink-600 hidden md:inline">{server.ipv4}</span>
                  )}
                </div>
              </div>

              {/* Actions */}
              <div className="flex items-center gap-2 shrink-0" onClick={(e) => e.stopPropagation()}>
                {isLoading ? (
                  <Loader2 className="w-4 h-4 text-ink-400 animate-spin" />
                ) : (
                  <>
                    {server.status === 'running' && (
                      <button
                        onClick={() => onAction(server, 'stop')}
                        className="w-9 h-9 rounded-lg bg-ink-800/40 hover:bg-ink-700/60 flex items-center justify-center transition-colors"
                        title="Stop"
                      >
                        <Square className="w-4 h-4 text-ink-300" />
                      </button>
                    )}
                    {(server.status === 'stopped' || server.status === 'error') && (
                      <button
                        onClick={() => onAction(server, 'start')}
                        className="w-9 h-9 rounded-lg bg-ink-800/40 hover:bg-ink-700/60 flex items-center justify-center transition-colors"
                        title="Start"
                      >
                        <Play className="w-4 h-4 text-ink-300" />
                      </button>
                    )}
                    <div className="relative" ref={menuOpen === server.id ? menuRef : undefined}>
                      <button
                        onClick={() => setMenuOpen(menuOpen === server.id ? null : server.id)}
                        className="w-9 h-9 rounded-lg bg-ink-800/40 hover:bg-ink-700/60 flex items-center justify-center transition-colors"
                      >
                        <MoreVertical className="w-4 h-4 text-ink-300" />
                      </button>
                      {menuOpen === server.id && (
                        <div className="absolute right-0 top-full mt-1 w-44 glass rounded-xl border border-ink-700/60 shadow-xl z-20 overflow-hidden animate-fade-in">
                          <button
                            onClick={() => { onAction(server, 'restart'); setMenuOpen(null); }}
                            className="w-full px-4 py-2.5 text-left text-sm text-ink-200 hover:bg-ink-800/60 flex items-center gap-2"
                          >
                            <ArrowRight className="w-3.5 h-3.5" /> Restart
                          </button>
                          <button
                            onClick={() => { onAction(server, 'delete'); setMenuOpen(null); }}
                            className="w-full px-4 py-2.5 text-left text-sm text-red-400 hover:bg-red-500/10 flex items-center gap-2"
                          >
                            <Trash2 className="w-3.5 h-3.5" /> Delete
                          </button>
                        </div>
                      )}
                    </div>
                  </>
                )}
                <ArrowRight className="w-4 h-4 text-ink-700 group-hover:text-ink-400 transition-colors ml-1" />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

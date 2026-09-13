import { useState, useEffect } from 'react';
import {
  ArrowLeft, Server, Cpu, MemoryStick, HardDrive, Globe,
  Loader2, Check, AlertCircle, Zap,
} from 'lucide-react';
import { Navigation } from './Navigation';
import { serverService } from '@/services/serverService';
import type { ServerPlanInfo, RegionInfo, ImageInfo, ServerPlan } from '@/services/types';

interface CreateServerFormProps {
  onCreated: (serverId: string) => void;
  onBack: () => void;
}

const defaultPlans: ServerPlanInfo[] = [
  { id: 'micro', label: 'Micro', cpu_cores: 1, memory_mb: 1024, disk_gb: 20, price_per_hour: 0.005 },
  { id: 'small', label: 'Small', cpu_cores: 2, memory_mb: 2048, disk_gb: 40, price_per_hour: 0.012 },
  { id: 'medium', label: 'Medium', cpu_cores: 4, memory_mb: 4096, disk_gb: 80, price_per_hour: 0.024 },
  { id: 'large', label: 'Large', cpu_cores: 8, memory_mb: 8192, disk_gb: 160, price_per_hour: 0.048 },
  { id: 'xlarge', label: 'X-Large', cpu_cores: 16, memory_mb: 16384, disk_gb: 320, price_per_hour: 0.096 },
];

const defaultRegions: RegionInfo[] = [
  { id: 'us-east-1', label: 'US East 1', country: 'United States' },
  { id: 'us-west-1', label: 'US West 1', country: 'United States' },
  { id: 'eu-central-1', label: 'EU Central 1', country: 'Germany' },
  { id: 'ap-south-1', label: 'AP South 1', country: 'Singapore' },
  { id: 'me-central-1', label: 'ME Central 1', country: 'UAE' },
];

const defaultImages: ImageInfo[] = [
  { id: 'ubuntu-22.04', label: 'Ubuntu 22.04 LTS', version: '22.04' },
  { id: 'ubuntu-24.04', label: 'Ubuntu 24.04 LTS', version: '24.04' },
  { id: 'debian-12', label: 'Debian 12', version: '12' },
];

export function CreateServerForm({ onCreated, onBack }: CreateServerFormProps) {
  const [name, setName] = useState('');
  const [hostname, setHostname] = useState('');
  const [plan, setPlan] = useState<ServerPlan>('small');
  const [region, setRegion] = useState('us-east-1');
  const [image, setImage] = useState('ubuntu-24.04');
  const [plans, setPlans] = useState<ServerPlanInfo[]>(defaultPlans);
  const [regions, setRegions] = useState<RegionInfo[]>(defaultRegions);
  const [images, setImages] = useState<ImageInfo[]>(defaultImages);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      serverService.plans().catch(() => defaultPlans),
      serverService.regions().catch(() => defaultRegions),
      serverService.images().catch(() => defaultImages),
    ]).then(([p, r, i]) => {
      if (Array.isArray(p) && p.length) setPlans(p);
      if (Array.isArray(r) && r.length) setRegions(r);
      if (Array.isArray(i) && i.length) setImages(i);
    });
  }, []);

  const selectedPlan = plans.find((p) => p.id === plan) || defaultPlans[1];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !hostname.trim()) {
      setError('Server name and hostname are required');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const server = await serverService.create({
        name: name.trim(),
        hostname: hostname.trim(),
        plan,
        region,
        image,
      });
      onCreated(server.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-ink-950">
      <Navigation
        onLogoClick={onBack}
        onNavigate={() => onBack()}
      />

      <div className="pt-20 pb-12 px-6 max-w-4xl mx-auto">
        <button onClick={onBack} className="btn-ghost flex items-center gap-2 mb-6 -ml-2">
          <ArrowLeft className="w-4 h-4" />
          Back to Dashboard
        </button>

        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white tracking-tight">Create New Server</h1>
          <p className="text-sm text-ink-400 mt-1">Configure and provision a new virtual machine</p>
        </div>

        {error && (
          <div className="glass-card border-red-500/20 bg-red-500/5 p-4 mb-6 flex items-start gap-3 animate-fade-in">
            <AlertCircle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
            <p className="text-sm text-red-300">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Info */}
          <div className="glass-card p-6">
            <h2 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
              <Server className="w-4 h-4 text-ink-400" />
              Basic Configuration
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-medium text-ink-400 mb-1.5 block">Server Name</label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="my-web-server"
                  className="input-field"
                  required
                />
              </div>
              <div>
                <label className="text-xs font-medium text-ink-400 mb-1.5 block">Hostname</label>
                <input
                  type="text"
                  value={hostname}
                  onChange={(e) => setHostname(e.target.value)}
                  placeholder="web-01.shaheen.cloud"
                  className="input-field font-mono"
                  required
                />
              </div>
            </div>
          </div>

          {/* Plan Selection */}
          <div className="glass-card p-6">
            <h2 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-ink-400" />
              Server Plan
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {plans.map((p) => (
                <button
                  key={p.id}
                  type="button"
                  onClick={() => setPlan(p.id)}
                  className={`relative p-4 rounded-xl border text-left transition-all duration-200 ${
                    plan === p.id
                      ? 'border-ink-500 bg-ink-800/60 shadow-glow'
                      : 'border-ink-800 bg-ink-900/40 hover:border-ink-700 hover:bg-ink-800/40'
                  }`}
                >
                  {plan === p.id && (
                    <div className="absolute top-3 right-3 w-5 h-5 rounded-full bg-ink-100 flex items-center justify-center">
                      <Check className="w-3 h-3 text-ink-950" strokeWidth={3} />
                    </div>
                  )}
                  <div className="text-sm font-semibold text-white mb-1">{p.label}</div>
                  <div className="flex items-center gap-3 text-xs text-ink-400 mb-2">
                    <span className="flex items-center gap-1"><Cpu className="w-3 h-3" />{p.cpu_cores}</span>
                    <span className="flex items-center gap-1"><MemoryStick className="w-3 h-3" />{p.memory_mb >= 1024 ? `${p.memory_mb / 1024}GB` : `${p.memory_mb}MB`}</span>
                    <span className="flex items-center gap-1"><HardDrive className="w-3 h-3" />{p.disk_gb}GB</span>
                  </div>
                  <div className="text-xs text-ink-500 font-mono">${p.price_per_hour.toFixed(3)}/hr</div>
                </button>
              ))}
            </div>
          </div>

          {/* Region & Image */}
          <div className="glass-card p-6">
            <h2 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
              <Globe className="w-4 h-4 text-ink-400" />
              Region & Image
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-medium text-ink-400 mb-1.5 block">Region</label>
                <select
                  value={region}
                  onChange={(e) => setRegion(e.target.value)}
                  className="input-field cursor-pointer"
                >
                  {regions.map((r) => (
                    <option key={r.id} value={r.id} className="bg-ink-900">
                      {r.label} — {r.country}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-xs font-medium text-ink-400 mb-1.5 block">Operating System</label>
                <select
                  value={image}
                  onChange={(e) => setImage(e.target.value)}
                  className="input-field cursor-pointer"
                >
                  {images.map((img) => (
                    <option key={img.id} value={img.id} className="bg-ink-900">
                      {img.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Summary & Submit */}
          <div className="glass-card p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-sm font-semibold text-white flex items-center gap-2">
                <Zap className="w-4 h-4 text-ink-400" />
                Summary
              </h2>
              <div className="text-xs text-ink-400">
                Estimated cost: <span className="text-white font-mono font-semibold">${selectedPlan.price_per_hour.toFixed(3)}/hr</span>
              </div>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
              {[
                { icon: Cpu, label: 'vCPU', value: selectedPlan.cpu_cores },
                { icon: MemoryStick, label: 'Memory', value: selectedPlan.memory_mb >= 1024 ? `${selectedPlan.memory_mb / 1024} GB` : `${selectedPlan.memory_mb} MB` },
                { icon: HardDrive, label: 'Disk', value: `${selectedPlan.disk_gb} GB` },
                { icon: Globe, label: 'Region', value: regions.find((r) => r.id === region)?.label || region },
              ].map((item) => (
                <div key={item.label} className="bg-ink-900/40 rounded-xl p-3 border border-ink-800/50">
                  <item.icon className="w-4 h-4 text-ink-400 mb-2" strokeWidth={1.5} />
                  <div className="text-sm font-semibold text-white">{item.value}</div>
                  <div className="text-xs text-ink-500">{item.label}</div>
                </div>
              ))}
            </div>
            <button
              type="submit"
              disabled={loading || !name.trim() || !hostname.trim()}
              className="btn-primary w-full flex items-center justify-center gap-2 py-3.5"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Provisioning...
                </>
              ) : (
                <>
                  <Zap className="w-4 h-4" />
                  Provision Server
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export type ServerStatus = 'running' | 'stopped' | 'provisioning' | 'error' | 'deleting';

export type ServerPlan = 'micro' | 'small' | 'medium' | 'large' | 'xlarge';

export interface CloudServer {
  id: string;
  name: string;
  hostname: string;
  plan: ServerPlan;
  region: string;
  image: string;
  status: ServerStatus;
  ipv4: string | null;
  ipv6: string | null;
  cpu_cores: number;
  memory_mb: number;
  disk_gb: number;
  created_at: string;
  updated_at: string;
}

export interface CreateServerRequest {
  name: string;
  hostname: string;
  plan: ServerPlan;
  region: string;
  image: string;
}

export interface Job {
  id: string;
  server_id: string | null;
  job_type: 'provision' | 'destroy' | 'start' | 'stop' | 'restart';
  status: 'queued' | 'running' | 'completed' | 'failed';
  message: string;
  created_at: string;
  updated_at: string;
}

export interface HealthStatus {
  status: 'healthy' | 'unhealthy';
  version: string;
  redis_connected: boolean;
  worker_active: boolean;
}

export interface ServerPlanInfo {
  id: ServerPlan;
  label: string;
  cpu_cores: number;
  memory_mb: number;
  disk_gb: number;
  price_per_hour: number;
}

export interface RegionInfo {
  id: string;
  label: string;
  country: string;
}

export interface ImageInfo {
  id: string;
  label: string;
  version: string;
}

import { api } from './api';
import type {
  CloudServer,
  CreateServerRequest,
  Job,
  HealthStatus,
  ServerPlanInfo,
  RegionInfo,
  ImageInfo,
} from './types';

export const serverService = {
  list: () => api.get<CloudServer[]>('/api/v1/servers'),
  get: (id: string) => api.get<CloudServer>(`/api/v1/servers/${id}`),
  create: (data: CreateServerRequest) => api.post<CloudServer>('/api/v1/servers', data),
  delete: (id: string) => api.delete<void>(`/api/v1/servers/${id}`),
  start: (id: string) => api.post<Job>(`/api/v1/servers/${id}/start`),
  stop: (id: string) => api.post<Job>(`/api/v1/servers/${id}/stop`),
  restart: (id: string) => api.post<Job>(`/api/v1/servers/${id}/restart`),

  listJobs: () => api.get<Job[]>('/api/v1/jobs'),
  getJob: (id: string) => api.get<Job>(`/api/v1/jobs/${id}`),

  health: () => api.get<HealthStatus>('/api/v1/health'),

  plans: () => api.get<ServerPlanInfo[]>('/api/v1/plans'),
  regions: () => api.get<RegionInfo[]>('/api/v1/regions'),
  images: () => api.get<ImageInfo[]>('/api/v1/images'),
};

export interface Plugin {
  id: string;
  name: string;
  category: string;
  status: string;
  avgDurationMs: number;
  lastRunAt: string | null;
}

export interface TimingBucket {
  bucket: string;
  count: number;
}

// User and Authentication Types
export interface User {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
  date_joined: string;
  profile?: UserProfile;
}

export interface UserProfile {
  plan: 'free' | 'basic' | 'pro' | 'enterprise';
  plan_expires_at?: string;
  company?: string;
  phone?: string;
  website?: string;
  webhook_notifications: boolean;
  email_notifications: boolean;
  timezone: string;
  total_conversions: number;
  total_storage_used_mb: number;
}

export interface APIKey {
  id: number;
  name: string;
  prefix: string;
  masked_key: string;
  is_active: boolean;
  permissions: Record<string, any>;
  last_used?: string;
  usage_count: number;
  rate_limit_requests_per_hour: number;
  expires_at?: string;
  created_at: string;
}

// File Format and Conversion Types
export interface FileFormat {
  id: number;
  name: string;
  category: string;
  mime_type?: string;
  description?: string;
  is_input_supported: boolean;
  is_output_supported: boolean;
}

export interface ConversionJob {
  id: string;
  user?: number;
  input_file: string;
  input_format: number;
  output_format: number;
  input_format_name?: string;
  output_format_name?: string;
  output_file?: string;
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'cancelled';
  priority?: number;
  progress_percentage: number;
  conversion_options?: Record<string, any>;
  created_at: string;
  updated_at: string;
  started_at?: string;
  completed_at?: string;
  error_message?: string;
  retry_count?: number;
  max_retries?: number;
  webhook_url?: string;
  input_file_size?: number;
  output_file_size?: number;
  is_completed: boolean;
  duration?: number;
}

export interface BatchConversionJob {
  id: string;
  user: number;
  name: string;
  description?: string;
  output_format: FileFormat;
  conversion_options: Record<string, any>;
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'cancelled';
  created_at: string;
  updated_at: string;
  started_at?: string;
  completed_at?: string;
  webhook_url?: string;
  webhook_sent: boolean;
  individual_jobs: ConversionJob[];
  total_files: number;
  completed_files: number;
  failed_files: number;
  progress_percentage: number;
}

export interface ConversionQuota {
  user: number;
  monthly_conversions_limit: number;
  monthly_conversions_used: number;
  monthly_storage_limit_mb: number;
  monthly_storage_used_mb: number;
  last_reset_date: string;
  is_premium: boolean;
  premium_expires_at?: string;
  conversions_remaining: number;
  storage_remaining_mb: number;
}

export interface ConversionHistory {
  id: number;
  user: number;
  conversion_job: string;
  input_format: string;
  output_format: string;
  file_size_bytes: number;
  processing_time_seconds?: number;
  created_at: string;
  ip_address?: string;
  user_agent?: string;
}

// Cloud Storage Types
export interface CloudStorageProvider {
  name: string;
  display_name: string;
  is_active: boolean;
  supports_import: boolean;
  supports_export: boolean;
  required_fields: string[];
  optional_fields: string[];
}

export interface UserCloudStorage {
  id: number;
  user: number;
  provider: CloudStorageProvider;
  name: string;
  credentials: Record<string, any>;
  default_bucket?: string;
  default_folder?: string;
  is_active: boolean;
  is_default: boolean;
  last_tested?: string;
  connection_status: 'unknown' | 'connected' | 'error';
  connection_error?: string;
  created_at: string;
  updated_at: string;
}

// API Response Types
export interface PaginatedResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}

export interface APIResponse<T = any> {
  data?: T;
  message?: string;
  error?: string;
  errors?: Record<string, string[]>;
}

// Health Check Types
export interface HealthStatus {
  status: 'healthy' | 'unhealthy' | 'degraded';
  service: string;
  version: string;
  components?: {
    database: string;
    redis: string;
    celery: string;
    storage: string;
  };
}

// Form and UI Types
export interface ConversionFormData {
  files: File[];
  outputFormat: string;
  conversionOptions?: Record<string, any>;
  webhookUrl?: string;
  priority?: number;
}

export interface UploadProgress {
  loaded: number;
  total: number;
  percentage: number;
}

export interface ConversionSettings {
  quality?: number;
  compression?: string;
  resolution?: string;
  format_options?: Record<string, any>;
}

// Error Types
export interface APIError {
  message: string;
  code?: string;
  details?: any;
  status?: number;
}

import axios from 'axios';

// API Configuration
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

// Create axios instance with default configuration
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds for file uploads
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth tokens
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    const apiKey = localStorage.getItem('api_key');
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    } else if (apiKey) {
      config.headers.Authorization = `Api-Key ${apiKey}`;
    }
    
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear auth tokens on unauthorized
      localStorage.removeItem('auth_token');
      localStorage.removeItem('api_key');
      // Redirect to login if needed
    }
    return Promise.reject(error);
  }
);

// API Service Classes
export class ConversionAPI {
  static async getFormats() {
    return await apiClient.get('/conversions/formats/');
  }

  static async getFormatsByCategory() {
    return await apiClient.get('/conversions/formats/by_category/');
  }

  static async createJob(formData: FormData) {
    return await apiClient.post('/conversions/convert/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }

  static async getJobs(page = 1, limit = 20) {
    return await apiClient.get(`/conversions/jobs/?page=${page}&limit=${limit}`);
  }

  static async getJobStatus(jobId: string) {
    return await apiClient.get(`/conversions/jobs/${jobId}/`);
  }

  static async getJobProgress(jobId: string) {
    return await apiClient.get(`/conversions/jobs/${jobId}/progress/`);
  }

  static async downloadResult(jobId: string) {
    return await apiClient.get(`/conversions/jobs/${jobId}/download/`, {
      responseType: 'blob',
    });
  }

  static async cancelJob(jobId: string) {
    return await apiClient.post(`/conversions/jobs/${jobId}/cancel/`);
  }

  static async retryJob(jobId: string) {
    return await apiClient.post(`/conversions/jobs/${jobId}/retry/`);
  }

  static async batchConvert(files: File[], outputFormat: string, options?: any) {
    const formData = new FormData();
    
    files.forEach((file) => {
      formData.append(`files`, file);
    });
    
    formData.append('output_format', outputFormat);
    formData.append('name', `Batch conversion ${new Date().toLocaleString()}`);
    
    if (options) {
      Object.keys(options).forEach(key => {
        formData.append(key, options[key]);
      });
    }

    return await apiClient.post('/conversions/batch-convert/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }

  static async getUserQuota() {
    return await apiClient.get('/conversions/quota/');
  }

  static async getAnalytics() {
    return await apiClient.get('/conversions/analytics/');
  }
}

export class AuthAPI {
  static async login(username: string, password: string) {
    return await apiClient.post('/auth/login/', {
      username,
      password,
    });
  }

  static async register(userData: any) {
    return await apiClient.post('/auth/register/', userData);
  }

  static async getUserProfile() {
    return await apiClient.get('/auth/profile/');
  }

  static async generateAPIKey(name: string) {
    return await apiClient.post('/auth/api-keys/generate/', { name });
  }

  static async getAPIKeys() {
    return await apiClient.get('/auth/api-keys/');
  }
}

export class HealthAPI {
  static async checkHealth() {
    return await apiClient.get('/health/', {
      baseURL: 'http://127.0.0.1:8000', // Health endpoint is not under /api/v1
    });
  }

  static async checkDetailedHealth() {
    return await apiClient.get('/health/detailed/', {
      baseURL: 'http://127.0.0.1:8000',
    });
  }
}

// Export instances for easy use
export const conversionApi = ConversionAPI;
export const authApi = AuthAPI;
export const healthApi = HealthAPI;

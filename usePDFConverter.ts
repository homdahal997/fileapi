// Custom Hook for PDF to Text Conversion
// usePDFConverter.ts

import { useState } from 'react';

const API_BASE_URL = 'https://your-actual-app-name.onrender.com';

interface ConversionJob {
  job_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  download_url?: string;
  error_message?: string;
}

export const usePDFConverter = () => {
  const [isConverting, setIsConverting] = useState(false);
  const [progress, setProgress] = useState('');
  const [error, setError] = useState('');

  const convertPDFToText = async (file: File): Promise<string | null> => {
    if (!file || file.type !== 'application/pdf') {
      setError('Please provide a valid PDF file');
      return null;
    }

    setIsConverting(true);
    setError('');
    setProgress('Uploading...');

    try {
      // Upload file
      const formData = new FormData();
      formData.append('input_file', file);
      formData.append('output_format', 'txt');

      const response = await fetch(`${API_BASE_URL}/api/convert/`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const job: ConversionJob = await response.json();
      setProgress('Processing...');

      // Poll for completion
      const downloadUrl = await pollJobStatus(job.job_id);
      
      // Download and return text content
      if (downloadUrl) {
        const textResponse = await fetch(downloadUrl);
        const textContent = await textResponse.text();
        setProgress('Completed!');
        return textContent;
      }

      return null;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Conversion failed');
      return null;
    } finally {
      setIsConverting(false);
    }
  };

  const pollJobStatus = async (jobId: string): Promise<string | null> => {
    const maxAttempts = 60;
    let attempts = 0;

    return new Promise((resolve, reject) => {
      const poll = async () => {
        try {
          const response = await fetch(`${API_BASE_URL}/api/convert/${jobId}/status/`);
          const job: ConversionJob = await response.json();

          switch (job.status) {
            case 'completed':
              resolve(`${API_BASE_URL}/api/convert/${jobId}/download/`);
              return;
            case 'failed':
              reject(new Error(job.error_message || 'Conversion failed'));
              return;
            case 'processing':
            case 'pending':
              attempts++;
              if (attempts < maxAttempts) {
                setTimeout(poll, 5000);
              } else {
                reject(new Error('Conversion timeout'));
              }
              break;
          }
        } catch (err) {
          reject(err);
        }
      };
      poll();
    });
  };

  return {
    convertPDFToText,
    isConverting,
    progress,
    error,
  };
};

// Usage Example:
/*
import { usePDFConverter } from './usePDFConverter';

const MyComponent = () => {
  const { convertPDFToText, isConverting, progress, error } = usePDFConverter();

  const handleFileUpload = async (file: File) => {
    const textContent = await convertPDFToText(file);
    if (textContent) {
      console.log('Converted text:', textContent);
      // Use the text content in your app
    }
  };

  return (
    <div>
      <input 
        type="file" 
        accept=".pdf" 
        onChange={(e) => e.target.files?.[0] && handleFileUpload(e.target.files[0])} 
        disabled={isConverting}
      />
      {progress && <p>{progress}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};
*/

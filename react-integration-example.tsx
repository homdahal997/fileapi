// PDF to Text Converter Component for Third-Party React Apps
// Replace API_BASE_URL with your actual Render.com URL

import React, { useState } from 'react';

const API_BASE_URL = 'https://your-actual-app-name.onrender.com';

interface ConversionJob {
  job_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  input_format: string;
  output_format: string;
  created_at: string;
  download_url?: string;
  error_message?: string;
}

const PDFToTextConverter: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isConverting, setIsConverting] = useState(false);
  const [conversionStatus, setConversionStatus] = useState<string>('');
  const [downloadUrl, setDownloadUrl] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Validate file type
      if (file.type !== 'application/pdf') {
        setError('Please select a PDF file');
        return;
      }
      // Validate file size (100MB limit)
      if (file.size > 100 * 1024 * 1024) {
        setError('File size must be less than 100MB');
        return;
      }
      setSelectedFile(file);
      setError('');
    }
  };

  const convertPDFToText = async () => {
    if (!selectedFile) {
      setError('Please select a PDF file first');
      return;
    }

    setIsConverting(true);
    setError('');
    setConversionStatus('Uploading...');

    try {
      // Step 1: Upload and start conversion
      const formData = new FormData();
      formData.append('input_file', selectedFile);
      formData.append('output_format', 'txt');

      const response = await fetch(`${API_BASE_URL}/api/convert/`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const job: ConversionJob = await response.json();
      setConversionStatus('Processing...');

      // Step 2: Poll for completion
      await pollJobStatus(job.job_id);

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Conversion failed');
      setIsConverting(false);
    }
  };

  const pollJobStatus = async (jobId: string) => {
    const maxAttempts = 60; // 5 minutes max
    let attempts = 0;

    const poll = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/convert/${jobId}/status/`);
        
        if (!response.ok) {
          throw new Error('Failed to check conversion status');
        }

        const job: ConversionJob = await response.json();
        
        switch (job.status) {
          case 'completed':
            setConversionStatus('Conversion completed!');
            setDownloadUrl(`${API_BASE_URL}/api/convert/${jobId}/download/`);
            setIsConverting(false);
            return;
            
          case 'failed':
            throw new Error(job.error_message || 'Conversion failed');
            
          case 'processing':
          case 'pending':
            setConversionStatus(`Status: ${job.status}...`);
            attempts++;
            
            if (attempts < maxAttempts) {
              setTimeout(poll, 5000); // Check every 5 seconds
            } else {
              throw new Error('Conversion timeout - please try again');
            }
            break;
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Status check failed');
        setIsConverting(false);
      }
    };

    poll();
  };

  const downloadFile = async () => {
    if (!downloadUrl) return;

    try {
      const response = await fetch(downloadUrl);
      if (!response.ok) {
        throw new Error('Download failed');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${selectedFile?.name?.replace('.pdf', '')}_converted.txt` || 'converted.txt';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Download failed');
    }
  };

  const resetConverter = () => {
    setSelectedFile(null);
    setIsConverting(false);
    setConversionStatus('');
    setDownloadUrl('');
    setError('');
  };

  return (
    <div style={{ maxWidth: '500px', margin: '0 auto', padding: '20px' }}>
      <h2>PDF to Text Converter</h2>
      
      {/* File Selection */}
      <div style={{ marginBottom: '20px' }}>
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileSelect}
          disabled={isConverting}
          style={{ marginBottom: '10px' }}
        />
        {selectedFile && (
          <p>Selected: {selectedFile.name} ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)</p>
        )}
      </div>

      {/* Convert Button */}
      <button
        onClick={convertPDFToText}
        disabled={!selectedFile || isConverting}
        style={{
          backgroundColor: '#007bff',
          color: 'white',
          padding: '10px 20px',
          border: 'none',
          borderRadius: '5px',
          cursor: selectedFile && !isConverting ? 'pointer' : 'not-allowed',
          marginBottom: '20px'
        }}
      >
        {isConverting ? 'Converting...' : 'Convert to Text'}
      </button>

      {/* Status Display */}
      {conversionStatus && (
        <div style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#f8f9fa', borderRadius: '5px' }}>
          <p>{conversionStatus}</p>
        </div>
      )}

      {/* Download Button */}
      {downloadUrl && (
        <div style={{ marginBottom: '20px' }}>
          <button
            onClick={downloadFile}
            style={{
              backgroundColor: '#28a745',
              color: 'white',
              padding: '10px 20px',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
              marginRight: '10px'
            }}
          >
            Download Text File
          </button>
          <button
            onClick={resetConverter}
            style={{
              backgroundColor: '#6c757d',
              color: 'white',
              padding: '10px 20px',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer'
            }}
          >
            Convert Another File
          </button>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div style={{ color: 'red', padding: '10px', backgroundColor: '#f8d7da', borderRadius: '5px' }}>
          <p>Error: {error}</p>
        </div>
      )}
    </div>
  );
};

export default PDFToTextConverter;

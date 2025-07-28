// Enhanced PDF to Text Converter with Structure Preservation
// Replace YOUR_RENDER_APP_NAME with your actual Render.com app name

import React, { useState } from 'react';

const API_BASE_URL = 'https://YOUR_RENDER_APP_NAME.onrender.com';

interface ConversionJob {
  job_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  input_format: string;
  output_format: string;
  created_at: string;
  download_url?: string;
  error_message?: string;
  conversion_options?: {
    preserve_structure: boolean;
    extract_metadata: boolean;
  };
}

interface ConversionOptions {
  preserveStructure: boolean;
  extractMetadata: boolean;
}

const EnhancedPDFConverter: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isConverting, setIsConverting] = useState(false);
  const [conversionStatus, setConversionStatus] = useState<string>('');
  const [downloadUrl, setDownloadUrl] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [rateLimitInfo, setRateLimitInfo] = useState<string>('');
  const [options, setOptions] = useState<ConversionOptions>({
    preserveStructure: true,
    extractMetadata: false,
  });

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

  const handleOptionChange = (option: keyof ConversionOptions, value: boolean) => {
    setOptions(prev => ({
      ...prev,
      [option]: value
    }));
  };

  const convertPDFToText = async () => {
    if (!selectedFile) {
      setError('Please select a PDF file first');
      return;
    }

    setIsConverting(true);
    setError('');
    setConversionStatus('Uploading with enhanced structure detection...');

    try {
      // Step 1: Upload and start conversion with options
      const formData = new FormData();
      formData.append('input_file', selectedFile);
      formData.append('output_format', 'txt');
      formData.append('preserve_structure', options.preserveStructure.toString());
      formData.append('extract_metadata', options.extractMetadata.toString());

      const response = await fetch(`${API_BASE_URL}/api/convert/`, {
        method: 'POST',
        body: formData,
      });

      // Check rate limiting
      const remaining = response.headers.get('X-RateLimit-Remaining');
      const limit = response.headers.get('X-RateLimit-Limit');
      if (remaining && limit) {
        setRateLimitInfo(`Rate limit: ${remaining}/${limit} requests remaining this hour`);
      }

      if (!response.ok) {
        if (response.status === 429) {
          throw new Error('Rate limit exceeded. Please wait before making more requests.');
        }
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const job: ConversionJob = await response.json();
      setConversionStatus('Processing with structure analysis...');

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
            setConversionStatus('Structure-preserved conversion completed!');
            setDownloadUrl(`${API_BASE_URL}/api/convert/${jobId}/download/`);
            setIsConverting(false);
            return;
            
          case 'failed':
            throw new Error(job.error_message || 'Conversion failed');
            
          case 'processing':
          case 'pending':
            const statusMsg = options.preserveStructure 
              ? `Analyzing document structure... (${attempts + 1}/60)`
              : `Processing... (${attempts + 1}/60)`;
            setConversionStatus(statusMsg);
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
      
      const suffix = options.preserveStructure ? '_structured' : '_basic';
      const filename = `${selectedFile?.name?.replace('.pdf', '')}${suffix}.txt` || 'converted.txt';
      a.download = filename;
      
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
    setRateLimitInfo('');
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h2>Enhanced PDF to Text Converter</h2>
      <p style={{ color: '#666', fontSize: '14px', marginBottom: '20px' }}>
        Convert PDFs to text with intelligent structure preservation including headers, lists, and content boundaries.
      </p>
      
      {/* Rate Limit Info */}
      {rateLimitInfo && (
        <div style={{ marginBottom: '15px', padding: '8px', backgroundColor: '#e7f3ff', borderRadius: '4px', fontSize: '12px' }}>
          {rateLimitInfo}
        </div>
      )}
      
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

      {/* Conversion Options */}
      <div style={{ marginBottom: '20px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '5px' }}>
        <h4 style={{ margin: '0 0 10px 0' }}>Conversion Options</h4>
        
        <label style={{ display: 'block', marginBottom: '10px' }}>
          <input
            type="checkbox"
            checked={options.preserveStructure}
            onChange={(e) => handleOptionChange('preserveStructure', e.target.checked)}
            disabled={isConverting}
            style={{ marginRight: '8px' }}
          />
          <strong>Preserve Document Structure</strong>
          <div style={{ fontSize: '12px', color: '#666', marginLeft: '20px' }}>
            Detect and preserve headers, subheaders, lists, and content boundaries
          </div>
        </label>
        
        <label style={{ display: 'block' }}>
          <input
            type="checkbox"
            checked={options.extractMetadata}
            onChange={(e) => handleOptionChange('extractMetadata', e.target.checked)}
            disabled={isConverting}
            style={{ marginRight: '8px' }}
          />
          <strong>Extract Document Metadata</strong>
          <div style={{ fontSize: '12px', color: '#666', marginLeft: '20px' }}>
            Include document statistics and structural analysis in output
          </div>
        </label>
      </div>

      {/* Convert Button */}
      <button
        onClick={convertPDFToText}
        disabled={!selectedFile || isConverting}
        style={{
          backgroundColor: '#007bff',
          color: 'white',
          padding: '12px 24px',
          border: 'none',
          borderRadius: '5px',
          cursor: selectedFile && !isConverting ? 'pointer' : 'not-allowed',
          marginBottom: '20px',
          fontSize: '16px'
        }}
      >
        {isConverting ? 'Converting...' : 'Convert with Structure Detection'}
      </button>

      {/* Status Display */}
      {conversionStatus && (
        <div style={{ marginBottom: '20px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '5px' }}>
          <p style={{ margin: 0 }}>{conversionStatus}</p>
          {options.preserveStructure && isConverting && (
            <div style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>
              Analyzing font sizes, detecting headers, identifying lists and content boundaries...
            </div>
          )}
        </div>
      )}

      {/* Download Section */}
      {downloadUrl && (
        <div style={{ marginBottom: '20px', padding: '15px', backgroundColor: '#d4edda', borderRadius: '5px' }}>
          <h4 style={{ margin: '0 0 10px 0', color: '#155724' }}>Conversion Complete!</h4>
          <p style={{ margin: '0 0 15px 0', fontSize: '14px', color: '#155724' }}>
            {options.preserveStructure 
              ? 'Your PDF has been converted with structure preservation. Headers, lists, and content boundaries have been detected and formatted.'
              : 'Your PDF has been converted to plain text.'}
          </p>
          
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
            Download Structured Text
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
        <div style={{ color: 'red', padding: '15px', backgroundColor: '#f8d7da', borderRadius: '5px' }}>
          <p style={{ margin: 0 }}>Error: {error}</p>
        </div>
      )}

      {/* Feature Info */}
      <div style={{ marginTop: '30px', padding: '15px', backgroundColor: '#e9ecef', borderRadius: '5px', fontSize: '14px' }}>
        <h4 style={{ margin: '0 0 10px 0' }}>Enhanced Features:</h4>
        <ul style={{ margin: 0, paddingLeft: '20px' }}>
          <li>Intelligent header detection (H1-H6 levels)</li>
          <li>List structure preservation (bullets, numbers, nested lists)</li>
          <li>Content boundary detection</li>
          <li>Table content identification</li>
          <li>Page break indicators</li>
          <li>Document structure metadata</li>
          <li>Multiple extraction methods with fallbacks</li>
        </ul>
      </div>
    </div>
  );
};

export default EnhancedPDFConverter;

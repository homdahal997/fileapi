import React, { useState } from 'react';
import './FileConverter.css';

interface ConversionJob {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  input_format: { name: string };
  output_format: { name: string };
  error_message?: string;
  download_url?: string;
}

const FileConverter: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [outputFormat, setOutputFormat] = useState<string>('txt');
  const [isConverting, setIsConverting] = useState<boolean>(false);
  const [job, setJob] = useState<ConversionJob | null>(null);
  const [error, setError] = useState<string>('');

  const API_BASE = 'http://127.0.0.1:8000/api/v1/conversions';

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setError('');
    }
  };

  const handleConvert = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setIsConverting(true);
    setError('');

    try {
      // Create FormData for file upload
      const formData = new FormData();
      formData.append('input_file', selectedFile);
      formData.append('output_format', outputFormat);

      // Start conversion
      const response = await fetch(`${API_BASE}/convert/`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      if (result.success) {
        // Poll for job completion
        await pollJobStatus(result.job_id);
      } else {
        throw new Error(result.error || 'Conversion failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setIsConverting(false);
    }
  };

  const pollJobStatus = async (jobId: string) => {
    const maxAttempts = 30; // 30 seconds timeout
    let attempts = 0;

    const poll = async () => {
      try {
        const response = await fetch(`${API_BASE}/jobs/${jobId}/`);
        if (!response.ok) {
          throw new Error('Failed to check job status');
        }

        const jobData: ConversionJob = await response.json();
        setJob(jobData);

        if (jobData.status === 'completed') {
          setIsConverting(false);
          return;
        } else if (jobData.status === 'failed') {
          setError(jobData.error_message || 'Conversion failed');
          setIsConverting(false);
          return;
        } else if (attempts < maxAttempts) {
          attempts++;
          setTimeout(poll, 1000); // Poll every second
        } else {
          setError('Conversion timed out');
          setIsConverting(false);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to check status');
        setIsConverting(false);
      }
    };

    poll();
  };

  const handleDownload = async () => {
    if (!job?.id) return;

    try {
      const response = await fetch(`${API_BASE}/jobs/${job.id}/download/`);
      if (!response.ok) {
        throw new Error('Download failed');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `converted.${outputFormat}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Download failed');
    }
  };

  const getFileExtension = (filename: string) => {
    return filename.split('.').pop()?.toLowerCase() || '';
  };

  const isConversionSupported = () => {
    if (!selectedFile) return false;
    const inputFormat = getFileExtension(selectedFile.name);
    
    // Define supported conversions
    const supportedConversions: Record<string, string[]> = {
      'pdf': ['txt', 'html'],
      'txt': ['docx', 'html', 'pdf'],
      'docx': ['txt', 'html'],
      'html': ['txt', 'docx'],
    };

    return supportedConversions[inputFormat]?.includes(outputFormat) || false;
  };

  return (
    <div className="file-converter">
      <div className="converter-container">
        <h1>File Converter</h1>
        <p>Convert your documents between different formats</p>

        {/* File Selection */}
        <div className="form-group">
          <label htmlFor="file-input">Select File:</label>
          <input
            id="file-input"
            type="file"
            onChange={handleFileSelect}
            accept=".pdf,.txt,.docx,.html"
            disabled={isConverting}
          />
          {selectedFile && (
            <div className="file-info">
              <strong>Selected:</strong> {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
              <br />
              <strong>Format:</strong> {getFileExtension(selectedFile.name).toUpperCase()}
            </div>
          )}
        </div>

        {/* Output Format Selection */}
        <div className="form-group">
          <label htmlFor="output-format">Convert To:</label>
          <select
            id="output-format"
            value={outputFormat}
            onChange={(e) => setOutputFormat(e.target.value)}
            disabled={isConverting}
          >
            <option value="txt">Text (.txt)</option>
            <option value="docx">Word Document (.docx)</option>
            <option value="html">HTML (.html)</option>
            <option value="pdf">PDF (.pdf)</option>
          </select>
        </div>

        {/* Conversion Support Check */}
        {selectedFile && !isConversionSupported() && (
          <div className="warning">
            ⚠️ Conversion from {getFileExtension(selectedFile.name).toUpperCase()} to {outputFormat.toUpperCase()} is not supported
          </div>
        )}

        {/* Convert Button */}
        <button
          onClick={handleConvert}
          disabled={!selectedFile || isConverting || !isConversionSupported()}
          className="convert-btn"
        >
          {isConverting ? 'Converting...' : 'Convert File'}
        </button>

        {/* Progress Indicator */}
        {isConverting && (
          <div className="progress">
            <div className="progress-bar">
              <div className="progress-fill"></div>
            </div>
            <p>Converting your file, please wait...</p>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="error">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Job Status */}
        {job && (
          <div className="job-status">
            <h3>Conversion Status</h3>
            <div className="status-info">
              <p><strong>Job ID:</strong> {job.id}</p>
              <p><strong>Status:</strong> 
                <span className={`status ${job.status}`}>{job.status}</span>
              </p>
              <p><strong>From:</strong> {job.input_format.name.toUpperCase()}</p>
              <p><strong>To:</strong> {job.output_format.name.toUpperCase()}</p>
            </div>

            {job.status === 'completed' && (
              <button onClick={handleDownload} className="download-btn">
                📥 Download Converted File
              </button>
            )}
          </div>
        )}

        {/* Reset Button */}
        {job && !isConverting && (
          <button
            onClick={() => {
              setJob(null);
              setSelectedFile(null);
              setError('');
            }}
            className="reset-btn"
          >
            Convert Another File
          </button>
        )}
      </div>
    </div>
  );
};

export default FileConverter;

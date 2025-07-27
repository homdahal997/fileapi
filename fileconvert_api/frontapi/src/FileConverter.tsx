import { useState, useEffect } from 'react'

// File format interface
interface FileFormat {
  id: number
  name: string
  category: string
  description: string
  is_input_supported: boolean
  is_output_supported: boolean
}

interface ConversionJob {
  id: number
  filename: string
  sourceFormat: string
  targetFormat: string
  status: 'uploading' | 'processing' | 'completed' | 'error'
  progress: number
  fileSize: number
  createdAt: Date
  downloadUrl?: string
  conversionId?: number
  error?: string
}

function FileConverter() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [targetFormat, setTargetFormat] = useState<string>('')
  const [jobs, setJobs] = useState<ConversionJob[]>([])
  const [dragActive, setDragActive] = useState(false)
  const [error, setError] = useState<string>('')
  const [formats, setFormats] = useState<FileFormat[]>([])
  const [loadingFormats, setLoadingFormats] = useState(true)

  // Fetch available formats on component mount
  useEffect(() => {
    const fetchFormats = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/conversions/formats/')
        if (response.ok) {
          const data = await response.json()
          // Filter to only output-supported formats for the dropdown
          const outputFormats = data.results.filter((format: FileFormat) => format.is_output_supported)
          setFormats(outputFormats)
        }
      } catch (error) {
        console.error('Failed to fetch formats:', error)
        // Fallback to some basic formats if API fails
        setFormats([
          { id: 1, name: 'pdf', category: 'document', description: 'Portable Document Format', is_input_supported: true, is_output_supported: true },
          { id: 2, name: 'docx', category: 'document', description: 'Microsoft Word Document', is_input_supported: true, is_output_supported: true },
          { id: 3, name: 'txt', category: 'document', description: 'Plain Text File', is_input_supported: true, is_output_supported: true },
          { id: 4, name: 'jpg', category: 'image', description: 'JPEG Image', is_input_supported: true, is_output_supported: true },
          { id: 5, name: 'png', category: 'image', description: 'PNG Image', is_input_supported: true, is_output_supported: true },
        ])
      } finally {
        setLoadingFormats(false)
      }
    }
    
    fetchFormats()
  }, [])

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      setError('')
    }
  }

  const handleDragEvents = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
  }

  const handleDragEnter = (e: React.DragEvent) => {
    handleDragEvents(e)
    setDragActive(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    handleDragEvents(e)
    setDragActive(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    handleDragEvents(e)
    setDragActive(false)
    const files = e.dataTransfer.files
    if (files && files[0]) {
      setSelectedFile(files[0])
      setError('')
    }
  }

  const getFileExtension = (filename: string) => {
    return filename.split('.').pop()?.toLowerCase() || ''
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const performActualConversion = async (job: ConversionJob, file: File) => {
    try {
      // Update status to processing
      setJobs(prev => prev.map(j => 
        j.id === job.id ? { ...j, status: 'processing' as const } : j
      ))

      // Create FormData for file upload
      const formData = new FormData()
      formData.append('file', file)
      formData.append('output_format', job.targetFormat.toLowerCase())
      formData.append('webhook_url', '') // Add empty webhook_url to avoid NOT NULL constraint

      // Make API call to Django backend
      const response = await fetch('http://127.0.0.1:8000/api/v1/conversions/convert/', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.text()
        console.error('API Error Response:', errorData)
        throw new Error(`Conversion failed: ${response.status} ${response.statusText} - ${errorData}`)
      }

      const result = await response.json()
      
      // Update job with conversion result
      setJobs(prev => prev.map(j => 
        j.id === job.id ? { 
          ...j, 
          status: 'completed' as const, 
          progress: 100,
          downloadUrl: result.download_url || `http://127.0.0.1:8000/api/v1/conversions/jobs/${result.id}/download/`,
          conversionId: result.id
        } : j
      ))

    } catch (error) {
      console.error('Conversion error:', error)
      setJobs(prev => prev.map(j => 
        j.id === job.id ? { 
          ...j, 
          status: 'error' as const, 
          error: error instanceof Error ? error.message : 'Conversion failed'
        } : j
      ))
    }
  }

  const handleConvert = async () => {
    if (!selectedFile || !targetFormat) {
      setError('Please select a file and target format')
      return
    }

    const sourceFormat = getFileExtension(selectedFile.name)
    if (sourceFormat === targetFormat) {
      setError('Source and target formats cannot be the same')
      return
    }

    // Create new job
    const newJob: ConversionJob = {
      id: Date.now(),
      filename: selectedFile.name,
      sourceFormat: sourceFormat.toUpperCase(),
      targetFormat: targetFormat.toUpperCase(),
      status: 'uploading',
      progress: 0,
      fileSize: selectedFile.size,
      createdAt: new Date()
    }

    setJobs(prev => [newJob, ...prev])
    setError('')

    // Start conversion with real backend
    performActualConversion(newJob, selectedFile)

    // Reset form
    setSelectedFile(null)
    setTargetFormat('')
  }

  const downloadFile = async (job: ConversionJob) => {
    try {
      if (job.downloadUrl) {
        // Download from Django backend URL
        const response = await fetch(job.downloadUrl)
        if (!response.ok) {
          throw new Error('Download failed')
        }
        
        const blob = await response.blob()
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${job.filename.split('.')[0]}.${job.targetFormat.toLowerCase()}`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
      } else if (job.conversionId) {
        // Alternative: download by conversion ID
        const response = await fetch(`http://127.0.0.1:8000/api/v1/conversions/jobs/${job.conversionId}/download/`)
        if (!response.ok) {
          throw new Error('Download failed')
        }
        
        const blob = await response.blob()
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${job.filename.split('.')[0]}.${job.targetFormat.toLowerCase()}`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
      } else {
        throw new Error('No download URL available')
      }
    } catch (error) {
      console.error('Download error:', error)
      alert(`Download failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '20px',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <h1 style={{
            fontSize: '3.5rem',
            fontWeight: 'bold',
            color: 'white',
            marginBottom: '10px',
            textShadow: '0 2px 4px rgba(0,0,0,0.3)'
          }}>
            🚀 File Converter Pro
          </h1>
          <p style={{
            fontSize: '1.2rem',
            color: 'rgba(255,255,255,0.9)',
            marginBottom: '20px'
          }}>
            Convert files between 200+ formats instantly
          </p>
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            gap: '30px',
            flexWrap: 'wrap'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'white' }}>
              <div style={{ width: '8px', height: '8px', background: '#4ade80', borderRadius: '50%' }}></div>
              <span>200+ Formats</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'white' }}>
              <div style={{ width: '8px', height: '8px', background: '#60a5fa', borderRadius: '50%' }}></div>
              <span>Lightning Fast</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'white' }}>
              <div style={{ width: '8px', height: '8px', background: '#f472b6', borderRadius: '50%' }}></div>
              <span>Secure & Private</span>
            </div>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px' }}>
          {/* Upload & Convert Section */}
          <div style={{
            background: 'rgba(255,255,255,0.95)',
            borderRadius: '20px',
            padding: '30px',
            boxShadow: '0 20px 40px rgba(0,0,0,0.1)'
          }}>
            <h2 style={{
              fontSize: '1.8rem',
              fontWeight: 'bold',
              color: '#333',
              marginBottom: '20px',
              display: 'flex',
              alignItems: 'center',
              gap: '10px'
            }}>
              📁 Upload & Convert
            </h2>

            {/* File Upload Area */}
            <div
              style={{
                border: `3px dashed ${dragActive ? '#667eea' : selectedFile ? '#4ade80' : '#ccc'}`,
                borderRadius: '15px',
                padding: '40px 20px',
                textAlign: 'center',
                marginBottom: '20px',
                cursor: 'pointer',
                backgroundColor: dragActive ? '#f0f4ff' : selectedFile ? '#f0fdf4' : '#fafafa',
                transition: 'all 0.3s ease',
                transform: dragActive ? 'scale(1.02)' : 'scale(1)'
              }}
              onClick={() => document.getElementById('file-upload')?.click()}
              onDragEnter={handleDragEnter}
              onDragOver={handleDragEvents}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              {selectedFile ? (
                <div>
                  <div style={{ fontSize: '4rem', marginBottom: '15px' }}>✅</div>
                  <h3 style={{ fontSize: '1.3rem', fontWeight: 'bold', color: '#333', marginBottom: '8px' }}>
                    {selectedFile.name}
                  </h3>
                  <p style={{ color: '#666', marginBottom: '15px' }}>
                    {formatFileSize(selectedFile.size)} • {selectedFile.type || 'Unknown type'}
                  </p>
                  <div style={{
                    display: 'inline-block',
                    padding: '6px 12px',
                    background: '#e0e7ff',
                    color: '#3730a3',
                    borderRadius: '20px',
                    fontSize: '0.9rem',
                    fontWeight: 'bold'
                  }}>
                    {getFileExtension(selectedFile.name).toUpperCase()} FILE
                  </div>
                  <div style={{ marginTop: '15px' }}>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        setSelectedFile(null)
                      }}
                      style={{
                        padding: '8px 16px',
                        border: '2px solid #ddd',
                        borderRadius: '8px',
                        background: 'white',
                        cursor: 'pointer',
                        fontSize: '0.9rem'
                      }}
                    >
                      Remove File
                    </button>
                  </div>
                </div>
              ) : (
                <div>
                  <div style={{ fontSize: '4rem', marginBottom: '15px' }}>📁</div>
                  <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#333', marginBottom: '10px' }}>
                    Drop your file here
                  </h3>
                  <p style={{ color: '#666', marginBottom: '20px', fontSize: '1.1rem' }}>
                    or click to browse your computer
                  </p>
                  <button style={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    color: 'white',
                    border: 'none',
                    padding: '12px 24px',
                    borderRadius: '10px',
                    fontSize: '1.1rem',
                    fontWeight: 'bold',
                    cursor: 'pointer'
                  }}>
                    Choose File
                  </button>
                  <div style={{ marginTop: '20px', display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '8px' }}>
                    {['PDF', 'DOCX', 'JPG', 'PNG', 'MP4', 'TXT', '+200 more'].map(format => (
                      <span key={format} style={{
                        padding: '4px 8px',
                        background: '#f3f4f6',
                        color: '#6b7280',
                        borderRadius: '12px',
                        fontSize: '0.8rem'
                      }}>
                        {format}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              <input
                type="file"
                onChange={handleFileSelect}
                style={{ display: 'none' }}
                id="file-upload"
                accept="*/*"
              />
            </div>

            {/* Target Format Selection */}
            <div style={{ marginBottom: '20px' }}>
              <label style={{
                display: 'block',
                fontSize: '1.1rem',
                fontWeight: 'bold',
                color: '#333',
                marginBottom: '8px'
              }}>
                🎯 Convert to:
              </label>
              <select
                value={targetFormat}
                onChange={(e) => setTargetFormat(e.target.value)}
                style={{
                  width: '100%',
                  padding: '12px',
                  fontSize: '1rem',
                  border: '2px solid #e5e7eb',
                  borderRadius: '10px',
                  backgroundColor: 'white',
                  cursor: 'pointer'
                }}
              >
                <option value="">
                  {loadingFormats ? '🔄 Loading formats...' : '🔍 Choose target format...'}
                </option>
                {formats.map(format => (
                  <option key={format.id} value={format.name}>
                    {format.name.toUpperCase()} - {format.description}
                  </option>
                ))}
              </select>
            </div>

            {/* Error Message */}
            {error && (
              <div style={{
                padding: '12px',
                background: '#fef2f2',
                border: '1px solid #fecaca',
                borderRadius: '8px',
                color: '#dc2626',
                marginBottom: '20px',
                fontSize: '0.9rem'
              }}>
                ⚠️ {error}
              </div>
            )}

            {/* Convert Button */}
            <button
              onClick={handleConvert}
              disabled={!selectedFile || !targetFormat}
              style={{
                width: '100%',
                padding: '16px',
                fontSize: '1.2rem',
                fontWeight: 'bold',
                background: (!selectedFile || !targetFormat) 
                  ? '#d1d5db' 
                  : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '12px',
                cursor: (!selectedFile || !targetFormat) ? 'not-allowed' : 'pointer',
                boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
                transition: 'transform 0.2s ease',
                transform: 'scale(1)'
              }}
              onMouseOver={(e) => {
                if (selectedFile && targetFormat) {
                  e.currentTarget.style.transform = 'scale(1.02)'
                }
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.transform = 'scale(1)'
              }}
            >
              🚀 Start Conversion
            </button>
          </div>

          {/* Conversion Jobs Section */}
          <div style={{
            background: 'rgba(255,255,255,0.95)',
            borderRadius: '20px',
            padding: '30px',
            boxShadow: '0 20px 40px rgba(0,0,0,0.1)'
          }}>
            <h2 style={{
              fontSize: '1.8rem',
              fontWeight: 'bold',
              color: '#333',
              marginBottom: '20px',
              display: 'flex',
              alignItems: 'center',
              gap: '10px'
            }}>
              📋 Conversion Queue
            </h2>

            <div style={{ maxHeight: '500px', overflowY: 'auto' }}>
              {jobs.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '60px 20px', color: '#6b7280' }}>
                  <div style={{ fontSize: '4rem', marginBottom: '20px' }}>📝</div>
                  <h3 style={{ fontSize: '1.3rem', marginBottom: '10px' }}>No conversions yet</h3>
                  <p>Upload a file above to start your first conversion</p>
                </div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                  {jobs.map((job) => (
                    <div
                      key={job.id}
                      style={{
                        border: '1px solid #e5e7eb',
                        borderRadius: '12px',
                        padding: '20px',
                        background: 'white',
                        boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                          <div style={{
                            width: '8px',
                            height: '8px',
                            borderRadius: '50%',
                            background: 
                              job.status === 'completed' ? '#22c55e' :
                              job.status === 'processing' ? '#3b82f6' :
                              job.status === 'error' ? '#ef4444' : '#f59e0b'
                          }}></div>
                          <h4 style={{ fontSize: '1rem', fontWeight: 'bold', color: '#333' }}>
                            {job.filename}
                          </h4>
                        </div>
                        <span style={{
                          padding: '4px 8px',
                          borderRadius: '12px',
                          fontSize: '0.8rem',
                          fontWeight: 'bold',
                          background: 
                            job.status === 'completed' ? '#dcfce7' :
                            job.status === 'processing' ? '#dbeafe' :
                            job.status === 'error' ? '#fee2e2' : '#fef3c7',
                          color:
                            job.status === 'completed' ? '#166534' :
                            job.status === 'processing' ? '#1e40af' :
                            job.status === 'error' ? '#991b1b' : '#92400e'
                        }}>
                          {job.status.toUpperCase()}
                        </span>
                      </div>

                      <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '12px', fontSize: '0.9rem', color: '#6b7280' }}>
                        <span>{job.sourceFormat}</span>
                        <span>→</span>
                        <span style={{ fontWeight: 'bold', color: '#667eea' }}>{job.targetFormat}</span>
                        <span>•</span>
                        <span>{formatFileSize(job.fileSize)}</span>
                      </div>

                      {job.status === 'processing' && (
                        <div style={{ marginBottom: '12px' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '5px' }}>
                            <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>Converting...</span>
                            <span style={{ fontSize: '0.8rem', fontWeight: 'bold', color: '#3b82f6' }}>{job.progress}%</span>
                          </div>
                          <div style={{
                            width: '100%',
                            height: '6px',
                            background: '#e5e7eb',
                            borderRadius: '3px',
                            overflow: 'hidden'
                          }}>
                            <div style={{
                              width: `${job.progress}%`,
                              height: '100%',
                              background: 'linear-gradient(90deg, #3b82f6, #1d4ed8)',
                              transition: 'width 0.3s ease'
                            }}></div>
                          </div>
                        </div>
                      )}

                      {job.status === 'error' && job.error && (
                        <div style={{
                          padding: '8px',
                          background: '#fef2f2',
                          border: '1px solid #fecaca',
                          borderRadius: '6px',
                          color: '#dc2626',
                          marginBottom: '12px',
                          fontSize: '0.8rem'
                        }}>
                          ❌ {job.error}
                        </div>
                      )}

                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>
                          {job.createdAt.toLocaleString()}
                        </span>
                        {job.status === 'completed' && (
                          <button
                            onClick={() => downloadFile(job)}
                            style={{
                              padding: '6px 12px',
                              background: 'linear-gradient(135deg, #22c55e, #16a34a)',
                              color: 'white',
                              border: 'none',
                              borderRadius: '6px',
                              fontSize: '0.8rem',
                              fontWeight: 'bold',
                              cursor: 'pointer'
                            }}
                          >
                            📥 Download
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default FileConverter

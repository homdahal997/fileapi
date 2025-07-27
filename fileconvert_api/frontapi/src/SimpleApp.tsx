import { useState } from 'react'

function SimpleApp() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [targetFormat, setTargetFormat] = useState<string>('')

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
    }
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '20px',
      color: 'white',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <h1 style={{ 
          fontSize: '3rem', 
          textAlign: 'center', 
          marginBottom: '2rem',
          fontWeight: 'bold'
        }}>
          🚀 File Converter Pro
        </h1>
        
        <div style={{ 
          background: 'rgba(255, 255, 255, 0.95)',
          borderRadius: '16px',
          padding: '2rem',
          color: '#333',
          boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
          marginBottom: '2rem'
        }}>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem', color: '#333' }}>Upload & Convert</h2>
          
          {/* File Upload */}
          <div style={{ 
            border: '3px dashed #ccc',
            borderRadius: '12px',
            padding: '2rem',
            textAlign: 'center',
            marginBottom: '1.5rem',
            cursor: 'pointer',
            backgroundColor: selectedFile ? '#f0f9ff' : '#fafafa',
            transition: 'all 0.3s ease'
          }}
          onClick={() => document.getElementById('file-upload')?.click()}
          onMouseOver={(e) => e.currentTarget.style.borderColor = '#667eea'}
          onMouseOut={(e) => e.currentTarget.style.borderColor = '#ccc'}
          >
            {selectedFile ? (
              <div>
                <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>✅</div>
                <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem', color: '#333' }}>{selectedFile.name}</h3>
                <p style={{ color: '#666' }}>{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                <button 
                  onClick={(e) => {
                    e.stopPropagation()
                    setSelectedFile(null)
                  }}
                  style={{
                    marginTop: '1rem',
                    padding: '8px 16px',
                    border: '1px solid #ddd',
                    borderRadius: '6px',
                    background: 'white',
                    cursor: 'pointer'
                  }}
                >
                  Remove File
                </button>
              </div>
            ) : (
              <div>
                <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📁</div>
                <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem', color: '#333' }}>Drop your file here</h3>
                <p style={{ marginBottom: '1rem', color: '#666' }}>or click to browse your computer</p>
                <button style={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  border: 'none',
                  padding: '12px 24px',
                  borderRadius: '8px',
                  fontSize: '1rem',
                  cursor: 'pointer',
                  fontWeight: 'bold'
                }}>
                  Choose File
                </button>
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

          {/* Format Selection */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ 
              display: 'block', 
              fontSize: '1.1rem', 
              fontWeight: 'bold', 
              marginBottom: '0.5rem',
              color: '#333'
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
                border: '2px solid #ddd',
                borderRadius: '8px',
                backgroundColor: 'white',
                color: '#333'
              }}
            >
              <option value="">🔍 Choose target format...</option>
              <option value="pdf">PDF - Portable Document Format</option>
              <option value="docx">DOCX - Microsoft Word Document</option>
              <option value="jpg">JPG - JPEG Image</option>
              <option value="png">PNG - Portable Network Graphics</option>
              <option value="mp4">MP4 - MPEG-4 Video</option>
              <option value="txt">TXT - Plain Text</option>
              <option value="xlsx">XLSX - Microsoft Excel Spreadsheet</option>
              <option value="csv">CSV - Comma Separated Values</option>
            </select>
          </div>

          {/* Convert Button */}
          <button
            disabled={!selectedFile || !targetFormat}
            style={{
              width: '100%',
              padding: '16px',
              fontSize: '1.2rem',
              fontWeight: 'bold',
              background: (!selectedFile || !targetFormat) ? '#ccc' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              border: 'none',
              borderRadius: '12px',
              cursor: (!selectedFile || !targetFormat) ? 'not-allowed' : 'pointer',
              boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
              transition: 'all 0.3s ease'
            }}
            onClick={() => {
              if (selectedFile && targetFormat) {
                alert(`🚀 Converting ${selectedFile.name} to ${targetFormat.toUpperCase()}!\n\nThis is a demo - the actual conversion would start here.`)
              }
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
            {(!selectedFile || !targetFormat) ? '⚠️ Select file and format' : '🚀 Start Conversion'}
          </button>
        </div>

        {/* Status Card */}
        <div style={{ 
          background: 'rgba(255, 255, 255, 0.9)',
          borderRadius: '16px',
          padding: '1.5rem',
          color: '#333',
          boxShadow: '0 10px 20px rgba(0,0,0,0.1)'
        }}>
          <h3 style={{ fontSize: '1.2rem', marginBottom: '1rem', color: '#333' }}>🔧 System Status</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
            <div style={{ textAlign: 'center', padding: '1rem' }}>
              <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>✅</div>
              <p style={{ fontWeight: 'bold', color: '#333' }}>React Working</p>
            </div>
            <div style={{ textAlign: 'center', padding: '1rem' }}>
              <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>✅</div>
              <p style={{ fontWeight: 'bold', color: '#333' }}>File Upload Ready</p>
            </div>
            <div style={{ textAlign: 'center', padding: '1rem' }}>
              <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>✅</div>
              <p style={{ fontWeight: 'bold', color: '#333' }}>Format Selection Ready</p>
            </div>
            <div style={{ textAlign: 'center', padding: '1rem' }}>
              <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🚀</div>
              <p style={{ fontWeight: 'bold', color: '#333' }}>200+ Formats Supported</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SimpleApp

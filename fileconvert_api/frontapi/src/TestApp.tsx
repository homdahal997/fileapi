

function TestApp() {
  return (
    <div style={{ 
      minHeight: '100vh', 
      padding: '20px',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      color: 'white',
      fontFamily: 'Arial, sans-serif'
    }}>
      <h1 style={{ fontSize: '3rem', textAlign: 'center', marginBottom: '2rem' }}>
        File Converter Pro - Test
      </h1>
      <div style={{
        maxWidth: '800px',
        margin: '0 auto',
        background: 'rgba(255, 255, 255, 0.1)',
        padding: '2rem',
        borderRadius: '1rem',
        backdropFilter: 'blur(10px)'
      }}>
        <h2>UI Test</h2>
        <p>If you can see this, React is working!</p>
        <div style={{ marginTop: '2rem' }}>
          <p>✅ React rendering works</p>
          <p>✅ CSS gradients work</p>
          <p>✅ Basic styling works</p>
        </div>
        <button style={{
          background: 'linear-gradient(45deg, #ff6b6b, #ee5a24)',
          border: 'none',
          padding: '12px 24px',
          borderRadius: '8px',
          color: 'white',
          cursor: 'pointer',
          marginTop: '1rem',
          fontSize: '1rem'
        }}>
          Test Button
        </button>
      </div>
    </div>
  )
}

export default TestApp

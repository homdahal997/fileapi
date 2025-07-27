function TestSimple() {
  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1>🚀 Test Component</h1>
      <p>If you can see this, React is working!</p>
      <button onClick={() => alert('Button clicked!')}>
        Click me!
      </button>
    </div>
  )
}

export default TestSimple

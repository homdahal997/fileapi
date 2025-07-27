import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import FileConverter from './FileConverter'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <FileConverter />
  </StrictMode>,
)

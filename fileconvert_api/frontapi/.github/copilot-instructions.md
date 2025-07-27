# Copilot Instructions for File Conversion API Frontend

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is a React TypeScript frontend built with Vite for testing our File Conversion API service. The application provides a modern, intuitive interface for testing file conversions with real-time progress tracking and comprehensive format support.

## Technology Stack
- **Frontend Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS with custom design system
- **UI Components**: Radix UI primitives for accessibility
- **HTTP Client**: Axios for API communication
- **File Upload**: React Dropzone for drag-and-drop functionality
- **Icons**: Lucide React for consistent iconography

## Architecture Principles
- **Component-Based**: Modular, reusable React components
- **Type Safety**: Full TypeScript coverage for better developer experience
- **Accessibility**: WCAG compliant using Radix UI primitives
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **API Integration**: RESTful API communication with proper error handling
- **Real-time Updates**: WebSocket integration for conversion progress

## Project Structure
```
src/
├── components/           # Reusable UI components
│   ├── ui/              # Base UI components (buttons, inputs, etc.)
│   ├── file-upload/     # File upload and dropzone components
│   ├── conversion/      # Conversion-related components
│   └── layout/          # Layout and navigation components
├── hooks/               # Custom React hooks
├── lib/                 # Utility functions and API client
├── types/               # TypeScript type definitions
├── services/            # API service layer
└── pages/               # Main application pages
```

## API Integration
- **Base URL**: http://127.0.0.1:8000/api/v1/
- **Authentication**: JWT tokens and API keys
- **Endpoints**: 
  - `/conversions/` - File conversion operations
  - `/auth/` - Authentication and user management
  - `/storage/` - Cloud storage integration

## Component Guidelines
- Use TypeScript interfaces for all props
- Implement proper error boundaries
- Follow React best practices (hooks, context)
- Use Tailwind CSS classes for styling
- Ensure accessibility with proper ARIA labels
- Implement loading states and error handling

## File Upload Features
- Drag and drop interface
- Multiple file selection
- File type validation
- Progress tracking
- Format preview and selection
- Batch conversion support

## Conversion Workflow
1. **File Selection**: Drag & drop or browse files
2. **Format Selection**: Choose target format from supported list
3. **Options Configuration**: Set conversion parameters
4. **Upload & Convert**: Submit job to API
5. **Progress Tracking**: Real-time conversion status
6. **Download Results**: Retrieve converted files

## Error Handling
- Network error recovery
- File validation feedback
- API error display
- Retry mechanisms
- User-friendly error messages

## Performance Considerations
- Lazy loading for large file lists
- Virtual scrolling for conversion history
- Optimized re-renders with React.memo
- Debounced API calls
- Efficient state management

## Testing Strategy
- Component testing with React Testing Library
- API integration testing
- File upload testing
- Conversion workflow testing
- Cross-browser compatibility testing

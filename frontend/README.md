# Backend Oracle - Frontend Documentation

React-based web interface for the Backend Oracle RAG coding assistant.

## Overview

A modern, responsive chat interface built with React 18 and TypeScript that provides an intuitive way to interact with the Backend Oracle API.

## Features

- 💬 Real-time chat interface
- 🎨 Clean, professional UI
- 📝 Markdown rendering with code syntax highlighting
- 📋 One-click code copying
- 🔌 Backend health monitoring
- ⚡ Fast and responsive

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface.tsx    # Main chat component
│   │   ├── ChatInterface.css    # Chat styling
│   │   ├── Header.tsx           # App header
│   │   └── Header.css           # Header styling
│   ├── lib/
│   │   └── api.ts              # API client
│   ├── app.tsx                 # Root component
│   ├── app.css                 # App styles
│   ├── main.tsx                # Entry point
│   └── index.css               # Global styles
├── index.html                  # HTML template
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript config
├── vite.config.ts              # Vite config
├── nginx.conf                  # Production server config
└── Dockerfile                  # Container config
```

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Environment Variables

Copy `.env.example` to `.env`:

```bash
VITE_API_URL=http://localhost:8000/api/v1
```

### Local Development

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Access the app:**
   - Open http://localhost:5173
   - Ensure backend is running on port 8000

### Production Build

```bash
# Build the application
npm run build

# Preview production build
npm run preview
```

### Docker Deployment

From repository root:
```bash
docker compose up web
```

The frontend will be available at http://localhost:3000

## Components

### ChatInterface

The main chat component that handles:
- Message display and formatting
- User input
- API communication
- Loading states
- Error handling

Features:
- Auto-scroll to latest message
- Code block rendering with syntax highlighting
- Copy-to-clipboard functionality
- Connection status indicator

### Header

Simple header component displaying:
- Application name
- Branding

### API Client

Located in `src/lib/api.ts`, provides:
- `getHealth()` - Check backend status
- `chat(message)` - Send chat messages

## Styling

The UI uses custom CSS with:
- Modern, clean design
- Responsive layout
- Dark theme optimized for code
- Smooth animations
- Accessible color contrasts

## Message Rendering

The chat interface supports:
- **Plain text**: Regular messages
- **Code blocks**: Syntax-highlighted code with language labels
- **Markdown**: Bold, italic, and inline code
- **Timestamps**: Message time display

Example code block in response:
````markdown
```python
from fastapi import FastAPI
app = FastAPI()
```
````

## Development

### Adding New Components

Create component files in `src/components/`:

```tsx
import React from 'react'
import './MyComponent.css'

function MyComponent(): React.ReactElement {
  return <div>My Component</div>
}

export default MyComponent
```

### Modifying API Client

Edit `src/lib/api.ts` to add new endpoints:

```typescript
export const apiClient = {
  // Existing methods...
  
  async newEndpoint(): Promise<ResponseType> {
    const response = await axios.get(`${API_URL}/new`)
    return response.data
  }
}
```

## Building for Production

The production build:
1. Compiles TypeScript
2. Bundles with Vite
3. Optimizes assets
4. Minifies code
5. Serves via Nginx

### Nginx Configuration

The `nginx.conf` includes:
- Gzip compression
- Static asset caching
- Security headers
- SPA routing support

## Environment-Specific Configuration

### Development
- Hot module replacement
- Source maps
- Debug logging

### Production
- Minified bundles
- Optimized assets
- No debug logs
- Nginx serving

## Troubleshooting

### Common Issues

1. **API connection failed**
   - Check `VITE_API_URL` in `.env`
   - Ensure backend is running
   - Check CORS settings in backend

2. **Port already in use**
   - Change dev server port: `vite --port 5174`
   - Or stop conflicting service

3. **Module not found errors**
   - Run `npm install`
   - Check import paths (case-sensitive)

4. **Build fails**
   - Check TypeScript errors: `npm run lint`
   - Ensure all dependencies installed

## Performance

- Initial load: < 1s (gzipped)
- First Contentful Paint: < 0.5s
- Time to Interactive: < 1s
- Bundle size: ~150KB (production)

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions

## Accessibility

- Semantic HTML
- Keyboard navigation
- ARIA labels
- Screen reader support

## License

See LICENSE file in repository root.

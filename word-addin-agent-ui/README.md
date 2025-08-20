# Patent Drafting Agent - Word Add-in

A modern Word add-in that integrates with the Patent Drafting Agent backend to provide AI-powered patent drafting assistance, real-time document analysis, and intelligent claim generation.

## Features

- 🤖 **AI Chatbot Interface**: Interactive chat with the patent drafting agent
- 📄 **Document Integration**: Seamless integration with Word documents
- 🔄 **Real-time Streaming**: Live streaming responses from the backend
- 📝 **Smart Insertion**: Insert AI responses directly into documents
- 🎯 **Track Changes**: Support for Word's native track changes
- 💾 **Session Management**: Persistent conversation history
- 🔐 **Authentication**: Secure API access with bearer tokens
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Word Add-in   │    │   React Frontend │    │  Backend API    │
│                 │◄──►│                 │◄──►│                 │
│ • Office.js     │    │ • ChatBot       │    │ • FastAPI       │
│ • Document API  │    │ • DocumentPanel │    │ • LLM Agent     │
│ • Taskpane      │    │ • Streaming     │    │ • Patent Models │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Technology Stack

- **Frontend**: React 18 + TypeScript
- **Office Integration**: Office.js API
- **Styling**: CSS3 with modern design patterns
- **Build Tool**: Webpack 5
- **State Management**: React Context API
- **HTTP Client**: Axios + Fetch API
- **Streaming**: Server-Sent Events (SSE)

## Prerequisites

- Node.js 16+ and npm
- Microsoft Word (desktop or online)
- Backend API running (see agentic-native-drafting)
- Office Add-in development certificates

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Development Server

```bash
npm run dev-server
```

This starts the development server at `http://localhost:3000`

### 3. Build for Production

```bash
npm run build
```

### 4. Start in Word

```bash
npm start
```

This will launch Word with the add-in loaded.

## Development

### Project Structure

```
src/
├── components/          # React components
│   ├── ChatBot.tsx     # Main chat interface
│   ├── DocumentPanel.tsx # Document info panel
│   ├── MessageBubble.tsx # Individual messages
│   └── InsertButton.tsx # Document insertion
├── contexts/            # React context providers
│   ├── AuthContext.tsx  # Authentication state
│   └── ConversationContext.tsx # Chat history
├── services/            # API and document services
│   ├── api.ts          # Backend API client
│   └── documentService.ts # Word document operations
├── styles/              # CSS stylesheets
└── index.tsx            # Application entry point
```

### Key Components

#### ChatBot
- Handles user input and AI responses
- Manages streaming responses
- Integrates with document service

#### DocumentPanel
- Shows document statistics
- Provides document analysis tools
- Enables track changes

#### DocumentService
- Office.js integration for Word operations
- Document content extraction
- Text insertion and formatting

### API Integration

The add-in communicates with the backend via:

- **Chat Endpoint**: `/chat` for regular requests
- **Streaming Endpoint**: `/chat/stream` for real-time responses
- **Document Analysis**: `/analyze-document` for content analysis
- **Change Application**: `/apply-changes` for document modifications

### Authentication

Uses bearer token authentication stored in localStorage:

```typescript
const token = localStorage.getItem('auth_token');
// Automatically included in API requests
```

## Configuration

### Environment Variables

Create a `.env` file:

```env
REACT_APP_API_URL=http://localhost:8000
```

### Backend API

Ensure the backend is running and accessible at the configured URL.

## Testing

```bash
npm test
```

## Deployment

### 1. Build the Add-in

```bash
npm run build
```

### 2. Update Manifest

Update the `manifest.xml` file with your production URLs and icons.

### 3. Deploy to Office Store

Follow Microsoft's Office Add-in deployment process.

## Troubleshooting

### Common Issues

1. **Office.js not loading**: Check if the add-in is properly sideloaded
2. **API connection errors**: Verify backend is running and accessible
3. **Document operations failing**: Ensure proper Office.js permissions

### Debug Mode

Enable Office.js debugging:

```typescript
Office.context.document.settings.set('Office.Debug', true);
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For support and questions:
- Create an issue in this repository
- Check the Office Add-ins documentation
- Review the backend API documentation

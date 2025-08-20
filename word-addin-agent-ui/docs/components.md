# Components

## Overview

The Patent Drafting Agent Word Add-in is built using React 18 with TypeScript, following modern component architecture patterns. This document details the component hierarchy, state management, and UI/UX design patterns.

## Component Architecture

### Component Hierarchy

```
App (Root Component)
├── AuthProvider (Context Provider)
├── ConversationProvider (Context Provider)
├── ErrorBoundary (Error Handling)
├── ChatBot (Main UI Component)
│   ├── LoginForm (Authentication)
│   ├── DocumentPanel (Document Operations)
│   ├── MessageBubble (Chat Messages)
│   └── InsertButton (Content Insertion)
└── Office Initialization (Office.js Setup)
```

### Component Categories

1. **Container Components**: Manage state and business logic
2. **Presentational Components**: Handle UI rendering and user interactions
3. **Context Providers**: Manage global application state
4. **Utility Components**: Provide reusable functionality

## Core Components

### 1. App Component

**File**: `src/App.tsx`

**Purpose**: Root component that sets up the application structure and providers.

**Responsibilities**:
- Initialize Office.js
- Set up context providers
- Handle routing and navigation
- Manage global error boundaries

**Key Features**:
```typescript
export const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <ConversationProvider>
          <ChatBot />
        </ConversationProvider>
      </AuthProvider>
    </ErrorBoundary>
  );
};
```

### 2. ChatBot Component

**File**: `src/components/ChatBot.tsx`

**Purpose**: Main user interface component that handles the chat interface and patent drafting workflow.

**State Management**:
```typescript
const [inputValue, setInputValue] = useState('');
const [isLoading, setIsLoading] = useState(false);
const [streamingResponse, setStreamingResponse] = useState('');
const [error, setError] = useState<string | null>(null);
const [retryCount, setRetryCount] = useState(0);
```

**Key Features**:
- **Real-time Chat Interface**: Streaming AI responses
- **Document Integration**: Word.js integration for document operations
- **Error Handling**: Comprehensive error management with retry logic
- **Session Management**: Conversation history and session persistence

**User Interactions**:
```typescript
const handleSubmit = async (e: React.FormEvent) => {
  // Handle user message submission
  // Process document context
  // Send API request
  // Handle streaming response
};

const handleInsertToDocument = async (content: string) => {
  // Insert AI-generated content into Word document
};

const handleClearChat = () => {
  // Clear conversation and reset state
};
```

### 3. LoginForm Component

**File**: `src/components/LoginForm.tsx`

**Purpose**: Handles user authentication and login flow.

**Features**:
- **Auth0 Integration**: Modern authentication with hosted login
- **Responsive Design**: Mobile-friendly interface
- **Error Handling**: Clear error messages and recovery options
- **Loading States**: Visual feedback during authentication

**Authentication Flow**:
```typescript
const handleLogin = async () => {
  try {
    setLoading(true);
    // Open Auth0 login dialog
    // Handle authentication flow
    // Update application state
  } catch (error) {
    setError('Authentication failed. Please try again.');
  } finally {
    setLoading(false);
  }
};
```

### 4. MessageBubble Component

**File**: `src/components/MessageBubble.tsx`

**Purpose**: Renders individual chat messages with appropriate styling and actions.

**Props Interface**:
```typescript
interface MessageBubbleProps {
  message: ChatMessage;
  onInsert: (content: string) => void;
}
```

**Features**:
- **Role-based Styling**: Different styles for user vs. AI messages
- **Content Insertion**: Insert button for AI responses
- **Timestamp Display**: Message timing information
- **Responsive Layout**: Adapts to different screen sizes

### 5. InsertButton Component

**File**: `src/components/InsertButton.tsx`

**Purpose**: Provides functionality to insert AI-generated content into Word documents.

**Features**:
- **Content Validation**: Ensures content is valid before insertion
- **User Feedback**: Visual confirmation of insertion actions
- **Error Handling**: Graceful handling of insertion failures
- **Accessibility**: Keyboard navigation and screen reader support

**Insertion Logic**:
```typescript
const handleInsert = async () => {
  if (!content.trim()) return;
  
  try {
    setInserting(true);
    await onInsert(content);
    // Show success feedback
  } catch (error) {
    // Handle insertion error
  } finally {
    setInserting(false);
  }
};
```

### 6. DocumentPanel Component

**File**: `src/components/DocumentPanel.tsx`

**Purpose**: Provides document analysis and management capabilities.

**Features**:
- **Document Overview**: Summary of current document content
- **Content Analysis**: AI-powered document insights
- **Quick Actions**: Common document operations
- **Status Information**: Document state and metadata

## Context Providers

### 1. AuthContext

**File**: `src/contexts/AuthContext.tsx`

**Purpose**: Manages authentication state and user session information.

**State**:
```typescript
interface AuthContextType {
  isAuthenticated: boolean;
  token: string | null;
  user: User | null;
  loading: boolean;
}
```

**Methods**:
```typescript
const loginWithRedirect = () => Promise<void>;
const handleRedirectCallback = () => Promise<void>;
const logout = () => void;
const refreshFromStorage = () => void;
```

**Usage**:
```typescript
const { isAuthenticated, user, logout } = useAuth();

if (!isAuthenticated) {
  return <LoginForm />;
}
```

### 2. ConversationContext

**File**: `src/contexts/ConversationContext.tsx`

**Purpose**: Manages conversation state, messages, and session information.

**State**:
```typescript
interface ConversationContextType {
  messages: ChatMessage[];
  sessionId: string | null;
}
```

**Methods**:
```typescript
const addMessage = (message: ChatMessage) => void;
const clearConversation = () => void;
const getConversationHistory = () => ChatMessage[];
const updateSessionId = (sessionId: string) => void;
```

**Usage**:
```typescript
const { messages, addMessage, sessionId } = useConversation();

const handleNewMessage = (content: string) => {
  const message: ChatMessage = {
    role: 'user',
    content,
    timestamp: new Date().toISOString(),
  };
  addMessage(message);
};
```

## Custom Hooks

### 1. useWordJs Hook

**File**: `src/hooks/useWordJs.ts`

**Purpose**: Provides safe access to Word.js functionality with proper initialization handling.

**Return Values**:
```typescript
interface UseWordJsReturn {
  isReady: boolean;
  isLoading: boolean;
  error: string | null;
  execute: <T>(operation: () => Promise<T>) => Promise<T | null>;
}
```

**Features**:
- **Initialization Management**: Handles Office.js and Word.js setup
- **Error Handling**: Comprehensive error management
- **Safe Execution**: Ensures Word.js is ready before operations
- **Timeout Management**: Configurable initialization timeouts

**Usage**:
```typescript
const { isReady, isLoading, error, execute } = useWordJs();

const handleDocumentOperation = async () => {
  const result = await execute(async () => {
    // Word.js operation
    return await documentService.getDocumentContent();
  });
  
  if (result) {
    // Handle successful operation
  }
};
```

## UI/UX Design Patterns

### 1. Responsive Design

**Mobile-First Approach**:
- Flexible layouts that adapt to different screen sizes
- Touch-friendly interface elements
- Optimized for both desktop and mobile Office applications

**CSS Implementation**:
```css
/* Responsive breakpoints */
@media (max-width: 768px) {
  .chatbot-container {
    padding: 10px;
  }
  
  .header-buttons {
    flex-direction: column;
  }
}
```

### 2. Loading States

**Progressive Loading**:
- Skeleton screens for initial content
- Loading spinners for operations
- Progress indicators for long-running tasks

**Implementation**:
```typescript
{isLoading && !streamingResponse && (
  <div className="message assistant">
    <div className="message-content">
      <div className="loading-indicator">
        <div className="typing-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
  </div>
)}
```

### 3. Error Handling

**User-Friendly Errors**:
- Clear error messages
- Recovery suggestions
- Retry mechanisms
- Graceful degradation

**Error Display**:
```typescript
{error && (
  <div className="error-message">
    {error}
    {retryCount > 0 && (
      <button 
        onClick={() => setRetryCount(0)}
        className="retry-btn"
      >
        Reset
      </button>
    )}
  </div>
)}
```

### 4. Accessibility

**ARIA Support**:
- Proper labeling for screen readers
- Keyboard navigation support
- Focus management
- Semantic HTML structure

**Implementation**:
```typescript
<button 
  className="send-button"
  disabled={isLoading || !inputValue.trim() || !isReady}
  title={!isReady ? "Word.js not ready" : "Send message"}
  aria-label="Send message"
>
  {isLoading ? 'Sending...' : 'Send'}
</button>
```

## State Management Patterns

### 1. Local State

**Component-Level State**:
- Form inputs and validation
- UI state (loading, errors, etc.)
- Component-specific data

**Example**:
```typescript
const [inputValue, setInputValue] = useState('');
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState<string | null>(null);
```

### 2. Context State

**Global Application State**:
- User authentication
- Conversation history
- Application settings

**Example**:
```typescript
const { messages, addMessage, sessionId } = useConversation();
const { isAuthenticated, user } = useAuth();
```

### 3. Derived State

**Computed Values**:
- Filtered messages
- Form validation
- UI state calculations

**Example**:
```typescript
const hasMessages = messages.length > 0;
const canSendMessage = inputValue.trim().length > 0 && !isLoading;
```

## Performance Optimizations

### 1. Component Memoization

**React.memo Usage**:
- Prevent unnecessary re-renders
- Optimize performance for expensive components
- Maintain referential equality

**Example**:
```typescript
export const MessageBubble = React.memo<MessageBubbleProps>(({ message, onInsert }) => {
  // Component implementation
});
```

### 2. Callback Optimization

**useCallback Usage**:
- Prevent function recreation on every render
- Optimize child component re-renders
- Maintain stable references

**Example**:
```typescript
const handleInsertToDocument = useCallback(async (content: string) => {
  if (!isReady) return;
  
  try {
    await documentService.insertText(content);
  } catch (error) {
    console.error('Error inserting content:', error);
  }
}, [isReady]);
```

### 3. Effect Optimization

**useEffect Dependencies**:
- Minimize unnecessary effect executions
- Proper cleanup and dependency management
- Prevent memory leaks

**Example**:
```typescript
useEffect(() => {
  scrollToBottom();
}, [messages, streamingResponse]);

useEffect(() => {
  return () => cleanup();
}, []);
```

## Testing Strategy

### 1. Component Testing

**Testing Library Usage**:
- Render components in isolation
- Test user interactions
- Verify component behavior
- Mock dependencies

**Example**:
```typescript
import { render, screen, fireEvent } from '@testing-library/react';

test('should display login form when not authenticated', () => {
  render(<ChatBot />);
  expect(screen.getByText('Sign In')).toBeInTheDocument();
});
```

### 2. Hook Testing

**Custom Hook Testing**:
- Test hook behavior in isolation
- Verify state changes
- Test error scenarios
- Mock external dependencies

### 3. Integration Testing

**End-to-End Testing**:
- Test complete user workflows
- Verify component interactions
- Test error handling
- Validate user experience

## Future Component Enhancements

### 1. Advanced UI Components

**Planned Components**:
- **Wizard Interface**: Step-by-step patent drafting guidance
- **Document Preview**: Rich document preview and editing
- **Collaboration Tools**: Multi-user editing features
- **Analytics Dashboard**: Usage statistics and insights

### 2. Component Library

**Design System**:
- Consistent component styling
- Reusable UI patterns
- Accessibility guidelines
- Performance benchmarks

### 3. Plugin Architecture

**Extensibility**:
- Component plugin system
- Custom UI extensions
- Third-party integrations
- Modular architecture

---

*This component architecture provides a solid foundation for the Patent Drafting Agent Word Add-in, with clear separation of concerns, maintainable code structure, and excellent user experience.*

# Development Guide

## Overview

This guide provides comprehensive instructions for setting up, developing, testing, and deploying the Patent Drafting Agent Word Add-in. It covers the development environment, workflow, and best practices for contributors and developers.

## Prerequisites

### 1. System Requirements

**Operating System**
- **Windows**: Windows 10/11 (recommended)
- **macOS**: macOS 10.15+ (Catalina or later)
- **Linux**: Ubuntu 18.04+ (for development only)

**Software Requirements**
- **Node.js**: Version 18.0.0 or higher
- **npm**: Version 8.0.0 or higher (comes with Node.js)
- **Git**: Version 2.20.0 or higher
- **Office**: Microsoft Office 2016+ or Office 365

**Browser Requirements**
- **Chrome**: Version 90+ (recommended)
- **Firefox**: Version 88+
- **Safari**: Version 14+ (macOS)
- **Edge**: Version 90+

### 2. Development Tools

**Code Editor**
- **VS Code**: Recommended with extensions
- **WebStorm**: Alternative IDE option
- **Vim/Emacs**: For advanced users

**VS Code Extensions**
```json
{
  "recommendations": [
    "ms-vscode.vscode-typescript-next",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-eslint",
    "ms-vscode.vscode-jest"
  ]
}
```

**Browser Developer Tools**
- **Chrome DevTools**: Primary debugging tool
- **Firefox Developer Tools**: Alternative debugging
- **Office.js Debugging**: Office Add-in debugging tools

## Environment Setup

### 1. Repository Setup

**Clone Repository**
```bash
git clone https://github.com/your-org/agentic-native-drafting.git
cd agentic-native-drafting/word-addin-agent-ui
```

**Install Dependencies**
```bash
npm install
```

**Environment Configuration**
```bash
# Copy environment template
cp env.example .env

# Edit environment variables
nano .env
```

**Environment Variables**
```bash
# Development environment
NODE_ENV=development
API_URL=http://localhost:8000
AUTH0_DOMAIN=your-auth0-domain
AUTH0_CLIENT_ID=your-auth0-client-id
```

### 2. Office.js Setup

**Office Add-in Development Tools**
```bash
# Install Office Add-in CLI tools
npm install -g office-addin-dev-certs
npm install -g office-addin-debugging
npm install -g office-addin-manifest

# Generate development certificates
office-addin-dev-certs install
```

**SSL Certificate Setup**
```bash
# Generate self-signed certificates for HTTPS
cd ssl
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

**Office.js Script Loading**
```typescript
// src/office-init.ts
const script = document.createElement('script');
script.src = 'https://appsforoffice.microsoft.com/lib/1/hosted/office.js';
script.type = 'text/javascript';
document.head.appendChild(script);
```

### 3. Backend Integration

**Patent Drafting Backend**
```bash
# Ensure backend is running
cd ../agentic_native_drafting
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

**API Configuration**
```typescript
// src/config/environment.ts
export const API_URL = env.API_URL; // http://localhost:8000
```

## Development Workflow

### 1. Development Server

**Start Development Server**
```bash
# Start HTTPS development server
npm run https-server

# Start webpack dev server
npm run dev-server

# Start Office Add-in debugging
npm start
```

**Development URLs**
- **Local Development**: `https://localhost:3000`
- **Office Add-in**: `https://localhost:3000`
- **Backend API**: `http://localhost:8000`

**Hot Reload**
- **Frontend Changes**: Automatic browser refresh
- **Office.js Changes**: Manual refresh required
- **Backend Changes**: Restart backend service

### 2. Code Organization

**Project Structure**
```
src/
├── components/          # React components
├── contexts/           # React Context providers
├── hooks/              # Custom React hooks
├── services/           # API and business logic
├── config/             # Configuration files
├── styles/             # Global styles
└── office-init.ts      # Office.js initialization
```

**Component Development**
```typescript
// src/components/NewComponent.tsx
import React, { useState, useEffect } from 'react';
import './NewComponent.css';

interface NewComponentProps {
  title: string;
  onAction: (data: any) => void;
}

export const NewComponent: React.FC<NewComponentProps> = ({ title, onAction }) => {
  const [state, setState] = useState('');

  useEffect(() => {
    // Component initialization
  }, []);

  return (
    <div className="new-component">
      <h2>{title}</h2>
      {/* Component content */}
    </div>
  );
};
```

**Service Development**
```typescript
// src/services/newService.ts
export interface NewServiceInterface {
  method1(): Promise<any>;
  method2(data: any): Promise<any>;
}

class NewService implements NewServiceInterface {
  async method1(): Promise<any> {
    // Implementation
  }

  async method2(data: any): Promise<any> {
    // Implementation
  }
}

export const newService = new NewService();
```

### 3. State Management

**Context Development**
```typescript
// src/contexts/NewContext.tsx
import React, { createContext, useContext, useState, ReactNode } from 'react';

interface NewContextType {
  data: any;
  updateData: (newData: any) => void;
}

const NewContext = createContext<NewContextType | undefined>(undefined);

export const useNewContext = () => {
  const context = useContext(NewContext);
  if (!context) {
    throw new Error('useNewContext must be used within NewProvider');
  }
  return context;
};

export const NewProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [data, setData] = useState(null);

  const updateData = (newData: any) => {
    setData(newData);
  };

  return (
    <NewContext.Provider value={{ data, updateData }}>
      {children}
    </NewContext.Provider>
  );
};
```

**Custom Hooks**
```typescript
// src/hooks/useNewHook.ts
import { useState, useEffect } from 'react';

export function useNewHook(initialValue: any) {
  const [value, setValue] = useState(initialValue);

  useEffect(() => {
    // Hook logic
  }, [value]);

  return [value, setValue];
}
```

## Testing Strategy

### 1. Unit Testing

**Jest Configuration**
```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  moduleNameMapping: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '^@/(.*)$': '<rootDir>/src/$1'
  }
};
```

**Component Testing**
```typescript
// src/components/__tests__/NewComponent.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { NewComponent } from '../NewComponent';

describe('NewComponent', () => {
  test('renders with title', () => {
    render(<NewComponent title="Test Title" onAction={() => {}} />);
    expect(screen.getByText('Test Title')).toBeInTheDocument();
  });

  test('calls onAction when button clicked', () => {
    const mockAction = jest.fn();
    render(<NewComponent title="Test" onAction={mockAction} />);
    
    fireEvent.click(screen.getByRole('button'));
    expect(mockAction).toHaveBeenCalled();
  });
});
```

**Hook Testing**
```typescript
// src/hooks/__tests__/useNewHook.test.ts
import { renderHook, act } from '@testing-library/react';
import { useNewHook } from '../useNewHook';

describe('useNewHook', () => {
  test('initializes with value', () => {
    const { result } = renderHook(() => useNewHook('initial'));
    expect(result.current[0]).toBe('initial');
  });

  test('updates value', () => {
    const { result } = renderHook(() => useNewHook('initial'));
    
    act(() => {
      result.current[1]('updated');
    });
    
    expect(result.current[0]).toBe('updated');
  });
});
```

### 2. Integration Testing

**API Testing**
```typescript
// src/services/__tests__/api.test.ts
import { apiService } from '../api';

describe('ApiService', () => {
  test('handles authentication correctly', async () => {
    // Mock authentication
    sessionStorage.setItem('auth_token', 'test-token');
    
    // Test API call
    const result = await apiService.healthCheck();
    expect(result).toBeDefined();
  });
});
```

**Office.js Testing**
```typescript
// src/hooks/__tests__/useWordJs.test.ts
import { renderHook } from '@testing-library/react';
import { useWordJs } from '../useWordJs';

// Mock Office.js
global.Office = {
  onReady: jest.fn(),
  HostType: { Word: 'Word' }
};

describe('useWordJs', () => {
  test('initializes correctly', () => {
    const { result } = renderHook(() => useWordJs());
    expect(result.current.isLoading).toBe(true);
  });
});
```

### 3. End-to-End Testing

**Playwright Setup**
```bash
# Install Playwright
npm install -D @playwright/test

# Install browsers
npx playwright install
```

**E2E Test Example**
```typescript
// e2e/patent-drafting.spec.ts
import { test, expect } from '@playwright/test';

test('complete patent drafting workflow', async ({ page }) => {
  // Navigate to add-in
  await page.goto('https://localhost:3000');
  
  // Login
  await page.click('[data-testid="login-button"]');
  await page.fill('[data-testid="email-input"]', 'test@example.com');
  await page.fill('[data-testid="password-input"]', 'password');
  await page.click('[data-testid="submit-button"]');
  
  // Test chat functionality
  await page.fill('[data-testid="chat-input"]', 'Draft a patent claim');
  await page.click('[data-testid="send-button"]');
  
  // Verify response
  await expect(page.locator('[data-testid="ai-response"]')).toBeVisible();
});
```

## Debugging

### 1. Frontend Debugging

**React Developer Tools**
```bash
# Install React Developer Tools browser extension
# Chrome: https://chrome.google.com/webstore/detail/react-developer-tools
# Firefox: https://addons.mozilla.org/en-US/firefox/addon/react-devtools/
```

**Console Logging**
```typescript
// Debug logging
console.log('Component state:', state);
console.log('API response:', response);
console.log('Office.js status:', Office.context.document);

// Debug groups
console.group('API Call Details');
console.log('Request:', request);
console.log('Response:', response);
console.groupEnd();
```

**React DevTools**
- **Components**: Inspect component hierarchy and props
- **Profiler**: Performance analysis and optimization
- **Hooks**: Debug custom hooks and state

### 2. Office.js Debugging

**Office.js Debugging Tools**
```bash
# Start Office Add-in debugging
npm start

# View debugging information
# Office.js will show debugging information in the taskpane
```

**Office.js Console**
```typescript
// Office.js debugging
Office.context.document.getSelectedDataAsync(Office.CoercionType.Text, (result) => {
  if (result.status === Office.AsyncResultStatus.Failed) {
    console.error('Office.js error:', result.error);
  } else {
    console.log('Selected text:', result.value);
  }
});
```

**Manifest Validation**
```bash
# Validate manifest file
office-addin-manifest validate manifest.xml
```

### 3. Network Debugging

**Network Tab**
- **API Calls**: Monitor all API requests and responses
- **Headers**: Check authentication and request headers
- **Timing**: Analyze request/response timing
- **Errors**: Identify network errors and failures

**API Debugging**
```typescript
// API request debugging
this.api.interceptors.request.use((config) => {
  console.log('API Request:', config);
  return config;
});

this.api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response);
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);
```

## Build & Deployment

### 1. Build Process

**Production Build**
```bash
# Build for production
npm run build

# Build for development
npm run build:dev
```

**Build Configuration**
```javascript
// webpack.config.js
module.exports = {
  mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',
  entry: './src/index.tsx',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
    clean: true
  },
  // ... other configuration
};
```

**Build Output**
```
dist/
├── bundle.js           # Main application bundle
├── index.html          # Main HTML file
├── manifest.xml        # Office Add-in manifest
└── assets/             # Static assets
```

### 2. Deployment

**Development Deployment**
```bash
# Start development server
npm run https-server

# Sideload add-in in Office
# Use Office Add-in debugging tools
```

**Production Deployment**
```bash
# Build production version
npm run build

# Deploy to hosting service
npm run deploy

# Update manifest URLs for production
# Deploy manifest to Office Add-in catalog
```

**Deployment Scripts**
```bash
#!/bin/bash
# deploy.sh

echo "Building for production..."
npm run build

echo "Deploying to production..."
# Add deployment commands here

echo "Deployment complete!"
```

## Code Quality

### 1. Linting & Formatting

**ESLint Configuration**
```javascript
// eslint.config.js
module.exports = {
  extends: [
    '@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended'
  ],
  rules: {
    // Custom rules
  }
};
```

**Prettier Configuration**
```json
// .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

**Code Quality Scripts**
```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npx prettier --write src/
```

### 2. TypeScript Configuration

**TypeScript Config**
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"]
}
```

**Type Definitions**
```typescript
// src/types/index.ts
export interface User {
  id: string;
  email: string;
  name: string;
}

export interface ApiResponse<T> {
  data: T;
  status: string;
  message?: string;
}
```

## Performance Optimization

### 1. Bundle Optimization

**Code Splitting**
```typescript
// Lazy load components
const LazyComponent = React.lazy(() => import('./LazyComponent'));

// Route-based splitting
const routes = [
  {
    path: '/feature',
    component: React.lazy(() => import('./Feature'))
  }
];
```

**Tree Shaking**
```typescript
// Import only what you need
import { useState } from 'react'; // Good
import React from 'react'; // Avoid

// Use named imports
import { Button } from '@fluentui/react'; // Good
import * as FluentUI from '@fluentui/react'; // Avoid
```

### 2. Runtime Optimization

**Component Optimization**
```typescript
// Memoize expensive components
export const ExpensiveComponent = React.memo(({ data }) => {
  // Component implementation
});

// Optimize callbacks
const handleClick = useCallback((id: string) => {
  // Handle click
}, []);
```

**Memory Management**
```typescript
// Cleanup effects
useEffect(() => {
  const subscription = api.subscribe();
  
  return () => {
    subscription.unsubscribe();
  };
}, []);

// Abort controllers for API calls
const abortController = new AbortController();
api.call(data, { signal: abortController.signal });

// Cleanup
return () => abortController.abort();
```

## Troubleshooting

### 1. Common Issues

**Office.js Not Loading**
```bash
# Check SSL certificates
office-addin-dev-certs install

# Verify manifest URLs
# Ensure HTTPS is working correctly
```

**Build Failures**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check TypeScript errors
npx tsc --noEmit

# Verify webpack configuration
npm run build:dev
```

**Authentication Issues**
```bash
# Check Auth0 configuration
# Verify environment variables
# Check browser console for errors
# Verify CORS configuration
```

### 2. Debug Commands

**Development Commands**
```bash
# Start all services
npm run dev

# Check Office.js status
npm run validate

# Test build
npm run build && npm run test

# Debug Office Add-in
npm start
```

**Logging Commands**
```bash
# View build logs
npm run build 2>&1 | tee build.log

# View test logs
npm test 2>&1 | tee test.log

# View development logs
npm run dev-server 2>&1 | tee dev.log
```

## Best Practices

### 1. Development Practices

**Code Organization**
- Keep components small and focused
- Use consistent naming conventions
- Separate concerns (UI, logic, data)
- Follow React best practices

**State Management**
- Use Context for global state
- Keep local state minimal
- Avoid prop drilling
- Use appropriate state management patterns

**Error Handling**
- Implement comprehensive error boundaries
- Provide user-friendly error messages
- Log errors for debugging
- Implement retry mechanisms

### 2. Office.js Best Practices

**API Usage**
- Always check Office.js readiness
- Use proper error handling
- Implement proper cleanup
- Follow Office.js patterns

**Performance**
- Minimize Office.js API calls
- Batch operations when possible
- Implement proper loading states
- Handle large documents efficiently

### 3. Testing Best Practices

**Test Coverage**
- Aim for high test coverage
- Test edge cases and error scenarios
- Mock external dependencies
- Test user interactions

**Test Organization**
- Organize tests by feature
- Use descriptive test names
- Keep tests focused and simple
- Use proper test data

---

*This development guide provides a comprehensive overview of the development process. For specific issues or questions, refer to the troubleshooting section or contact the development team.*

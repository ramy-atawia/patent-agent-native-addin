import React from 'react';
import { AuthProvider } from './contexts/AuthContext';
import { ConversationProvider } from './contexts/ConversationContext';
import { ChatBot } from './components/ChatBot';
import './styles/App.css';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <ConversationProvider>
        <div className="App">
          <ChatBot />
        </div>
      </ConversationProvider>
    </AuthProvider>
  );
};

export default App;

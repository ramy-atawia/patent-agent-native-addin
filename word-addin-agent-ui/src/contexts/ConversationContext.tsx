import React, { createContext, useContext, useState, ReactNode } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

interface ConversationContextType {
  messages: Message[];
  addMessage: (contentOrMessage: string | Message, sender?: 'user' | 'assistant') => void;
  getConversationHistory: () => Message[];
  sessionId: string | null;
  updateSessionId: (id: string) => void;
  clearConversation: () => void;
  clearMessages: () => void;
}

const ConversationContext = createContext<ConversationContextType | undefined>(undefined);

export const useConversation = () => {
  const context = useContext(ConversationContext);
  if (context === undefined) {
    throw new Error('useConversation must be used within a ConversationProvider');
  }
  return context;
};

interface ConversationProviderProps {
  children: ReactNode;
}

export const ConversationProvider: React.FC<ConversationProviderProps> = ({ children }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);

  const addMessage = (contentOrMessage: string | Message, role?: 'user' | 'assistant') => {
    if (typeof contentOrMessage === 'string' && role) {
      const newMessage: Message = {
        content: contentOrMessage,
        role,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, newMessage]);
    } else if (typeof contentOrMessage === 'object') {
      setMessages(prev => [...prev, contentOrMessage]);
    }
  };

  const getConversationHistory = () => messages;

  const updateSessionId = (id: string) => {
    setSessionId(id);
  };

  const clearConversation = () => {
    setMessages([]);
    setSessionId(null);
  };

  const clearMessages = () => {
    setMessages([]);
  };

  const value: ConversationContextType = {
    messages,
    addMessage,
    getConversationHistory,
    sessionId,
    updateSessionId,
    clearConversation,
    clearMessages,
  };

  return (
    <ConversationContext.Provider value={value}>
      {children}
    </ConversationContext.Provider>
  );
};

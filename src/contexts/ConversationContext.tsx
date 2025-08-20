import React, { createContext, useContext, useState, ReactNode } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

interface ConversationContextType {
  messages: Message[];
  addMessage: (content: string, sender: 'user' | 'assistant') => void;
  addMessage: (message: Message) => void;
  getConversationHistory: () => Message[];
  sessionId: string | null;
  updateSessionId: (id: string) => void;
  clearConversation: () => void;
  clearMessages: () => void;
}

interface ConversationProviderProps {
  children: ReactNode;
}

const ConversationContext = createContext<ConversationContextType | undefined>(undefined);

export const useConversation = () => {
  const context = useContext(ConversationContext);
  if (context === undefined) {
    throw new Error('useConversation must be used within a ConversationProvider');
  }
  return context;
};

export const ConversationProvider: React.FC<ConversationProviderProps> = ({ children }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);

  const addMessage = (contentOrMessage: string | Message, sender?: 'user' | 'assistant') => {
    if (typeof contentOrMessage === 'string' && sender) {
      const newMessage: Message = {
        role: sender,
        content: contentOrMessage,
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

  return (
    <ConversationContext.Provider value={{ 
      messages, 
      addMessage, 
      getConversationHistory, 
      sessionId, 
      updateSessionId, 
      clearConversation, 
      clearMessages 
    }}>
      {children}
    </ConversationContext.Provider>
  );
};

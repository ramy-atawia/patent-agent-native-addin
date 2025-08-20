import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useConversation } from '../contexts/ConversationContext';
import { apiService, ChatMessage } from '../services/api';
import { documentService } from '../services/documentService';
import { useWordJs } from '../hooks/useWordJs';
import { MessageBubble } from './MessageBubble';
import InsertButton from './InsertButton';
import { LoginForm } from './LoginForm';
import './ChatBot.css';

export const ChatBot: React.FC = () => {
  const { isAuthenticated, user } = useAuth();
  const { messages, addMessage, getConversationHistory, sessionId, updateSessionId, clearConversation } = useConversation();
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [streamingResponse, setStreamingResponse] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);
  const maxRetries = 3;
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);
  const profileMenuRef = useRef<HTMLDivElement | null>(null);
  const [profileMenuOpen, setProfileMenuOpen] = useState(false);
  const [showUndoToast, setShowUndoToast] = useState(false);
  const undoTimerRef = useRef<number | null>(null);
  const backupRef = useRef<{ messages: ChatMessage[]; sessionId: string | null } | null>(null);
  const displayName = (user && (user.name || user.nickname)) ? (user.name || user.nickname) : null;

  // close profile menu on outside click or Escape
  useEffect(() => {
    const onDocClick = (e: MouseEvent) => {
      if (!profileMenuRef.current) return;
      if (!(e.target instanceof Node)) return;
      if (!profileMenuRef.current.contains(e.target)) {
        setProfileMenuOpen(false);
      }
    };
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setProfileMenuOpen(false); };
    document.addEventListener('click', onDocClick);
    document.addEventListener('keydown', onKey);
    return () => { document.removeEventListener('click', onDocClick); document.removeEventListener('keydown', onKey); };
  }, []);
  
  // Use the Word.js hook for safe access
  const { isReady, isLoading: wordJsLoading, error: wordJsError } = useWordJs();
  
  // Get logout function from auth context
  const { logout } = useAuth();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const cleanup = () => {
    try {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
        abortControllerRef.current = null;
      }
    } catch (e) {
      // ignore
    }
    setStreamingResponse('');
    setIsLoading(false);
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingResponse]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    setError(null); // Clear previous errors
    
    const userMessage: ChatMessage = {
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString(),
    };

    addMessage(userMessage);
    setInputValue('');
    setIsLoading(true);
    setStreamingResponse('');

    try {
      // Abort any previous in-flight request
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
        abortControllerRef.current = null;
      }
      abortControllerRef.current = new AbortController();
      
      // Get document content more efficiently
      let documentContent = '';
      if (isReady) {
        try {
          const docContent = await documentService.getDocumentContent();
          documentContent = docContent.text || '';
        } catch (error) {
          console.warn('Failed to get document content:', error);
          // Don't fail the request if document content can't be retrieved
        }
      }
      
      // Build request with new labeled structure
      const request = {
        user_message: inputValue,
        conversation_history: getConversationHistory(),
        document_content: {
          text: documentContent,
          paragraphs: documentContent ? [documentContent] : undefined,
          selection: undefined
        },
        session_id: sessionId,
      };

      // Use streaming API for real-time response
      await apiService.chatStream(
        request,
        (chunk: string) => {
          // ignore updates if aborted
          if (abortControllerRef.current && abortControllerRef.current.signal.aborted) return;
          setStreamingResponse(chunk); // Replace instead of append for cleaner streaming
        },
        (response) => {
          // Handle complete response
          const assistantMessage: ChatMessage = {
            role: 'assistant',
            content: response.response, // Changed from conversation_response to response
            timestamp: new Date().toISOString(),
          };
          
          addMessage(assistantMessage);
          setStreamingResponse('');
          
          // Update session ID if provided
          if (response.session_id) {
            updateSessionId(response.session_id);
          }
          
          // Reset retry count on success
          setRetryCount(0);
          
          // Log metadata for debugging
          console.log('Response metadata:', response.metadata);
          if (response.data?.claims) {
            console.log('Generated claims:', response.data.claims);
          }
        },
        (error) => {
          if (error && (error.name === 'AbortError' || String(error).includes('aborted'))) {
            // aborted by user or cleanup; do not show error
            return;
          }
          
          console.error('Chat error:', error);
          
          // Handle retry logic
          if (retryCount < maxRetries) {
            setRetryCount(prev => prev + 1);
            setError(`Request failed. Retrying... (${retryCount + 1}/${maxRetries})`);
            // Could implement auto-retry here
          } else {
            setError('Request failed after multiple attempts. Please try again.');
            const errorMessage: ChatMessage = {
              role: 'assistant',
              content: 'Sorry, I encountered an error after multiple attempts. Please try again or check your connection.',
              timestamp: new Date().toISOString(),
            };
            addMessage(errorMessage);
          }
        },
        abortControllerRef.current.signal
      );
    } catch (error) {
      console.error('Error sending message:', error);
      setError('Failed to send message. Please try again.');
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      };
      addMessage(errorMessage);
    } finally {
      // cleanup controller but keep streamingResponse for a moment
      if (abortControllerRef.current) {
        abortControllerRef.current = null;
      }
      setIsLoading(false);
    }
  };

  // cleanup on unmount
  useEffect(() => {
    return () => cleanup();
  }, []);

  // ensure undo timer cleaned up on unmount
  useEffect(() => {
    return () => {
      if (undoTimerRef.current) { window.clearTimeout(undoTimerRef.current); undoTimerRef.current = null; }
    };
  }, []);

  const handleInsertToDocument = async (content: string) => {
    if (!isReady) {
      console.warn('Word.js not ready, cannot insert content');
      return;
    }

    try {
      await documentService.insertText(content);
    } catch (error) {
      console.error('Error inserting content:', error);
    }
  };

  const handleClearChat = () => {
    // Backup current conversation to allow undo
    try {
      backupRef.current = { messages: [...messages], sessionId };
    } catch (e) { backupRef.current = null; }

    cleanup(); // Stop any ongoing requests
    clearConversation(); // Clear the conversation history
    setError(null);
    setRetryCount(0);

    // Show undo toast for 5 seconds
    setShowUndoToast(true);
    if (undoTimerRef.current) { window.clearTimeout(undoTimerRef.current); undoTimerRef.current = null; }
    undoTimerRef.current = window.setTimeout(() => {
      // expire backup
      backupRef.current = null;
      setShowUndoToast(false);
      undoTimerRef.current = null;
    }, 5000) as unknown as number;
  };

  const handleUndoClear = () => {
    if (backupRef.current) {
      // restore
      const b = backupRef.current;
      try {
        // add messages back
        b.messages.forEach(m => addMessage(m));
        if (b.sessionId) updateSessionId(b.sessionId);
      } catch (e) { console.warn('Failed to restore conversation backup', e); }
      backupRef.current = null;
    }
    if (undoTimerRef.current) { window.clearTimeout(undoTimerRef.current); undoTimerRef.current = null; }
    setShowUndoToast(false);
  };

  useEffect(() => {
    const handleOutsideClick = (event: MouseEvent) => {
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target as Node)) {
        setProfileMenuOpen(false);
      }
    };

    document.addEventListener('mousedown', handleOutsideClick);
    return () => document.removeEventListener('mousedown', handleOutsideClick);
  }, []);

  if (!isAuthenticated) {
    return (
      <div className="chatbot-container">
        <LoginForm />
      </div>
    );
  }

  return (
    <div className="chatbot-container">
      {wordJsError && (
        <div className="wordjs-warning">
          ⚠️ Word.js failed to initialize: {wordJsError}
        </div>
      )}
      {(!wordJsError && !isReady && wordJsLoading) && (
        <div className="wordjs-warning">
          ⚠️ Word.js loading... document features disabled until ready.
        </div>
      )}
      
      <div className="chatbot-header" role="banner">
        <div className="header-left">
          <div className="header-logo-container">
            <img
              src="/assets/novitai-logo.png"
              alt="Novitai"
              className="header-logo large"
              aria-hidden="false"
            />
          </div>
          <div className="header-greeting">
            <h3>{`Welcome${user && (user.name || user.nickname) ? ', ' + (user.name || user.nickname) : ''}`}</h3>
          </div>
        </div>
        <div className="header-buttons">
          {/* Profile / avatar menu */}
          <div className="profile-menu-container" ref={(el) => profileMenuRef.current = el}>
            <button
              className="profile-button"
              onClick={() => setProfileMenuOpen(prev => !prev)}
              aria-haspopup="true"
              aria-expanded={profileMenuOpen}
              aria-label="Open profile menu"
            >
              {user && (user.picture) ? (
                <img src={user.picture} alt="User avatar" className="avatar" />
              ) : (
                <div className="avatar initials">{displayName ? displayName.split(' ').map(n => n[0]).slice(0,2).join('').toUpperCase() : 'U'}</div>
              )}
            </button>

            {profileMenuOpen && (
              <div className="profile-menu" role="menu" aria-label="Profile menu">
                <button role="menuitem" className="profile-menu-item" onClick={() => { setProfileMenuOpen(false); handleClearChat(); }}>
                  Clear conversation
                </button>
                <button role="menuitem" className="profile-menu-item" aria-disabled="true" disabled>
                  Settings
                </button>
                <div className="menu-divider" />
                <button role="menuitem" className="profile-menu-item" onClick={() => { setProfileMenuOpen(false); logout(); }}>
                  Sign out
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

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

      <div className="messages-container">
        {messages.length === 0 && (
          <div className="welcome-message">
            <div className="welcome-content">
              <h3>Novitai Patent Assistant</h3>
              <p>I can assist you with patent drafting, prior art research, and professional documentation.</p>
              <ul>
                <li>Prior art research and analysis</li>
                <li>Patent claim drafting and review</li>
                <li>Professional patent reports</li>
                <li>Patent strategy recommendations</li>
              </ul>
              <p><strong>Example queries:</strong> "Draft claims for a 5G networking invention" or "Analyze prior art for wireless protocols"</p>
            </div>
          </div>
        )}
        
        {messages.map((message, index) => (
          <MessageBubble
            key={index}
            message={message}
            onInsert={handleInsertToDocument}
          />
        ))}
        
        {isLoading && streamingResponse && (
          <div className="message assistant">
            <div className="message-content streaming-message">
              <div className="streaming-response">
                {streamingResponse}
                <span className="typing-indicator">▋</span>
              </div>
              <InsertButton 
                content={streamingResponse}
                onInsert={handleInsertToDocument}
                disabled={!isReady}
              />
            </div>
          </div>
        )}

        {isLoading && !streamingResponse && (
          <div className="message assistant">
            <div className="message-content loading-message">
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
        
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        <div className="input-container">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder={!isReady ? "Word.js not ready..." : "Ask about patent drafting, claims, or document analysis..."}
            disabled={isLoading || !isReady}
            className="chat-input"
          />
          <button 
            type="submit" 
            disabled={isLoading || !inputValue.trim() || !isReady}
            className="send-button"
            title={!isReady ? "Word.js not ready" : "Send message"}
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </form>
      {showUndoToast && (
        <div className="undo-toast" role="status" aria-live="polite">
          <div>Conversation cleared</div>
          <button onClick={handleUndoClear} aria-label="Undo clear conversation">Undo</button>
        </div>
      )}
    </div>
  );
};

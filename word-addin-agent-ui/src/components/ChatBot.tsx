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
  const [streamingThoughts, setStreamingThoughts] = useState<string[]>([]);
  const [streamingAnalysis, setStreamingAnalysis] = useState('');
  const [isStreamingThoughtsExpanded, setIsStreamingThoughtsExpanded] = useState(false);
  
  // Fixed: Single ref for current streaming state
  const streamingStateRef = useRef({
    thoughts: [] as string[],
    analysis: '',
    response: ''
  });
  
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

  // Fixed: Sync all streaming states with ref
  useEffect(() => {
    streamingStateRef.current = {
      thoughts: streamingThoughts,
      analysis: streamingAnalysis,
      response: streamingResponse
    };
  }, [streamingThoughts, streamingAnalysis, streamingResponse]);
  
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
    setStreamingThoughts([]);
    setStreamingAnalysis('');
    streamingStateRef.current = { thoughts: [], analysis: '', response: '' };
    setIsLoading(false);
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingResponse, streamingThoughts, streamingAnalysis]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    setError(null);
    
    const userMessage: ChatMessage = {
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString(),
    };

    addMessage(userMessage);
    setInputValue('');
    setIsLoading(true);
    setStreamingResponse('');
    setStreamingThoughts([]);
    setStreamingAnalysis('');
    streamingStateRef.current = { thoughts: [], analysis: '', response: '' };

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

      console.log('🚀 STARTING STREAMING API CALL with request:', request);
      
      // Use streaming API for real-time response
      await apiService.chatStream(
        request,
        (chunk: string, eventType?: string) => {
          // ignore updates if aborted
          if (abortControllerRef.current && abortControllerRef.current.signal.aborted) return;
          
          console.log('🔍 STREAMING CHUNK:', {
            chunk: chunk.substring(0, 100) + (chunk.length > 100 ? '...' : ''),
            eventType,
            timestamp: new Date().toISOString()
          });
          
          // Simplified: Just two types - thoughts and results!
          const isThoughtEvent = eventType === 'thoughts';
          const isFinalResult = eventType === 'results';
          const isErrorEvent = eventType === 'error' || eventType === 'low_confidence';
          
          if (isThoughtEvent) {
            // Add all thoughts to the thoughts array - simple accumulation
            setStreamingThoughts(prev => {
              const newThoughts = [...prev, chunk];
              streamingStateRef.current.thoughts = newThoughts;
              return newThoughts;
            });
            // Clear any existing response when new thoughts come in
            if (streamingResponse) {
              setStreamingResponse('');
              streamingStateRef.current.response = '';
            }
          } else if (isFinalResult) {
            // Set final response
            setStreamingResponse(chunk);
            streamingStateRef.current.response = chunk;
          } else if (isErrorEvent) {
            // Add error to thoughts
            setStreamingThoughts(prev => {
              const errorMsg = `❌ ${chunk}`;
              const newThoughts = [...prev, errorMsg];
              streamingStateRef.current.thoughts = newThoughts;
              return newThoughts;
            });
          } else {
            // Unknown event - add to thoughts with prefix
            const prefixedChunk = eventType ? `[${eventType}] ${chunk}` : chunk;
            setStreamingThoughts(prev => {
              const newThoughts = [...prev, prefixedChunk];
              streamingStateRef.current.thoughts = newThoughts;
              return newThoughts;
            });
          }
        },
        (response) => {
          // Fixed: Use current ref state for final message
          const currentState = streamingStateRef.current;
          
          console.log('Creating final message with state:', {
            thoughtsCount: currentState.thoughts.length,
            hasAnalysis: !!currentState.analysis,
            hasResponse: !!currentState.response
          });
          
          // Combine all thoughts
          const allThoughts = [...currentState.thoughts];
          if (currentState.analysis) {
            allThoughts.push(`🔍 Analysis: ${currentState.analysis}`);
          }
          
          // Clean up thoughts - remove empty ones
          const cleanedThoughts = allThoughts.filter(thought => thought.trim());
          
          const assistantMessage: ChatMessage = {
            role: 'assistant',
            content: response.response,
            timestamp: new Date().toISOString(),
            thoughts: cleanedThoughts.length > 0 ? cleanedThoughts : undefined,
          };
          
          console.log('Final message created:', {
            contentLength: assistantMessage.content.length,
            thoughtsCount: assistantMessage.thoughts?.length || 0
          });
          
          addMessage(assistantMessage);
          
          // Clear all streaming state
          setStreamingResponse('');
          setStreamingThoughts([]);
          setStreamingAnalysis('');
          streamingStateRef.current = { thoughts: [], analysis: '', response: '' };
          
          // Update session ID if provided
          if (response.session_id) {
            updateSessionId(response.session_id);
          }
          
          setRetryCount(0);
          
          console.log('Response metadata:', response.metadata);
          if (response.data?.claims) {
            console.log('Generated claims:', response.data.claims);
          }
        },
        (error) => {
          if (error && (error.name === 'AbortError' || String(error).includes('aborted'))) {
            return;
          }
          
          console.error('Chat error:', error);
          
          if (retryCount < maxRetries) {
            setRetryCount(prev => prev + 1);
            setError(`Request failed. Retrying... (${retryCount + 1}/${maxRetries})`);
          } else {
            setError('Request failed after multiple attempts. Please try again.');
            const errorMessage: ChatMessage = {
              role: 'assistant',
              content: 'Sorry, I encountered an error after multiple attempts. Please try again or check your connection.',
              timestamp: new Date().toISOString(),
            };
            addMessage(errorMessage);
          }
          
          // Clean up streaming state on error
          setStreamingResponse('');
          setStreamingThoughts([]);
          setStreamingAnalysis('');
          streamingStateRef.current = { thoughts: [], analysis: '', response: '' };
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
      
      // Clean up streaming state on error
      setStreamingResponse('');
      setStreamingThoughts([]);
      setStreamingAnalysis('');
      streamingStateRef.current = { thoughts: [], analysis: '', response: '' };
    } finally {
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
      if (undoTimerRef.current) { 
        window.clearTimeout(undoTimerRef.current); 
        undoTimerRef.current = null; 
      }
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
    try {
      backupRef.current = { messages: [...messages], sessionId };
    } catch (e) { 
      backupRef.current = null; 
    }

    cleanup();
    clearConversation();
    setError(null);
    setRetryCount(0);

    setShowUndoToast(true);
    if (undoTimerRef.current) { 
      window.clearTimeout(undoTimerRef.current); 
      undoTimerRef.current = null; 
    }
    undoTimerRef.current = window.setTimeout(() => {
      backupRef.current = null;
      setShowUndoToast(false);
      undoTimerRef.current = null;
    }, 5000) as unknown as number;
  };

  const handleUndoClear = () => {
    if (backupRef.current) {
      const b = backupRef.current;
      try {
        b.messages.forEach(m => addMessage(m));
        if (b.sessionId) updateSessionId(b.sessionId);
      } catch (e) { 
        console.warn('Failed to restore conversation backup', e); 
      }
      backupRef.current = null;
    }
    if (undoTimerRef.current) { 
      window.clearTimeout(undoTimerRef.current); 
      undoTimerRef.current = null; 
    }
    setShowUndoToast(false);
  };

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
        </div>
        
        <div className="header-center">
          <h3>{`Welcome${user && (user.name || user.nickname) ? ', ' + (user.name || user.nickname) : ''}`}</h3>
        </div>
        
        <div className="header-buttons">
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
            user={user}
          />
        ))}
        
        {/* Fixed: Show streaming content when available */}
        {(streamingThoughts.length > 0 || streamingAnalysis || streamingResponse || isLoading) && (
          <div className="message assistant">
            <div className="message-content streaming-message">
              {/* Show streaming thoughts during processing */}
              {(streamingThoughts.length > 0 || isLoading) && (
                <div className={`thoughts-section ${isLoading ? 'streaming' : ''} ${isStreamingThoughtsExpanded ? 'expanded' : ''}`}>
                  <div 
                    className={`thoughts-toggle ${isLoading ? 'streaming' : ''} ${isStreamingThoughtsExpanded ? 'expanded' : ''}`}
                    onClick={() => setIsStreamingThoughtsExpanded(!isStreamingThoughtsExpanded)}
                    style={{ cursor: 'pointer' }}
                  >
                    <span className="thoughts-icon" style={{
                      transition: 'transform 0.2s ease',
                      transform: isStreamingThoughtsExpanded ? 'rotate(90deg)' : 'rotate(0deg)',
                      fontSize: '0.9em'
                    }}>
                      ▶
                    </span>
                    <span style={{ flex: 1 }}>
                      {streamingThoughts.length > 0 
                        ? `${isStreamingThoughtsExpanded ? 'Hide' : 'Show'} AI Thinking (${streamingThoughts.length} thoughts)` 
                        : `${isStreamingThoughtsExpanded ? 'Hide' : 'Show'} AI Thinking Process`
                      }
                    </span>
                    {isLoading && (
                      <span style={{
                        fontSize: '0.8em',
                        color: '#1b5e20',
                        background: 'linear-gradient(135deg, #f1f8e9, #e8f5e8)',
                        padding: '2px 8px',
                        borderRadius: '12px',
                        border: '1px solid #a5d6a7'
                      }}>
                        Processing...
                      </span>
                    )}
                  </div>
                  <div className={`thoughts-content ${isStreamingThoughtsExpanded ? 'expanded' : ''}`}>
                    {/* Show thinking indicator when loading and no thoughts yet */}
                    {isLoading && streamingThoughts.length === 0 && (
                      <div className="thoughts-thinking-indicator">
                        <span>Processing your request</span>
                        <div className="thoughts-thinking-dots">
                          <span></span>
                          <span></span>
                          <span></span>
                        </div>
                      </div>
                    )}
                    
                    {/* Show accumulated streaming analysis if available */}
                    {streamingAnalysis && (
                      <div className="thought-item">
                        <strong>🔍 Invention Analysis:</strong>
                        <div className="analysis-text">
                          {streamingAnalysis}
                          {isLoading && <span className="typing-indicator">▋</span>}
                        </div>
                      </div>
                    )}
                    
                    {/* Show other thoughts as individual items */}
                    <div className="thoughts-flowing">
                      {streamingThoughts.map((thought, index) => (
                        <div key={index} className="thought-item new-thought">
                          {thought.trim()}
                        </div>
                      ))}
                      
                      {/* Show thinking indicator when actively loading more thoughts */}
                      {isLoading && streamingThoughts.length > 0 && (
                        <div className="thoughts-thinking-indicator">
                          <span>Thinking more</span>
                          <div className="thoughts-thinking-dots">
                            <span></span>
                            <span></span>
                            <span></span>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}
              
              {/* Show final streaming response */}
              {streamingResponse && (
                <div className="streaming-response">
                  <div className="streaming-content">
                    <div>{streamingResponse}</div>
                    <span className="typing-indicator">▋</span>
                  </div>
                </div>
              )}
              
              {/* Insert button for streaming content */}
              {(streamingResponse || streamingThoughts.length > 0) && (
                <InsertButton 
                  content={streamingResponse || streamingThoughts.join('\n')}
                  onInsert={handleInsertToDocument}
                  disabled={!isReady}
                />
              )}
            </div>
          </div>
        )}

        {/* Show loading indicator when no streaming content yet */}
        {isLoading && !streamingResponse && streamingThoughts.length === 0 && !streamingAnalysis && (
          <div className="message assistant">
            <div className="message-content loading-message">
              <div className="loading-indicator">
                <div className="typing-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <span className="loading-text">Starting analysis...</span>
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
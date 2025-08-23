import React, { useState } from 'react';
import InsertButton from './InsertButton';
import { ChatMessage } from '../services/api';
import MarkdownConverter from './MarkdownConverter';
import './MessageBubble.css';

interface MessageBubbleProps {
  message: ChatMessage;
  onInsert: (content: string) => void;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message, onInsert }) => {
  const [isReasoningExpanded, setIsReasoningExpanded] = useState(false);
  const [isThoughtsExpanded, setIsThoughtsExpanded] = useState(false);
  const [convertedHtml, setConvertedHtml] = useState<string>('');

  // Debug logging
  console.log('MessageBubble received message:', {
    role: message.role,
    contentLength: message.content?.length || 0,
    thoughtsCount: message.thoughts?.length || 0,
    thoughts: message.thoughts
  });

  const isUser = message.role === 'user';
  const isAssistant = message.role === 'assistant';
  const messageClass = `message ${message.role}`;

  // Parse the message content to extract reasoning if it's an assistant message
  const parseAssistantMessage = (content: string) => {
    const parts = content.split('---REASONING---');
    if (parts.length > 1) {
      return {
        mainContent: parts[0].trim(),
        reasoning: parts[1].trim(),
      };
    }
    return {
      mainContent: content,
      reasoning: null,
    };
  };

  const { mainContent, reasoning } = isAssistant ? parseAssistantMessage(message.content) : { mainContent: message.content, reasoning: null };

  const avatarNode = isAssistant ? (
    <img src="/assets/novitai-logo.png" alt="Novitai" className="avatar inside" />
  ) : (
    <div className="avatar initials inside">{(message && message.role === 'user') ? 'U' : 'A'}</div>
  );
  
  return (
    <div className={messageClass}>
      <div className="bubble-avatar">
        {avatarNode}
      </div>
      
      <div className="message-content">
        {/* Thoughts section at the top for better visibility - only for assistant messages */}
        {isAssistant && message.thoughts && message.thoughts.length > 0 && (
          <div className="thoughts-section thoughts-section-top">
            <button
              className={`thoughts-toggle ${isThoughtsExpanded ? 'expanded' : 'collapsed'}`}
              onClick={() => setIsThoughtsExpanded(!isThoughtsExpanded)}
              aria-expanded={isThoughtsExpanded}
              aria-label={`${isThoughtsExpanded ? 'Hide' : 'Show'} AI thinking process`}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                background: 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
                border: '1px solid #dee2e6',
                borderRadius: '6px',
                cursor: 'pointer',
                padding: '8px 12px',
                fontSize: '0.85em',
                color: '#495057',
                width: '100%',
                textAlign: 'left',
                marginBottom: '12px',
                transition: 'all 0.2s ease',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
              }}
            >
              <span className="thoughts-icon" style={{
                transition: 'transform 0.2s ease',
                transform: isThoughtsExpanded ? 'rotate(90deg)' : 'rotate(0deg)',
                fontSize: '0.9em',
                color: '#6c757d'
              }}>
                ▶
              </span>
              <span className="thoughts-label" style={{
                fontWeight: '500',
                flex: 1
              }}>
                {isThoughtsExpanded ? 'Hide' : 'Show'} AI Thinking Process
              </span>
              <span className="thoughts-count" style={{
                fontSize: '0.8em',
                color: '#6c757d',
                background: '#ffffff',
                padding: '2px 8px',
                borderRadius: '12px',
                border: '1px solid #dee2e6'
              }}>
                {message.thoughts.length} step{message.thoughts.length !== 1 ? 's' : ''}
              </span>
            </button>
            
            {/* Conditionally render thoughts content */}
            {isThoughtsExpanded && (
              <div className="thoughts-content" style={{
                marginTop: '8px',
                padding: '12px',
                backgroundColor: '#f8f9fa',
                borderRadius: '8px',
                border: '1px solid #e9ecef',
                borderLeft: '3px solid #28a745'
              }}>
                <div className="thoughts-flowing-paragraph" style={{
                  fontSize: '0.9em',
                  lineHeight: '1.6',
                  color: '#495057',
                  whiteSpace: 'pre-wrap',
                  wordWrap: 'break-word'
                }}>
                  {message.thoughts.join(' ')}
                </div>
              </div>
            )}
          </div>
        )}

        <div className="main-content">
          {isAssistant ? (
            <MarkdownConverter 
              markdown={mainContent}
              className="assistant-markdown"
              showPreview={true}
              onConvert={setConvertedHtml}
            />
          ) : (
            mainContent
          )}
        </div>
        
        {reasoning && (
          <div className="reasoning-section">
            <button
              className="reasoning-toggle"
              onClick={() => setIsReasoningExpanded(!isReasoningExpanded)}
              aria-expanded={isReasoningExpanded}
            >
              {isReasoningExpanded ? 'Hide' : 'Show'} Reasoning
            </button>
            {isReasoningExpanded && (
              <div className="reasoning-content">
                <pre>{reasoning}</pre>
              </div>
            )}
          </div>
        )}
        
        {isAssistant && (
          <div className="insert-button-container">
            <InsertButton 
              content={convertedHtml && convertedHtml.trim() ? convertedHtml : mainContent}
              onInsert={onInsert}
            />
          </div>
        )}
        
        <div className="message-timestamp">
          {message.timestamp ? new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ''}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;
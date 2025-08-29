import React, { useState } from 'react';
import InsertButton from './InsertButton';
import { ChatMessage } from '../services/api';
import MarkdownConverter from './MarkdownConverter';
import { User } from '@auth0/auth0-spa-js';
import './MessageBubble.css';

interface MessageBubbleProps {
  message: ChatMessage;
  onInsert: (content: string) => void;
  user?: User | null;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message, onInsert, user }) => {
  const [isReasoningExpanded, setIsReasoningExpanded] = useState(false);
  const [isThoughtsExpanded, setIsThoughtsExpanded] = useState(message.thoughtsExpanded ?? false);
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

  // Match header avatar logic exactly
  const displayName = (user && (user.name || user.nickname)) ? (user.name || user.nickname) : null;
  
  const avatarNode = isAssistant ? (
    <img src="/assets/novitai-logo.png" alt="Novitai" className="avatar" />
  ) : (
    user && user.picture ? (
      <img src={user.picture} alt="User avatar" className="avatar" />
    ) : (
      <div className="initials">
        {displayName ? displayName.split(' ').map(n => n[0]).slice(0,2).join('').toUpperCase() : 'U'}
      </div>
    )
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
            >
              <span className="thoughts-icon" style={{
                transition: 'transform 0.2s ease',
                transform: isThoughtsExpanded ? 'rotate(90deg)' : 'rotate(0deg)',
                fontSize: '0.9em'
              }}>
                ▶
              </span>
              <span className="thoughts-label">
                {isThoughtsExpanded ? 'Hide' : 'Show'} AI Thinking Process
              </span>
              <span className="thoughts-count">
                {message.thoughts.length} step{message.thoughts.length !== 1 ? 's' : ''}
              </span>
            </button>
            
            {/* Thoughts content with proper CSS-controlled styling */}
            <div className={`thoughts-content ${isThoughtsExpanded ? 'expanded' : ''}`}>
              {isThoughtsExpanded && (
                <div className="thoughts-content-inner">
                  {message.thoughts.map((thought, index) => (
                    <div key={index} className="thought-item">
                      {thought.trim()}
                    </div>
                  ))}
                </div>
              )}
            </div>
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
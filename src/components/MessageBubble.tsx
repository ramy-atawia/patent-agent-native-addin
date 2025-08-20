import React, { useState } from 'react';
import { InsertButton } from './InsertButton';
import './MessageBubble.css';

interface MessageBubbleProps {
  message: ChatMessage;
  onInsert: (content: string) => void;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message, onInsert }) => {
  const [isReasoningExpanded, setIsReasoningExpanded] = useState(false);

  const isAssistant = message.role === 'assistant';
  // Treat user messages as left-aligned per request
  const messageClass = `message ${message.role}`;

  // Parse the message content to extract reasoning if it's an assistant message
  const parseAssistantMessage = (content: string) => {
    // Simple parsing - in a real implementation, this would be more sophisticated
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

  const isSingleLine = !mainContent.includes('\n') && mainContent.trim().length <= 80;

  const displayName = null; // handled elsewhere for initials if needed

  const avatarNode = isAssistant ? (
    <img src="/assets/novitai-logo.png" alt="Novitai" className="avatar inside" />
  ) : (
    <div className="avatar initials inside">{(message && message.role === 'user') ? 'U' : 'A'}</div>
  );
  
  return (
    <div className={messageClass}>
      <div className="message-content">
        <div className="message-header">
          {avatarNode}
          {displayName && <div className="message-sender">{displayName}</div>}
        </div>
        
        <div className={`message-text ${isSingleLine ? 'single-line' : ''}`}>
          {mainContent}
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
          <div className="message-actions">
            <InsertButton 
              content={mainContent}
              onInsert={onInsert}
            />
          </div>
        )}
        
        <div className="message-timestamp">
          {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;

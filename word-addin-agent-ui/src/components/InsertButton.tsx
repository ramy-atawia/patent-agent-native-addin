import React from 'react';
import './InsertButton.css';

interface InsertButtonProps {
  content: string;
  disabled?: boolean;
  onInsert?: (content: string) => Promise<void> | void;
}

const InsertButton: React.FC<InsertButtonProps> = ({ content, disabled = false, onInsert }) => {
  const handleInsert = async () => {
    if (disabled || !content.trim()) return;
    
    try {
      // Try callback first, then fallback to Office.js
      if (onInsert) {
        await onInsert(content);
      } else if (typeof Office !== 'undefined' && typeof Word !== 'undefined') {
        await Word.run(async (context: any) => {
          const selection = context.document.getSelection();
          
          if (content.includes('<') && content.includes('>')) {
            // Use insertHtml with proper Word.InsertLocation to prevent auto-conversion
            selection.insertHtml(content, Word.InsertLocation.replace);
            
            // Force context sync and then select the inserted content
            await context.sync();
            
            // This prevents Word's auto-conversion back to raw HTML
            selection.select();
            await context.sync();
          } else {
            // Insert as plain text for non-HTML content
            selection.insertText(content, 'Replace');
          }
          
          await context.sync();
        });
      } else {
        console.warn('Office.js not available');
      }
    } catch (error) {
      console.error('Error inserting content:', error);
    }
  };

  return (
    <button 
      className="insert-button" 
      onClick={handleInsert}
      disabled={disabled}
      title={disabled ? "Word.js not ready" : "Insert this content into the Word document"}
      aria-label="Insert content into Word document"
    >
      <svg 
        width="16" 
        height="16" 
        viewBox="0 0 24 24" 
        fill="none" 
        stroke="currentColor" 
        strokeWidth="2" 
        strokeLinecap="round" 
        strokeLinejoin="round"
      >
        <path d="M3 17v2a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-2"/>
        <path d="m8 12 4 4 4-4"/>
        <line x1="12" y1="2" x2="12" y2="16"/>
      </svg>
    </button>
  );
};

export default InsertButton;

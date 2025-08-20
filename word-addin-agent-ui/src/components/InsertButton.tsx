import React from 'react';
import './InsertButton.css';

interface InsertButtonProps {
  content: string;
  onInsert: (content: string) => void;
  disabled?: boolean;
}

const InsertButton: React.FC<InsertButtonProps> = ({ content, onInsert, disabled = false }) => {
  const handleInsert = async () => {
    if (disabled) return;
    
    try {
      // Check if Office.js is available
      if (typeof Office !== 'undefined' && typeof Word !== 'undefined') {
        await Word.run(async (context: any) => {
          const selection = context.document.getSelection();
          selection.insertText(content, 'Replace');
          await context.sync();
        });
        // Call the onInsert callback after successful insertion
        onInsert(content);
      } else {
        console.warn('Office.js not available');
        // Fallback to the onInsert callback
        onInsert(content);
      }
    } catch (error) {
      console.error('Error inserting content:', error);
      // Still call onInsert even if Word.js fails
      onInsert(content);
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

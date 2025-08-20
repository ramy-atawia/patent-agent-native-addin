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
    >
      📄 Insert into Document
    </button>
  );
};

export default InsertButton;

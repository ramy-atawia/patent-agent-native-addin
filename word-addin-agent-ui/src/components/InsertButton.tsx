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
          try {
            const selection = context.document.getSelection();
            
            if (content.includes('<') && content.includes('>')) {
              // Clean and format HTML content for Word
              let formattedContent = content.trim();
              
              // Ensure content starts with a proper HTML tag
              if (!formattedContent.startsWith('<')) {
                formattedContent = `<div>${formattedContent}</div>`;
              }
              
              // Use Word's insertHtml method with proper location
              // Word.InsertLocation.replace will replace the current selection
              selection.insertHtml(formattedContent, Word.InsertLocation.replace);
              
              // Sync to ensure the HTML is inserted
              await context.sync();
              
              // Get the inserted range and apply formatting
              const insertedRange = selection.getRange();
              insertedRange.load('text,paragraphs');
              await context.sync();
              
              // Apply consistent formatting to the inserted content
              insertedRange.font.name = 'Calibri';
              insertedRange.font.size = 11;
              
              // Ensure proper paragraph spacing
              if (insertedRange.paragraphs) {
                insertedRange.paragraphs.load('firstLineIndent,spacing');
                await context.sync();
                
                // Set consistent paragraph formatting
                insertedRange.paragraphs.firstLineIndent = 0;
                insertedRange.paragraphs.spacing.after = 240; // 12pt spacing
              }
              
              await context.sync();
              
            } else {
              // Insert as plain text with formatting
              selection.insertText(content, 'Replace');
              
              // Apply formatting to plain text
              const insertedRange = selection.getRange();
              insertedRange.font.name = 'Calibri';
              insertedRange.font.size = 11;
              
              await context.sync();
            }
          } catch (error) {
            console.error('Error in Word.run:', error);
            throw error;
          }
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

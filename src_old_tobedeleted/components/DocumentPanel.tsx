import React, { useState, useEffect } from 'react';
import { documentService, DocumentContent } from '../services/documentService';
import { WordFormatting } from '../services/documentService';
import { useWordJs } from '../hooks/useWordJs';
import './DocumentPanel.css';

export const DocumentPanel: React.FC = () => {
  const [documentInfo, setDocumentInfo] = useState<DocumentContent | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [wordCount, setWordCount] = useState(0);
  const [paragraphCount, setParagraphCount] = useState(0);
  
  // Use the Word.js hook for safe access
  const { isReady, isLoading: wordJsLoading, error: wordJsError, execute } = useWordJs();

  useEffect(() => {
    if (isReady) {
      loadDocumentInfo();
    }
  }, [isReady]);

  const loadDocumentInfo = async () => {
    if (!isReady) {
      console.warn('Word.js not ready, cannot load document info');
      return;
    }

    try {
      setIsLoading(true);
      const content = await execute(async () => documentService.getDocumentContent());
      
      if (content) {
        setDocumentInfo(content);
        
        // Calculate statistics
        setWordCount(content.text.split(/\s+/).filter(word => word.length > 0).length);
        setParagraphCount(content.paragraphs.length);
      }
    } catch (error) {
      console.error('Error loading document info:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Document analysis UI removed; service placeholder remains in documentService

  const handleEnableTrackChanges = async () => {
    if (!isReady) {
      console.warn('Word.js not ready, cannot enable track changes');
      return;
    }

    try {
      await execute(async () => documentService.enableTrackChanges());
      console.log('Track changes enabled');
    } catch (error) {
      console.error('Error enabling track changes:', error);
    }
  };

  const handleAddReviewComment = async () => {
    if (!isReady) {
      console.warn('Word.js not ready, cannot add review comment');
      return;
    }

    const comment = prompt('Enter your review comment:');
    if (comment) {
      try {
        await execute(async () => documentService.addReviewComment(comment));
        console.log('Review comment added');
      } catch (error) {
        console.error('Error adding review comment:', error);
      }
    }
  };

  // Show loading state while Word.js is initializing
  if (wordJsLoading) {
    return (
      <div className="document-panel">
        <div className="panel-header">
          <h3>Document Info</h3>
        </div>
        <div className="loading-indicator">Initializing Word.js...</div>
      </div>
    );
  }

  // Show error state if Word.js failed to initialize
  if (wordJsError) {
    return (
      <div className="document-panel">
        <div className="panel-header">
          <h3>Document Info</h3>
        </div>
        <div className="error-message">
          <p>❌ Failed to initialize Word.js</p>
          <p className="error-details">{wordJsError}</p>
          <button 
            className="retry-btn"
            onClick={() => window.location.reload()}
          >
            🔄 Retry
          </button>
        </div>
      </div>
    );
  }

  // Show loading state while loading document info
  if (isLoading && !documentInfo) {
    return (
      <div className="document-panel">
        <div className="panel-header">
          <h3>Document Info</h3>
        </div>
        <div className="loading-indicator">Loading document...</div>
      </div>
    );
  }

  return (
    <div className="document-panel">
      <div className="panel-header">
        <h3>Document Info</h3>
        <button 
          className="refresh-btn"
          onClick={loadDocumentInfo}
          disabled={isLoading || !isReady}
          title={!isReady ? "Word.js not ready" : "Refresh document info"}
        >
          🔄
        </button>
      </div>

      {documentInfo && (
        <div className="document-stats">
          <div className="stat-item">
            <span className="stat-label">Words:</span>
            <span className="stat-value">{wordCount.toLocaleString()}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Paragraphs:</span>
            <span className="stat-value">{paragraphCount}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Characters:</span>
            <span className="stat-value">{documentInfo.text.length.toLocaleString()}</span>
          </div>
        </div>
      )}

      <div className="document-actions">
        {/* Document analysis removed from UI; keep service placeholder in documentService */}
        
        <button
          className="action-button secondary"
          onClick={handleEnableTrackChanges}
          disabled={!isReady}
          title={!isReady ? "Word.js not ready" : "Enable track changes"}
        >
          📝 Enable Track Changes
        </button>
        
        <button
          className="action-button secondary"
          onClick={() => handleAddReviewComment()}
          disabled={!isReady}
          title={!isReady ? "Word.js not ready" : "Add review comment"}
        >
          💬 Add Review Comment
        </button>
      </div>

      {documentInfo && (
        <div className="document-preview">
          <h4>Document Preview</h4>
          <div className="preview-content">
            {documentInfo.text.length > 200 
              ? `${documentInfo.text.substring(0, 200)}...`
              : documentInfo.text
            }
          </div>
        </div>
      )}
    </div>
  );
};

// Local DocumentChange type (removed dependency on api.ts DocumentChange)
export interface DocumentChange {
  type: 'insert' | 'replace' | 'delete';
  content: string;
  location: 'start' | 'end' | 'specific';
  target_text?: string;
  formatting?: {
    bold?: boolean;
    italic?: boolean;
    color?: string;
  };
}

export interface WordFormatting {
  bold?: boolean;
  italic?: boolean;
  color?: string;
  fontSize?: number;
  fontName?: string;
}

export interface DocumentContent {
  text: string;
  paragraphs: string[];
  selection?: {
    text: string;
    start: number;
    end: number;
  };
}

class DocumentService {
  /**
   * Get the current document content
   */
  async getDocumentContent(): Promise<DocumentContent> {
    return new Promise((resolve, reject) => {
      Word.run(async (context) => {
        try {
          const body = context.document.body;
          body.load('text,paragraphs');
          
          await context.sync();
          
          const paragraphs = body.paragraphs.items.map(p => p.text);
          const text = body.text;
          
          resolve({
            text,
            paragraphs,
          });
        } catch (error) {
          reject(error);
        }
      });
    });
  }

  /**
   * Get the current selection
   */
  async getSelection(): Promise<DocumentContent['selection']> {
    return new Promise((resolve, reject) => {
      Word.run(async (context) => {
        try {
          const selection = context.document.getSelection();
          selection.load('text,start,end');
          
          await context.sync();
          
          resolve({
            text: selection.text,
            start: 0, // Office.js doesn't expose start/end positions directly
            end: selection.text.length,
          });
        } catch (error) {
          reject(error);
        }
      });
    });
  }

  /**
   * Insert text or HTML at the current selection or cursor position
   */
  async insertText(text: string, formatting?: WordFormatting): Promise<void> {
    return new Promise((resolve, reject) => {
      Word.run(async (context) => {
        try {
          const selection = context.document.getSelection();
          selection.load('text,start,end');
          
          await context.sync();
          
          // Check if content is HTML and handle accordingly
          if (text.includes('<') && text.includes('>')) {
            // Insert as HTML for proper formatting
            if (selection.text.length > 0) {
              selection.insertHtml(text, Word.InsertLocation.replace);
            } else {
              selection.insertHtml(text, Word.InsertLocation.before);
            }
          } else {
            // Insert as plain text
            if (selection.text.length > 0) {
              selection.insertText(text, 'Replace');
            } else {
              selection.insertText(text, 'Before');
            }
          }
          
          // Apply formatting if specified (only for plain text)
          if (formatting && !text.includes('<')) {
            this.applyFormattingToRange(selection, formatting);
          }
          
          await context.sync();
          resolve();
        } catch (error) {
          reject(error);
        }
      });
    });
  }

  /**
   * Insert text at the end of the document
   */
  async insertTextAtEnd(text: string, formatting?: WordFormatting): Promise<void> {
    return new Promise((resolve, reject) => {
      Word.run(async (context) => {
        try {
          const body = context.document.body;
          const paragraph = body.insertParagraph(text, 'End');
          
          // Apply formatting if specified
          if (formatting) {
            this.applyFormattingToRange(paragraph, formatting);
          }
          
          await context.sync();
          resolve();
        } catch (error) {
          reject(error);
        }
      });
    });
  }

  /**
   * Replace specific text in the document
   */
  async replaceText(searchText: string, replaceText: string, formatting?: WordFormatting): Promise<void> {
    return new Promise((resolve, reject) => {
      Word.run(async (context) => {
        try {
          const body = context.document.body;
          const range = body.search(searchText, { matchCase: false, matchWholeWord: false });
          
          if (range.items.length > 0) {
            const firstMatch = range.items[0];
            firstMatch.insertText(replaceText, 'Replace');
            
            // Apply formatting if specified
            if (formatting) {
              this.applyFormatting(firstMatch, formatting);
            }
          }
          
          await context.sync();
          resolve();
        } catch (error) {
          reject(error);
        }
      });
    });
  }

  /**
   * Delete specific text from the document
   */
  async deleteText(searchText: string): Promise<void> {
    return new Promise((resolve, reject) => {
      Word.run(async (context) => {
        try {
          const body = context.document.body;
          const range = body.search(searchText, { matchCase: false, matchWholeWord: false });
          
          if (range.items.length > 0) {
            range.items.forEach(item => {
              item.delete();
            });
          }
          
          await context.sync();
          resolve();
        } catch (error) {
          reject(error);
        }
      });
    });
  }

  /**
   * Enable track changes in the document
   */
  async enableTrackChanges(): Promise<void> {
    return new Promise((resolve, reject) => {
      Word.run(async (context) => {
        try {
          // Note: Office.js doesn't directly control track changes
          // This is handled by Word's built-in track changes feature
          // We can only ensure our operations work with track changes enabled
          await context.sync();
          resolve();
        } catch (error) {
          reject(error);
        }
      });
    });
  }

  /**
   * Add review comment to the document
   */
  async addReviewComment(comment: string, targetText?: string): Promise<void> {
    return new Promise((resolve, reject) => {
      Word.run(async (context) => {
        try {
          if (targetText) {
            // Find the target text and add comment
            const body = context.document.body;
            const range = body.search(targetText, { matchCase: false, matchWholeWord: false });
            
            if (range.items.length > 0) {
              const firstMatch = range.items[0];
              // Note: Office.js doesn't directly support comments in all versions
              // This is a placeholder for future implementation
              console.log(`Comment would be added to: ${targetText}`);
            }
          } else {
            // Add comment to current selection
            const selection = context.document.getSelection();
            selection.load('text');
            await context.sync();
            
            if (selection.text.length > 0) {
              console.log(`Comment would be added to selection: ${selection.text}`);
            }
          }
          
          await context.sync();
          resolve();
        } catch (error) {
          reject(error);
        }
      });
    });
  }

  /**
   * Apply formatting to a range (legacy method - use applyFormattingToRange instead)
   * @deprecated Use applyFormattingToRange for better error handling
   */
  private applyFormatting(range: Word.Range, formatting: WordFormatting): void {
    this.applyFormattingToRange(range, formatting);
  }

  /**
   * Apply multiple document changes with proper formatting preservation
   */
  async applyChanges(changes: DocumentChange[]): Promise<void> {
    return new Promise((resolve, reject) => {
      Word.run(async (context) => {
        try {
          for (const change of changes) {
            switch (change.type) {
              case 'insert':
                if (change.location === 'end') {
                  const body = context.document.body;
                  const paragraph = body.insertParagraph(change.content, 'End');
                  if (change.formatting) {
                    this.applyFormattingToRange(paragraph, change.formatting);
                  }
                } else {
                  const selection = context.document.getSelection();
                  selection.load('text,start,end');
                  await context.sync();
                  
                  if (selection.text.length > 0) {
                    selection.insertText(change.content, 'Replace');
                  } else {
                    selection.insertText(change.content, 'Before');
                  }
                  
                  if (change.formatting) {
                    this.applyFormattingToRange(selection, change.formatting);
                  }
                }
                break;
                
              case 'replace':
                if (change.target_text) {
                  const body = context.document.body;
                  const range = body.search(change.target_text, { matchCase: false, matchWholeWord: false });
                  
                  if (range.items.length > 0) {
                    const firstMatch = range.items[0];
                    firstMatch.insertText(change.content, 'Replace');
                    
                    if (change.formatting) {
                      this.applyFormatting(firstMatch, change.formatting);
                    }
                  }
                }
                break;
                
              case 'delete':
                if (change.target_text) {
                  const body = context.document.body;
                  const range = body.search(change.target_text, { matchCase: false, matchWholeWord: false });
                  
                  if (range.items.length > 0) {
                    range.items.forEach(item => {
                      item.delete();
                    });
                  }
                }
                break;
            }
          }
          
          await context.sync();
          resolve();
        } catch (error) {
          reject(error);
        }
      });
    });
  }

  /**
   * Apply formatting to a range or paragraph with proper error handling
   */
  private applyFormattingToRange(range: Word.Range | Word.Paragraph, formatting: WordFormatting): void {
    try {
      if (formatting.bold !== undefined) {
        range.font.bold = formatting.bold;
      }
      if (formatting.italic !== undefined) {
        range.font.italic = formatting.italic;
      }
      if (formatting.color) {
        range.font.color = formatting.color;
      }
      if (formatting.fontSize) {
        range.font.size = formatting.fontSize;
      }
      if (formatting.fontName) {
        range.font.name = formatting.fontName;
      }
    } catch (error) {
      console.warn('Failed to apply formatting:', error);
    }
  }
}

export const documentService = new DocumentService();
export default documentService;

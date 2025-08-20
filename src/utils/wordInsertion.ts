import { Word } from 'office-js';

export interface WordInsertionOptions {
  position?: 'start' | 'end' | 'cursor';
  preserveFormatting?: boolean;
  insertAsHtml?: boolean;
  addPageBreak?: boolean;
}

export class WordInsertionUtility {
  private static instance: WordInsertionUtility;
  private wordApp: Word.Application | null = null;

  private constructor() {}

  public static getInstance(): WordInsertionUtility {
    if (!WordInsertionUtility.instance) {
      WordInsertionUtility.instance = new WordInsertionUtility();
    }
    return WordInsertionUtility.instance;
  }

  /**
   * Initialize the Word application reference
   */
  public async initialize(): Promise<void> {
    try {
      await Word.run(async (context) => {
        this.wordApp = context.application;
        await context.sync();
      });
    } catch (error) {
      console.error('Failed to initialize Word application:', error);
      throw error;
    }
  }

  /**
   * Insert HTML content into Word document
   */
  public async insertHtml(
    htmlContent: string,
    options: WordInsertionOptions = {}
  ): Promise<void> {
    const {
      position = 'cursor',
      preserveFormatting = true,
      insertAsHtml = true,
      addPageBreak = false
    } = options;

    try {
      await Word.run(async (context) => {
        const body = context.document.body;
        let insertLocation: Word.Range;

        // Determine insertion location
        switch (position) {
          case 'start':
            insertLocation = body.getRange('Start');
            break;
          case 'end':
            insertLocation = body.getRange('End');
            break;
          case 'cursor':
          default:
            insertLocation = context.document.getSelection();
            break;
        }

        if (addPageBreak && position !== 'start') {
          // Add page break before content
          insertLocation.insertBreak(Word.BreakType.page, 'Before');
        }

        if (insertAsHtml) {
          // Insert as HTML for better formatting preservation
          await this.insertHtmlContent(context, insertLocation, htmlContent);
        } else {
          // Insert as plain text
          await this.insertPlainText(context, insertLocation, htmlContent);
        }

        // Preserve formatting if requested
        if (preserveFormatting) {
          await this.applyProfessionalFormatting(context, insertLocation);
        }

        await context.sync();
      });
    } catch (error) {
      console.error('Failed to insert HTML content:', error);
      throw error;
    }
  }

  /**
   * Insert HTML content with proper Word formatting
   */
  private async insertHtmlContent(
    context: Word.RequestContext,
    location: Word.Range,
    htmlContent: string
  ): Promise<void> {
    try {
      // Convert HTML to Word-compatible format
      const wordHtml = this.convertHtmlForWord(htmlContent);
      
      // Insert the HTML content
      location.insertHtml(wordHtml, 'Replace');
    } catch (error) {
      console.error('Failed to insert HTML content:', error);
      // Fallback to plain text insertion
      await this.insertPlainText(context, location, htmlContent);
    }
  }

  /**
   * Insert plain text content
   */
  private async insertPlainText(
    context: Word.RequestContext,
    location: Word.Range,
    textContent: string
  ): Promise<void> {
    // Convert HTML to plain text
    const plainText = this.htmlToPlainText(textContent);
    location.insertText(plainText, 'Replace');
  }

  /**
   * Convert HTML to Word-compatible format
   */
  private convertHtmlForWord(html: string): string {
    // Clean and optimize HTML for Word
    let wordHtml = html
      // Remove unsupported CSS classes
      .replace(/class="[^"]*"/g, '')
      // Convert custom styling to Word-compatible inline styles
      .replace(/style="[^"]*"/g, '')
      // Ensure proper paragraph spacing
      .replace(/<p>/g, '<p style="margin: 12px 0;">')
      // Ensure proper table formatting
      .replace(/<table>/g, '<table style="border-collapse: collapse; width: 100%;">')
      .replace(/<th>/g, '<th style="border: 1px solid #ddd; padding: 8px; background-color: #f8f9fa; font-weight: bold;">')
      .replace(/<td>/g, '<td style="border: 1px solid #ddd; padding: 8px;">')
      // Ensure proper heading formatting
      .replace(/<h1>/g, '<h1 style="color: #2c3e50; font-size: 24px; font-weight: bold; margin: 20px 0 15px 0; border-bottom: 3px solid #3498db; padding-bottom: 8px;">')
      .replace(/<h2>/g, '<h2 style="color: #34495e; font-size: 20px; font-weight: bold; margin: 18px 0 12px 0; border-bottom: 2px solid #ecf0f1; padding-bottom: 6px;">')
      .replace(/<h3>/g, '<h3 style="color: #2c3e50; font-size: 18px; font-weight: bold; margin: 16px 0 10px 0;">')
      .replace(/<h4>/g, '<h4 style="color: #34495e; font-size: 16px; font-weight: bold; margin: 14px 0 8px 0;">')
      // Ensure proper list formatting
      .replace(/<ul>/g, '<ul style="margin: 12px 0; padding-left: 25px;">')
      .replace(/<ol>/g, '<ol style="margin: 12px 0; padding-left: 25px;">')
      .replace(/<li>/g, '<li style="margin: 6px 0;">')
      // Ensure proper code formatting
      .replace(/<code>/g, '<code style="background-color: #f8f9fa; padding: 2px 6px; border-radius: 4px; font-family: Courier New, monospace; font-size: 13px; color: #e74c3c;">')
      .replace(/<pre>/g, '<pre style="background-color: #f8f9fa; padding: 15px; border-radius: 6px; border-left: 4px solid #3498db;">')
      // Ensure proper blockquote formatting
      .replace(/<blockquote>/g, '<blockquote style="border-left: 4px solid #3498db; margin: 15px 0; padding: 10px 20px; background-color: #f8f9fa; font-style: italic;">')
      // Ensure proper emphasis formatting
      .replace(/<strong>/g, '<strong style="font-weight: bold; color: #2c3e50;">')
      .replace(/<em>/g, '<em style="font-style: italic; color: #34495e;">')
      // Ensure proper horizontal rule formatting
      .replace(/<hr>/g, '<hr style="border: none; border-top: 2px solid #ecf0f1; margin: 20px 0;">');

    return wordHtml;
  }

  /**
   * Convert HTML to plain text
   */
  private htmlToPlainText(html: string): string {
    // Create a temporary DOM element to parse HTML
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;
    
    // Convert to plain text with proper spacing
    let text = tempDiv.textContent || tempDiv.innerText || '';
    
    // Clean up extra whitespace
    text = text
      .replace(/\s+/g, ' ')
      .replace(/\n\s*\n/g, '\n\n')
      .trim();
    
    return text;
  }

  /**
   * Apply professional formatting to inserted content
   */
  private async applyProfessionalFormatting(
    context: Word.RequestContext,
    location: Word.Range
  ): Promise<void> {
    try {
      // Get the inserted content range
      const contentRange = location.getRange('End');
      
      // Apply professional font
      contentRange.font.name = 'Calibri';
      contentRange.font.size = 11;
      
      // Apply proper line spacing
      contentRange.paragraphFormat.lineSpacing = 1.15;
      
      // Apply proper paragraph spacing
      contentRange.paragraphFormat.spaceAfter = 6;
      contentRange.paragraphFormat.spaceBefore = 6;
      
      await context.sync();
    } catch (error) {
      console.error('Failed to apply professional formatting:', error);
    }
  }

  /**
   * Insert a patent report with professional formatting
   */
  public async insertPatentReport(
    markdownContent: string,
    options: WordInsertionOptions = {}
  ): Promise<void> {
    try {
      // Convert markdown to HTML first
      const htmlContent = await this.markdownToHtml(markdownContent);
      
      // Insert with professional formatting
      await this.insertHtml(htmlContent, {
        ...options,
        preserveFormatting: true,
        insertAsHtml: true,
        addPageBreak: true
      });
      
      console.log('Patent report inserted successfully');
    } catch (error) {
      console.error('Failed to insert patent report:', error);
      throw error;
    }
  }

  /**
   * Convert markdown to HTML (basic conversion)
   */
  private async markdownToHtml(markdown: string): Promise<string> {
    // Basic markdown to HTML conversion
    // In a real implementation, you might use a more sophisticated converter
    let html = markdown
      // Headers
      .replace(/^# (.*$)/gim, '<h1>$1</h1>')
      .replace(/^## (.*$)/gim, '<h2>$1</h2>')
      .replace(/^### (.*$)/gim, '<h3>$1</h3>')
      .replace(/^#### (.*$)/gim, '<h4>$1</h4>')
      // Bold and italic
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      // Lists
      .replace(/^\* (.*$)/gim, '<li>$1</li>')
      .replace(/^\- (.*$)/gim, '<li>$1</li>')
      .replace(/^\d+\. (.*$)/gim, '<li>$1</li>')
      // Wrap lists
      .replace(/(<li>.*<\/li>)/gims, '<ul>$1</ul>')
      // Paragraphs
      .replace(/\n\n/g, '</p><p>')
      .replace(/^(?!<[h|u|o]|<li>)(.*$)/gim, '<p>$1</p>')
      // Clean up empty paragraphs
      .replace(/<p><\/p>/g, '')
      // Tables (basic support)
      .replace(/\|(.+)\|/g, '<tr><td>$1</td></tr>')
      .replace(/<tr><td>(.+)<\/td><\/tr>/g, '<table><tr><td>$1</td></tr></table>')
      // Code blocks
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      // Links
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>')
      // Horizontal rules
      .replace(/^---$/gim, '<hr>');

    return html;
  }

  /**
   * Get document statistics
   */
  public async getDocumentStats(): Promise<{
    wordCount: number;
    characterCount: number;
    paragraphCount: number;
  }> {
    try {
      let stats = { wordCount: 0, characterCount: 0, paragraphCount: 0 };
      
      await Word.run(async (context) => {
        const body = context.document.body;
        stats.wordCount = body.getWordCount();
        stats.characterCount = body.getCharacterCount();
        stats.paragraphCount = body.paragraphs.getCount();
        
        await context.sync();
      });
      
      return stats;
    } catch (error) {
      console.error('Failed to get document stats:', error);
      return { wordCount: 0, characterCount: 0, paragraphCount: 0 };
    }
  }
}

export default WordInsertionUtility;

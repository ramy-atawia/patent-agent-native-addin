import React, { useState, useEffect } from 'react';
import MarkdownConverter from './MarkdownConverter';
import WordInsertionUtility from '../utils/wordInsertion';
import styled from 'styled-components';

interface PatentReportDemoProps {
  className?: string;
}

const DemoContainer = styled.div`
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
`;

const DemoSection = styled.div`
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  background-color: #ffffff;
`;

const DemoTitle = styled.h2`
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 20px;
  border-bottom: 2px solid #3498db;
  padding-bottom: 8px;
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 10px;
  margin: 15px 0;
  flex-wrap: wrap;
`;

const Button = styled.button<{ variant?: 'primary' | 'secondary' | 'success' | 'danger' }>`
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  
  ${({ variant = 'primary' }) => {
    switch (variant) {
      case 'primary':
        return `
          background-color: #3498db;
          color: white;
          &:hover { background-color: #2980b9; }
        `;
      case 'secondary':
        return `
          background-color: #95a5a6;
          color: white;
          &:hover { background-color: #7f8c8d; }
        `;
      case 'success':
        return `
          background-color: #27ae60;
          color: white;
          &:hover { background-color: #229954; }
        `;
      case 'danger':
        return `
          background-color: #e74c3c;
          color: white;
          &:hover { background-color: #c0392b; }
        `;
    }
  }}
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const StatusMessage = styled.div<{ type: 'success' | 'error' | 'info' }>`
  padding: 12px;
  border-radius: 6px;
  margin: 15px 0;
  font-weight: 500;
  
  ${({ type }) => {
    switch (type) {
      case 'success':
        return `
          background-color: #d4edda;
          color: #155724;
          border: 1px solid #c3e6cb;
        `;
      case 'error':
        return `
          background-color: #f8d7da;
          color: #721c24;
          border: 1px solid #f5c6cb;
        `;
      case 'info':
        return `
          background-color: #d1ecf1;
          color: #0c5460;
          border: 1px solid #bee5eb;
        `;
    }
  }}
`;

const SampleMarkdown = styled.div`
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  padding: 15px;
  margin: 15px 0;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.4;
  max-height: 300px;
  overflow-y: auto;
`;

const PatentReportDemo: React.FC<PatentReportDemoProps> = ({ className }) => {
  const [markdownContent, setMarkdownContent] = useState<string>('');
  const [htmlContent, setHtmlContent] = useState<string>('');
  const [status, setStatus] = useState<{ type: 'success' | 'error' | 'info'; message: string } | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [wordUtility, setWordUtility] = useState<WordInsertionUtility | null>(null);

  // Sample patent report markdown
  const samplePatentReport = `# Prior Art Search Report: 5G Dynamic Spectrum Sharing QoS

## EXECUTIVE SUMMARY
- **Risk Level:** 🔴 High
- **Key Blocking Patents:**
  - Patent ID: 10004070 - Method and system for sharing frequency spectrum between GSM system and LTE system
  - Patent ID: 10003541 - Flow state aware management of QoS with a distributed classifier
  - Patent ID: 10002036 - System, method and computer program product for sharing information in a distributed framework

## RISK ASSESSMENT MATRIX
| Patent ID | Title | Risk Level | Specific Blocking Claims | What's Blocking | Action Required |
|-----------|-------|------------|-------------------------|------------------|------------------|
| 10004070  | Method and system for sharing frequency spectrum between GSM system and LTE system | 🔴 High | Claim 1: Method for sharing the whole available LTE spectrum bandwidth between GSM and LTE systems | The method outlines a framework for sharing frequency resources, which overlaps with dynamic spectrum sharing in 5G. | Conduct a detailed analysis of the claims and consider redesigning the technology to avoid infringement. |

## TECHNICAL ANALYSIS
### What's Blocking
- **Patent 10004070**: The method for sharing frequency spectrum directly impacts the ability to implement dynamic spectrum sharing in 5G networks, as it outlines specific techniques for resource allocation that could be applicable to 5G technologies.

### What's NOT Blocking
- Innovations that focus on alternative methods of spectrum sharing that do not rely on the specific techniques outlined in the blocking patents may provide pathways for development.

## BUSINESS RECOMMENDATIONS
- **Licensing Strategy**: Engage with the assignees of the blocking patents to explore licensing agreements. Estimated costs could range from $50,000 to $200,000 depending on the scope of use.
- **Development Strategy**: Focus on developing alternative QoS management systems that leverage machine learning or AI to differentiate from existing patents.

## NEXT STEPS
- **Week 1**: Assemble a team to analyze the blocking patents in detail.
- **Month 1**: Initiate contact with patent holders for potential licensing discussions.
- **Month 3**: Develop alternative strategies and begin prototyping new technologies.`;

  useEffect(() => {
    // Initialize with sample content
    setMarkdownContent(samplePatentReport);
    
    // Initialize Word utility
    const initWordUtility = async () => {
      try {
        const utility = WordInsertionUtility.getInstance();
        await utility.initialize();
        setWordUtility(utility);
        setStatus({ type: 'success', message: 'Word integration initialized successfully!' });
      } catch (error) {
        setStatus({ type: 'error', message: 'Failed to initialize Word integration. Make sure you\'re running in Word.' });
      }
    };

    initWordUtility();
  }, []);

  const handleMarkdownChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMarkdownContent(event.target.value);
  };

  const handleHtmlConvert = (html: string) => {
    setHtmlContent(html);
    setStatus({ type: 'success', message: 'Markdown converted to HTML successfully!' });
  };

  const handleInsertIntoWord = async () => {
    if (!wordUtility) {
      setStatus({ type: 'error', message: 'Word integration not initialized. Please wait or refresh the page.' });
      return;
    }

    setIsLoading(true);
    try {
      await wordUtility.insertPatentReport(markdownContent, {
        position: 'cursor',
        preserveFormatting: true,
        addPageBreak: true
      });
      setStatus({ type: 'success', message: 'Patent report inserted into Word document successfully!' });
    } catch (error) {
      setStatus({ type: 'error', message: `Failed to insert into Word: ${error}` });
    } finally {
      setIsLoading(false);
    }
  };

  const handleInsertHtmlIntoWord = async () => {
    if (!wordUtility || !htmlContent) {
      setStatus({ type: 'error', message: 'HTML content not available or Word integration not initialized.' });
      return;
    }

    setIsLoading(true);
    try {
      await wordUtility.insertHtml(htmlContent, {
        position: 'cursor',
        preserveFormatting: true,
        addPageBreak: true
      });
      setStatus({ type: 'success', message: 'HTML content inserted into Word document successfully!' });
    } catch (error) {
      setStatus({ type: 'error', message: `Failed to insert HTML into Word: ${error}` });
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearContent = () => {
    setMarkdownContent('');
    setHtmlContent('');
    setStatus({ type: 'info', message: 'Content cleared successfully.' });
  };

  const handleLoadSample = () => {
    setMarkdownContent(samplePatentReport);
    setStatus({ type: 'info', message: 'Sample patent report loaded.' });
  };

  return (
    <DemoContainer className={className}>
      <DemoTitle>Patent Report Markdown to Word Converter Demo</DemoTitle>
      
      {/* Status Messages */}
      {status && (
        <StatusMessage type={status.type}>
          {status.message}
        </StatusMessage>
      )}

      {/* Markdown Input Section */}
      <DemoSection>
        <DemoTitle>1. Markdown Input</DemoTitle>
        <p>Enter or edit your patent report in markdown format:</p>
        <textarea
          value={markdownContent}
          onChange={handleMarkdownChange}
          style={{
            width: '100%',
            minHeight: '200px',
            padding: '12px',
            border: '1px solid #ddd',
            borderRadius: '6px',
            fontFamily: 'Courier New, monospace',
            fontSize: '13px',
            lineHeight: '1.4'
          }}
          placeholder="Enter your patent report markdown here..."
        />
        <ButtonGroup>
          <Button variant="secondary" onClick={handleLoadSample}>
            Load Sample Report
          </Button>
          <Button variant="danger" onClick={handleClearContent}>
            Clear Content
          </Button>
        </ButtonGroup>
      </DemoSection>

      {/* HTML Preview Section */}
      <DemoSection>
        <DemoTitle>2. HTML Preview</DemoTitle>
        <p>Preview how your markdown will look when converted to HTML:</p>
        <MarkdownConverter
          markdown={markdownContent}
          onConvert={handleHtmlConvert}
          showPreview={true}
        />
      </DemoSection>

      {/* Word Insertion Section */}
      <DemoSection>
        <DemoTitle>3. Word Document Insertion</DemoTitle>
        <p>Insert your patent report directly into the current Word document:</p>
        <ButtonGroup>
          <Button
            variant="primary"
            onClick={handleInsertIntoWord}
            disabled={isLoading || !wordUtility}
          >
            {isLoading ? 'Inserting...' : 'Insert Markdown as HTML'}
          </Button>
          <Button
            variant="success"
            onClick={handleInsertHtmlIntoWord}
            disabled={isLoading || !wordUtility || !htmlContent}
          >
            {isLoading ? 'Inserting...' : 'Insert HTML Content'}
          </Button>
        </ButtonGroup>
        
        {wordUtility ? (
          <StatusMessage type="success">
            ✅ Word integration ready - You can insert content into your document
          </StatusMessage>
        ) : (
          <StatusMessage type="error">
            ❌ Word integration not available - Make sure you're running this in Word
          </StatusMessage>
        )}
      </DemoSection>

      {/* HTML Output Section */}
      <DemoSection>
        <DemoTitle>4. Generated HTML (Word-Ready)</DemoTitle>
        <p>This is the HTML content that will be inserted into Word:</p>
        <SampleMarkdown>
          {htmlContent || 'HTML content will appear here after conversion...'}
        </SampleMarkdown>
      </DemoSection>

      {/* Instructions Section */}
      <DemoSection>
        <DemoTitle>📋 How to Use</DemoTitle>
        <ol>
          <li><strong>Input Markdown:</strong> Enter your patent report in markdown format or load the sample</li>
          <li><strong>Preview HTML:</strong> See how your content will look when converted</li>
          <li><strong>Insert into Word:</strong> Click the insert button to add the report to your Word document</li>
          <li><strong>Professional Formatting:</strong> The content will be automatically formatted with professional styling</li>
        </ol>
        
        <h4>Features:</h4>
        <ul>
          <li>✅ Professional patent attorney styling</li>
          <li>✅ Word-compatible HTML output</li>
          <li>✅ Automatic page breaks</li>
          <li>✅ Professional font and spacing</li>
          <li>✅ Table formatting support</li>
          <li>✅ Responsive design</li>
        </ul>
      </DemoSection>
    </DemoContainer>
  );
};

export default PatentReportDemo;

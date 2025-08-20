import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import styled from 'styled-components';

interface MarkdownConverterProps {
  markdown: string;
  onConvert?: (html: string) => void;
  showPreview?: boolean;
  className?: string;
}

// Professional styling for patent reports
const StyledMarkdown = styled.div`
  font-family: 'Calibri', 'Arial', sans-serif;
  line-height: 1.6;
  color: #333;
  max-width: 100%;
  
  /* Headers */
  h1 {
    color: #2c3e50;
    font-size: 24px;
    font-weight: bold;
    margin: 20px 0 15px 0;
    border-bottom: 3px solid #3498db;
    padding-bottom: 8px;
  }
  
  h2 {
    color: #34495e;
    font-size: 20px;
    font-weight: bold;
    margin: 18px 0 12px 0;
    border-bottom: 2px solid #ecf0f1;
    padding-bottom: 6px;
  }
  
  h3 {
    color: #2c3e50;
    font-size: 18px;
    font-weight: bold;
    margin: 16px 0 10px 0;
  }
  
  h4 {
    color: #34495e;
    font-size: 16px;
    font-weight: bold;
    margin: 14px 0 8px 0;
  }
  
  /* Paragraphs */
  p {
    margin: 12px 0;
    text-align: justify;
  }
  
  /* Lists */
  ul, ol {
    margin: 12px 0;
    padding-left: 25px;
  }
  
  li {
    margin: 6px 0;
  }
  
  /* Tables */
  table {
    border-collapse: collapse;
    width: 100%;
    margin: 15px 0;
    font-size: 14px;
  }
  
  th, td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
  }
  
  th {
    background-color: #f8f9fa;
    font-weight: bold;
    color: #2c3e50;
  }
  
  tr:nth-child(even) {
    background-color: #f8f9fa;
  }
  
  tr:hover {
    background-color: #e9ecef;
  }
  
  /* Code blocks */
  code {
    background-color: #f8f9fa;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    color: #e74c3c;
  }
  
  pre {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 6px;
    overflow-x: auto;
    border-left: 4px solid #3498db;
  }
  
  pre code {
    background-color: transparent;
    padding: 0;
    color: #2c3e50;
  }
  
  /* Blockquotes */
  blockquote {
    border-left: 4px solid #3498db;
    margin: 15px 0;
    padding: 10px 20px;
    background-color: #f8f9fa;
    font-style: italic;
  }
  
  /* Links */
  a {
    color: #3498db;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  
  /* Emphasis */
  strong {
    font-weight: bold;
    color: #2c3e50;
  }
  
  em {
    font-style: italic;
    color: #34495e;
  }
  
  /* Horizontal rules */
  hr {
    border: none;
    border-top: 2px solid #ecf0f1;
    margin: 20px 0;
  }
  
  /* Patent-specific styling */
  .patent-id {
    font-weight: bold;
    color: #e74c3c;
    background-color: #fdf2f2;
    padding: 4px 8px;
    border-radius: 4px;
    border: 1px solid #fecaca;
  }
  
  .risk-level {
    font-weight: bold;
    padding: 6px 12px;
    border-radius: 6px;
    display: inline-block;
    margin: 5px 0;
  }
  
  .risk-high {
    background-color: #fef2f2;
    color: #dc2626;
    border: 1px solid #fecaca;
  }
  
  .risk-medium {
    background-color: #fffbeb;
    color: #d97706;
    border: 1px solid #fed7aa;
  }
  
  .risk-low {
    background-color: #f0fdf4;
    color: #16a34a;
    border: 1px solid #bbf7d0;
  }
  
  /* Executive summary styling */
  .executive-summary {
    background-color: #f8f9fa;
    border: 2px solid #3498db;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
  }
  
  .executive-summary h2 {
    border-bottom: none;
    color: #2c3e50;
    margin-top: 0;
  }
  
  /* Action items */
  .action-item {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 6px;
    padding: 12px;
    margin: 10px 0;
  }
  
  .action-item strong {
    color: #856404;
  }
  
  /* Timeline styling */
  .timeline {
    background-color: #e8f4fd;
    border: 1px solid #bee5eb;
    border-radius: 6px;
    padding: 15px;
    margin: 15px 0;
  }
  
  .timeline h3 {
    color: #0c5460;
    margin-top: 0;
  }
  
  /* Responsive design */
  @media (max-width: 768px) {
    font-size: 14px;
    
    h1 { font-size: 20px; }
    h2 { font-size: 18px; }
    h3 { font-size: 16px; }
    
    table {
      font-size: 12px;
    }
    
    th, td {
      padding: 8px;
    }
  }
`;

const MarkdownConverter: React.FC<MarkdownConverterProps> = ({
  markdown,
  onConvert,
  showPreview = true,
  className
}) => {
  
  // Convert markdown to HTML and notify parent
  const handleMarkdownRender = (node: any) => {
    if (onConvert && node) {
      // Get the HTML content
      const htmlContent = node.innerHTML;
      onConvert(htmlContent);
    }
  };

  // Custom components for enhanced styling
  const components = {
    // Custom heading components
    h1: ({ children, ...props }: any) => (
      <h1 {...props} style={{ color: '#2c3e50', borderBottom: '3px solid #3498db' }}>
        {children}
      </h1>
    ),
    
    h2: ({ children, ...props }: any) => (
      <h2 {...props} style={{ color: '#34495e', borderBottom: '2px solid #ecf0f1' }}>
        {children}
      </h2>
    ),
    
    // Custom table component
    table: ({ children, ...props }: any) => (
      <table {...props} style={{ borderCollapse: 'collapse', width: '100%' }}>
        {children}
      </table>
    ),
    
    // Custom code block component
    code: ({ node, inline, className, children, ...props }: any) => {
      const match = /language-(\w+)/.exec(className || '');
      return !inline ? (
        <pre style={{ backgroundColor: '#f8f9fa', padding: '15px', borderRadius: '6px' }}>
          <code className={className} {...props}>
            {children}
          </code>
        </pre>
      ) : (
        <code className={className} {...props} style={{ backgroundColor: '#f8f9fa', padding: '2px 6px' }}>
          {children}
        </code>
      );
    },
    
    // Custom blockquote component
    blockquote: ({ children, ...props }: any) => (
      <blockquote {...props} style={{ borderLeft: '4px solid #3498db', backgroundColor: '#f8f9fa' }}>
        {children}
      </blockquote>
    ),
  };

  return (
    <div className={className}>
      {showPreview && (
        <StyledMarkdown>
                  <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          rehypePlugins={[rehypeRaw]}
          components={components}
        >
            {markdown}
          </ReactMarkdown>
        </StyledMarkdown>
      )}
    </div>
  );
};

export default MarkdownConverter;

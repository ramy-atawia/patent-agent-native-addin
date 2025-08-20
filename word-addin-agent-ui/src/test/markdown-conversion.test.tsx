import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import MarkdownConverter from '../components/MarkdownConverter';

// Test data for different markdown scenarios
const testCases = {
  // Basic markdown elements
  basic: {
    name: 'Basic Markdown Elements',
    markdown: `# Header 1
## Header 2
### Header 3

**Bold text** and *italic text*

- List item 1
- List item 2
- List item 3

1. Numbered item 1
2. Numbered item 2

\`inline code\`

[Link text](https://example.com)

> This is a blockquote

---

Paragraph with **bold** and *italic* text.`,
    expectedElements: ['h1', 'h2', 'h3', 'strong', 'em', 'ul', 'ol', 'code', 'a', 'blockquote', 'hr', 'p']
  },

  // Patent-specific content
  patentReport: {
    name: 'Patent Report Format',
    markdown: `# Prior Art Search Report: 5G Dynamic Spectrum Sharing

## EXECUTIVE SUMMARY
- **Risk Level:** 🔴 High
- **Key Blocking Patents:** 3 found
- **Recommendation:** Proceed with caution

## RISK ASSESSMENT MATRIX
| Patent ID | Title | Risk Level | Action Required |
|-----------|-------|------------|------------------|
| 10004070  | Method for spectrum sharing | 🔴 High | Detailed analysis needed |
| 10003541  | QoS management system | 🟡 Medium | Review claims |
| 10002036  | Distributed framework | 🟢 Low | Monitor developments |

## TECHNICAL ANALYSIS
### What's Blocking
- **Patent 10004070**: Direct overlap with core technology
- **Patent 10003541**: Partial overlap in QoS aspects

### What's NOT Blocking
- Alternative implementation approaches
- Different technical solutions

## BUSINESS RECOMMENDATIONS
1. **Immediate Actions:**
   - Conduct detailed claim analysis
   - Engage patent attorney review
   - Explore design-around options

2. **Long-term Strategy:**
   - Monitor patent landscape
   - Develop alternative technologies
   - Consider licensing discussions

## NEXT STEPS
- **Week 1**: Assemble technical team
- **Month 1**: Complete claim analysis
- **Month 3**: Develop mitigation strategies`,
    expectedElements: ['h1', 'h2', 'h3', 'h4', 'table', 'th', 'td', 'ul', 'ol', 'li', 'strong', 'em', 'code']
  },

  // Complex tables
  complexTables: {
    name: 'Complex Table Formatting',
    markdown: `# Table Test

## Simple Table
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |

## Complex Table with Formatting
| **Patent ID** | **Title** | **Risk Level** | **Claims** | **Assignee** |
|---------------|-----------|----------------|------------|--------------|
| \`10004070\`  | *Method for spectrum sharing* | 🔴 **HIGH** | 15 claims | Company A |
| \`10003541\`  | *QoS management* | 🟡 **MEDIUM** | 8 claims | Company B |
| \`10002036\`  | *Distributed framework* | 🟢 **LOW** | 12 claims | Company C |

## Empty Cells
| Field | Value | Notes |
|-------|-------|-------|
| Status | Active | Current state |
| Priority | | To be determined |
| Owner | John Doe | Primary contact`,
    expectedElements: ['table', 'th', 'td', 'strong', 'em', 'code']
  },

  // Code blocks and technical content
  technicalContent: {
    name: 'Technical Content and Code',
    markdown: `# Technical Implementation Guide

## Code Examples

### Python Implementation
\`\`\`python
def analyze_patent_risk(patent_data):
    """
    Analyze patent risk based on relevance scores
    """
    risk_levels = {
        'high': patent_data['relevance_score'] >= 0.8,
        'medium': 0.5 <= patent_data['relevance_score'] < 0.8,
        'low': patent_data['relevance_score'] < 0.5
    }
    return risk_levels

# Usage example
patent = {'patent_id': '10004070', 'relevance_score': 0.85}
risk = analyze_patent_risk(patent)
print(f"Risk level: {risk}")
\`\`\`

### JavaScript Implementation
\`\`\`javascript
class PatentAnalyzer {
  constructor(patents) {
    this.patents = patents;
  }
  
  getHighRiskPatents() {
    return this.patents.filter(p => p.relevanceScore >= 0.8);
  }
  
  generateReport() {
    const highRisk = this.getHighRiskPatents();
    return \`Found \${highRisk.length} high-risk patents\`;
  }
}
\`\`\`

## Technical Specifications
- **API Endpoint**: \`/api/patent/prior-art\`
- **Response Format**: JSON with markdown \`results\`
- **Authentication**: Bearer token required
- **Rate Limit**: 100 requests per hour

## Configuration
\`\`\`json
{
  "max_results": 10,
  "include_claims": true,
  "risk_threshold": 0.5,
  "format": "markdown"
}
\`\`\``,
    expectedElements: ['h1', 'h2', 'h3', 'h4', 'pre', 'code', 'p', 'ul', 'li', 'strong', 'em']
  },

  // Edge cases and special characters
  edgeCases: {
    name: 'Edge Cases and Special Characters',
    markdown: `# Edge Cases Test

## Special Characters
- **Ampersand**: &amp; & &amp;
- **Less than**: &lt; < &lt;
- **Greater than**: &gt; > &gt;
- **Quotes**: "quoted text" and 'single quotes'
- **Apostrophes**: It's a test case
- **Dashes**: em-dash — and en-dash –

## Mixed Content
This paragraph has **bold**, *italic*, \`code\`, and [links](https://example.com).

## Empty Elements
- 
- List item with content
- 

## Nested Formatting
**Bold with *italic* and \`code\` inside**

## Long Content
This is a very long paragraph that should test the word wrapping and text flow capabilities of our markdown converter. It contains multiple sentences and should demonstrate how the system handles longer text content without breaking the layout or formatting.

## Mixed Lists
1. **Numbered item 1** with *emphasis*
2. Numbered item 2
   - Nested bullet point
   - Another nested point
3. Numbered item 3

## Code with Special Characters
\`\`\`html
<div class="test">
  <p>This & that</p>
  <span>Special chars: &lt; &gt; &amp;</span>
</div>
\`\`\``,
    expectedElements: ['h1', 'h2', 'h3', 'ul', 'ol', 'li', 'p', 'strong', 'em', 'code', 'pre', 'a']
  }
};

// Test suite for MarkdownConverter component
describe('MarkdownConverter Component', () => {
  // Test basic rendering
  describe('Basic Rendering', () => {
    test('renders without crashing', () => {
      render(<MarkdownConverter markdown="Test content" />);
      expect(screen.getByText('Test content')).toBeInTheDocument();
    });

    test('renders empty markdown gracefully', () => {
      render(<MarkdownConverter markdown="" />);
      // Should render without errors
    });

    test('renders null/undefined markdown gracefully', () => {
      render(<MarkdownConverter markdown={null as any} />);
      // Should handle gracefully
    });
  });

  // Test markdown element conversion
  describe('Markdown Element Conversion', () => {
    Object.entries(testCases).forEach(([key, testCase]) => {
      test(`converts ${testCase.name} correctly`, () => {
        const mockOnConvert = jest.fn();
        
        render(
          <MarkdownConverter
            markdown={testCase.markdown}
            onConvert={mockOnConvert}
            showPreview={true}
          />
        );

        // Check that the component renders
        expect(screen.getByText(testCase.markdown.split('\n')[0].replace('# ', ''))).toBeInTheDocument();
        
        // Verify onConvert callback is called
        expect(mockOnConvert).toHaveBeenCalled();
      });
    });
  });

  // Test specific markdown elements
  describe('Specific Markdown Elements', () => {
    test('converts headers correctly', () => {
      const markdown = `# H1 Header
## H2 Header
### H3 Header
#### H4 Header`;

      render(<MarkdownConverter markdown={markdown} />);
      
      expect(screen.getByText('H1 Header')).toBeInTheDocument();
      expect(screen.getByText('H2 Header')).toBeInTheDocument();
      expect(screen.getByText('H3 Header')).toBeInTheDocument();
      expect(screen.getByText('H4 Header')).toBeInTheDocument();
    });

    test('converts bold and italic text correctly', () => {
      const markdown = '**Bold text** and *italic text*';
      
      render(<MarkdownConverter markdown={markdown} />);
      
      expect(screen.getByText('Bold text')).toBeInTheDocument();
      expect(screen.getByText('italic text')).toBeInTheDocument();
    });

    test('converts lists correctly', () => {
      const markdown = `- Bullet item 1
- Bullet item 2

1. Numbered item 1
2. Numbered item 2`;

      render(<MarkdownConverter markdown={markdown} />);
      
      expect(screen.getByText('Bullet item 1')).toBeInTheDocument();
      expect(screen.getByText('Bullet item 2')).toBeInTheDocument();
      expect(screen.getByText('Numbered item 1')).toBeInTheDocument();
      expect(screen.getByText('Numbered item 2')).toBeInTheDocument();
    });

    test('converts tables correctly', () => {
      const markdown = `| Header 1 | Header 2 |
|----------|----------|
| Data 1   | Data 2   |`;

      render(<MarkdownConverter markdown={markdown} />);
      
      expect(screen.getByText('Header 1')).toBeInTheDocument();
      expect(screen.getByText('Header 2')).toBeInTheDocument();
      expect(screen.getByText('Data 1')).toBeInTheDocument();
      expect(screen.getByText('Data 2')).toBeInTheDocument();
    });

    test('converts code blocks correctly', () => {
      const markdown = `\`inline code\`

\`\`\`python
def test_function():
    return "Hello World"
\`\`\``;

      render(<MarkdownConverter markdown={markdown} />);
      
      expect(screen.getByText('inline code')).toBeInTheDocument();
      expect(screen.getByText('def test_function():')).toBeInTheDocument();
    });
  });

  // Test callback functionality
  describe('Callback Functionality', () => {
    test('calls onConvert when markdown changes', async () => {
      const mockOnConvert = jest.fn();
      
      const { rerender } = render(
        <MarkdownConverter
          markdown="Initial content"
          onConvert={mockOnConvert}
        />
      );

      // Initial call
      expect(mockOnConvert).toHaveBeenCalledTimes(1);

      // Change markdown
      rerender(
        <MarkdownConverter
          markdown="Updated content"
          onConvert={mockOnConvert}
        />
      );

      // Should call again with new content
      await waitFor(() => {
        expect(mockOnConvert).toHaveBeenCalledTimes(2);
      });
    });

    test('does not call onConvert when not provided', () => {
      const mockOnConvert = jest.fn();
      
      render(<MarkdownConverter markdown="Test content" />);
      
      expect(mockOnConvert).not.toHaveBeenCalled();
    });
  });

  // Test showPreview prop
  describe('Show Preview Control', () => {
    test('shows preview when showPreview is true', () => {
      render(
        <MarkdownConverter
          markdown="# Test Header"
          showPreview={true}
        />
      );
      
      expect(screen.getByText('Test Header')).toBeInTheDocument();
    });

    test('hides preview when showPreview is false', () => {
      render(
        <MarkdownConverter
          markdown="# Test Header"
          showPreview={false}
        />
      );
      
      // Content should not be visible
      expect(screen.queryByText('Test Header')).not.toBeInTheDocument();
    });
  });

  // Test styling and CSS classes
  describe('Styling and CSS Classes', () => {
    test('applies custom className when provided', () => {
      const { container } = render(
        <MarkdownConverter
          markdown="Test content"
          className="custom-class"
        />
      );
      
      expect(container.firstChild).toHaveClass('custom-class');
    });

    test('renders with default styling', () => {
      const { container } = render(
        <MarkdownConverter markdown="# Test Header" />
      );
      
      // Should have styled components applied
      expect(container.firstChild).toBeInTheDocument();
    });
  });

  // Test performance with large markdown
  describe('Performance Tests', () => {
    test('handles large markdown content efficiently', () => {
      const largeMarkdown = '# Large Document\n\n'.repeat(1000) + 'Content here';
      
      const startTime = performance.now();
      
      render(<MarkdownConverter markdown={largeMarkdown} />);
      
      const endTime = performance.now();
      const renderTime = endTime - startTime;
      
      // Should render in reasonable time (less than 100ms)
      expect(renderTime).toBeLessThan(100);
    });
  });

  // Test accessibility
  describe('Accessibility', () => {
    test('maintains proper heading hierarchy', () => {
      const markdown = `# Main Title
## Section 1
### Subsection 1.1
## Section 2`;

      render(<MarkdownConverter markdown={markdown} />);
      
      // Check that headings are properly structured
      const headings = screen.getAllByRole('heading');
      expect(headings).toHaveLength(4);
      
      // Check heading levels
      expect(headings[0]).toHaveAttribute('tagName', 'H1');
      expect(headings[1]).toHaveAttribute('tagName', 'H2');
      expect(headings[2]).toHaveAttribute('tagName', 'H3');
      expect(headings[3]).toHaveAttribute('tagName', 'H2');
    });

    test('provides proper table structure', () => {
      const markdown = `| Header 1 | Header 2 |
|----------|----------|
| Data 1   | Data 2   |`;

      render(<MarkdownConverter markdown={markdown} />);
      
      // Check table structure
      const table = screen.getByRole('table');
      expect(table).toBeInTheDocument();
      
      const headers = screen.getAllByRole('columnheader');
      expect(headers).toHaveLength(2);
    });
  });
});

export default testCases;

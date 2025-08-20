# Markdown to Word Conversion System

## 🎯 Overview

This system converts patent report markdown into professionally formatted HTML that can be directly inserted into Microsoft Word documents. It's designed specifically for patent attorneys and inventors who need to create professional prior art search reports.

## 🚀 Features

### ✅ Core Functionality
- **Markdown Input**: Accepts patent reports in markdown format
- **HTML Conversion**: Converts markdown to professional HTML
- **Word Integration**: Direct insertion into Word documents
- **Professional Styling**: Patent attorney-grade formatting

### 🎨 Styling Features
- **Professional Headers**: Styled with borders and proper spacing
- **Table Formatting**: Clean, professional table layouts
- **Code Blocks**: Syntax-highlighted code sections
- **Lists**: Properly formatted bullet and numbered lists
- **Blockquotes**: Styled quote sections
- **Responsive Design**: Works on all screen sizes

## 📦 Installation

### Prerequisites
- Node.js 16+ 
- npm or yarn
- Microsoft Word (for testing)

### Setup
```bash
# Navigate to the frontend directory
cd word-addin-agent-ui

# Install dependencies
npm install

# Install markdown conversion packages
npm install react-markdown remark-gfm rehype-raw styled-components @types/styled-components
```

## 🏗️ Architecture

### Components
1. **`MarkdownConverter.tsx`** - Core markdown to HTML converter
2. **`WordInsertionUtility.ts`** - Word document integration utility
3. **`PatentReportDemo.tsx`** - Demo component showing usage

### Utilities
- **Markdown Processing**: React-markdown with GFM support
- **HTML Styling**: Styled-components for professional appearance
- **Word Integration**: Office.js API for document manipulation

## 💻 Usage

### Basic Usage

```tsx
import MarkdownConverter from './components/MarkdownConverter';
import WordInsertionUtility from './utils/wordInsertion';

// Initialize Word utility
const wordUtility = WordInsertionUtility.getInstance();
await wordUtility.initialize();

// Convert markdown to HTML
<MarkdownConverter
  markdown={markdownContent}
  onConvert={(html) => console.log('HTML generated:', html)}
  showPreview={true}
/>

// Insert into Word
await wordUtility.insertPatentReport(markdownContent, {
  position: 'cursor',
  preserveFormatting: true,
  addPageBreak: true
});
```

### Advanced Usage

```tsx
// Custom styling options
const customComponents = {
  h1: ({ children, ...props }) => (
    <h1 {...props} style={{ color: '#custom-color' }}>
      {children}
    </h1>
  ),
  table: ({ children, ...props }) => (
    <table {...props} style={{ customTableStyle: true }}>
      {children}
    </table>
  )
};

<MarkdownConverter
  markdown={markdownContent}
  components={customComponents}
  onConvert={handleHtmlConvert}
/>
```

## 🎨 Customization

### Styling
The system uses styled-components for styling. You can customize:

```tsx
// Custom color scheme
const CustomStyledMarkdown = styled.div`
  h1 {
    color: #your-brand-color;
    border-bottom: 3px solid #your-accent-color;
  }
  
  table {
    background-color: #your-table-bg;
    border-color: #your-border-color;
  }
`;
```

### Word Integration Options
```tsx
interface WordInsertionOptions {
  position?: 'start' | 'end' | 'cursor';
  preserveFormatting?: boolean;
  insertAsHtml?: boolean;
  addPageBreak?: boolean;
}
```

## 📋 Supported Markdown

### Headers
```markdown
# H1 Header
## H2 Header
### H3 Header
#### H4 Header
```

### Text Formatting
```markdown
**Bold text**
*Italic text*
`inline code`
```

### Lists
```markdown
- Bullet item 1
- Bullet item 2

1. Numbered item 1
2. Numbered item 2
```

### Tables
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |
```

### Code Blocks
```markdown
```python
def hello_world():
    print("Hello, World!")
```
```

### Links
```markdown
[Link Text](https://example.com)
```

## 🔧 Configuration

### Environment Variables
```bash
# Word Add-in configuration
REACT_APP_WORD_ADDIN_ID=your-addin-id
REACT_APP_OFFICE_VERSION=1.1
```

### Webpack Configuration
```javascript
// webpack.config.js
module.exports = {
  resolve: {
    extensions: ['.ts', '.tsx', '.js', '.jsx'],
    alias: {
      '@components': path.resolve(__dirname, 'src/components'),
      '@utils': path.resolve(__dirname, 'src/utils')
    }
  }
};
```

## 🧪 Testing

### Unit Tests
```bash
npm test
npm run test:watch
```

### Integration Tests
```bash
# Test Word integration
npm run test:integration

# Test markdown conversion
npm run test:markdown
```

### Manual Testing
1. Start the development server: `npm run dev-server`
2. Open in Word (using Office Add-in debugging)
3. Test markdown input and conversion
4. Test Word insertion

## 🚨 Troubleshooting

### Common Issues

#### Word Integration Not Working
```bash
# Check Office.js version
npm list @types/office-js

# Ensure Word is running
# Check browser console for errors
```

#### Markdown Not Converting
```bash
# Check package installation
npm list react-markdown

# Verify markdown syntax
# Check browser console for errors
```

#### Styling Issues
```bash
# Check styled-components installation
npm list styled-components

# Verify CSS is loading
# Check browser developer tools
```

### Debug Mode
```typescript
// Enable debug logging
const wordUtility = WordInsertionUtility.getInstance();
wordUtility.setDebugMode(true);
```

## 📚 API Reference

### MarkdownConverter Props
```tsx
interface MarkdownConverterProps {
  markdown: string;           // Markdown content to convert
  onConvert?: (html: string) => void;  // Callback for HTML output
  showPreview?: boolean;      // Show HTML preview
  className?: string;         // CSS class name
}
```

### WordInsertionUtility Methods
```tsx
class WordInsertionUtility {
  // Initialize Word integration
  async initialize(): Promise<void>
  
  // Insert HTML content
  async insertHtml(html: string, options?: WordInsertionOptions): Promise<void>
  
  // Insert patent report
  async insertPatentReport(markdown: string, options?: WordInsertionOptions): Promise<void>
  
  // Get document statistics
  async getDocumentStats(): Promise<DocumentStats>
}
```

## 🔄 Updates and Maintenance

### Version Updates
```bash
# Update dependencies
npm update

# Update specific packages
npm install react-markdown@latest
npm install styled-components@latest
```

### Security Updates
```bash
# Check for vulnerabilities
npm audit

# Fix vulnerabilities
npm audit fix
```

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Style
- Use TypeScript for all new code
- Follow React best practices
- Use styled-components for styling
- Add JSDoc comments for complex functions

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Getting Help
- Check the troubleshooting section
- Review the API reference
- Search existing issues
- Create a new issue with detailed information

### Contact
- **Issues**: GitHub Issues
- **Documentation**: This README
- **Examples**: See `PatentReportDemo.tsx`

---

## 🎉 Quick Start

1. **Install**: `npm install`
2. **Import**: `import MarkdownConverter from './components/MarkdownConverter'`
3. **Use**: `<MarkdownConverter markdown={content} onConvert={handleHtml} />`
4. **Insert**: `await wordUtility.insertPatentReport(markdownContent)`

**That's it!** Your markdown is now professionally formatted HTML ready for Word insertion.

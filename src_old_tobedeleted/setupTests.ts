import '@testing-library/jest-dom';

// Mock Office.js
(window as any).Office = {
  context: {
    document: {
      body: {
        text: 'Mock document content',
        paragraphs: {
          items: [
            { text: 'Paragraph 1' },
            { text: 'Paragraph 2' }
          ]
        }
      },
      getSelection: () => ({
        text: 'Mock selection',
        start: 0,
        end: 10
      }),
      settings: {
        get: () => 'Mock setting',
        set: () => {}
      }
    }
  },
  onReady: (callback: any) => callback({ host: 'Document' }),
  HostType: {
    Document: 'Document'
  }
} as any;

// Mock Word.js
(window as any).Word = {
  run: async (callback: any) => {
    const context = {
      document: {
        body: {
          text: 'Mock document content',
          paragraphs: {
            items: [
              { text: 'Paragraph 1' },
              { text: 'Paragraph 2' }
            ]
          },
          load: () => {},
          insertParagraph: () => ({})
        },
        getSelection: () => ({
          text: 'Mock selection',
          start: 0,
          end: 10,
          load: () => {},
          insertText: () => {},
          delete: () => {}
        })
      },
      sync: async () => {}
    };
    await callback(context);
  }
} as any;

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
  writable: true
});

// Mock fetch
Object.defineProperty(window, 'fetch', {
  value: jest.fn(),
  writable: true
});

// Mock console methods to reduce noise in tests
const originalConsole = { ...console };
Object.defineProperty(window, 'console', {
  value: {
    ...originalConsole,
    warn: jest.fn(),
    error: jest.fn(),
  },
  writable: true
});

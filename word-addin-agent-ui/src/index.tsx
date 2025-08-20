import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/global.css';
import { initializeOffice } from './office-init';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

// Initialize Office.js before rendering the app
initializeOffice({
  onReady: () => {
    console.log('Office.js initialized successfully');
    // Render the app after Office.js is ready
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
  },
  onError: (error) => {
    console.error('Office.js initialization failed:', error);
    // Render the app anyway for development
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
  }
});

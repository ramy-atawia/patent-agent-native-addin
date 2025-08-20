import React, { useState, useRef, useEffect } from 'react';
import './LoginForm.css';

export const LoginForm: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);

  const openLoginDialog = async () => {
    try {
      setIsLoading(true);
      const dialogUrl = `${window.location.origin}/login-dialog.html`;
      const popup = window.open(dialogUrl, 'auth', 'width=600,height=700');
      setIsLoading(false);
    } catch (error) {
      console.error('Failed to open login dialog:', error);
      setIsLoading(false);
    }
  };

  return (
    <div className="login-form-container">
      <div className="login-header">
        <div className="header-logo-container">
          <img 
            src="/assets/novitai-logo.png" 
            alt="Novitai Logo" 
            className="header-logo large"
          />
        </div>
        <div className="header-text">
          <h2>Welcome to Novitai Patent Assistant</h2>
          <p>Your AI-powered patent drafting companion</p>
        </div>
      </div>
      
      <div className="login-description">
        <h3>What you can do:</h3>
        <ul>
          <li>Generate comprehensive patent claims using AI</li>
          <li>Search and analyze prior art efficiently</li>
          <li>Create professional patent reports</li>
          <li>Get intelligent drafting suggestions</li>
          <li>Export content directly to Word documents</li>
        </ul>
      </div>
      
      <div className="login-form">
        <button 
          onClick={openLoginDialog}
          className="login-button primary"
          disabled={isLoading}
        >
          {isLoading ? 'Opening login...' : 'Sign In with Auth0'}
        </button>
      </div>
      
      <div className="login-footer">
        <p>Secure authentication powered by Auth0</p>
        <p>Your data is protected and never shared</p>
      </div>
    </div>
  );
};

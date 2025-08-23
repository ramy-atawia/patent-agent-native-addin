import React, { useState, useRef, useEffect } from 'react';
import './LoginForm.css';

export const LoginForm: React.FC = () => {
  // Login handled entirely via Office dialog/popup in this simplified flow
  const [isLoading, setIsLoading] = useState(false);

  const openLoginDialog = async () => {
    try {
      setIsLoading(true);
      // If running inside Office with the dialog API, prefer the dialog (popup) flow
      const officeUi = (window as any).Office && (window as any).Office.context && (window as any).Office.context.ui;

      // Fallback to dialog-based flow (legacy)
      const dialogUrl = `${window.location.origin}/login-dialog.html`;

      if (officeUi && typeof officeUi.displayDialogAsync === 'function') {
        (window as any).Office.context.ui.displayDialogAsync(
          dialogUrl,
          { height: 60, width: 35, displayInIframe: false },
          (result: any) => {
            if (result.status === (window as any).Office.AsyncResultStatus.Failed) {
              console.error('Dialog failed to open:', result.error && result.error.message);
              setIsLoading(false);
              return;
            }

            const dialog = result.value;
            dialog.addEventHandler((window as any).Office.EventType.DialogMessageReceived, (arg: any) => {
              try {
                const msg = JSON.parse(arg.message);
                if (msg.type === 'auth-success') {
                  // Dispatch tokens via a custom event to avoid using browser storage (artifacts environment)
                  try {
                    const ev = new CustomEvent('auth-tokens', { detail: { accessToken: msg.accessToken || null, idToken: msg.idToken || null, userProfile: msg.userProfile || null } });
                    window.dispatchEvent(ev);
                  } catch (e) { console.warn('Failed to dispatch auth-tokens event', e); }

                  dialog.close();
                  setIsLoading(false);
                } else if (msg.type === 'auth-error') {
                  console.error('Auth error from dialog:', msg.error);
                  dialog.close();
                  setIsLoading(false);
                }
              } catch (e) {
                console.error('Invalid message from dialog:', e);
              }
            });

            dialog.addEventHandler((window as any).Office.EventType.DialogEventReceived, (evt: any) => {
              console.warn('Dialog closed or error:', evt);
              setIsLoading(false);
            });
          }
        );
      } else {
        const popup = window.open(dialogUrl, 'auth', 'width=600,height=700');
        const handler = (event: MessageEvent) => {
          try {
            const msg = typeof event.data === 'string' ? JSON.parse(event.data) : event.data;
            if (msg && msg.type === 'auth-success') {
              try {
                const ev = new CustomEvent('auth-tokens', { detail: { accessToken: msg.accessToken || null, idToken: msg.idToken || null, userProfile: msg.userProfile || null } });
                window.dispatchEvent(ev);
              } catch (e) { console.warn('Failed to dispatch auth-tokens event', e); }

              setIsLoading(false);
              window.removeEventListener('message', handler);
              if (popup) popup.close();
            } else if (msg && msg.type === 'auth-error') {
              console.error('Auth error from popup:', msg.error);
              setIsLoading(false);
              window.removeEventListener('message', handler);
            }
          } catch (e) {
            console.error('Invalid message from popup:', e);
          }
        };
        window.addEventListener('message', handler);
        handlerRef.current = handler; // keep reference for cleanup
      }
    } catch (error) {
      console.error('Failed to open login dialog:', error);
      setIsLoading(false);
    }
  };

  // Keep a ref to the message handler so we can remove it if component unmounts
  const handlerRef = useRef<((e: MessageEvent) => void) | null>(null);

  useEffect(() => {
    return () => {
      // cleanup any leftover message handler
      try {
        if (handlerRef.current) {
          window.removeEventListener('message', handlerRef.current);
          handlerRef.current = null;
        }
      } catch (e) {}
    };
  }, []);

  return (
    <div className="login-form-container">
      <div className="login-header">
        <div style={{display: 'flex', alignItems: 'center', gap: '16px'}}>
          <div className="header-logo-container" style={{margin: 0}}>
            <img 
              src="/assets/novitai-logo.png" 
              alt="Novitai" 
              className="header-logo large"
            />
          </div>
          <div className="header-text">
            <h2>Welcome</h2>
          </div>
        </div>
      </div>

      <div className="login-description">
        <h3>AI Patent Agent</h3>
        <ul>
          <li>End‑to‑end patent workflow — disclosure to filing‑ready application</li>
          <li>Domain‑aware claim generation &amp; review</li>
          <li>Conversational drafting that captures user preferences</li>
          <li>Patent figure &amp; drawing assistance — generate compliant figures, callouts, and labels suitable for filings</li>
        </ul>
      </div>

      <div className="login-form">
        <button 
          onClick={openLoginDialog}
          className="login-button primary"
          disabled={isLoading}
        >
          {isLoading ? 'Opening login...' : 'Sign In'}
        </button>
      </div>

      <div className="login-footer">
        <p>This add-in requires authentication to access Novitai's backend services.</p>
        <p>Contact your administrator for API credentials and setup instructions.</p>
      </div>
    </div>
  );
};

/**
 * Office.js initialization and configuration
 * Follows Microsoft's best practices for Office Add-ins
 */

declare global {
    interface Window {
      Office: any;
      Word: any;
      wordJsReady?: boolean;
    }
  }
  
  export interface OfficeInitializationOptions {
    onReady?: () => void;
    onError?: (error: Error) => void;
  }
  
  /**
   * Initialize Office.js with proper error handling
   */
  export function initializeOffice(options: OfficeInitializationOptions = {}): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        // If Office.js object exists, wait for Office.onReady instead of resolving immediately
        if (window.Office && typeof window.Office.onReady === 'function') {
          console.log('Office.js object detected, waiting for Office.onReady');
          try {
            window.Office.onReady((info: any) => {
              console.log('Office.onReady fired (pre-existing):', info);
              
              // Initialize Word.js after Office.js is ready
              if (info.host === window.Office.HostType.Word) {
                initializeWord().then(() => {
                  if (options.onReady) options.onReady();
                  resolve();
                }).catch((wordError) => {
                  console.warn('Word.js initialization failed, but continuing:', wordError);
                  if (options.onReady) options.onReady();
                  resolve();
                });
              } else {
                console.warn('Not in Word, but continuing for development');
                if (options.onReady) options.onReady();
                resolve();
              }
            });
            return;
          } catch (err) {
            console.warn('Office.onReady invocation failed, proceeding to load script', err);
          }
        }

        // If Office.js is not loaded, load it first
        if (!window.Office) {
          console.log('Office.js not detected, loading...');
          const script = document.createElement('script');
          script.src = 'https://appsforoffice.microsoft.com/lib/1/hosted/office.js';
          script.type = 'text/javascript';
          
          script.onload = () => {
            console.log('Office.js loaded successfully');
            // Now wait for Office.onReady
            window.Office.onReady((info: any) => {
              console.log('Office.js ready:', info);
              
              if (info.host === window.Office.HostType.Word) {
                console.log('Running in Word environment');
                
                initializeWord().then(() => {
                  if (options.onReady) options.onReady();
                  resolve();
                }).catch((wordError) => {
                  console.warn('Word.js initialization failed, but continuing:', wordError);
                  if (options.onReady) options.onReady();
                  resolve();
                });
              } else {
                console.warn('Not running in Word environment, but continuing for development...');
                if (options.onReady) options.onReady();
                resolve();
              }
            });
          };
          
          script.onerror = (error) => {
            console.error('Failed to load Office.js:', error);
            console.warn('Continuing without Office.js for development...');
            if (options.onReady) options.onReady();
            resolve();
          };
          
          document.head.appendChild(script);
        }
  
        // Office.js loading is now handled above
        
      } catch (error) {
        console.error('Error initializing Office.js:', error);
        if (options.onError) options.onError(error as Error);
        reject(error);
      }
    });
  }
  
  /**
   * Initialize Word-specific functionality with simpler verification
   */
  async function initializeWord(): Promise<void> {
    try {
      console.log('Starting Word.js initialization...');
      
      // Wait for Word library with shorter timeout
      const waitForWordLibrary = async (maxWaitMs = 3000): Promise<boolean> => {
        const startTime = Date.now();
        const interval = 100;
        
        while (Date.now() - startTime < maxWaitMs) {
          if (typeof window.Word !== 'undefined') {
            console.log('Word library detected');
            return true;
          }
          await new Promise(r => setTimeout(r, interval));
        }
        
        console.warn('Word library not available after', maxWaitMs, 'ms');
        return false;
      };

      const isWordAvailable = await waitForWordLibrary();
      if (!isWordAvailable) {
        console.warn('Word.js not available - document features will be disabled');
        window.wordJsReady = false;
        return;
      }

      // Simple existence check - don't try to run anything during initialization
      if (typeof window.Word.run === 'function') {
        window.wordJsReady = true;
        console.log('Word.js initialization completed successfully');
      } else {
        console.warn('Word.run not available - document features disabled');
        window.wordJsReady = false;
      }
      
    } catch (error) {
      console.error('Error in Word.js initialization:', error);
      window.wordJsReady = false;
    }
  }
  
  /**
   * Check if Office.js is ready
   */
  export function isOfficeReady(): boolean {
    const ready = !!(window.Office && window.Office.context);
    console.log('isOfficeReady:', ready);
    return ready;
  }
  
  /**
   * Check if running in Word
   */
  export function isWordHost(): boolean {
    const inWord = isOfficeReady() && 
      window.Office.context.host === window.Office.HostType.Word;
    console.log('isWordHost:', inWord);
    return inWord;
  }
  
  /**
   * Check if Word.js is ready and available
   */
  export function isWordJsReady(): boolean {
    const ready = !!(window.Word && window.wordJsReady === true);
    console.log('isWordJsReady:', ready, { 
      wordExists: !!window.Word, 
      wordJsReady: window.wordJsReady 
    });
    return ready;
  }
  
  /**
   * Wait for Word.js to be ready with timeout
   */
  export function waitForWordJs(timeoutMs = 30000): Promise<void> {
    return new Promise((resolve, reject) => {
      console.log('waitForWordJs: Starting wait...');
      
      if (isWordJsReady()) {
        console.log('waitForWordJs: Already ready');
        resolve();
        return;
      }
  
      const startTime = Date.now();
      const checkInterval = 250;
      
      const timeout = setTimeout(() => {
        console.log('waitForWordJs: Timeout after', timeoutMs, 'ms');
        reject(new Error(`Word.js initialization timeout after ${timeoutMs}ms`));
      }, timeoutMs);
  
      const check = () => {
        const elapsed = Date.now() - startTime;
        console.log(`waitForWordJs: Checking... (${elapsed}ms elapsed)`);
        
        if (isWordJsReady()) {
          clearTimeout(timeout);
          console.log('waitForWordJs: Ready!');
          resolve();
          return;
        }
        
        if (elapsed < timeoutMs) {
          setTimeout(check, checkInterval);
        }
      };
  
      // Start checking
      setTimeout(check, checkInterval);
    });
  }
  
  /**
   * Get Office.js version information
   */
  export function getOfficeVersion(): string | null {
    if (window.Office && window.Office.context) {
      return window.Office.context.document?.settings?.get('Office.Version') || 'Unknown';
    }
    return null;
  }
  
  /**
   * Enable Office.js debugging
   */
  export function enableOfficeDebugging(): void {
    if (window.Office && window.Office.context) {
      try {
        window.Office.context.document.settings.set('Office.Debug', true);
        console.log('Office.js debugging enabled');
      } catch (error) {
        console.warn('Could not enable Office.js debugging:', error);
      }
    }
  }
  
  /**
   * Disable Office.js debugging
   */
  export function disableOfficeDebugging(): void {
    if (window.Office && window.Office.context) {
      try {
        window.Office.context.document.settings.set('Office.Debug', false);
        console.log('Office.js debugging disabled');
      } catch (error) {
        console.warn('Could not disable Office.js debugging:', error);
      }
    }
  }

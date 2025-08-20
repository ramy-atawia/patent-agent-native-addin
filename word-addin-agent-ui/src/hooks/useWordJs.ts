import { useState, useEffect } from 'react';
import { isWordJsReady, waitForWordJs, isOfficeReady, isWordHost } from '../office-init';

export interface UseWordJsReturn {
  isReady: boolean;
  isLoading: boolean;
  error: string | null;
  execute: <T>(operation: () => Promise<T>) => Promise<T | null>;
}

/**
 * Custom hook for safely using Word.js functionality
 * Ensures Word.js is properly initialized before executing operations
 */
export function useWordJs(): UseWordJsReturn {
  const [isReady, setIsReady] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    let timeoutId: NodeJS.Timeout | null = null; // Initialize as null

    const initializeWordJs = async () => {
      try {
        console.log('useWordJs: Starting initialization...');
        setIsLoading(true);
        setError(null);

        // First check if Office.js is ready
        if (!isOfficeReady()) {
          console.log('useWordJs: Office.js not ready, waiting...');
          
          // Wait up to 5 seconds for Office.js
          let attempts = 0;
          const maxAttempts = 20; // 20 * 250ms = 5 seconds
          
          while (attempts < maxAttempts && !isOfficeReady() && mounted) {
            await new Promise(resolve => setTimeout(resolve, 250));
            attempts++;
          }
          
          if (!mounted) return;
          
          if (!isOfficeReady()) {
            throw new Error('Office.js failed to initialize within 5 seconds');
          }
        }

        // Check if we're in Word
        if (!isWordHost()) {
          console.warn('useWordJs: Not running in Word - continuing in development mode');
          // Don't throw error in development - just set not ready
          setIsReady(false);
          setError('Word environment not detected - running in development mode');
          return;
        }

        // Wait for Word.js with shorter timeout
        try {
          await waitForWordJs(5000); // 5 second timeout
          if (mounted) {
            setIsReady(true);
            setError(null);
          }
        } catch (timeoutError) {
          console.warn('useWordJs: Word.js timeout - continuing in development mode');
          if (mounted) {
            setIsReady(false);
            setError('Word.js timeout - running in development mode');
          }
          return;
        }

      } catch (err) {
        console.error('useWordJs: Initialization error:', err);
        if (mounted) {
          setError(err instanceof Error ? err.message : 'Initialization failed');
          setIsReady(false);
        }
      } finally {
        if (mounted) {
          setIsLoading(false);
        }
      }
    };

    initializeWordJs();

    return () => {
      mounted = false;
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, []);

  /**
   * Execute a Word.js operation safely
   */
  const execute = async <T>(operation: () => Promise<T>): Promise<T | null> => {
    if (!isReady) {
      const errorMsg = error || 'Word.js is not ready';
      setError(errorMsg);
      console.warn('useWordJs: Operation attempted but Word.js not ready:', errorMsg);
      return null;
    }

    try {
      setError(null);
      const result = await operation();
      console.log('useWordJs: Operation completed successfully');
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Operation failed';
      setError(errorMessage);
      console.error('Word.js operation failed:', err);
      return null;
    }
  };

  // Debug logging
  useEffect(() => {
    console.log('useWordJs state update:', { isReady, isLoading, error });
  }, [isReady, isLoading, error]);

  return {
    isReady,
    isLoading,
    error,
    execute,
  };
}

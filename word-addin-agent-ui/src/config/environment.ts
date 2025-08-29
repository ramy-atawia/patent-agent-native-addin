// Environment configuration for the browser
// This file provides environment variables that work in the browser context

interface EnvironmentConfig {
  API_URL: string;
  NODE_ENV: string;
}

// Get environment variables from window object or use defaults
const getEnvironmentConfig = (): EnvironmentConfig => {
  // Check if we're in development mode
  const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  
  return {
    API_URL: isDevelopment ? 'http://localhost:8001' : 'https://your-production-api.com',
    NODE_ENV: isDevelopment ? 'development' : 'production',
  };
};

export const env = getEnvironmentConfig();

// Export individual values for convenience
export const API_URL = env.API_URL;
export const NODE_ENV = env.NODE_ENV;

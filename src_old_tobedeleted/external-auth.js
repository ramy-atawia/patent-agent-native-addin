// Auth0 configuration
const auth0Config = {
  // Realistic values copied from the original myword-addin
  domain: "dev-bktskx5kbc655wcl.us.auth0.com",
  clientId: "INws849yDXaC6MZVXnLhMJi6CZC4nx6U",
  // Use the callback path used across the UI bundle
  redirectUri: "https://localhost:3000/auth-callback.html",
  scope: "openid profile email",
  cacheLocation: "memory",
  useRefreshTokens: true,
};



// Dialog instance
let dialog = null;

// Login function - opens the Auth0 login dialog
function login() {
  // Calculate dialog dimensions
  const dialogWidth = 35;
  const dialogHeight = 45;
  
  // Open a dialog that will handle the Auth0 login
  // Use a complete URL rather than a relative path
  const dialogUrl = window.location.origin + window.location.pathname.substring(0, window.location.pathname.lastIndexOf('/')) + '/login-dialog.html';
  
  Office.context.ui.displayDialogAsync(
      dialogUrl,
      { height: dialogHeight, width: dialogWidth, displayInIframe: false },
      function(result) {
          if (result.status === Office.AsyncResultStatus.Failed) {
              console.error("Dialog failed to open: " + result.error.message);
          } else {
              dialog = result.value;
              
              // Event handler for messages from the dialog
              dialog.addEventHandler(Office.EventType.DialogMessageReceived, processDialogMessage);
              
              // Event handler for dialog close event
              dialog.addEventHandler(Office.EventType.DialogEventReceived, processDialogClosed);
          }
      }
  );
}

// Process messages sent from the dialog
function processDialogMessage(arg) {
  try {
      const messageFromDialog = JSON.parse(arg.message);
      
      // Check the message type
      if (messageFromDialog.type === "auth-success") {
          try {
              const ev = new CustomEvent('auth-tokens', { detail: { accessToken: messageFromDialog.accessToken || null, idToken: messageFromDialog.idToken || null, userProfile: messageFromDialog.userProfile || null } });
              window.dispatchEvent(ev);
          } catch (e) { console.warn('Failed to dispatch auth-tokens event', e); }
          
          // Close the dialog
          if (dialog) {
              dialog.close();
              dialog = null;
          }
      } else if (messageFromDialog.type === "auth-error") {
          console.error("Authentication error: " + messageFromDialog.error);
          
          // Close the dialog
          if (dialog) {
              dialog.close();
              dialog = null;
          }
      }
  } catch (error) {
      console.error("Error processing message: " + error);
  }
}

// Handle dialog closed event
function processDialogClosed(arg) {
  dialog = null;
}

// Logout function
function logout() {
  // Clear the auth tokens from session storage
  try { window.dispatchEvent(new CustomEvent('auth-tokens', { detail: { accessToken: null, idToken: null, userProfile: null } })); } catch (e) { console.warn('Failed to clear auth tokens via event', e); }
  // Show login UI
  showLoginUI();
}

// expose for imports
if (typeof module !== 'undefined' && module.exports) {
  module.exports = auth0Config;
}
if (typeof window !== 'undefined') {
  window.__AUTH0_CONFIG__ = auth0Config;
}

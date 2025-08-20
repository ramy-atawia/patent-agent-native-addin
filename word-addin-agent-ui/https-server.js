const https = require('https');
const fs = require('fs');
const path = require('path');

// SSL certificate files
const options = {
  key: fs.readFileSync('./ssl/key.pem'),
  cert: fs.readFileSync('./ssl/cert.pem'),
};

// Create HTTPS server
const server = https.createServer(options, (req, res) => {
  let filePath = req.url === '/' ? '/index.html' : req.url;
  filePath = path.join(__dirname, 'dist', filePath);
  
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }
  
  // Read and serve files
  fs.readFile(filePath, (err, data) => {
    if (err) {
      if (err.code === 'ENOENT') {
        // File not found, serve index.html for SPA routing
        fs.readFile(path.join(__dirname, 'dist', 'index.html'), (err, data) => {
          if (err) {
            res.writeHead(500);
            res.end('Error loading index.html');
          } else {
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(data);
          }
        });
      } else {
        res.writeHead(500);
        res.end('Server error');
      }
    } else {
      // Determine content type
      const ext = path.extname(filePath);
      let contentType = 'text/plain';
      
      switch (ext) {
        case '.html':
          contentType = 'text/html';
          break;
        case '.js':
          contentType = 'application/javascript';
          break;
        case '.css':
          contentType = 'text/css';
          break;
        case '.png':
          contentType = 'image/png';
          break;
        case '.xml':
          contentType = 'application/xml';
          break;
      }
      
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(data);
    }
  });
});

const PORT = 3000;

server.listen(PORT, () => {
  console.log(`🚀 HTTPS Server running on https://localhost:${PORT}`);
  console.log(`📁 Serving files from: ${path.join(__dirname, 'dist')}`);
  console.log(`🔐 SSL Certificate: ${path.join(__dirname, 'ssl')}`);
  console.log(`📱 Frontend: https://localhost:${PORT}`);
  console.log(`📋 Commands: https://localhost:${PORT}/commands.html`);
  console.log(`📄 Manifest: https://localhost:${PORT}/manifest.xml`);
  console.log('');
  console.log('⚠️  Note: This is a self-signed certificate.');
  console.log('   You may see a security warning in your browser.');
  console.log('   Click "Advanced" → "Proceed to localhost (unsafe)" to continue.');
  console.log('');
  console.log('Press Ctrl+C to stop the server');
});

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n🛑 Shutting down HTTPS server...');
  server.close(() => {
    console.log('✅ Server stopped');
    process.exit(0);
  });
});

# 🚀 Patent Drafting Agent - Automation Guide

This guide covers all the automation options for running the Patent Drafting Agent system.

## 📋 **Available Automation Options**

### 1. **Bash Scripts (Recommended for Development)**
- **`./start-all.sh`** - Start both backend and frontend servers
- **`./stop-all.sh`** - Stop both servers
- **`./restart-all.sh`** - Restart both servers
- **`./quick-test.sh`** - Quick health check of both servers

### 2. **Makefile Commands**
- **`make start`** - Start both servers
- **`make stop`** - Stop both servers
- **`make restart`** - Restart both servers
- **`make status`** - Show server status
- **`make logs`** - Show real-time logs
- **`make clean`** - Clean up log files
- **`make dev`** - Quick development start

### 3. **Docker Compose (Production Ready)**
- **`docker-compose up -d`** - Start all services
- **`docker-compose down`** - Stop all services
- **`docker-compose build`** - Build Docker images

## 🎯 **Quick Start Guide**

### **Option 1: One-Command Start (Easiest)**
```bash
# From the agentic-native-drafting directory
./start-all.sh
```

### **Option 2: Make Commands**
```bash
# Start everything
make start

# Check status
make status

# View logs
make logs

# Stop everything
make stop
```

### **Option 3: Docker (Production)**
```bash
# Start with Docker
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 🔧 **What Each Script Does**

### **`start-all.sh`**
1. ✅ Checks and creates virtual environment
2. ✅ Installs missing dependencies
3. ✅ Copies environment variables
4. ✅ Starts backend server (port 8000)
5. ✅ Starts frontend server (port 3000)
6. ✅ Waits for both servers to be ready
7. ✅ Shows real-time logs

### **`stop-all.sh`**
1. 🛑 Stops backend server
2. 🛑 Stops frontend server
3. 🧹 Cleans up PID files

### **`restart-all.sh`**
1. 🛑 Stops existing servers
2. ⏳ Waits 3 seconds
3. 🚀 Starts servers again

## 📊 **Monitoring & Debugging**

### **Check Server Status**
```bash
./quick-test.sh
# or
make status
```

### **View Real-Time Logs**
```bash
make logs
# or
tail -f backend.log frontend.log
```

### **Individual Server Logs**
```bash
# Backend logs
tail -f backend.log

# Frontend logs
tail -f frontend.log
```

## 🐳 **Docker Deployment**

### **Build Images**
```bash
docker-compose build
```

### **Start Services**
```bash
docker-compose up -d
```

### **Production with Nginx**
```bash
docker-compose --profile production up -d
```

## 🚨 **Troubleshooting**

### **Port Already in Use**
```bash
# Check what's using the port
lsof -i :8000
lsof -i :3000

# Kill processes
./stop-all.sh
```

### **Dependencies Missing**
```bash
# Install backend dependencies
source .venv/bin/activate
pip install -r agentic_native_drafting/requirements.txt

# Install frontend dependencies
cd word-addin-agent-ui
npm install
```

### **Environment Variables**
```bash
# Check if .env exists
ls -la .env

# Copy from subdirectory if needed
cp agentic_native_drafting/.env .
```

## 📁 **File Structure**
```
agentic-native-drafting/
├── start-all.sh          # 🚀 Start everything
├── stop-all.sh           # 🛑 Stop everything
├── restart-all.sh        # 🔄 Restart everything
├── quick-test.sh         # 🧪 Quick health check
├── Makefile              # 🛠️  Make commands
├── docker-compose.yml    # 🐳 Docker setup
├── Dockerfile.backend    # 🐳 Backend container
├── .env                  # 🔐 Environment variables
├── .venv/                # 🐍 Python virtual environment
├── agentic_native_drafting/  # 🔧 Backend source
└── word-addin-agent-ui/      # 🎨 Frontend source
```

## 🎉 **Success Indicators**

When everything is working correctly, you should see:

### **Backend (Port 8000)**
```json
{
  "service": "Simple Patent Drafting Service",
  "version": "1.0",
  "functions": ["draft_claims", "general_conversation"],
  "status": "operational"
}
```

### **Frontend (Port 3000)**
- HTML page loads without errors
- No console errors in browser dev tools

## 🔄 **Development Workflow**

1. **Start Development Environment**
   ```bash
   make dev
   ```

2. **Make Changes** to your code

3. **View Logs** in real-time
   ```bash
   make logs
   ```

4. **Restart When Needed**
   ```bash
   make restart
   ```

5. **Stop Everything**
   ```bash
   make stop
   ```

## 🚀 **Next Steps**

1. **Test the Integration**: Open http://localhost:3000 in your browser
2. **Check Backend API**: Visit http://localhost:8000
3. **View Logs**: Use `make logs` to monitor both servers
4. **Deploy to Production**: Use Docker Compose for production deployment

---

**🎯 Pro Tip**: Use `make help` to see all available commands!

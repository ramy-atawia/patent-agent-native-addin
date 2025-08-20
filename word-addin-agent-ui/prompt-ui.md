I need a word addin for patnet drafting agetn .. 
* primarily a chatbot 
* connected to backedn llm ai agent (via REST API)
* connected to the word doc content (takes the content of word doc, proces it and sends it tot eh backedn via REST API)
* recieved REST API response  (JSON) from backend and shows it in the chatbot
* allwos the user to click on a button and insert the chatbot AI repsonse tot he word doc
* the chatbot output will contain main content and also some supporting outut (reasoning/thouhgt) in a different color and font that could also be colloabsed
* the AI backend output can be also result in changing the words and paragphs in te open word doc (with track changes eabled and add revirw comments)

You are an experienced full stack architect and developer with experience in AI, LLM, patent drafting and OFFICE Java script, your task is to:
1) design and architect an office word addin with the above requirements
2) define repo structure
3) implement and code ALL the functions in a modular and efficient way, without complicating the logic
4) follow the office JS API scheme
5) define test cases for functionalities tests and regression
6) do no make any assumptions, and ask questions to me if you find something not clear
7) moving/insering test from chatbout output to word shall be formated
8) authenticate via auth api bearer token stored in ur local storage when theuser logs in and retrieved during calling backend
9) sotres the conv jistory of current sessions (input to the backend api and output response) and sends it in future api requesys
10) the output of backend is trramled in realtime to frontend
11) Please refer to other fodler in this directory to understand more regarding frontend redirect and authtneication and brand name .. etc.
12) While the UI is waiting for  backend response, display a loadig/typing message until backend starts streaming
13) memory-efficient conversation management system
14) Track changrs might replace specific words, adds new words or paragorahs, deletes workd or paragraphs, while 
perserving formating

user Webpack for bundling
Office.js API Integration Pattern --> use Separate Word API services as a service layer decoipled from REACT


please agree with backend first on the API and highglit if there is any gap or overlap

in mvp, act as mcp client

Clear Recommendation: Server-Sent Events (SSE)
Based on your specific requirements, SSE is definitively the better choice. Here's why:
🎯 Perfect Match for Your Use Case:
Your streaming needs are 100% unidirectional:

AI responses → Frontend ✅
Document changes → Frontend ✅
Reasoning updates → Frontend ✅
Error notifications → Frontend ✅

You don't need bidirectional communication, which is WebSocket's main advantage.
🏢 Corporate Environment Reality:
Many patent law firms and corporate environments have:

Strict firewall policies that block WebSocket
HTTP proxies that SSE handles seamlessly
Security policies favoring standard HTTP protocols

💡 Implementation Simplicity:
SSE (Simple):
typescript// Just 10 lines for basic streaming!
const eventSource = new EventSource('/api/chat/stream');
eventSource.onmessage = (event) => {
  updateChatUI(JSON.parse(event.data));
};
// Automatic reconnection built-in!
WebSocket (Complex):
typescript// 50+ lines needed for proper error handling
const ws = new WebSocket('wss://...');
// Manual reconnection logic
// Connection state management  
// Heartbeat/ping-pong implementation
// Error recovery strategies
🔒 Enterprise Security Benefits:

SSE uses standard HTTPS (port 443)
No special firewall rules needed
Works through corporate proxies
Standard HTTP authentication headers
Better audit trail in network logs

⚡ Office Add-in Optimization:

Lower memory footprint
Less interference with Word's performance
Handles add-in suspension/resume better
Simpler resource cleanup

📊 Final Scores:

SSE: 9/10 (perfect fit, minor limitations with connection pooling)
WebSocket: 6/10 (overkill, potential corporate network issues)

Proceed with SSE - it's simpler to implement, more reliable in your target environment, and perfectly suited for AI response streaming.


I need to see a roadmap with POC -> MVP -> Prod way, always prioirtize progeess over perfection ... and seek my feedback after each milestone 
includecalso a script to run ui loclaly for now and then help me with manifest file to dpeloy it on word

Based on this analysis, React + TypeScript is the clear winner for your patent drafting Word add-in. Here's why:
Key Insights:
React Excels At:

Chatbot Interface - Perfect for message rendering, user input, and conversation flow
Real-time Streaming - Ideal for displaying streaming responses from your AI backend
State Management - Conversation history, authentication state, UI state
Dynamic Content - Collapsible reasoning sections, formatted responses
Developer Experience - Faster development, better testing, component reuse

TypeScript Maintains Strength In:

Office.js Integration - You can still use pure TypeScript services for Word API calls
Type Safety - Full type checking for API responses and Office APIs
Performance - Critical Word operations can bypass React entirely

Recommended Hybrid Architecture:
typescript// React for UI Components
const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [streaming, setStreaming] = useState(false);
  // ... React component logic
};

// Pure TypeScript for Word Operations  
class DocumentService {
  async insertContent(content: string, formatting: WordFormatting) {
    await Word.run(async (context) => {
      // Direct Office.js calls without React overhead
    });
  }
}
This gives you the UI benefits of React while maintaining direct Word API performance where it matters most.





https://learn.microsoft.com/en-us/javascript/api/word?view=word-js-preview
https://learn.microsoft.com/en-us/office/dev/add-ins/develop/application-specific-api-model
https://learn.microsoft.com/en-us/javascript/api/office?view=common-js-preview

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Icon } from '@iconify/react';
import { Footer } from '../components/layout/Footer';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export const AIDashboard: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m FORGE AI, your development assistant. How can I help you today?',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Simulate AI response (in production, this would call DeepSeek API)
    setTimeout(() => {
      const aiResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: getAIResponse(input),
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiResponse]);
      setIsLoading(false);
    }, 1000);
  };

  const getAIResponse = (input: string): string => {
    const lower = input.toLowerCase();
    if (lower.includes('create') || lower.includes('generate')) {
      return "I can help you generate code! Just describe what you need and I'll create it for you. Try something like: 'Create a React button component'";
    } else if (lower.includes('fix') || lower.includes('bug')) {
      return "I can help you debug issues! Paste your code and describe the problem, and I'll analyze it.";
    } else if (lower.includes('explain')) {
      return "I'd be happy to explain code! Paste any code snippet and I'll break it down for you.";
    } else if (lower.includes('hello') || lower.includes('hi')) {
      return "Hello! I'm ready to help with your development tasks. What would you like to work on?";
    }
    return "I'm here to help with code generation, debugging, explanations, and more. Just let me know what you need!";
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 pb-12">
      {/* Background Effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse" />
      </div>

      {/* Main Content */}
      <div className="relative z-10 container mx-auto p-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between mb-6"
        >
          <div>
            <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
              FORGE AI Dashboard
            </h1>
            <p className="text-white/40 text-sm mt-1">
              AI-Native Development Environment • Powered by DeepSeek
            </p>
          </div>
          
          <div className="flex items-center space-x-2 glass px-3 py-1 rounded-full text-xs">
            <span className="text-green-400">●</span> 
            <span>DeepSeek Connected</span>
          </div>
        </motion.div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="glass-card p-4 cursor-pointer hover:border-purple-500/50 transition-colors"
          >
            <div className="flex items-center space-x-3 mb-2">
              <div className="p-2 bg-purple-500/20 rounded-lg">
                <Icon icon="lucide:sparkles" className="text-purple-400" width="20" height="20" />
              </div>
              <h3 className="font-semibold">AI Assistant</h3>
            </div>
            <p className="text-sm text-white/60">Chat with DeepSeek about your code, get instant help and code generation.</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="glass-card p-4 cursor-pointer hover:border-blue-500/50 transition-colors"
          >
            <div className="flex items-center space-x-3 mb-2">
              <div className="p-2 bg-blue-500/20 rounded-lg">
                <Icon icon="lucide:code" className="text-blue-400" width="20" height="20" />
              </div>
              <h3 className="font-semibold">Code Generation</h3>
            </div>
            <p className="text-sm text-white/60">Generate components, functions, and full applications with AI.</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="glass-card p-4 cursor-pointer hover:border-green-500/50 transition-colors"
          >
            <div className="flex items-center space-x-3 mb-2">
              <div className="p-2 bg-green-500/20 rounded-lg">
                <Icon icon="lucide:database" className="text-green-400" width="20" height="20" />
              </div>
              <h3 className="font-semibold">Database AI</h3>
            </div>
            <p className="text-sm text-white/60">AI-powered query optimization and database management.</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="glass-card p-4 cursor-pointer hover:border-cyan-500/50 transition-colors"
          >
            <div className="flex items-center space-x-3 mb-2">
              <div className="p-2 bg-cyan-500/20 rounded-lg">
                <Icon icon="lucide:terminal" className="text-cyan-400" width="20" height="20" />
              </div>
              <h3 className="font-semibold">Terminal</h3>
            </div>
            <p className="text-sm text-white/60">Execute commands and run code with AI assistance.</p>
          </motion.div>
        </div>

        {/* Chat Interface */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="glass-card mb-6 overflow-hidden"
        >
          <div className="p-4 border-b border-white/10">
            <h2 className="text-lg font-semibold flex items-center">
              <Icon icon="lucide:message-square" className="mr-2" width="20" height="20" />
              AI Chat
            </h2>
          </div>
          
          {/* Messages */}
          <div className="h-80 overflow-y-auto p-4 space-y-4">
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-[80%] p-3 rounded-lg ${
                  msg.role === 'user' 
                    ? 'bg-purple-500/20 border border-purple-500/30' 
                    : 'bg-blue-500/20 border border-blue-500/30'
                }`}>
                  <p className="text-sm">{msg.content}</p>
                  <span className="text-xs text-white/40 mt-1 block">
                    {msg.timestamp.toLocaleTimeString()}
                  </span>
                </div>
              </motion.div>
            ))}
            {isLoading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex justify-start"
              >
                <div className="bg-blue-500/20 border border-blue-500/30 p-3 rounded-lg">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </motion.div>
            )}
          </div>
          
          {/* Input */}
          <div className="p-4 border-t border-white/10">
            <div className="flex space-x-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                className="flex-1 bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-purple-500/50 transition-colors"
              />
              <button
                onClick={handleSend}
                disabled={!input.trim() || isLoading}
                className="px-4 py-2 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg font-medium text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:opacity-90 transition-opacity"
              >
                <Icon icon="lucide:send" width="18" height="18" />
              </button>
            </div>
          </div>
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="glass-card p-6"
        >
          <h2 className="text-xl font-bold mb-4 flex items-center">
            <Icon icon="lucide:zap" className="mr-2" width="20" height="20" />
            Quick Actions
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <button 
              onClick={() => setInput('Create a React component')}
              className="p-3 bg-white/5 hover:bg-white/10 rounded-lg text-left transition-colors"
            >
              <Icon icon="lucide:component" className="text-purple-400 mb-2" width="20" height="20" />
              <span className="text-sm">New Component</span>
            </button>
            <button 
              onClick={() => setInput('Explain this code')}
              className="p-3 bg-white/5 hover:bg-white/10 rounded-lg text-left transition-colors"
            >
              <Icon icon="lucide:file-code" className="text-blue-400 mb-2" width="20" height="20" />
              <span className="text-sm">Explain Code</span>
            </button>
            <button 
              onClick={() => setInput('Fix this bug')}
              className="p-3 bg-white/5 hover:bg-white/10 rounded-lg text-left transition-colors"
            >
              <Icon icon="lucide:bug" className="text-red-400 mb-2" width="20" height="20" />
              <span className="text-sm">Fix Bug</span>
            </button>
            <button 
              onClick={() => setInput('Write unit tests')}
              className="p-3 bg-white/5 hover:bg-white/10 rounded-lg text-left transition-colors"
            >
              <Icon icon="lucide:check-circle" className="text-green-400 mb-2" width="20" height="20" />
              <span className="text-sm">Write Tests</span>
            </button>
          </div>
        </motion.div>
      </div>

      {/* Footer with Attribution */}
      <Footer />
    </div>
  );
};

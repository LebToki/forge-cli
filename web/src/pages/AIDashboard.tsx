import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Cpu, Database, Code2, Terminal } from 'lucide-react';
import { Footer } from '../components/layout/Footer';

export const AIDashboard: React.FC = () => {
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
            className="glass-card p-4"
          >
            <div className="flex items-center space-x-3 mb-2">
              <div className="p-2 bg-purple-500/20 rounded-lg">
                <Sparkles className="text-purple-400" size={20} />
              </div>
              <h3 className="font-semibold">AI Assistant</h3>
            </div>
            <p className="text-sm text-white/60">Chat with DeepSeek about your code, get instant help and code generation.</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="glass-card p-4"
          >
            <div className="flex items-center space-x-3 mb-2">
              <div className="p-2 bg-blue-500/20 rounded-lg">
                <Code2 className="text-blue-400" size={20} />
              </div>
              <h3 className="font-semibold">Code Generation</h3>
            </div>
            <p className="text-sm text-white/60">Generate components, functions, and full applications with AI.</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="glass-card p-4"
          >
            <div className="flex items-center space-x-3 mb-2">
              <div className="p-2 bg-green-500/20 rounded-lg">
                <Database className="text-green-400" size={20} />
              </div>
              <h3 className="font-semibold">Database AI</h3>
            </div>
            <p className="text-sm text-white/60">AI-powered query optimization and database management.</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="glass-card p-4"
          >
            <div className="flex items-center space-x-3 mb-2">
              <div className="p-2 bg-cyan-500/20 rounded-lg">
                <Terminal className="text-cyan-400" size={20} />
              </div>
              <h3 className="font-semibold">Terminal</h3>
            </div>
            <p className="text-sm text-white/60">Execute commands and run code with AI assistance.</p>
          </motion.div>
        </div>

        {/* Coming Soon */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="glass-card p-8 text-center"
        >
          <h2 className="text-2xl font-bold mb-4">🚀 More AI Features Coming Soon</h2>
          <p className="text-white/60 mb-4">
            We're building the ultimate AI-powered development environment. Stay tuned for:
          </p>
          <div className="flex flex-wrap justify-center gap-2 text-sm">
            <span className="px-3 py-1 glass rounded-full">Component Explorer</span>
            <span className="px-3 py-1 glass rounded-full">AI Manifests</span>
            <span className="px-3 py-1 glass rounded-full">Smart Debugging</span>
            <span className="px-3 py-1 glass rounded-full">Performance Analysis</span>
          </div>
        </motion.div>
      </div>

      {/* Footer with Attribution */}
      <Footer />
    </div>
  );
};

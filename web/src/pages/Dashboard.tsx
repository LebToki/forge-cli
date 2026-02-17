import { motion } from 'framer-motion';
import { Icon } from '@iconify/react';
import { Footer } from '../components/layout/Footer';

const features = [
  {
    icon: <Icon icon="lucide:terminal" width="32" height="32" />,
    title: 'Glassmorphic CLI',
    description: 'Beautiful terminal interface with animated spinners and gradient text',
    color: 'from-blue-400 to-cyan-400'
  },
  {
    icon: <Icon icon="lucide:code" width="32" height="32" />,
    title: 'AI Code Generation',
    description: 'Generate code with DeepSeek AI in multiple languages',
    color: 'from-purple-400 to-pink-400'
  },
  {
    icon: <Icon icon="lucide:database" width="32" height="32" />,
    title: 'Database Support',
    description: 'MySQL, SQLite, and AI-powered query optimization',
    color: 'from-green-400 to-emerald-400'
  },
  {
    icon: <Icon icon="lucide:globe" width="32" height="32" />,
    title: 'PHP/WordPress',
    description: 'Full WordPress plugin and theme generation',
    color: 'from-yellow-400 to-orange-400'
  },
  {
    icon: <Icon icon="lucide:github" width="32" height="32" />,
    title: 'GitHub Integration',
    description: 'Clone, branch, commit, and create PRs with AI assistance',
    color: 'from-gray-400 to-slate-400'
  },
  {
    icon: <Icon icon="lucide:zap" width="32" height="32" />,
    title: 'Testing & Debugging',
    description: 'Generate tests, debug code, and profile performance',
    color: 'from-red-400 to-rose-400'
  }
];

const Dashboard: React.FC = () => {
  return (
    <div className="min-h-screen pb-12">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500/30 rounded-full blur-3xl animate-pulse" />
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500/30 rounded-full blur-3xl animate-pulse delay-1000" />
        </div>

        <div className="relative z-10 container mx-auto px-6 py-20">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center"
          >
            <div className="flex items-center justify-center mb-4">
              <span className="text-6xl">🔥</span>
            </div>
            <h1 className="text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 mb-4">
              FORGE
            </h1>
            <p className="text-xl text-white/60 mb-8">
              AI Development Ecosystem • Shape Code • Ship Faster
            </p>
            <div className="flex items-center justify-center space-x-4">
              <a
                href="/ai"
                className="px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg font-semibold hover:opacity-90 transition-opacity flex items-center"
              >
                <Icon icon="lucide:sparkles" className="mr-2" width="20" height="20" />
                Launch AI Dashboard
              </a>
              <button className="px-8 py-3 glass rounded-lg font-semibold hover:bg-white/10 transition-colors flex items-center">
                <Icon icon="lucide:terminal" className="mr-2" width="20" height="20" />
                CLI Documentation
              </button>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="container mx-auto px-6 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * index }}
              className="glass-card p-6 cursor-pointer group"
            >
              <div className={`w-14 h-14 rounded-xl bg-gradient-to-r ${feature.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-white/60 text-sm">{feature.description}</p>
            </motion.div>
          ))}
        </motion.div>
      </div>

      {/* Quick Start */}
      <div className="container mx-auto px-6 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="glass rounded-2xl p-8"
        >
          <h2 className="text-2xl font-bold mb-6">🚀 Quick Start</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold mb-3 text-blue-400">Python CLI</h3>
              <pre className="bg-black/30 rounded-lg p-4 text-sm overflow-x-auto">
                <code className="text-green-400">
{`pip install forge-cli
forge ask "Hello, world!"
forge chat`}
                </code>
              </pre>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-3 text-purple-400">TypeScript CLI</h3>
              <pre className="bg-black/30 rounded-lg p-4 text-sm overflow-x-auto">
                <code className="text-green-400">
{`npm install -g forge
forge ask "Hello, world!"
forge generate "React button"`}
                </code>
              </pre>
            </div>
          </div>
        </motion.div>
      </div>

      <Footer />
    </div>
  );
};

export default Dashboard;

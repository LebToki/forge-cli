import { Icon } from '@iconify/react';
import { motion } from 'framer-motion';

export const Footer: React.FC = () => {
  return (
    <motion.footer 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="fixed bottom-0 left-0 right-0 glass border-t border-glass-border py-2 px-4 text-xs text-white/40 z-50"
    >
      <div className="container mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-1">
          <span>Made with</span>
          <Icon icon="lucide:heart" width="12" height="12" className="text-red-400 animate-pulse" />
          <span>by</span>
          <a 
            href="https://github.com/LebToki" 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-purple-400 hover:text-purple-300 transition-colors font-medium"
          >
            Tarek Tarabichi
          </a>
          <span>from</span>
          <a 
            href="https://2tinteractive.com" 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-blue-400 hover:text-blue-300 transition-colors font-medium"
          >
            2TInteractive
          </a>
        </div>
        
        <div className="flex items-center space-x-4">
          <a 
            href="https://github.com/LebToki/forge-cli" 
            target="_blank" 
            rel="noopener noreferrer"
            className="hover:text-white/60 transition-colors flex items-center"
          >
            <Icon icon="lucide:github" width="12" height="12" className="mr-1" /> GitHub
          </a>
          <div className="flex items-center space-x-1 border-l border-glass-border pl-4">
            <Icon icon="lucide:sparkles" width="12" height="12" className="text-primary-400" />
            <span>Powered by</span>
            <a 
              href="https://deepseek.com" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-primary-400 hover:text-primary-300 transition-colors font-semibold"
            >
              DeepSeek AI
            </a>
          </div>
        </div>
      </div>
    </motion.footer>
  );
};

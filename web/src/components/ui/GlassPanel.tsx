import React from 'react';
import { motion } from 'framer-motion';
import { clsx } from 'clsx';

interface GlassPanelProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  icon?: React.ReactNode;
}

export const GlassPanel: React.FC<GlassPanelProps> = ({ 
  children, 
  className, 
  title,
  icon 
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={clsx(
        'glass rounded-xl p-4',
        className
      )}
    >
      {title && (
        <div className="flex items-center space-x-2 mb-3 pb-2 border-b border-glass-border">
          {icon && <span className="text-primary-400">{icon}</span>}
          <h3 className="text-lg font-semibold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
            {title}
          </h3>
        </div>
      )}
      {children}
    </motion.div>
  );
};

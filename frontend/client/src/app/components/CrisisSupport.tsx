'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Phone, 
  AlertTriangle, 
  X, 
  Heart,
  Shield,
  Clock
} from 'lucide-react';
import { cn } from '../lib/utils';

interface CrisisSupportProps {
  language: string;
  t: (key: string) => string;
}

export function CrisisSupport({ language, t }: CrisisSupportProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const crisisNumbers = [
    {
      name: 'National Suicide Prevention Lifeline',
      number: '988',
      description: '24/7 crisis support',
      icon: Heart,
    },
    {
      name: 'National Domestic Violence Hotline',
      number: '1-800-799-7233',
      description: '24/7 support for survivors',
      icon: Shield,
    },
    {
      name: 'Long Beach Crisis Line',
      number: '(562) 434-4949',
      description: 'Local crisis support',
      icon: Phone,
    },
  ];

  const handleCall = (number: string) => {
    window.open(`tel:${number}`, '_self');
  };

  return (
    <div className="fixed bottom-4 left-4 z-50">
      {/* Crisis Button */}
      <motion.button
        onClick={() => setIsExpanded(!isExpanded)}
        className={cn(
          "flex items-center space-x-2 px-4 py-3 rounded-full shadow-lg text-white font-medium transition-all duration-200",
          "bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-4 focus:ring-red-200"
        )}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <AlertTriangle className="w-5 h-5" />
        <span className="hidden sm:inline">Crisis Support</span>
      </motion.button>

      {/* Crisis Panel */}
      <AnimatePresence>
        {isExpanded && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black bg-opacity-50 z-40"
              onClick={() => setIsExpanded(false)}
            />
            
            {/* Panel */}
            <motion.div
              initial={{ opacity: 0, y: 20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 20, scale: 0.95 }}
              className="fixed bottom-20 left-4 w-80 bg-white rounded-lg shadow-xl z-50 border border-neutral-200"
            >
              {/* Header */}
              <div className="flex items-center justify-between p-4 border-b border-neutral-200 bg-red-50 rounded-t-lg">
                <div className="flex items-center space-x-2">
                  <AlertTriangle className="w-5 h-5 text-red-600" />
                  <h3 className="text-lg font-semibold text-red-900">
                    Crisis Support
                  </h3>
                </div>
                <button
                  onClick={() => setIsExpanded(false)}
                  className="p-1 hover:bg-red-100 rounded-md transition-colors duration-200"
                >
                  <X className="w-4 h-4 text-red-600" />
                </button>
              </div>

              {/* Emergency Message */}
              <div className="p-4 bg-red-50 border-b border-red-200">
                <div className="flex items-start space-x-3">
                  <Clock className="w-5 h-5 text-red-600 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-red-900">
                      Need immediate help?
                    </p>
                    <p className="text-xs text-red-700 mt-1">
                      These services are available 24/7 for crisis situations.
                    </p>
                  </div>
                </div>
              </div>

              {/* Crisis Numbers */}
              <div className="p-4 space-y-3">
                {crisisNumbers.map((crisis, index) => {
                  const Icon = crisis.icon;
                  return (
                    <motion.button
                      key={index}
                      onClick={() => handleCall(crisis.number)}
                      className="w-full flex items-center space-x-3 p-3 rounded-lg hover:bg-red-50 transition-colors duration-200 border border-neutral-200 hover:border-red-300"
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
                        <Icon className="w-5 h-5 text-red-600" />
                      </div>
                      <div className="flex-1 text-left">
                        <p className="text-sm font-medium text-neutral-900">
                          {crisis.name}
                        </p>
                        <p className="text-lg font-bold text-red-600">
                          {crisis.number}
                        </p>
                        <p className="text-xs text-neutral-500">
                          {crisis.description}
                        </p>
                      </div>
                    </motion.button>
                  );
                })}
              </div>

              {/* Footer */}
              <div className="p-4 border-t border-neutral-200 bg-neutral-50 rounded-b-lg">
                <div className="text-center">
                  <p className="text-xs text-neutral-600">
                    If you're in immediate danger, call 911
                  </p>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
}

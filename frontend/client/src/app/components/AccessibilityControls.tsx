'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Settings, 
  Eye, 
  Type, 
  Move, 
  Volume2, 
  Keyboard,
  X,
  Check
} from 'lucide-react';
import { cn } from '../lib/utils';

interface AccessibilityControlsProps {
  highContrast: boolean;
  largeText: boolean;
  reducedMotion: boolean;
  screenReader: boolean;
  onToggleHighContrast: () => void;
  onToggleLargeText: () => void;
  onToggleReducedMotion: () => void;
  onToggleScreenReader: () => void;
}

export function AccessibilityControls({
  highContrast,
  largeText,
  reducedMotion,
  screenReader,
  onToggleHighContrast,
  onToggleLargeText,
  onToggleReducedMotion,
  onToggleScreenReader,
}: AccessibilityControlsProps) {
  const [isOpen, setIsOpen] = useState(false);

  const controls = [
    {
      id: 'highContrast',
      label: 'High Contrast',
      description: 'Increase contrast for better visibility',
      icon: Eye,
      enabled: highContrast,
      onToggle: onToggleHighContrast,
    },
    {
      id: 'largeText',
      label: 'Large Text',
      description: 'Increase text size for better readability',
      icon: Type,
      enabled: largeText,
      onToggle: onToggleLargeText,
    },
    {
      id: 'reducedMotion',
      label: 'Reduced Motion',
      description: 'Minimize animations and transitions',
      icon: Move,
      enabled: reducedMotion,
      onToggle: onToggleReducedMotion,
    },
    {
      id: 'screenReader',
      label: 'Screen Reader',
      description: 'Optimize for screen reader users',
      icon: Volume2,
      enabled: screenReader,
      onToggle: onToggleScreenReader,
    },
  ];

  return (
    <>
      {/* Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-4 right-4 z-50 w-12 h-12 bg-primary-600 hover:bg-primary-700 text-white rounded-full shadow-lg flex items-center justify-center transition-colors duration-200 focus:outline-none focus:ring-4 focus:ring-primary-200"
        aria-label="Accessibility Controls"
      >
        <Settings className="w-6 h-6" />
      </button>

      {/* Controls Panel */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black bg-opacity-50 z-40"
              onClick={() => setIsOpen(false)}
            />
            
            {/* Panel */}
            <motion.div
              initial={{ opacity: 0, y: 20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 20, scale: 0.95 }}
              className="fixed bottom-20 right-4 w-80 bg-white rounded-lg shadow-xl z-50 border border-neutral-200"
            >
              {/* Header */}
              <div className="flex items-center justify-between p-4 border-b border-neutral-200">
                <div className="flex items-center space-x-2">
                  <Settings className="w-5 h-5 text-primary-600" />
                  <h3 className="text-lg font-semibold text-neutral-900">
                    Accessibility Controls
                  </h3>
                </div>
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-1 hover:bg-neutral-100 rounded-md transition-colors duration-200"
                >
                  <X className="w-4 h-4 text-neutral-500" />
                </button>
              </div>

              {/* Controls */}
              <div className="p-4 space-y-3">
                {controls.map((control) => {
                  const Icon = control.icon;
                  return (
                    <div
                      key={control.id}
                      className="flex items-center justify-between p-3 rounded-lg hover:bg-neutral-50 transition-colors duration-200"
                    >
                      <div className="flex items-center space-x-3">
                        <Icon className="w-5 h-5 text-neutral-600" />
                        <div>
                          <p className="text-sm font-medium text-neutral-900">
                            {control.label}
                          </p>
                          <p className="text-xs text-neutral-500">
                            {control.description}
                          </p>
                        </div>
                      </div>
                      <button
                        onClick={control.onToggle}
                        className={cn(
                          "relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2",
                          control.enabled ? "bg-primary-600" : "bg-neutral-200"
                        )}
                      >
                        <span
                          className={cn(
                            "inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-200",
                            control.enabled ? "translate-x-6" : "translate-x-1"
                          )}
                        />
                      </button>
                    </div>
                  );
                })}
              </div>

              {/* Footer */}
              <div className="p-4 border-t border-neutral-200 bg-neutral-50 rounded-b-lg">
                <div className="flex items-center space-x-2 text-xs text-neutral-600">
                  <Keyboard className="w-4 h-4" />
                  <span>Press Alt + A to toggle accessibility controls</span>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}

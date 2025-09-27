'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Toaster } from 'react-hot-toast';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { KioskInterface } from './components/KioskInterface';
import { LanguageSelector } from './components/LanguageSelector';
import { AccessibilityControls } from './components/AccessibilityControls';
import { CrisisAlert } from './components/CrisisAlert';
import { LoadingSpinner } from './components/LoadingSpinner';
import { useLanguage } from './hooks/useLanguage';
import { useAccessibility } from './hooks/useAccessibility';
import { useWebSocket } from './hooks/useWebSocket';
import { useServiceWorker } from './hooks/useServiceWorker';
import { useVoiceControl } from './hooks/useVoiceControl';
import { translations } from './lib/translations';
import { cn } from './lib/utils';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    },
  },
});

export default function KioskPortal() {
  const [isLoading, setIsLoading] = useState(true);
  const [isOnline, setIsOnline] = useState(true);
  const { language, setLanguage, t } = useLanguage();
  const { 
    highContrast, 
    largeText, 
    reducedMotion, 
    screenReader, 
    voiceControl,
    toggleHighContrast, 
    toggleLargeText, 
    toggleReducedMotion, 
    toggleScreenReader,
    toggleVoiceControl
  } = useAccessibility();
  
  // Initialize WebSocket connection
  useWebSocket();
  
  // Initialize service worker for offline support
  useServiceWorker();

  // Initialize voice control
  useVoiceControl({
    enabled: voiceControl,
    language: language,
    onCommand: (command) => {
      console.log('Voice command received:', command);
      // Handle voice commands
    }
  });

  // Check online status
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Initialize app
  useEffect(() => {
    const initApp = async () => {
      try {
        // Initialize kiosk mode
        await new Promise(resolve => setTimeout(resolve, 2000));
      } catch (error) {
        console.error('Failed to initialize kiosk:', error);
      } finally {
        setIsLoading(false);
      }
    };

    initApp();
  }, []);

  // Apply accessibility settings
  useEffect(() => {
    const root = document.documentElement;
    
    if (highContrast) {
      root.classList.add('high-contrast');
    } else {
      root.classList.remove('high-contrast');
    }
    
    if (largeText) {
      root.classList.add('large-text');
    } else {
      root.classList.remove('large-text');
    }
    
    if (reducedMotion) {
      root.classList.add('reduced-motion');
    } else {
      root.classList.remove('reduced-motion');
    }
    
    if (screenReader) {
      root.classList.add('screen-reader');
    } else {
      root.classList.remove('screen-reader');
    }

    if (voiceControl) {
      root.classList.add('voice-control');
    } else {
      root.classList.remove('voice-control');
    }
  }, [highContrast, largeText, reducedMotion, screenReader, voiceControl]);

  // Prevent right-click and other browser features in kiosk mode
  useEffect(() => {
    const handleContextMenu = (e: MouseEvent) => e.preventDefault();
    const handleKeyDown = (e: KeyboardEvent) => {
      // Disable F12, Ctrl+Shift+I, Ctrl+U, etc.
      if (e.key === 'F12' || 
          (e.ctrlKey && e.shiftKey && e.key === 'I') ||
          (e.ctrlKey && e.key === 'u')) {
        e.preventDefault();
      }
    };

    document.addEventListener('contextmenu', handleContextMenu);
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('contextmenu', handleContextMenu);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex items-center justify-center">
        <div className="text-center">
          <LoadingSpinner size="lg" />
          <p className="mt-4 text-lg text-neutral-600">Initializing Kiosk Interface...</p>
        </div>
      </div>
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <div className={cn(
        "min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 kiosk-mode",
        highContrast && "high-contrast",
        largeText && "large-text",
        reducedMotion && "reduced-motion",
        screenReader && "screen-reader",
        voiceControl && "voice-control"
      )}>
        {/* Global Styles */}
        <style jsx global>{`
          .kiosk-mode {
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
            -webkit-touch-callout: none;
            -webkit-tap-highlight-color: transparent;
          }
          
          .kiosk-mode * {
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
          }
          
          .kiosk-mode input,
          .kiosk-mode textarea {
            -webkit-user-select: text;
            -moz-user-select: text;
            -ms-user-select: text;
            user-select: text;
          }
          
          .high-contrast {
            --tw-bg-opacity: 1;
            --tw-text-opacity: 1;
            --tw-border-opacity: 1;
          }
          
          .large-text {
            font-size: 1.25rem;
            line-height: 1.8rem;
          }
          
          .reduced-motion * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
          }
          
          .screen-reader .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
          }
          
          .voice-control .voice-active {
            background-color: #3b82f6;
            color: white;
          }
        `}</style>

        {/* Main Content */}
        <main className="flex-1">
          <KioskInterface 
            language={language}
            t={t}
            isOnline={isOnline}
          />
        </main>

        {/* Accessibility Controls */}
        <AccessibilityControls
          highContrast={highContrast}
          largeText={largeText}
          reducedMotion={reducedMotion}
          screenReader={screenReader}
          voiceControl={voiceControl}
          onToggleHighContrast={toggleHighContrast}
          onToggleLargeText={toggleLargeText}
          onToggleReducedMotion={toggleReducedMotion}
          onToggleScreenReader={toggleScreenReader}
          onToggleVoiceControl={toggleVoiceControl}
        />

        {/* Crisis Alert */}
        <CrisisAlert 
          language={language}
          t={t}
        />

        {/* Language Selector */}
        <LanguageSelector
          currentLanguage={language}
          onLanguageChange={setLanguage}
          t={t}
        />

        {/* Toast Notifications */}
        <Toaster
          position="top-center"
          toastOptions={{
            duration: 6000,
            style: {
              background: '#363636',
              color: '#fff',
              fontSize: '1.125rem',
              padding: '1rem 1.5rem',
            },
            success: {
              duration: 4000,
              iconTheme: {
                primary: '#22c55e',
                secondary: '#fff',
              },
            },
            error: {
              duration: 8000,
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },
          }}
        />
      </div>
    </QueryClientProvider>
  );
}

'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Toaster } from 'react-hot-toast';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ClientDashboard } from './components/ClientDashboard';
import { LanguageSelector } from './components/LanguageSelector';
import { AccessibilityControls } from './components/AccessibilityControls';
import { CrisisSupport } from './components/CrisisSupport';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { LoadingSpinner } from './components/LoadingSpinner';
import { useAuth } from './hooks/useAuth';
import { useLanguage } from './hooks/useLanguage';
import { useAccessibility } from './hooks/useAccessibility';
import { useWebSocket } from './hooks/useWebSocket';
import { useServiceWorker } from './hooks/useServiceWorker';
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

export default function ClientPortal() {
  const [isLoading, setIsLoading] = useState(true);
  const [isOnline, setIsOnline] = useState(true);
  const { user, login, logout, isAuthenticated } = useAuth();
  const { language, setLanguage, t } = useLanguage();
  const { 
    highContrast, 
    largeText, 
    reducedMotion, 
    screenReader, 
    toggleHighContrast, 
    toggleLargeText, 
    toggleReducedMotion, 
    toggleScreenReader 
  } = useAccessibility();
  
  // Initialize WebSocket connection
  useWebSocket();
  
  // Initialize service worker for offline support
  useServiceWorker();

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
        // Check if user is already authenticated
        const token = localStorage.getItem('access_token');
        if (token) {
          // Validate token and get user info
          // This would typically make an API call
          // For now, we'll simulate it
          await new Promise(resolve => setTimeout(resolve, 1000));
        }
      } catch (error) {
        console.error('Failed to initialize app:', error);
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
  }, [highContrast, largeText, reducedMotion, screenReader]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <div className={cn(
        "min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50",
        highContrast && "high-contrast",
        largeText && "large-text",
        reducedMotion && "reduced-motion",
        screenReader && "screen-reader"
      )}>
        {/* Global Styles */}
        <style jsx global>{`
          .high-contrast {
            --tw-bg-opacity: 1;
            --tw-text-opacity: 1;
            --tw-border-opacity: 1;
          }
          
          .large-text {
            font-size: 1.125rem;
            line-height: 1.75rem;
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
        `}</style>

        {/* Header */}
        <Header 
          user={user}
          isAuthenticated={isAuthenticated}
          onLogin={login}
          onLogout={logout}
          language={language}
          onLanguageChange={setLanguage}
          isOnline={isOnline}
        />

        {/* Main Content */}
        <main className="flex-1">
          {isAuthenticated ? (
            <ClientDashboard 
              user={user}
              language={language}
              t={t}
            />
          ) : (
            <LandingPage 
              onLogin={login}
              language={language}
              t={t}
            />
          )}
        </main>

        {/* Footer */}
        <Footer 
          language={language}
          t={t}
        />

        {/* Accessibility Controls */}
        <AccessibilityControls
          highContrast={highContrast}
          largeText={largeText}
          reducedMotion={reducedMotion}
          screenReader={screenReader}
          onToggleHighContrast={toggleHighContrast}
          onToggleLargeText={toggleLargeText}
          onToggleReducedMotion={toggleReducedMotion}
          onToggleScreenReader={toggleScreenReader}
        />

        {/* Crisis Support */}
        <CrisisSupport 
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
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#22c55e',
                secondary: '#fff',
              },
            },
            error: {
              duration: 5000,
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

// Landing Page Component
function LandingPage({ 
  onLogin, 
  language, 
  t 
}: { 
  onLogin: () => void;
  language: string;
  t: (key: string) => string;
}) {
  return (
    <div className="container mx-auto px-4 py-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center"
      >
        <h1 className="text-4xl md:text-6xl font-bold text-primary-900 mb-6">
          {t('welcome.title')}
        </h1>
        <p className="text-xl md:text-2xl text-neutral-600 mb-8 max-w-3xl mx-auto">
          {t('welcome.subtitle')}
        </p>
        
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="bg-white rounded-lg shadow-lg p-6"
          >
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">🏠</span>
            </div>
            <h3 className="text-xl font-semibold text-primary-900 mb-2">
              {t('features.housing.title')}
            </h3>
            <p className="text-neutral-600">
              {t('features.housing.description')}
            </p>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="bg-white rounded-lg shadow-lg p-6"
          >
            <div className="w-16 h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">💼</span>
            </div>
            <h3 className="text-xl font-semibold text-primary-900 mb-2">
              {t('features.employment.title')}
            </h3>
            <p className="text-neutral-600">
              {t('features.employment.description')}
            </p>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
            className="bg-white rounded-lg shadow-lg p-6"
          >
            <div className="w-16 h-16 bg-accent-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">🏥</span>
            </div>
            <h3 className="text-xl font-semibold text-primary-900 mb-2">
              {t('features.healthcare.title')}
            </h3>
            <p className="text-neutral-600">
              {t('features.healthcare.description')}
            </p>
          </motion.div>
        </div>
        
        <motion.button
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          onClick={onLogin}
          className="bg-primary-600 hover:bg-primary-700 text-white font-semibold py-4 px-8 rounded-lg text-lg transition-colors duration-200 focus:outline-none focus:ring-4 focus:ring-primary-200"
        >
          {t('welcome.get_started')}
        </motion.button>
      </motion.div>
    </div>
  );
}

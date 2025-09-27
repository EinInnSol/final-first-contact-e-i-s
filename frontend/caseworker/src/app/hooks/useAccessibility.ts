'use client';

import { useState, useEffect, useCallback } from 'react';

interface AccessibilitySettings {
  highContrast: boolean;
  largeText: boolean;
  reducedMotion: boolean;
  screenReader: boolean;
  keyboardNavigation: boolean;
  voiceControl: boolean;
  colorBlindSupport: boolean;
  fontSize: 'small' | 'medium' | 'large' | 'extra-large';
  lineHeight: 'tight' | 'normal' | 'relaxed';
  letterSpacing: 'tight' | 'normal' | 'wide';
}

const DEFAULT_SETTINGS: AccessibilitySettings = {
  highContrast: false,
  largeText: false,
  reducedMotion: false,
  screenReader: false,
  keyboardNavigation: false,
  voiceControl: false,
  colorBlindSupport: false,
  fontSize: 'medium',
  lineHeight: 'normal',
  letterSpacing: 'normal',
};

export function useAccessibility() {
  const [settings, setSettings] = useState<AccessibilitySettings>(DEFAULT_SETTINGS);

  // Load settings from localStorage on mount
  useEffect(() => {
    const savedSettings = localStorage.getItem('accessibility_settings');
    if (savedSettings) {
      try {
        const parsed = JSON.parse(savedSettings);
        setSettings({ ...DEFAULT_SETTINGS, ...parsed });
      } catch (error) {
        console.error('Failed to parse accessibility settings:', error);
      }
    }
  }, []);

  // Save settings to localStorage when they change
  useEffect(() => {
    localStorage.setItem('accessibility_settings', JSON.stringify(settings));
  }, [settings]);

  // Apply accessibility settings to the document
  useEffect(() => {
    const root = document.documentElement;
    
    // High contrast
    if (settings.highContrast) {
      root.classList.add('high-contrast');
    } else {
      root.classList.remove('high-contrast');
    }
    
    // Large text
    if (settings.largeText) {
      root.classList.add('large-text');
    } else {
      root.classList.remove('large-text');
    }
    
    // Reduced motion
    if (settings.reducedMotion) {
      root.classList.add('reduced-motion');
    } else {
      root.classList.remove('reduced-motion');
    }
    
    // Screen reader
    if (settings.screenReader) {
      root.classList.add('screen-reader');
    } else {
      root.classList.remove('screen-reader');
    }
    
    // Keyboard navigation
    if (settings.keyboardNavigation) {
      root.classList.add('keyboard-navigation');
    } else {
      root.classList.remove('keyboard-navigation');
    }
    
    // Voice control
    if (settings.voiceControl) {
      root.classList.add('voice-control');
    } else {
      root.classList.remove('voice-control');
    }
    
    // Color blind support
    if (settings.colorBlindSupport) {
      root.classList.add('color-blind-support');
    } else {
      root.classList.remove('color-blind-support');
    }
    
    // Font size
    root.classList.remove('font-small', 'font-medium', 'font-large', 'font-extra-large');
    root.classList.add(`font-${settings.fontSize}`);
    
    // Line height
    root.classList.remove('line-tight', 'line-normal', 'line-relaxed');
    root.classList.add(`line-${settings.lineHeight}`);
    
    // Letter spacing
    root.classList.remove('letter-tight', 'letter-normal', 'letter-wide');
    root.classList.add(`letter-${settings.letterSpacing}`);
  }, [settings]);

  const toggleHighContrast = useCallback(() => {
    setSettings(prev => ({ ...prev, highContrast: !prev.highContrast }));
  }, []);

  const toggleLargeText = useCallback(() => {
    setSettings(prev => ({ ...prev, largeText: !prev.largeText }));
  }, []);

  const toggleReducedMotion = useCallback(() => {
    setSettings(prev => ({ ...prev, reducedMotion: !prev.reducedMotion }));
  }, []);

  const toggleScreenReader = useCallback(() => {
    setSettings(prev => ({ ...prev, screenReader: !prev.screenReader }));
  }, []);

  const toggleKeyboardNavigation = useCallback(() => {
    setSettings(prev => ({ ...prev, keyboardNavigation: !prev.keyboardNavigation }));
  }, []);

  const toggleVoiceControl = useCallback(() => {
    setSettings(prev => ({ ...prev, voiceControl: !prev.voiceControl }));
  }, []);

  const toggleColorBlindSupport = useCallback(() => {
    setSettings(prev => ({ ...prev, colorBlindSupport: !prev.colorBlindSupport }));
  }, []);

  const setFontSize = useCallback((size: AccessibilitySettings['fontSize']) => {
    setSettings(prev => ({ ...prev, fontSize: size }));
  }, []);

  const setLineHeight = useCallback((height: AccessibilitySettings['lineHeight']) => {
    setSettings(prev => ({ ...prev, lineHeight: height }));
  }, []);

  const setLetterSpacing = useCallback((spacing: AccessibilitySettings['letterSpacing']) => {
    setSettings(prev => ({ ...prev, letterSpacing: spacing }));
  }, []);

  const resetSettings = useCallback(() => {
    setSettings(DEFAULT_SETTINGS);
  }, []);

  const updateSettings = useCallback((newSettings: Partial<AccessibilitySettings>) => {
    setSettings(prev => ({ ...prev, ...newSettings }));
  }, []);

  // Keyboard navigation helpers
  const handleKeyDown = useCallback((event: KeyboardEvent, callback: () => void) => {
    if (settings.keyboardNavigation) {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        callback();
      }
    }
  }, [settings.keyboardNavigation]);

  // Focus management
  const focusElement = useCallback((selector: string) => {
    const element = document.querySelector(selector) as HTMLElement;
    if (element) {
      element.focus();
    }
  }, []);

  const trapFocus = useCallback((container: HTMLElement) => {
    const focusableElements = container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

    const handleTabKey = (e: KeyboardEvent) => {
      if (e.key === 'Tab') {
        if (e.shiftKey) {
          if (document.activeElement === firstElement) {
            lastElement.focus();
            e.preventDefault();
          }
        } else {
          if (document.activeElement === lastElement) {
            firstElement.focus();
            e.preventDefault();
          }
        }
      }
    };

    container.addEventListener('keydown', handleTabKey);
    firstElement?.focus();

    return () => {
      container.removeEventListener('keydown', handleTabKey);
    };
  }, []);

  return {
    ...settings,
    toggleHighContrast,
    toggleLargeText,
    toggleReducedMotion,
    toggleScreenReader,
    toggleKeyboardNavigation,
    toggleVoiceControl,
    toggleColorBlindSupport,
    setFontSize,
    setLineHeight,
    setLetterSpacing,
    resetSettings,
    updateSettings,
    handleKeyDown,
    focusElement,
    trapFocus,
  };
}

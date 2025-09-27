'use client';

import { useState, useEffect, useCallback } from 'react';

export type Language = 'en' | 'es' | 'km' | 'tl' | 'ko';

const SUPPORTED_LANGUAGES: Language[] = ['en', 'es', 'km', 'tl', 'ko'];

const LANGUAGE_NAMES = {
  en: 'English',
  es: 'Español',
  km: 'ខ្មែរ',
  tl: 'Tagalog',
  ko: '한국어'
};

export function useLanguage() {
  const [language, setLanguageState] = useState<Language>('en');

  // Load language from localStorage on mount
  useEffect(() => {
    const savedLanguage = localStorage.getItem('language') as Language;
    if (savedLanguage && SUPPORTED_LANGUAGES.includes(savedLanguage)) {
      setLanguageState(savedLanguage);
    } else {
      // Try to detect browser language
      const browserLanguage = navigator.language.split('-')[0];
      if (SUPPORTED_LANGUAGES.includes(browserLanguage as Language)) {
        setLanguageState(browserLanguage as Language);
      }
    }
  }, []);

  // Save language to localStorage when it changes
  useEffect(() => {
    localStorage.setItem('language', language);
    document.documentElement.lang = language;
  }, [language]);

  const setLanguage = useCallback((newLanguage: Language) => {
    if (SUPPORTED_LANGUAGES.includes(newLanguage)) {
      setLanguageState(newLanguage);
    }
  }, []);

  const t = useCallback((key: string, fallback?: string): string => {
    // This would typically load from a translation file
    // For now, we'll return the key or fallback
    return fallback || key;
  }, [language]);

  const getLanguageName = useCallback((lang: Language): string => {
    return LANGUAGE_NAMES[lang];
  }, []);

  const getSupportedLanguages = useCallback((): Language[] => {
    return SUPPORTED_LANGUAGES;
  }, []);

  const isRTL = useCallback((): boolean => {
    // None of our supported languages are RTL
    return false;
  }, []);

  const formatDate = useCallback((date: Date | string, options?: Intl.DateTimeFormatOptions): string => {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    return new Intl.DateTimeFormat(language, {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      ...options
    }).format(dateObj);
  }, [language]);

  const formatNumber = useCallback((number: number, options?: Intl.NumberFormatOptions): string => {
    return new Intl.NumberFormat(language, options).format(number);
  }, [language]);

  const formatCurrency = useCallback((amount: number, currency = 'USD'): string => {
    return new Intl.NumberFormat(language, {
      style: 'currency',
      currency
    }).format(amount);
  }, [language]);

  return {
    language,
    setLanguage,
    t,
    getLanguageName,
    getSupportedLanguages,
    isRTL,
    formatDate,
    formatNumber,
    formatCurrency,
  };
}

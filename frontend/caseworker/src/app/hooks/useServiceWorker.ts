'use client';

import { useEffect, useCallback, useState } from 'react';

interface ServiceWorkerState {
  isSupported: boolean;
  isRegistered: boolean;
  isOnline: boolean;
  registration: ServiceWorkerRegistration | null;
}

export function useServiceWorker() {
  const [state, setState] = useState<ServiceWorkerState>({
    isSupported: false,
    isRegistered: false,
    isOnline: navigator.onLine,
    registration: null,
  });

  const registerServiceWorker = useCallback(async () => {
    if (!('serviceWorker' in navigator)) {
      console.log('Service Worker not supported');
      return;
    }

    try {
      const registration = await navigator.serviceWorker.register('/sw.js', {
        scope: '/',
      });

      console.log('Service Worker registered successfully:', registration);

      setState(prev => ({
        ...prev,
        isSupported: true,
        isRegistered: true,
        registration,
      }));

      // Listen for updates
      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing;
        if (newWorker) {
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed') {
              if (navigator.serviceWorker.controller) {
                // New content is available, notify user
                console.log('New content is available, please refresh.');
                // You could show a notification here
              } else {
                // Content is cached for the first time
                console.log('Content is cached for offline use.');
              }
            }
          });
        }
      });

    } catch (error) {
      console.error('Service Worker registration failed:', error);
      setState(prev => ({
        ...prev,
        isSupported: true,
        isRegistered: false,
      }));
    }
  }, []);

  const unregisterServiceWorker = useCallback(async () => {
    if (!('serviceWorker' in navigator)) {
      return;
    }

    try {
      const registrations = await navigator.serviceWorker.getRegistrations();
      await Promise.all(registrations.map(registration => registration.unregister()));
      
      setState(prev => ({
        ...prev,
        isRegistered: false,
        registration: null,
      }));

      console.log('Service Worker unregistered');
    } catch (error) {
      console.error('Service Worker unregistration failed:', error);
    }
  }, []);

  const updateServiceWorker = useCallback(async () => {
    if (!state.registration) {
      return;
    }

    try {
      await state.registration.update();
      console.log('Service Worker updated');
    } catch (error) {
      console.error('Service Worker update failed:', error);
    }
  }, [state.registration]);

  const clearCache = useCallback(async () => {
    if (!('caches' in window)) {
      return;
    }

    try {
      const cacheNames = await caches.keys();
      await Promise.all(
        cacheNames.map(cacheName => caches.delete(cacheName))
      );
      console.log('Cache cleared');
    } catch (error) {
      console.error('Cache clearing failed:', error);
    }
  }, []);

  const addToCache = useCallback(async (url: string, response: Response) => {
    if (!('caches' in window)) {
      return;
    }

    try {
      const cache = await caches.open('first-contact-eis-v1');
      await cache.put(url, response);
      console.log('Added to cache:', url);
    } catch (error) {
      console.error('Failed to add to cache:', error);
    }
  }, []);

  const getFromCache = useCallback(async (url: string): Promise<Response | undefined> => {
    if (!('caches' in window)) {
      return undefined;
    }

    try {
      const cache = await caches.open('first-contact-eis-v1');
      return await cache.match(url);
    } catch (error) {
      console.error('Failed to get from cache:', error);
      return undefined;
    }
  }, []);

  // Handle online/offline events
  useEffect(() => {
    const handleOnline = () => {
      setState(prev => ({ ...prev, isOnline: true }));
      console.log('App is online');
    };

    const handleOffline = () => {
      setState(prev => ({ ...prev, isOnline: false }));
      console.log('App is offline');
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Register service worker on mount
  useEffect(() => {
    registerServiceWorker();
  }, [registerServiceWorker]);

  // Handle service worker messages
  useEffect(() => {
    if (!('serviceWorker' in navigator)) {
      return;
    }

    const handleMessage = (event: MessageEvent) => {
      const { type, data } = event.data;
      
      switch (type) {
        case 'CACHE_UPDATED':
          console.log('Cache updated:', data);
          break;
        case 'OFFLINE_READY':
          console.log('App is ready for offline use');
          break;
        case 'CACHE_ERROR':
          console.error('Cache error:', data);
          break;
        default:
          console.log('Service Worker message:', type, data);
      }
    };

    navigator.serviceWorker.addEventListener('message', handleMessage);

    return () => {
      navigator.serviceWorker.removeEventListener('message', handleMessage);
    };
  }, []);

  return {
    ...state,
    registerServiceWorker,
    unregisterServiceWorker,
    updateServiceWorker,
    clearCache,
    addToCache,
    getFromCache,
  };
}

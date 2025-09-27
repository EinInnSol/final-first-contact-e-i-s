'use client';

import { useEffect, useState } from 'react';

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

  useEffect(() => {
    // Check if service workers are supported
    if (!('serviceWorker' in navigator)) {
      console.log('Service workers not supported');
      return;
    }

    setState(prev => ({ ...prev, isSupported: true }));

    // Register service worker
    const registerServiceWorker = async () => {
      try {
        const registration = await navigator.serviceWorker.register('/sw.js', {
          scope: '/',
        });

        console.log('Service worker registered:', registration);
        setState(prev => ({
          ...prev,
          isRegistered: true,
          registration,
        }));

        // Handle updates
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          if (newWorker) {
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                // New content is available, notify user
                if (confirm('New version available! Reload to update?')) {
                  window.location.reload();
                }
              }
            });
          }
        });

      } catch (error) {
        console.error('Service worker registration failed:', error);
      }
    };

    registerServiceWorker();

    // Handle online/offline events
    const handleOnline = () => {
      setState(prev => ({ ...prev, isOnline: true }));
    };

    const handleOffline = () => {
      setState(prev => ({ ...prev, isOnline: false }));
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Send message to service worker
  const sendMessage = async (message: any) => {
    if (state.registration?.active) {
      state.registration.active.postMessage(message);
    }
  };

  // Request background sync
  const requestBackgroundSync = async (tag: string) => {
    if (state.registration?.sync) {
      try {
        await state.registration.sync.register(tag);
        console.log('Background sync registered:', tag);
      } catch (error) {
        console.error('Background sync registration failed:', error);
      }
    }
  };

  // Request push notification permission
  const requestNotificationPermission = async () => {
    if (!('Notification' in window)) {
      console.log('Notifications not supported');
      return false;
    }

    if (Notification.permission === 'granted') {
      return true;
    }

    if (Notification.permission === 'denied') {
      console.log('Notification permission denied');
      return false;
    }

    const permission = await Notification.requestPermission();
    return permission === 'granted';
  };

  // Show notification
  const showNotification = async (title: string, options: NotificationOptions = {}) => {
    if (state.registration && Notification.permission === 'granted') {
      await state.registration.showNotification(title, {
        icon: '/icon-192x192.png',
        badge: '/badge-72x72.png',
        ...options,
      });
    }
  };

  // Cache data for offline use
  const cacheData = async (key: string, data: any) => {
    if (state.registration?.active) {
      state.registration.active.postMessage({
        type: 'CACHE_DATA',
        key,
        data,
      });
    }
  };

  // Get cached data
  const getCachedData = async (key: string) => {
    return new Promise((resolve) => {
      if (state.registration?.active) {
        const messageChannel = new MessageChannel();
        
        messageChannel.port1.onmessage = (event) => {
          resolve(event.data);
        };

        state.registration.active.postMessage({
          type: 'GET_CACHED_DATA',
          key,
        }, [messageChannel.port2]);
      } else {
        resolve(null);
      }
    });
  };

  return {
    ...state,
    sendMessage,
    requestBackgroundSync,
    requestNotificationPermission,
    showNotification,
    cacheData,
    getCachedData,
  };
}

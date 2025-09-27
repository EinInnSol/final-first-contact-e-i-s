'use client';

import { useEffect, useRef, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';

interface WebSocketMessage {
  type: string;
  data: any;
  timestamp: string;
}

interface UseWebSocketOptions {
  onMessage?: (message: WebSocketMessage) => void;
  onConnect?: () => void;
  onDisconnect?: () => void;
  onError?: (error: Error) => void;
}

export function useWebSocket(options: UseWebSocketOptions = {}) {
  const socketRef = useRef<Socket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = 5;
  const reconnectDelay = 1000; // Start with 1 second

  const connect = useCallback(() => {
    if (socketRef.current?.connected) return;

    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';
    
    try {
      socketRef.current = io(wsUrl, {
        transports: ['websocket', 'polling'],
        timeout: 20000,
        reconnection: true,
        reconnectionAttempts: maxReconnectAttempts,
        reconnectionDelay: reconnectDelay,
        reconnectionDelayMax: 5000,
        maxReconnectionAttempts: maxReconnectAttempts,
      });

      socketRef.current.on('connect', () => {
        console.log('WebSocket connected');
        reconnectAttempts.current = 0;
        options.onConnect?.();
      });

      socketRef.current.on('disconnect', (reason) => {
        console.log('WebSocket disconnected:', reason);
        options.onDisconnect?.();
      });

      socketRef.current.on('connect_error', (error) => {
        console.error('WebSocket connection error:', error);
        options.onError?.(error);
      });

      socketRef.current.on('message', (message: WebSocketMessage) => {
        console.log('WebSocket message received:', message);
        options.onMessage?.(message);
      });

      // Handle specific message types
      socketRef.current.on('crisis_alert', (data) => {
        options.onMessage?.({
          type: 'crisis_alert',
          data,
          timestamp: new Date().toISOString(),
        });
      });

      socketRef.current.on('notification', (data) => {
        options.onMessage?.({
          type: 'notification',
          data,
          timestamp: new Date().toISOString(),
        });
      });

      socketRef.current.on('case_update', (data) => {
        options.onMessage?.({
          type: 'case_update',
          data,
          timestamp: new Date().toISOString(),
        });
      });

      socketRef.current.on('ai_response', (data) => {
        options.onMessage?.({
          type: 'ai_response',
          data,
          timestamp: new Date().toISOString(),
        });
      });

    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
      options.onError?.(error as Error);
    }
  }, [options]);

  const disconnect = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.disconnect();
      socketRef.current = null;
    }
    
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
  }, []);

  const sendMessage = useCallback((type: string, data: any) => {
    if (socketRef.current?.connected) {
      socketRef.current.emit('message', { type, data });
    } else {
      console.warn('WebSocket not connected, cannot send message');
    }
  }, []);

  const joinRoom = useCallback((room: string) => {
    if (socketRef.current?.connected) {
      socketRef.current.emit('join_room', room);
    }
  }, []);

  const leaveRoom = useCallback((room: string) => {
    if (socketRef.current?.connected) {
      socketRef.current.emit('leave_room', room);
    }
  }, []);

  // Auto-connect on mount
  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  // Handle page visibility changes
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.hidden) {
        // Page is hidden, disconnect to save resources
        disconnect();
      } else {
        // Page is visible, reconnect
        connect();
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [connect, disconnect]);

  // Handle online/offline events
  useEffect(() => {
    const handleOnline = () => {
      console.log('Network online, reconnecting WebSocket');
      connect();
    };

    const handleOffline = () => {
      console.log('Network offline, disconnecting WebSocket');
      disconnect();
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [connect, disconnect]);

  return {
    isConnected: socketRef.current?.connected || false,
    connect,
    disconnect,
    sendMessage,
    joinRoom,
    leaveRoom,
  };
}

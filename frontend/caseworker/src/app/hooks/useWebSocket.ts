'use client';

import { useEffect, useRef, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';
import { toast } from 'react-hot-toast';

interface WebSocketMessage {
  type: string;
  data: any;
  timestamp: string;
}

interface WebSocketOptions {
  onMessage?: (message: WebSocketMessage) => void;
  onConnect?: () => void;
  onDisconnect?: () => void;
  onError?: (error: Error) => void;
}

export function useWebSocket(options: WebSocketOptions = {}) {
  const socketRef = useRef<Socket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = 5;
  const reconnectDelay = 1000; // Start with 1 second

  const connect = useCallback(() => {
    if (socketRef.current?.connected) {
      return;
    }

    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';
    const token = localStorage.getItem('access_token');

    socketRef.current = io(wsUrl, {
      auth: {
        token: token || undefined,
      },
      transports: ['websocket', 'polling'],
      timeout: 20000,
      forceNew: true,
    });

    const socket = socketRef.current;

    socket.on('connect', () => {
      console.log('WebSocket connected');
      reconnectAttempts.current = 0;
      options.onConnect?.();
    });

    socket.on('disconnect', (reason) => {
      console.log('WebSocket disconnected:', reason);
      options.onDisconnect?.();
      
      // Attempt to reconnect if not manually disconnected
      if (reason !== 'io client disconnect') {
        scheduleReconnect();
      }
    });

    socket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error);
      options.onError?.(error);
      scheduleReconnect();
    });

    socket.on('error', (error) => {
      console.error('WebSocket error:', error);
      options.onError?.(error);
    });

    // Listen for specific message types
    socket.on('message', (message: WebSocketMessage) => {
      console.log('WebSocket message received:', message);
      options.onMessage?.(message);
    });

    // Listen for crisis alerts
    socket.on('crisis_alert', (data) => {
      console.log('Crisis alert received:', data);
      options.onMessage?.({
        type: 'crisis_alert',
        data,
        timestamp: new Date().toISOString(),
      });
    });

    // Listen for case updates
    socket.on('case_update', (data) => {
      console.log('Case update received:', data);
      options.onMessage?.({
        type: 'case_update',
        data,
        timestamp: new Date().toISOString(),
      });
    });

    // Listen for notifications
    socket.on('notification', (data) => {
      console.log('Notification received:', data);
      options.onMessage?.({
        type: 'notification',
        data,
        timestamp: new Date().toISOString(),
      });
    });

    // Listen for system status updates
    socket.on('system_status', (data) => {
      console.log('System status update:', data);
      options.onMessage?.({
        type: 'system_status',
        data,
        timestamp: new Date().toISOString(),
      });
    });

  }, [options]);

  const scheduleReconnect = useCallback(() => {
    if (reconnectAttempts.current >= maxReconnectAttempts) {
      console.log('Max reconnection attempts reached');
      toast.error('Connection lost. Please refresh the page.');
      return;
    }

    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }

    const delay = reconnectDelay * Math.pow(2, reconnectAttempts.current);
    reconnectAttempts.current++;

    console.log(`Attempting to reconnect in ${delay}ms (attempt ${reconnectAttempts.current})`);

    reconnectTimeoutRef.current = setTimeout(() => {
      connect();
    }, delay);
  }, [connect]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }

    if (socketRef.current) {
      socketRef.current.disconnect();
      socketRef.current = null;
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

  const isConnected = useCallback(() => {
    return socketRef.current?.connected || false;
  }, []);

  // Connect on mount
  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, []);

  return {
    connect,
    disconnect,
    sendMessage,
    joinRoom,
    leaveRoom,
    isConnected,
  };
}

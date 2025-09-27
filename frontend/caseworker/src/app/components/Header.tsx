'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Bell, Settings, LogOut, User, Wifi, WifiOff } from 'lucide-react';
import { cn } from '../lib/utils';

interface HeaderProps {
  user: any;
  isAuthenticated: boolean;
  onLogin: () => void;
  onLogout: () => void;
  language: string;
  onLanguageChange: (lang: string) => void;
  isOnline: boolean;
}

export function Header({ 
  user, 
  isAuthenticated, 
  onLogin, 
  onLogout, 
  language, 
  onLanguageChange, 
  isOnline 
}: HeaderProps) {
  return (
    <header className="bg-white shadow-sm border-b border-neutral-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center space-x-3"
            >
              <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">FC</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-primary-900">
                  First Contact EIS
                </h1>
                <p className="text-sm text-neutral-500">
                  Caseworker Portal
                </p>
              </div>
            </motion.div>
          </div>

          {/* Right side */}
          <div className="flex items-center space-x-4">
            {/* Online Status */}
            <div className={cn(
              "flex items-center space-x-2 px-3 py-1 rounded-full text-sm",
              isOnline 
                ? "bg-success-100 text-success-700" 
                : "bg-error-100 text-error-700"
            )}>
              {isOnline ? (
                <Wifi className="w-4 h-4" />
              ) : (
                <WifiOff className="w-4 h-4" />
              )}
              <span>{isOnline ? 'Online' : 'Offline'}</span>
            </div>

            {/* Language Selector */}
            <select
              value={language}
              onChange={(e) => onLanguageChange(e.target.value)}
              className="px-3 py-1 border border-neutral-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="en">English</option>
              <option value="es">Español</option>
              <option value="km">ខ្មែរ</option>
              <option value="tl">Tagalog</option>
              <option value="ko">한국어</option>
            </select>

            {/* User Menu */}
            {isAuthenticated ? (
              <div className="flex items-center space-x-3">
                <button className="p-2 text-neutral-500 hover:text-neutral-700 transition-colors">
                  <Bell className="w-5 h-5" />
                </button>
                <button className="p-2 text-neutral-500 hover:text-neutral-700 transition-colors">
                  <Settings className="w-5 h-5" />
                </button>
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                    <User className="w-5 h-5 text-primary-600" />
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-neutral-900">
                      {user?.first_name} {user?.last_name}
                    </p>
                    <p className="text-xs text-neutral-500">
                      {user?.role}
                    </p>
                  </div>
                  <button
                    onClick={onLogout}
                    className="p-2 text-neutral-500 hover:text-error-600 transition-colors"
                    title="Logout"
                  >
                    <LogOut className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ) : (
              <button
                onClick={onLogin}
                className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
              >
                Login
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}

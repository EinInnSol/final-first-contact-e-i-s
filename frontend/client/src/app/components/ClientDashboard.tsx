'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { 
  MessageCircle, 
  FileText, 
  Calendar, 
  MapPin, 
  Phone, 
  Mail, 
  User, 
  Settings,
  Bell,
  Search,
  Filter,
  Plus,
  ChevronRight,
  AlertTriangle,
  CheckCircle,
  Clock,
  Star
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import { cn } from '../lib/utils';
import { useAuth } from '../hooks/useAuth';
import { useLanguage } from '../hooks/useLanguage';
import { useWebSocket } from '../hooks/useWebSocket';
import { AIChat } from './AIChat';
import { CaseManagement } from './CaseManagement';
import { ServiceRequests } from './ServiceRequests';
import { ResourceDirectory } from './ResourceDirectory';
import { ProfileSettings } from './ProfileSettings';
import { Notifications } from './Notifications';
import { CrisisAlert } from './CrisisAlert';

interface ClientDashboardProps {
  user: any;
  language: string;
  t: (key: string) => string;
}

export function ClientDashboard({ user, language, t }: ClientDashboardProps) {
  const [activeTab, setActiveTab] = useState('chat');
  const [crisisDetected, setCrisisDetected] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const { t: translate } = useLanguage();
  const queryClient = useQueryClient();

  // WebSocket connection for real-time updates
  useWebSocket({
    onMessage: (message) => {
      if (message.type === 'crisis_alert') {
        setCrisisDetected(true);
        toast.error(t('crisis.alert_detected'));
      } else if (message.type === 'notification') {
        setNotifications(prev => [...prev, message.data]);
        toast.success(t('notifications.new_notification'));
      } else if (message.type === 'case_update') {
        queryClient.invalidateQueries(['cases']);
        toast.info(t('cases.updated'));
      }
    }
  });

  // Fetch user data
  const { data: userData, isLoading: userLoading } = useQuery({
    queryKey: ['user', user?.id],
    queryFn: async () => {
      const response = await fetch('/api/v1/auth/me', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      if (!response.ok) throw new Error('Failed to fetch user data');
      return response.json();
    },
    enabled: !!user?.id
  });

  // Fetch cases
  const { data: cases, isLoading: casesLoading } = useQuery({
    queryKey: ['cases', user?.id],
    queryFn: async () => {
      const response = await fetch(`/api/v1/cases?client_id=${user?.id}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      if (!response.ok) throw new Error('Failed to fetch cases');
      return response.json();
    },
    enabled: !!user?.id
  });

  // Fetch resources
  const { data: resources, isLoading: resourcesLoading } = useQuery({
    queryKey: ['resources'],
    queryFn: async () => {
      const response = await fetch('/api/v1/resources', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      if (!response.ok) throw new Error('Failed to fetch resources');
      return response.json();
    }
  });

  const tabs = [
    { id: 'chat', label: t('tabs.ai_chat'), icon: MessageCircle },
    { id: 'cases', label: t('tabs.my_cases'), icon: FileText },
    { id: 'services', label: t('tabs.service_requests'), icon: Calendar },
    { id: 'resources', label: t('tabs.resources'), icon: MapPin },
    { id: 'profile', label: t('tabs.profile'), icon: User },
    { id: 'settings', label: t('tabs.settings'), icon: Settings }
  ];

  const handleCrisisResolved = () => {
    setCrisisDetected(false);
    toast.success(t('crisis.resolved'));
  };

  if (userLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Crisis Alert */}
      <AnimatePresence>
        {crisisDetected && (
          <CrisisAlert
            onResolve={handleCrisisResolved}
            t={t}
          />
        )}
      </AnimatePresence>

      {/* Header */}
      <div className="bg-white shadow-sm border-b border-neutral-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary-900">
                {t('dashboard.title')}
              </h1>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* Notifications */}
              <Notifications 
                notifications={notifications}
                onClear={() => setNotifications([])}
                t={t}
              />
              
              {/* User Menu */}
              <div className="flex items-center space-x-3">
                <div className="text-right">
                  <p className="text-sm font-medium text-neutral-900">
                    {userData?.first_name} {userData?.last_name}
                  </p>
                  <p className="text-xs text-neutral-500">
                    {t('dashboard.welcome_back')}
                  </p>
                </div>
                <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                  <User className="w-5 h-5 text-primary-600" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b border-neutral-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={cn(
                    "flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-200",
                    activeTab === tab.id
                      ? "border-primary-500 text-primary-600"
                      : "border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300"
                  )}
                >
                  <Icon className="w-5 h-5" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            {activeTab === 'chat' && (
              <AIChat 
                user={user}
                language={language}
                t={t}
              />
            )}
            
            {activeTab === 'cases' && (
              <CaseManagement 
                cases={cases}
                isLoading={casesLoading}
                user={user}
                t={t}
              />
            )}
            
            {activeTab === 'services' && (
              <ServiceRequests 
                user={user}
                t={t}
              />
            )}
            
            {activeTab === 'resources' && (
              <ResourceDirectory 
                resources={resources}
                isLoading={resourcesLoading}
                t={t}
              />
            )}
            
            {activeTab === 'profile' && (
              <ProfileSettings 
                user={userData}
                t={t}
              />
            )}
            
            {activeTab === 'settings' && (
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-semibold text-neutral-900 mb-4">
                  {t('settings.title')}
                </h2>
                <p className="text-neutral-600">
                  {t('settings.coming_soon')}
                </p>
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}

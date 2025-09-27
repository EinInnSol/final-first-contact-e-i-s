'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { 
  Users, 
  FileText, 
  Calendar, 
  BarChart3, 
  Settings,
  Bell,
  Search,
  Filter,
  Plus,
  ChevronRight,
  AlertTriangle,
  CheckCircle,
  Clock,
  Star,
  Bot,
  Shield,
  TrendingUp
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import { cn } from '../lib/utils';
import { useAuth } from '../hooks/useAuth';
import { useLanguage } from '../hooks/useLanguage';
import { useWebSocket } from '../hooks/useWebSocket';
import { CaseManagement } from './CaseManagement';
import { ClientList } from './ClientList';
import { AIAssistant } from './AIAssistant';
import { ComplianceDashboard } from './ComplianceDashboard';
import { Notifications } from './Notifications';
import { CrisisAlert } from './CrisisAlert';
import { PerformanceMetrics } from './PerformanceMetrics';

interface CaseworkerDashboardProps {
  user: any;
  language: string;
  t: (key: string) => string;
}

export function CaseworkerDashboard({ user, language, t }: CaseworkerDashboardProps) {
  const [activeTab, setActiveTab] = useState('cases');
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
      const response = await fetch(`/api/v1/cases?assigned_user_id=${user?.id}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      if (!response.ok) throw new Error('Failed to fetch cases');
      return response.json();
    },
    enabled: !!user?.id
  });

  // Fetch clients
  const { data: clients, isLoading: clientsLoading } = useQuery({
    queryKey: ['clients'],
    queryFn: async () => {
      const response = await fetch('/api/v1/clients', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      if (!response.ok) throw new Error('Failed to fetch clients');
      return response.json();
    }
  });

  // Fetch performance metrics
  const { data: metrics, isLoading: metricsLoading } = useQuery({
    queryKey: ['metrics', user?.id],
    queryFn: async () => {
      const response = await fetch(`/api/v1/analytics/performance?user_id=${user?.id}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      if (!response.ok) throw new Error('Failed to fetch metrics');
      return response.json();
    },
    enabled: !!user?.id
  });

  const tabs = [
    { id: 'cases', label: t('tabs.case_management'), icon: FileText },
    { id: 'clients', label: t('tabs.clients'), icon: Users },
    { id: 'ai', label: t('tabs.ai_assistant'), icon: Bot },
    { id: 'compliance', label: t('tabs.compliance'), icon: Shield },
    { id: 'metrics', label: t('tabs.performance'), icon: BarChart3 },
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
                  <Users className="w-5 h-5 text-primary-600" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="bg-white border-b border-neutral-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-primary-50 rounded-lg p-4">
              <div className="flex items-center">
                <FileText className="w-8 h-8 text-primary-600" />
                <div className="ml-3">
                  <p className="text-sm font-medium text-primary-600">Active Cases</p>
                  <p className="text-2xl font-bold text-primary-900">
                    {cases?.items?.filter(c => c.status === 'open' || c.status === 'in_progress').length || 0}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-secondary-50 rounded-lg p-4">
              <div className="flex items-center">
                <Users className="w-8 h-8 text-secondary-600" />
                <div className="ml-3">
                  <p className="text-sm font-medium text-secondary-600">Total Clients</p>
                  <p className="text-2xl font-bold text-secondary-900">
                    {clients?.items?.length || 0}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-warning-50 rounded-lg p-4">
              <div className="flex items-center">
                <Clock className="w-8 h-8 text-warning-600" />
                <div className="ml-3">
                  <p className="text-sm font-medium text-warning-600">Pending Tasks</p>
                  <p className="text-2xl font-bold text-warning-900">
                    {cases?.items?.filter(c => c.status === 'open').length || 0}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-success-50 rounded-lg p-4">
              <div className="flex items-center">
                <TrendingUp className="w-8 h-8 text-success-600" />
                <div className="ml-3">
                  <p className="text-sm font-medium text-success-600">Success Rate</p>
                  <p className="text-2xl font-bold text-success-900">
                    {metrics?.success_rate || 0}%
                  </p>
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
            {activeTab === 'cases' && (
              <CaseManagement 
                cases={cases}
                isLoading={casesLoading}
                user={user}
                t={t}
              />
            )}
            
            {activeTab === 'clients' && (
              <ClientList 
                clients={clients}
                isLoading={clientsLoading}
                t={t}
              />
            )}
            
            {activeTab === 'ai' && (
              <AIAssistant 
                user={user}
                language={language}
                t={t}
              />
            )}
            
            {activeTab === 'compliance' && (
              <ComplianceDashboard 
                user={user}
                t={t}
              />
            )}
            
            {activeTab === 'metrics' && (
              <PerformanceMetrics 
                metrics={metrics}
                isLoading={metricsLoading}
                user={user}
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

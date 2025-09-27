'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useMutation } from '@tanstack/react-query';
import { 
  FileText, 
  User, 
  Calendar, 
  Target, 
  CheckCircle, 
  Clock, 
  AlertTriangle,
  Bot,
  Sparkles,
  Download,
  Share,
  Edit,
  Trash2
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import { cn } from '../lib/utils';

interface CarePlan {
  id: string;
  client_id: string;
  client_name: string;
  goals: CareGoal[];
  interventions: Intervention[];
  timeline: string;
  status: 'draft' | 'active' | 'completed' | 'archived';
  created_at: string;
  updated_at: string;
  ai_generated: boolean;
  ai_confidence: number;
}

interface CareGoal {
  id: string;
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  target_date: string;
  status: 'not_started' | 'in_progress' | 'completed' | 'cancelled';
  progress: number;
}

interface Intervention {
  id: string;
  title: string;
  description: string;
  type: 'service' | 'referral' | 'follow_up' | 'assessment';
  provider: string;
  scheduled_date: string;
  status: 'scheduled' | 'completed' | 'cancelled' | 'rescheduled';
}

interface CarePlanGeneratorProps {
  clientId: string;
  clientName: string;
  onPlanGenerated?: (plan: CarePlan) => void;
  onPlanUpdated?: (plan: CarePlan) => void;
  language?: string;
  t?: (key: string) => string;
}

export function CarePlanGenerator({ 
  clientId, 
  clientName, 
  onPlanGenerated, 
  onPlanUpdated,
  language = 'en',
  t = (key: string) => key
}: CarePlanGeneratorProps) {
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentPlan, setCurrentPlan] = useState<CarePlan | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editingGoal, setEditingGoal] = useState<CareGoal | null>(null);

  // Generate care plan mutation
  const generatePlanMutation = useMutation({
    mutationFn: async (clientData: any) => {
      const response = await fetch('/api/v1/ai/generate-care-plan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          client_id: clientId,
          client_data: clientData,
          language: language
        })
      });

      if (!response.ok) {
        throw new Error('Failed to generate care plan');
      }

      return response.json();
    },
    onSuccess: (data) => {
      setCurrentPlan(data);
      onPlanGenerated?.(data);
      toast.success(t('care_plan.generated_successfully'));
    },
    onError: (error) => {
      console.error('Failed to generate care plan:', error);
      toast.error(t('care_plan.generation_failed'));
    }
  });

  // Update care plan mutation
  const updatePlanMutation = useMutation({
    mutationFn: async (planData: Partial<CarePlan>) => {
      const response = await fetch(`/api/v1/care-plans/${currentPlan?.id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(planData)
      });

      if (!response.ok) {
        throw new Error('Failed to update care plan');
      }

      return response.json();
    },
    onSuccess: (data) => {
      setCurrentPlan(data);
      onPlanUpdated?.(data);
      toast.success(t('care_plan.updated_successfully'));
    },
    onError: (error) => {
      console.error('Failed to update care plan:', error);
      toast.error(t('care_plan.update_failed'));
    }
  });

  const handleGeneratePlan = async () => {
    setIsGenerating(true);
    try {
      // Get client data
      const clientResponse = await fetch(`/api/v1/clients/${clientId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      
      if (!clientResponse.ok) {
        throw new Error('Failed to fetch client data');
      }
      
      const clientData = await clientResponse.json();
      await generatePlanMutation.mutateAsync(clientData);
    } catch (error) {
      console.error('Error generating care plan:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleUpdateGoal = (goalId: string, updates: Partial<CareGoal>) => {
    if (!currentPlan) return;

    const updatedGoals = currentPlan.goals.map(goal =>
      goal.id === goalId ? { ...goal, ...updates } : goal
    );

    updatePlanMutation.mutate({
      goals: updatedGoals
    });
  };

  const handleAddIntervention = (intervention: Omit<Intervention, 'id'>) => {
    if (!currentPlan) return;

    const newIntervention: Intervention = {
      ...intervention,
      id: Math.random().toString(36).substr(2, 9)
    };

    updatePlanMutation.mutate({
      interventions: [...currentPlan.interventions, newIntervention]
    });
  };

  const handleExportPlan = () => {
    if (!currentPlan) return;

    const planData = {
      client_name: currentPlan.client_name,
      goals: currentPlan.goals,
      interventions: currentPlan.interventions,
      timeline: currentPlan.timeline,
      generated_at: new Date().toISOString()
    };

    const dataStr = JSON.stringify(planData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `care-plan-${clientName}-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
            <FileText className="w-6 h-6 text-primary-600" />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-neutral-900">
              {t('care_plan.title')}
            </h2>
            <p className="text-sm text-neutral-500">
              {t('care_plan.for_client')}: {clientName}
            </p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {currentPlan && (
            <>
              <button
                onClick={handleExportPlan}
                className="p-2 text-neutral-500 hover:text-primary-600 transition-colors"
                title={t('care_plan.export')}
              >
                <Download className="w-5 h-5" />
              </button>
              <button
                onClick={() => setIsEditing(!isEditing)}
                className="p-2 text-neutral-500 hover:text-primary-600 transition-colors"
                title={t('care_plan.edit')}
              >
                <Edit className="w-5 h-5" />
              </button>
            </>
          )}
        </div>
      </div>

      {/* Generate Button */}
      {!currentPlan && (
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Bot className="w-8 h-8 text-primary-600" />
          </div>
          <h3 className="text-lg font-semibold text-neutral-900 mb-2">
            {t('care_plan.generate_title')}
          </h3>
          <p className="text-neutral-600 mb-6">
            {t('care_plan.generate_description')}
          </p>
          <button
            onClick={handleGeneratePlan}
            disabled={isGenerating}
            className="bg-primary-600 hover:bg-primary-700 disabled:bg-primary-300 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center space-x-2 mx-auto"
          >
            {isGenerating ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>{t('care_plan.generating')}</span>
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                <span>{t('care_plan.generate')}</span>
              </>
            )}
          </button>
        </div>
      )}

      {/* Care Plan Content */}
      <AnimatePresence>
        {currentPlan && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="space-y-6"
          >
            {/* AI Confidence Indicator */}
            {currentPlan.ai_generated && (
              <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
                <div className="flex items-center space-x-2">
                  <Bot className="w-5 h-5 text-primary-600" />
                  <span className="text-sm font-medium text-primary-700">
                    {t('care_plan.ai_generated')}
                  </span>
                  <div className="flex-1 bg-primary-200 rounded-full h-2">
                    <div 
                      className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${currentPlan.ai_confidence * 100}%` }}
                    />
                  </div>
                  <span className="text-sm text-primary-600">
                    {Math.round(currentPlan.ai_confidence * 100)}%
                  </span>
                </div>
              </div>
            )}

            {/* Goals Section */}
            <div>
              <h3 className="text-lg font-semibold text-neutral-900 mb-4 flex items-center space-x-2">
                <Target className="w-5 h-5" />
                <span>{t('care_plan.goals')}</span>
              </h3>
              
              <div className="space-y-4">
                {currentPlan.goals.map((goal) => (
                  <motion.div
                    key={goal.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-neutral-50 rounded-lg p-4 border border-neutral-200"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <h4 className="font-medium text-neutral-900">{goal.title}</h4>
                          <span className={cn(
                            "px-2 py-1 rounded-full text-xs font-medium",
                            goal.priority === 'high' && "bg-error-100 text-error-700",
                            goal.priority === 'medium' && "bg-warning-100 text-warning-700",
                            goal.priority === 'low' && "bg-success-100 text-success-700"
                          )}>
                            {t(`care_plan.priority.${goal.priority}`)}
                          </span>
                        </div>
                        <p className="text-sm text-neutral-600 mb-3">{goal.description}</p>
                        
                        {/* Progress Bar */}
                        <div className="flex items-center space-x-2">
                          <div className="flex-1 bg-neutral-200 rounded-full h-2">
                            <div 
                              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                              style={{ width: `${goal.progress}%` }}
                            />
                          </div>
                          <span className="text-sm text-neutral-500">{goal.progress}%</span>
                        </div>
                        
                        <div className="flex items-center space-x-4 mt-2 text-xs text-neutral-500">
                          <span className="flex items-center space-x-1">
                            <Calendar className="w-3 h-3" />
                            <span>{t('care_plan.target_date')}: {goal.target_date}</span>
                          </span>
                          <span className={cn(
                            "flex items-center space-x-1",
                            goal.status === 'completed' && "text-success-600",
                            goal.status === 'in_progress' && "text-primary-600",
                            goal.status === 'cancelled' && "text-error-600"
                          )}>
                            {goal.status === 'completed' && <CheckCircle className="w-3 h-3" />}
                            {goal.status === 'in_progress' && <Clock className="w-3 h-3" />}
                            {goal.status === 'cancelled' && <AlertTriangle className="w-3 h-3" />}
                            <span>{t(`care_plan.status.${goal.status}`)}</span>
                          </span>
                        </div>
                      </div>
                      
                      {isEditing && (
                        <button
                          onClick={() => setEditingGoal(goal)}
                          className="p-2 text-neutral-400 hover:text-primary-600 transition-colors"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* Interventions Section */}
            <div>
              <h3 className="text-lg font-semibold text-neutral-900 mb-4 flex items-center space-x-2">
                <Calendar className="w-5 h-5" />
                <span>{t('care_plan.interventions')}</span>
              </h3>
              
              <div className="space-y-3">
                {currentPlan.interventions.map((intervention) => (
                  <motion.div
                    key={intervention.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-neutral-50 rounded-lg p-4 border border-neutral-200"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <h4 className="font-medium text-neutral-900">{intervention.title}</h4>
                          <span className="px-2 py-1 bg-primary-100 text-primary-700 rounded-full text-xs font-medium">
                            {t(`care_plan.intervention_type.${intervention.type}`)}
                          </span>
                        </div>
                        <p className="text-sm text-neutral-600 mb-2">{intervention.description}</p>
                        <div className="flex items-center space-x-4 text-xs text-neutral-500">
                          <span>{t('care_plan.provider')}: {intervention.provider}</span>
                          <span>{t('care_plan.scheduled_date')}: {intervention.scheduled_date}</span>
                          <span className={cn(
                            intervention.status === 'completed' && "text-success-600",
                            intervention.status === 'scheduled' && "text-primary-600",
                            intervention.status === 'cancelled' && "text-error-600"
                          )}>
                            {t(`care_plan.intervention_status.${intervention.status}`)}
                          </span>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* Timeline */}
            <div>
              <h3 className="text-lg font-semibold text-neutral-900 mb-4 flex items-center space-x-2">
                <Clock className="w-5 h-5" />
                <span>{t('care_plan.timeline')}</span>
              </h3>
              <div className="bg-neutral-50 rounded-lg p-4 border border-neutral-200">
                <p className="text-sm text-neutral-600">{currentPlan.timeline}</p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

/**
 * API Hooks for Orchestration
 * Connects frontend to the Brain's recommendation system
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Types
interface Recommendation {
  recommendation_id: string;
  summary: string;
  reasoning: string[];
  impact: {
    cost_savings?: number;
    urgency_improvement?: string;
    efficiency_gain?: number;
  };
  confidence_score: number;
  actions_count: number;
  estimated_duration_seconds: number;
  affected_systems: string[];
  status: 'pending_approval' | 'approved' | 'rejected' | 'executing' | 'completed';
  created_at: string;
}

/**
 * Hook to fetch recommendations from orchestration API
 */
export function useRecommendations() {
  return useQuery<Recommendation[]>({
    queryKey: ['recommendations'],
    queryFn: async () => {
      const response = await fetch(`${API_BASE_URL}/orchestration/recommendations`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
      }

      return response.json();
    },
    refetchInterval: 5000, // Poll every 5 seconds for new recommendations
    staleTime: 0, // Always consider stale so we refetch
  });
}

/**
 * Hook to approve a recommendation
 */
export function useApproveRecommendation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (recommendationId: string) => {
      const response = await fetch(
        `${API_BASE_URL}/orchestration/recommendations/${recommendationId}/approve`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
          body: JSON.stringify({
            approved_by: localStorage.getItem('user_id') || 'caseworker',
          }),
        }
      );

      if (!response.ok) {
        throw new Error('Failed to approve recommendation');
      }

      return response.json();
    },
    onSuccess: (data, recommendationId) => {
      // Invalidate and refetch recommendations
      queryClient.invalidateQueries({ queryKey: ['recommendations'] });
      
      toast.success('Recommendation approved! Executing actions...', {
        duration: 3000,
        icon: '✅',
      });
    },
    onError: (error) => {
      toast.error('Failed to approve recommendation. Please try again.', {
        duration: 5000,
      });
      console.error('Approval error:', error);
    },
  });
}

/**
 * Hook to reject a recommendation
 */
export function useRejectRecommendation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (recommendationId: string) => {
      const response = await fetch(
        `${API_BASE_URL}/orchestration/recommendations/${recommendationId}/reject`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error('Failed to reject recommendation');
      }

      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['recommendations'] });
      toast.success('Recommendation rejected', {
        icon: '❌',
      });
    },
    onError: (error) => {
      toast.error('Failed to reject recommendation');
      console.error('Rejection error:', error);
    },
  });
}

/**
 * Hook to trigger a manual event (for demo/testing)
 */
export function useTriggerEvent() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (eventData: {
      event_type: string;
      client_id?: string;
      provider_id?: string;
      metadata?: Record<string, any>;
    }) => {
      const response = await fetch(
        `${API_BASE_URL}/orchestration/trigger-event`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
          body: JSON.stringify(eventData),
        }
      );

      if (!response.ok) {
        throw new Error('Failed to trigger event');
      }

      return response.json();
    },
    onSuccess: (data) => {
      // Invalidate recommendations to fetch the new one
      queryClient.invalidateQueries({ queryKey: ['recommendations'] });
      
      toast.success('Event triggered! New recommendation incoming...', {
        duration: 3000,
        icon: '⚡',
      });
    },
    onError: (error) => {
      toast.error('Failed to trigger event');
      console.error('Event trigger error:', error);
    },
  });
}

/**
 * Hook to get orchestration statistics
 */
export function useOrchestrationStats() {
  return useQuery({
    queryKey: ['orchestration-stats'],
    queryFn: async () => {
      const response = await fetch(`${API_BASE_URL}/orchestration/statistics`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch statistics');
      }

      return response.json();
    },
    refetchInterval: 30000, // Refetch every 30 seconds
  });
}

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Poll recommendations every 5 seconds
export function useRecommendations() {
  return useQuery({
    queryKey: ['recommendations'],
    queryFn: async () => {
      const res = await fetch(`${API_URL}/api/v1/orchestration/recommendations`)
      if (!res.ok) throw new Error('Failed to fetch recommendations')
      return res.json()
    },
    refetchInterval: 5000, // Auto-poll every 5s
  })
}

// Approve recommendation
export function useApproveRecommendation() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (recommendationId: string) => {
      const res = await fetch(
        `${API_URL}/api/v1/orchestration/recommendations/${recommendationId}/approve`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ approved_by: 'caseworker_demo' })
        }
      )
      if (!res.ok) throw new Error('Approval failed')
      return res.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['recommendations'] })
    }
  })
}

// Reject recommendation
export function useRejectRecommendation() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (recommendationId: string) => {
      const res = await fetch(
        `${API_URL}/api/v1/orchestration/recommendations/${recommendationId}/reject`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        }
      )
      if (!res.ok) throw new Error('Rejection failed')
      return res.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['recommendations'] })
    }
  })
}

// Trigger demo event
export function useTriggerDemoEvent() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async () => {
      const res = await fetch(`${API_URL}/api/v1/orchestration/trigger-event`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          event_type: 'appointment_cancelled',
          client_id: 'maria_demo_001',
          provider_id: 'dr_smith_001',
          metadata: {
            appointment_time: new Date(Date.now() + 86400000).toISOString(), // tomorrow
            reason: 'client_cancellation'
          }
        })
      })
      if (!res.ok) throw new Error('Failed to trigger event')
      return res.json()
    },
    onSuccess: () => {
      // Refetch recommendations after triggering
      setTimeout(() => {
        queryClient.invalidateQueries({ queryKey: ['recommendations'] })
      }, 2000)
    }
  })
}

// Also export as useTriggerEvent for compatibility
export const useTriggerEvent = useTriggerDemoEvent;

"use client"

import { useRecommendations, useApproveRecommendation, useRejectRecommendation, useTriggerDemoEvent } from '../hooks/useOrchestration'
import { Clock, DollarSign, Users, Zap, CheckCircle, XCircle, AlertCircle } from 'lucide-react'

export default function RecommendationsFeed() {
  const { data: recommendations, isLoading } = useRecommendations()
  const approveMutation = useApproveRecommendation()
  const rejectMutation = useRejectRecommendation()
  const triggerDemo = useTriggerDemoEvent()

  if (isLoading) {
    return <div className="animate-pulse">Loading recommendations...</div>
  }

  return (
    <div className="space-y-6">
      {/* Demo Trigger Button */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-yellow-900">Demo Mode</h3>
            <p className="text-sm text-yellow-700">Trigger Maria cancellation scenario</p>
          </div>
          <button
            onClick={() => triggerDemo.mutate()}
            disabled={triggerDemo.isPending}
            className="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 disabled:opacity-50"
          >
            {triggerDemo.isPending ? 'Triggering...' : 'Trigger Demo Event'}
          </button>
        </div>
      </div>

      {/* Recommendations List */}
      {(!recommendations || recommendations.length === 0) ? (
        <div className="text-center py-12 text-gray-500">
          <AlertCircle className="mx-auto h-12 w-12 mb-4" />
          <p className="text-lg font-medium">All Caught Up!</p>
          <p className="text-sm">No new recommendations</p>
        </div>
      ) : (
        <div className="space-y-4">
          {recommendations.map((rec) => (
            <RecommendationCard
              key={rec.recommendation_id}
              recommendation={rec}
              onApprove={() => approveMutation.mutate(rec.recommendation_id)}
              onReject={() => rejectMutation.mutate(rec.recommendation_id)}
            />
          ))}
        </div>
      )}
    </div>
  )
}

function RecommendationCard({ recommendation, onApprove, onReject }) {
  const { summary, reasoning, impact, confidence_score, actions_count, estimated_duration_seconds, status } = recommendation

  return (
    <div className="border border-gray-200 rounded-lg p-6 bg-white shadow-sm">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-2">
          <Zap className="h-5 w-5 text-blue-600" />
          <h3 className="font-semibold text-lg">OPTIMIZATION OPPORTUNITY</h3>
        </div>
      </div>

      <p className="text-xl font-medium text-gray-900 mb-4">{summary}</p>

      {/* Metrics */}
      <div className="grid grid-cols-4 gap-4 mb-4">
        <div className="flex items-center gap-2">
          <DollarSign className="h-4 w-4 text-green-600" />
          <div>
            <p className="text-xs text-gray-500">Savings</p>
            <p className="font-semibold">${impact.cost_savings || 0}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Users className="h-4 w-4 text-blue-600" />
          <div>
            <p className="text-xs text-gray-500">Actions</p>
            <p className="font-semibold">{actions_count}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Clock className="h-4 w-4 text-purple-600" />
          <div>
            <p className="text-xs text-gray-500">Duration</p>
            <p className="font-semibold">{estimated_duration_seconds}s</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Zap className="h-4 w-4 text-yellow-600" />
          <div>
            <p className="text-xs text-gray-500">Confidence</p>
            <p className="font-semibold">{Math.round(confidence_score * 100)}%</p>
          </div>
        </div>
      </div>

      {/* Reasoning */}
      <div className="bg-gray-50 rounded-lg p-4 mb-4">
        <p className="text-sm font-medium mb-2">Reasoning:</p>
        <ul className="space-y-1">
          {reasoning.map((reason, i) => (
            <li key={i} className="text-sm text-gray-600">• {reason}</li>
          ))}
        </ul>
      </div>

      {/* Buttons */}
      {status === 'pending_approval' && (
        <div className="flex gap-3">
          <button
            onClick={onApprove}
            className="flex-1 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium"
          >
            ✓ APPROVE
          </button>
          <button
            onClick={onReject}
            className="px-4 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium"
          >
            ✗ REJECT
          </button>
        </div>
      )}

      {status === 'completed' && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-3 text-sm text-green-800">
          ✓ Successfully completed
        </div>
      )}
    </div>
  )
}

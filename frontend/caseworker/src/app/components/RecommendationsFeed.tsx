"use client"

import { useRecommendations, useApproveRecommendation, useRejectRecommendation, useTriggerDemoEvent } from '../hooks/useOrchestration'
import { Clock, DollarSign, Users, Zap, CheckCircle, XCircle, AlertCircle, Activity } from 'lucide-react'

export function RecommendationsFeed() {
  const { data: recommendations, isLoading } = useRecommendations()
  const approveMutation = useApproveRecommendation()
  const rejectMutation = useRejectRecommendation()
  const triggerDemo = useTriggerDemoEvent()

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <span className="ml-3 text-neutral-600">Loading recommendations...</span>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Demo Trigger Card */}
      <div className="bg-gradient-to-r from-warning-50 to-warning-100 border border-warning-300 rounded-lg shadow-sm">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-warning-500 rounded-lg flex items-center justify-center">
                <Activity className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="font-semibold text-neutral-900">Demo Mode Active</h3>
                <p className="text-sm text-neutral-600">Trigger appointment cancellation scenario</p>
              </div>
            </div>
            <button
              onClick={() => triggerDemo.mutate()}
              disabled={triggerDemo.isPending}
              className="px-6 py-3 bg-warning-600 text-white rounded-lg hover:bg-warning-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold transition-all shadow-sm hover:shadow-md"
            >
              {triggerDemo.isPending ? 'Triggering...' : 'Trigger Demo Event'}
            </button>
          </div>
        </div>
      </div>

      {/* Recommendations List */}
      {(!recommendations || recommendations.length === 0) ? (
        <div className="bg-white border border-neutral-200 rounded-lg shadow-sm">
          <div className="text-center py-16">
            <div className="w-16 h-16 bg-success-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <CheckCircle className="w-8 h-8 text-success-600" />
            </div>
            <p className="text-xl font-semibold text-neutral-900 mb-2">All Caught Up!</p>
            <p className="text-neutral-500">No new recommendations at this time</p>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          {recommendations.map((rec) => (
            <RecommendationCard
              key={rec.recommendation_id}
              recommendation={rec}
              onApprove={() => approveMutation.mutate(rec.recommendation_id)}
              onReject={() => rejectMutation.mutate(rec.recommendation_id)}
              isApproving={approveMutation.isPending}
              isRejecting={rejectMutation.isPending}
            />
          ))}
        </div>
      )}
    </div>
  )
}

function RecommendationCard({ recommendation, onApprove, onReject, isApproving, isRejecting }) {
  const { 
    summary, 
    reasoning, 
    impact, 
    confidence_score, 
    actions_count, 
    estimated_duration_seconds, 
    affected_systems,
    status,
    created_at 
  } = recommendation

  const getStatusBadge = () => {
    switch(status) {
      case 'pending_approval':
        return (
          <div className="flex items-center gap-2 px-3 py-1 bg-warning-100 text-warning-700 rounded-full text-sm font-medium">
            <div className="w-2 h-2 bg-warning-500 rounded-full animate-pulse" />
            Pending Approval
          </div>
        )
      case 'executing':
        return (
          <div className="flex items-center gap-2 px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm font-medium">
            <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-primary-600" />
            Executing
          </div>
        )
      case 'completed':
        return (
          <div className="flex items-center gap-2 px-3 py-1 bg-success-100 text-success-700 rounded-full text-sm font-medium">
            <CheckCircle className="w-4 h-4" />
            Completed
          </div>
        )
      case 'rejected':
        return (
          <div className="flex items-center gap-2 px-3 py-1 bg-error-100 text-error-700 rounded-full text-sm font-medium">
            <XCircle className="w-4 h-4" />
            Rejected
          </div>
        )
      default:
        return null
    }
  }

  const getTimeAgo = () => {
    if (!created_at) return 'Just now'
    const now = new Date()
    const created = new Date(created_at)
    const diffMs = now - created
    const diffMins = Math.floor(diffMs / 60000)
    
    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins} min ago`
    const diffHours = Math.floor(diffMins / 60)
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
    return new Date(created_at).toLocaleDateString()
  }

  return (
    <div className="bg-white border border-neutral-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="px-6 py-4 border-b border-neutral-200 bg-neutral-50">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
              <Zap className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-neutral-900">
                AI Optimization Opportunity
              </h3>
              <p className="text-sm text-neutral-500">{getTimeAgo()}</p>
            </div>
          </div>
          {getStatusBadge()}
        </div>
      </div>

      {/* Body */}
      <div className="px-6 py-5 space-y-5">
        {/* Summary */}
        <div>
          <p className="text-xl font-medium text-neutral-900 leading-relaxed">
            {summary}
          </p>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-gradient-to-br from-success-50 to-success-100 border border-success-200 rounded-lg px-4 py-3">
            <div className="flex items-center gap-2 mb-1">
              <DollarSign className="w-4 h-4 text-success-600" />
              <div className="text-xs text-success-600 font-semibold uppercase tracking-wide">Cost Savings</div>
            </div>
            <div className="text-2xl font-bold text-success-700">${impact?.cost_savings || 0}</div>
          </div>
          
          <div className="bg-gradient-to-br from-primary-50 to-primary-100 border border-primary-200 rounded-lg px-4 py-3">
            <div className="flex items-center gap-2 mb-1">
              <Zap className="w-4 h-4 text-primary-600" />
              <div className="text-xs text-primary-600 font-semibold uppercase tracking-wide">Confidence</div>
            </div>
            <div className="text-2xl font-bold text-primary-700">{Math.round(confidence_score * 100)}%</div>
          </div>
          
          <div className="bg-gradient-to-br from-neutral-50 to-neutral-100 border border-neutral-200 rounded-lg px-4 py-3">
            <div className="flex items-center gap-2 mb-1">
              <Users className="w-4 h-4 text-neutral-600" />
              <div className="text-xs text-neutral-600 font-semibold uppercase tracking-wide">Actions</div>
            </div>
            <div className="text-2xl font-bold text-neutral-700">{actions_count}</div>
          </div>
          
          <div className="bg-gradient-to-br from-neutral-50 to-neutral-100 border border-neutral-200 rounded-lg px-4 py-3">
            <div className="flex items-center gap-2 mb-1">
              <Clock className="w-4 h-4 text-neutral-600" />
              <div className="text-xs text-neutral-600 font-semibold uppercase tracking-wide">Est. Duration</div>
            </div>
            <div className="text-2xl font-bold text-neutral-700">{estimated_duration_seconds}s</div>
          </div>
        </div>

        {/* Reasoning */}
        {reasoning && reasoning.length > 0 && (
          <div className="bg-neutral-50 border border-neutral-200 rounded-lg p-4">
            <h4 className="text-sm font-semibold text-neutral-700 mb-3">Reasoning</h4>
            <ul className="space-y-2">
              {reasoning.map((reason, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-neutral-700">
                  <svg className="w-5 h-5 text-success-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="leading-relaxed">{reason}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Systems Affected */}
        {affected_systems && affected_systems.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold text-neutral-700 mb-2">Systems Affected</h4>
            <div className="flex flex-wrap gap-2">
              {affected_systems.map((system, i) => (
                <span key={i} className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-xs font-medium">
                  {system}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Actions Footer */}
      <div className="px-6 py-4 bg-neutral-50 border-t border-neutral-200">
        {status === 'pending_approval' && (
          <div className="flex items-center justify-end gap-3">
            <button
              onClick={onReject}
              disabled={isRejecting || isApproving}
              className="px-5 py-2.5 text-sm font-semibold text-neutral-700 bg-white border border-neutral-300 rounded-lg hover:bg-neutral-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              {isRejecting ? 'Rejecting...' : 'Reject'}
            </button>
            <button
              onClick={onApprove}
              disabled={isApproving || isRejecting}
              className="px-6 py-2.5 text-sm font-semibold text-white bg-success-600 rounded-lg hover:bg-success-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-sm hover:shadow-md"
            >
              {isApproving ? 'Approving...' : '✓ Approve'}
            </button>
          </div>
        )}

        {status === 'executing' && (
          <div className="flex items-center justify-center gap-2 py-2">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary-600"></div>
            <span className="text-sm font-medium text-primary-700">Executing coordination plan...</span>
          </div>
        )}

        {status === 'completed' && (
          <div className="bg-success-50 border border-success-200 rounded-lg px-4 py-3 flex items-center gap-2">
            <CheckCircle className="w-5 h-5 text-success-600" />
            <span className="text-sm font-semibold text-success-700">Successfully completed all actions</span>
          </div>
        )}

        {status === 'rejected' && (
          <div className="bg-error-50 border border-error-200 rounded-lg px-4 py-3 flex items-center gap-2">
            <XCircle className="w-5 h-5 text-error-600" />
            <span className="text-sm font-semibold text-error-700">Recommendation rejected</span>
          </div>
        )}
      </div>
    </div>
  )
}

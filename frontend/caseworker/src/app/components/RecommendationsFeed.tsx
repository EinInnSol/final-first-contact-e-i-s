'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Zap, 
  CheckCircle, 
  XCircle, 
  Clock, 
  DollarSign,
  Users,
  TrendingUp,
  AlertCircle,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import { cn } from '../lib/utils';

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

interface RecommendationsFeedProps {
  recommendations: Recommendation[];
  onApprove: (recommendationId: string) => void;
  onReject: (recommendationId: string) => void;
  onModify: (recommendationId: string) => void;
  isLoading?: boolean;
}

export function RecommendationsFeed({ 
  recommendations, 
  onApprove, 
  onReject,
  onModify,
  isLoading = false 
}: RecommendationsFeedProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending_approval': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'approved': return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'executing': return 'bg-purple-100 text-purple-800 border-purple-300';
      case 'completed': return 'bg-green-100 text-green-800 border-green-300';
      case 'rejected': return 'bg-red-100 text-red-800 border-red-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getConfidenceColor = (score: number) => {
    if (score >= 0.9) return 'text-green-600';
    if (score >= 0.7) return 'text-yellow-600';
    return 'text-orange-600';
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (recommendations.length === 0) {
    return (
      <div className="text-center py-12">
        <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-gray-900 mb-2">All Caught Up!</h3>
        <p className="text-gray-600">No new recommendations at this time.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <AnimatePresence>
        {recommendations.map((rec) => (
          <motion.div
            key={rec.recommendation_id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className={cn(
              "bg-white rounded-lg shadow-lg border-2 overflow-hidden transition-all duration-200",
              rec.status === 'pending_approval' ? 'border-yellow-400' : 'border-gray-200'
            )}
          >
            {/* Header */}
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-yellow-100 rounded-lg">
                    <Zap className="h-6 w-6 text-yellow-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {rec.summary}
                    </h3>
                    <div className="flex items-center space-x-4 mt-1 text-sm text-gray-500">
                      <span className="flex items-center">
                        <Clock className="h-4 w-4 mr-1" />
                        {new Date(rec.created_at).toLocaleTimeString()}
                      </span>
                      <span className={cn(
                        "font-semibold",
                        getConfidenceColor(rec.confidence_score)
                      )}>
                        {Math.round(rec.confidence_score * 100)}% Confidence
                      </span>
                    </div>
                  </div>
                </div>
                <span className={cn(
                  "px-3 py-1 rounded-full text-xs font-medium border",
                  getStatusColor(rec.status)
                )}>
                  {rec.status.replace('_', ' ').toUpperCase()}
                </span>
              </div>

              {/* Impact Metrics */}
              <div className="grid grid-cols-3 gap-4 mb-4">
                {rec.impact.cost_savings && (
                  <div className="flex items-center space-x-2 text-sm">
                    <DollarSign className="h-5 w-5 text-green-600" />
                    <div>
                      <p className="font-semibold text-green-600">
                        ${rec.impact.cost_savings}
                      </p>
                      <p className="text-gray-500 text-xs">Cost Savings</p>
                    </div>
                  </div>
                )}
                <div className="flex items-center space-x-2 text-sm">
                  <Users className="h-5 w-5 text-blue-600" />
                  <div>
                    <p className="font-semibold text-blue-600">
                      {rec.actions_count} actions
                    </p>
                    <p className="text-gray-500 text-xs">Across Systems</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <TrendingUp className="h-5 w-5 text-purple-600" />
                  <div>
                    <p className="font-semibold text-purple-600">
                      {rec.estimated_duration_seconds}s
                    </p>
                    <p className="text-gray-500 text-xs">Est. Duration</p>
                  </div>
                </div>
              </div>

              {/* Reasoning */}
              <div className="bg-gray-50 rounded-lg p-4 mb-4">
                <h4 className="text-sm font-semibold text-gray-700 mb-2">Reasoning:</h4>
                <ul className="space-y-1">
                  {rec.reasoning.map((reason, idx) => (
                    <li key={idx} className="text-sm text-gray-600 flex items-start">
                      <span className="text-yellow-600 mr-2">•</span>
                      <span>{reason}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Expandable Details */}
              <button
                onClick={() => setExpandedId(expandedId === rec.recommendation_id ? null : rec.recommendation_id)}
                className="flex items-center justify-between w-full text-sm text-gray-600 hover:text-gray-900 transition-colors"
              >
                <span className="font-medium">
                  {expandedId === rec.recommendation_id ? 'Hide' : 'Show'} affected systems
                </span>
                {expandedId === rec.recommendation_id ? (
                  <ChevronUp className="h-4 w-4" />
                ) : (
                  <ChevronDown className="h-4 w-4" />
                )}
              </button>

              {expandedId === rec.recommendation_id && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="mt-3 bg-blue-50 rounded-lg p-3"
                >
                  <p className="text-xs font-semibold text-blue-900 mb-2">Affected Systems:</p>
                  <div className="flex flex-wrap gap-2">
                    {rec.affected_systems.map((system, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-1 bg-white rounded text-xs text-blue-700 border border-blue-200"
                      >
                        {system.replace('_', ' ')}
                      </span>
                    ))}
                  </div>
                </motion.div>
              )}

              {/* Action Buttons */}
              {rec.status === 'pending_approval' && (
                <div className="flex items-center space-x-3 mt-4 pt-4 border-t">
                  <button
                    onClick={() => onApprove(rec.recommendation_id)}
                    className="flex-1 bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
                  >
                    <CheckCircle className="h-5 w-5" />
                    <span>APPROVE</span>
                  </button>
                  <button
                    onClick={() => onModify(rec.recommendation_id)}
                    className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors duration-200"
                  >
                    MODIFY
                  </button>
                  <button
                    onClick={() => onReject(rec.recommendation_id)}
                    className="px-6 bg-red-600 hover:bg-red-700 text-white font-semibold py-3 rounded-lg transition-colors duration-200 flex items-center justify-center"
                  >
                    <XCircle className="h-5 w-5" />
                  </button>
                </div>
              )}

              {rec.status === 'executing' && (
                <div className="mt-4 pt-4 border-t">
                  <div className="flex items-center space-x-3 text-purple-600">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-purple-600"></div>
                    <span className="font-medium">Executing actions...</span>
                  </div>
                </div>
              )}

              {rec.status === 'completed' && (
                <div className="mt-4 pt-4 border-t">
                  <div className="flex items-center space-x-3 text-green-600">
                    <CheckCircle className="h-5 w-5" />
                    <span className="font-medium">Successfully completed</span>
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}

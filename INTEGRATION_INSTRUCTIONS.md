// ADD THIS NEAR THE TOP OF THE FILE (around line 34, after other imports):
import { RecommendationsFeed } from './RecommendationsFeed';
import { useRecommendations, useApproveRecommendation, useRejectRecommendation, useTriggerEvent } from '../hooks/useOrchestration';

// THEN IN THE COMPONENT, AFTER THE OTHER HOOKS (around line 110):

  // Orchestration hooks
  const { data: recommendations = [], isLoading: recommendationsLoading } = useRecommendations();
  const approveRecommendation = useApproveRecommendation();
  const rejectRecommendation = useRejectRecommendation();
  const triggerEvent = useTriggerEvent();

  const handleApproveRecommendation = (recommendationId: string) => {
    approveRecommendation.mutate(recommendationId);
  };

  const handleRejectRecommendation = (recommendationId: string) => {
    rejectRecommendation.mutate(recommendationId);
  };

  const handleModifyRecommendation = (recommendationId: string) => {
    // TODO: Open modal for modifying recommendation
    toast.info('Modification UI coming soon');
  };

  // DEMO: Trigger appointment cancellation event
  const handleTriggerDemo = () => {
    triggerEvent.mutate({
      event_type: 'appointment_cancelled',
      client_id: 'maria_demo',
      metadata: {
        appointment_time: new Date(Date.now() + 86400000).toISOString(), // Tomorrow
        provider_id: 'dr_smith',
        appointment_type: 'primary_care'
      }
    });
  };

// THEN UPDATE THE TABS ARRAY (around line 125):
const tabs = [
  { id: 'recommendations', label: 'AI Recommendations', icon: Zap },  // ADD THIS LINE
  { id: 'cases', label: t('tabs.case_management'), icon: FileText },
  { id: 'clients', label: t('tabs.clients'), icon: Users },
  { id: 'ai', label: t('tabs.ai_assistant'), icon: Bot },
  { id: 'compliance', label: t('tabs.compliance'), icon: Shield },
  { id: 'metrics', label: t('tabs.performance'), icon: BarChart3 },
  { id: 'settings', label: t('tabs.settings'), icon: Settings }
];

// THEN IN THE TAB CONTENT SECTION (around line 288), ADD THIS AT THE TOP:
{activeTab === 'recommendations' && (
  <div>
    {/* Demo Trigger Button */}
    <div className="mb-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
      <h3 className="text-sm font-semibold text-yellow-900 mb-2">
        🎬 Demo Mode
      </h3>
      <p className="text-sm text-yellow-700 mb-3">
        Trigger a demo "appointment cancellation" event to see the AI orchestration in action
      </p>
      <button
        onClick={handleTriggerDemo}
        disabled={triggerEvent.isPending}
        className="bg-yellow-600 hover:bg-yellow-700 disabled:bg-yellow-300 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200"
      >
        {triggerEvent.isPending ? 'Triggering...' : 'Trigger Demo Event'}
      </button>
    </div>

    {/* Recommendations Feed */}
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">AI Recommendations</h2>
          <p className="text-gray-600 mt-1">
            Real-time optimization opportunities detected by the orchestration engine
          </p>
        </div>
        {recommendations.length > 0 && (
          <span className="bg-yellow-100 text-yellow-800 text-sm font-semibold px-3 py-1 rounded-full">
            {recommendations.filter(r => r.status === 'pending_approval').length} pending
          </span>
        )}
      </div>

      <RecommendationsFeed
        recommendations={recommendations}
        onApprove={handleApproveRecommendation}
        onReject={handleRejectRecommendation}
        onModify={handleModifyRecommendation}
        isLoading={recommendationsLoading}
      />
    </div>
  </div>
)}

// DON'T FORGET TO IMPORT Zap AT THE TOP:
// Change the lucide-react import line to include Zap:
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
  TrendingUp,
  Zap  // ADD THIS
} from 'lucide-react';

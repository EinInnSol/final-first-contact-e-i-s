"use client";

import { useState, useEffect } from 'react';
import axios from 'axios';

interface NewClientEvent {
  id: string;
  client_name: string;
  case_number: string;
  crisis_level: string;
  crisis_score: number;
  ai_recommendation: {
    actions: string[];
    reason: string;
    impact: string;
    estimated_time: string;
    confidence: number;
  };
  timestamp: string;
}

export default function CaseworkerDemoPage() {
  const [events, setEvents] = useState<NewClientEvent[]>([]);
  const [selectedEvent, setSelectedEvent] = useState<NewClientEvent | null>(null);
  const [showComplianceModal, setShowComplianceModal] = useState(false);
  const [approvedCase, setApprovedCase] = useState<string | null>(null);

  // Poll for new events (simulating real-time)
  useEffect(() => {
    // For demo, add mock events after 2 seconds
    const timer = setTimeout(() => {
      // This would normally come from API or WebSocket
      const mockEvent: NewClientEvent = {
        id: '1',
        client_name: 'Maria Rodriguez',
        case_number: 'FC-20241114-A3F2B1',
        crisis_level: 'high',
        crisis_score: 78,
        ai_recommendation: {
          actions: [
            'Schedule emergency housing assessment within 24 hours',
            'Connect with childcare services immediately',
            'Initiate domestic violence safety planning',
            'Coordinate with legal aid for protection order',
            'Arrange transportation for appointments',
            'Update HMIS database with intake information'
          ],
          reason: 'Client B has higher medical urgency, all required documents uploaded, lives on existing transport route, and has no scheduling conflicts.',
          impact: 'Avoid $320 wasted appointment slot, better care for higher-urgency case, optimal resource utilization',
          estimated_time: '12 seconds',
          confidence: 94
        },
        timestamp: new Date().toISOString()
      };

      setEvents([mockEvent]);
      setSelectedEvent(mockEvent);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  const handleApprove = (event: NewClientEvent) => {
    // Send approval to backend
    setApprovedCase(event.case_number);

    // Show compliance notification after 1 second
    setTimeout(() => {
      setShowComplianceModal(true);
    }, 1000);
  };

  const handleApproveCompliance = () => {
    setShowComplianceModal(false);
    // In real app, would upload compliance report
  };

  const getCrisisColor = (level: string) => {
    switch (level) {
      case 'critical': return 'text-red-600 bg-red-100';
      case 'high': return 'text-orange-600 bg-orange-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      default: return 'text-green-600 bg-green-100';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">First Contact E.I.S. - Caseworker Dashboard</h1>
              <p className="text-gray-600 mt-1">Sarah Johnson | City of Long Beach | <span className="text-orange-600 font-semibold">{events.length} new events</span></p>
            </div>
            <div className="flex gap-3">
              <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                Filter ▼
              </button>
              <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                Sort ▼
              </button>
            </div>
          </div>
        </div>

        {/* Real-time Events Feed */}
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">REAL-TIME EVENTS FEED</h2>

          {events.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
              <div className="animate-pulse">
                <div className="w-16 h-16 bg-gray-200 rounded-full mx-auto mb-4"></div>
                <p>Waiting for new client intakes...</p>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {events.map((event) => (
                <div
                  key={event.id}
                  className={`bg-white rounded-lg shadow-lg border-l-4 ${event.id === selectedEvent?.id ? 'border-orange-500' : 'border-gray-300'}`}
                >
                  <div className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center gap-3">
                        <div className="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center">
                          <span className="text-2xl">⚡</span>
                        </div>
                        <div>
                          <h3 className="text-lg font-bold text-gray-900">NEW OPTIMIZATION OPPORTUNITY</h3>
                          <p className="text-sm text-gray-600">{new Date(event.timestamp).toLocaleTimeString()}</p>
                        </div>
                      </div>
                    </div>

                    <div className="bg-blue-50 rounded-lg p-6 mb-4">
                      <h4 className="font-semibold text-gray-900 mb-2">New Client Assigned: {event.client_name}</h4>
                      <p className="text-sm text-gray-700 mb-3">Case #{event.case_number}</p>

                      <div className="grid grid-cols-2 gap-4 mb-4">
                        <div>
                          <p className="text-xs text-gray-600 mb-1">Crisis Level</p>
                          <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getCrisisColor(event.crisis_level)}`}>
                            {event.crisis_level.toUpperCase()}
                          </span>
                        </div>
                        <div>
                          <p className="text-xs text-gray-600 mb-1">AI Confidence</p>
                          <p className="text-2xl font-bold text-blue-600">{event.ai_recommendation.confidence}%</p>
                        </div>
                      </div>

                      <div className="mb-4">
                        <p className="text-sm font-semibold text-gray-700 mb-2">📋 Reason:</p>
                        <p className="text-sm text-gray-600">{event.ai_recommendation.reason}</p>
                      </div>

                      <div className="mb-4">
                        <p className="text-sm font-semibold text-gray-700 mb-2">💡 Impact:</p>
                        <p className="text-sm text-gray-600">{event.ai_recommendation.impact}</p>
                      </div>

                      <div className="mb-4">
                        <p className="text-sm font-semibold text-gray-700 mb-2">🔧 Actions ({event.ai_recommendation.actions.length} steps across 4 systems):</p>
                        <ul className="space-y-2">
                          {event.ai_recommendation.actions.map((action, idx) => (
                            <li key={idx} className="flex items-start gap-2 text-sm text-gray-700">
                              <span className="text-blue-600 font-semibold">{idx + 1}.</span>
                              <span>{action}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      <div className="flex items-center gap-4 text-sm text-gray-600">
                        <div className="flex items-center gap-1">
                          <span>⏱️</span>
                          <span>Estimated execution time: {event.ai_recommendation.estimated_time}</span>
                        </div>
                      </div>
                    </div>

                    {approvedCase === event.case_number ? (
                      <div className="bg-green-50 border-2 border-green-500 rounded-lg p-4">
                        <div className="flex items-center gap-2 text-green-700 font-semibold">
                          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                          </svg>
                          <span>APPROVED - Actions executing...</span>
                        </div>
                      </div>
                    ) : (
                      <div className="flex gap-3">
                        <button
                          onClick={() => handleApprove(event)}
                          className="flex-1 bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
                        >
                          ✓ APPROVE
                        </button>
                        <button className="flex-1 bg-yellow-600 hover:bg-yellow-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors">
                          ✎ MODIFY
                        </button>
                        <button className="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors">
                          ✗ REJECT
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Today's Metrics */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">TODAY'S METRICS</h2>
          <div className="grid grid-cols-4 gap-6">
            <div>
              <p className="text-sm text-gray-600 mb-1">Recommendations approved</p>
              <p className="text-3xl font-bold text-gray-900">{approvedCase ? 1 : 0}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Time saved</p>
              <p className="text-3xl font-bold text-gray-900">{approvedCase ? '0.2' : '0'} hours</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Cost savings</p>
              <p className="text-3xl font-bold text-gray-900">${approvedCase ? '320' : '0'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Active cases</p>
              <p className="text-3xl font-bold text-gray-900">23</p>
            </div>
          </div>
        </div>
      </div>

      {/* Compliance Modal */}
      {showComplianceModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-2xl max-w-lg w-full p-6">
            <div className="text-center mb-6">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">📋</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Compliance Report Ready</h3>
              <p className="text-gray-600">Case #{approvedCase}</p>
            </div>

            <div className="bg-gray-50 rounded-lg p-4 mb-6">
              <p className="text-gray-700 mb-3">
                HUD/HMIS compliance report for {events[0]?.client_name} is ready for review and upload.
              </p>
              <p className="text-sm text-gray-600">
                This report includes all required fields from the Coordinated Entry Assessment and has been automatically formatted for HMIS submission.
              </p>
            </div>

            <p className="text-center font-semibold text-gray-900 mb-6">
              Should we proceed with upload?
            </p>

            <div className="flex gap-3">
              <button
                onClick={handleApproveCompliance}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
              >
                Yes, Upload Report
              </button>
              <button
                onClick={() => setShowComplianceModal(false)}
                className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold py-3 px-6 rounded-lg transition-colors"
              >
                Review First
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

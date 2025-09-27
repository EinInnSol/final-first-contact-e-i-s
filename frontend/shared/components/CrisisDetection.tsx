"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { 
  AlertTriangle, 
  Phone, 
  Shield, 
  Heart, 
  Home, 
  Users,
  Activity,
  Zap
} from 'lucide-react';

interface CrisisDetectionProps {
  onCrisisDetected: (crisis: CrisisData) => void;
  language?: string;
}

interface CrisisData {
  riskLevel: 'low' | 'medium' | 'high' | 'critical';
  confidence: number;
  triggers: string[];
  recommendedActions: string[];
  escalationRequired: boolean;
  emergencyContacts: Array<{
    name: string;
    phone: string;
    description: string;
  }>;
}

const CrisisDetection: React.FC<CrisisDetectionProps> = ({ onCrisisDetected, language = 'en' }) => {
  const [text, setText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [crisisData, setCrisisData] = useState<CrisisData | null>(null);
  const [showEmergencyContacts, setShowEmergencyContacts] = useState(false);

  const crisisKeywords = {
    suicide: ['suicide', 'kill myself', 'end it all', 'hurt myself', 'not worth living'],
    violence: ['abuse', 'violence', 'threat', 'fear', 'scared', 'beaten', 'hit'],
    homelessness: ['homeless', 'no home', 'sleeping outside', 'on the street', 'shelter'],
    hunger: ['hungry', 'starving', 'no food', 'can\'t eat', 'food stamps'],
    children: ['children', 'kids', 'baby', 'child', 'my son', 'my daughter'],
    mental_health: ['depressed', 'anxious', 'panic', 'overwhelmed', 'can\'t cope'],
    substance: ['drunk', 'high', 'overdose', 'addiction', 'using drugs'],
    financial: ['broke', 'no money', 'can\'t pay', 'eviction', 'utilities cut off']
  };

  const emergencyContacts = [
    {
      name: 'National Suicide Prevention Lifeline',
      phone: '988',
      description: '24/7 crisis support for suicidal thoughts'
    },
    {
      name: 'National Domestic Violence Hotline',
      phone: '1-800-799-7233',
      description: '24/7 support for domestic violence situations'
    },
    {
      name: 'Long Beach Crisis Line',
      phone: '(562) 434-4949',
      description: 'Local crisis intervention and support'
    },
    {
      name: 'Long Beach Emergency Services',
      phone: '911',
      description: 'Emergency services for immediate danger'
    },
    {
      name: 'Long Beach Housing Authority',
      phone: '(562) 570-6944',
      description: 'Emergency housing assistance'
    }
  ];

  const analyzeText = async () => {
    if (!text.trim()) return;

    setIsAnalyzing(true);
    
    // Simulate AI analysis delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    const textLower = text.toLowerCase();
    const detectedTriggers: string[] = [];
    let riskScore = 0;

    // Analyze for crisis keywords
    Object.entries(crisisKeywords).forEach(([category, keywords]) => {
      const foundKeywords = keywords.filter(keyword => textLower.includes(keyword));
      if (foundKeywords.length > 0) {
        detectedTriggers.push(category);
        riskScore += foundKeywords.length * 10;
      }
    });

    // Additional analysis for context
    if (textLower.includes('help') || textLower.includes('emergency')) {
      riskScore += 15;
    }

    if (textLower.includes('now') || textLower.includes('immediately')) {
      riskScore += 10;
    }

    // Determine risk level
    let riskLevel: 'low' | 'medium' | 'high' | 'critical';
    if (riskScore >= 80) {
      riskLevel = 'critical';
    } else if (riskScore >= 60) {
      riskLevel = 'high';
    } else if (riskScore >= 30) {
      riskLevel = 'medium';
    } else {
      riskLevel = 'low';
    }

    const confidence = Math.min(riskScore / 100, 1.0);

    const crisis: CrisisData = {
      riskLevel,
      confidence,
      triggers: detectedTriggers,
      recommendedActions: getRecommendedActions(riskLevel, detectedTriggers),
      escalationRequired: riskLevel === 'high' || riskLevel === 'critical',
      emergencyContacts: getRelevantContacts(detectedTriggers)
    };

    setCrisisData(crisis);
    setIsAnalyzing(false);

    if (crisis.escalationRequired) {
      onCrisisDetected(crisis);
    }
  };

  const getRecommendedActions = (level: string, triggers: string[]) => {
    const actions = [];

    if (level === 'critical') {
      actions.push('Call emergency services immediately (911)');
      actions.push('Ensure safety of all involved');
      actions.push('Connect with crisis intervention team');
    } else if (level === 'high') {
      actions.push('Contact crisis hotline immediately');
      actions.push('Schedule emergency intake appointment');
      actions.push('Develop safety plan');
    } else if (level === 'medium') {
      actions.push('Schedule intake appointment within 24 hours');
      actions.push('Connect with appropriate services');
      actions.push('Monitor situation closely');
    } else {
      actions.push('Schedule regular intake appointment');
      actions.push('Connect with caseworker');
    }

    // Add specific actions based on triggers
    if (triggers.includes('suicide')) {
      actions.push('Connect with mental health crisis team');
    }
    if (triggers.includes('violence')) {
      actions.push('Connect with domestic violence resources');
    }
    if (triggers.includes('homelessness')) {
      actions.push('Connect with emergency housing services');
    }
    if (triggers.includes('children')) {
      actions.push('Ensure child safety and welfare');
    }

    return actions;
  };

  const getRelevantContacts = (triggers: string[]) => {
    const relevant = [...emergencyContacts];

    if (triggers.includes('suicide') || triggers.includes('mental_health')) {
      relevant.unshift(emergencyContacts[0]); // Suicide prevention
    }
    if (triggers.includes('violence')) {
      relevant.unshift(emergencyContacts[1]); // Domestic violence
    }
    if (triggers.includes('homelessness')) {
      relevant.unshift(emergencyContacts[4]); // Housing authority
    }

    return relevant.slice(0, 3); // Return top 3 most relevant
  };

  const getRiskLevelColor = (level: string) => {
    switch (level) {
      case 'critical': return 'text-red-600 bg-red-100';
      case 'high': return 'text-orange-600 bg-orange-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      default: return 'text-green-600 bg-green-100';
    }
  };

  const getRiskLevelIcon = (level: string) => {
    switch (level) {
      case 'critical': return <Zap className="h-5 w-5" />;
      case 'high': return <AlertTriangle className="h-5 w-5" />;
      case 'medium': return <Activity className="h-5 w-5" />;
      default: return <Shield className="h-5 w-5" />;
    }
  };

  const getTriggerIcon = (trigger: string) => {
    switch (trigger) {
      case 'suicide': return <Heart className="h-4 w-4" />;
      case 'violence': return <Shield className="h-4 w-4" />;
      case 'homelessness': return <Home className="h-4 w-4" />;
      case 'children': return <Users className="h-4 w-4" />;
      default: return <AlertTriangle className="h-4 w-4" />;
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-orange-500" />
            AI Crisis Detection
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">
              Enter text to analyze for crisis indicators:
            </label>
            <Textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Describe your current situation or concerns..."
              className="min-h-[100px]"
            />
          </div>
          
          <Button 
            onClick={analyzeText} 
            disabled={!text.trim() || isAnalyzing}
            className="w-full"
          >
            {isAnalyzing ? 'Analyzing...' : 'Analyze for Crisis Indicators'}
          </Button>
        </CardContent>
      </Card>

      {isAnalyzing && (
        <Card>
          <CardContent className="p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600 mx-auto mb-4"></div>
            <h3 className="text-lg font-semibold mb-2">Analyzing Text</h3>
            <p className="text-gray-600">Our AI is analyzing your text for crisis indicators...</p>
          </CardContent>
        </Card>
      )}

      {crisisData && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              {getRiskLevelIcon(crisisData.riskLevel)}
              Crisis Analysis Results
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-4">
              <Badge className={`${getRiskLevelColor(crisisData.riskLevel)} px-3 py-1`}>
                {crisisData.riskLevel.toUpperCase()} RISK
              </Badge>
              <span className="text-sm text-gray-600">
                Confidence: {Math.round(crisisData.confidence * 100)}%
              </span>
            </div>

            {crisisData.triggers.length > 0 && (
              <div>
                <h4 className="font-semibold mb-2">Detected Crisis Indicators:</h4>
                <div className="flex flex-wrap gap-2">
                  {crisisData.triggers.map((trigger, index) => (
                    <Badge key={index} variant="outline" className="flex items-center gap-1">
                      {getTriggerIcon(trigger)}
                      {trigger.replace('_', ' ')}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            <div>
              <h4 className="font-semibold mb-2">Recommended Actions:</h4>
              <ul className="space-y-1">
                {crisisData.recommendedActions.map((action, index) => (
                  <li key={index} className="flex items-start gap-2 text-sm">
                    <span className="text-blue-500 mt-1">•</span>
                    <span>{action}</span>
                  </li>
                ))}
              </ul>
            </div>

            {crisisData.escalationRequired && (
              <Alert className="border-red-200 bg-red-50">
                <AlertTriangle className="h-4 w-4 text-red-600" />
                <AlertDescription className="text-red-800">
                  <strong>Immediate escalation required.</strong> Please contact emergency services or crisis hotlines immediately.
                </AlertDescription>
              </Alert>
            )}

            <div className="flex gap-2">
              <Button 
                onClick={() => setShowEmergencyContacts(!showEmergencyContacts)}
                variant="outline"
                className="flex-1"
              >
                <Phone className="h-4 w-4 mr-2" />
                Emergency Contacts
              </Button>
              <Button 
                onClick={() => window.location.href = '/caseworker'}
                className="flex-1"
              >
                Connect with Caseworker
              </Button>
            </div>

            {showEmergencyContacts && (
              <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                <h4 className="font-semibold mb-3">Emergency Contacts:</h4>
                <div className="space-y-2">
                  {crisisData.emergencyContacts.map((contact, index) => (
                    <div key={index} className="flex items-center justify-between p-2 bg-white rounded border">
                      <div>
                        <div className="font-medium">{contact.name}</div>
                        <div className="text-sm text-gray-600">{contact.description}</div>
                      </div>
                      <Button 
                        size="sm" 
                        onClick={() => window.open(`tel:${contact.phone}`)}
                        className="ml-2"
                      >
                        <Phone className="h-4 w-4 mr-1" />
                        {contact.phone}
                      </Button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default CrisisDetection;

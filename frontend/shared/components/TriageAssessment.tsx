"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { CheckCircle, AlertTriangle, XCircle, Clock } from 'lucide-react';

interface TriageAssessmentProps {
  onComplete: (assessment: TriageResult) => void;
  language?: string;
}

interface TriageResult {
  crisisLevel: 'low' | 'medium' | 'high' | 'critical';
  crisisScore: number;
  crisisIndicators: string[];
  recommendedServices: string[];
  immediateActions: string[];
  carePlan: {
    immediateNeeds: string[];
    shortTermGoals: string[];
    longTermGoals: string[];
  };
}

const TriageAssessment: React.FC<TriageAssessmentProps> = ({ onComplete, language = 'en' }) => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [responses, setResponses] = useState<Record<string, any>>({});
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [crisisDetected, setCrisisDetected] = useState(false);

  const questions = [
    {
      id: 'housing_status',
      question: 'What is your current housing situation?',
      type: 'select',
      options: [
        'I have stable housing',
        'I am at risk of losing my housing',
        'I am currently homeless',
        'I am staying with friends/family temporarily'
      ],
      crisisWeight: 3
    },
    {
      id: 'safety_concerns',
      question: 'Do you have any safety concerns?',
      type: 'select',
      options: [
        'No safety concerns',
        'Some concerns but manageable',
        'Significant safety concerns',
        'I feel unsafe and need immediate help'
      ],
      crisisWeight: 4
    },
    {
      id: 'children_involved',
      question: 'Are there children involved in your situation?',
      type: 'select',
      options: [
        'No children involved',
        'Children are safe and cared for',
        'Children may be at risk',
        'Children are in immediate danger'
      ],
      crisisWeight: 5
    },
    {
      id: 'mental_health',
      question: 'How would you describe your current mental health?',
      type: 'select',
      options: [
        'I am doing well mentally',
        'I have some stress but am coping',
        'I am struggling with mental health issues',
        'I am in crisis and need immediate help'
      ],
      crisisWeight: 4
    },
    {
      id: 'substance_use',
      question: 'Do you have any concerns about substance use?',
      type: 'select',
      options: [
        'No substance use concerns',
        'Occasional use, no problems',
        'Regular use with some problems',
        'Substance use is significantly impacting my life'
      ],
      crisisWeight: 3
    },
    {
      id: 'financial_situation',
      question: 'How would you describe your financial situation?',
      type: 'select',
      options: [
        'Financially stable',
        'Some financial stress but manageable',
        'Significant financial difficulties',
        'In financial crisis'
      ],
      crisisWeight: 2
    }
  ];

  const handleResponse = (questionId: string, response: string) => {
    setResponses(prev => ({
      ...prev,
      [questionId]: response
    }));
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      performTriageAnalysis();
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const performTriageAnalysis = async () => {
    setIsAnalyzing(true);
    
    // Simulate AI analysis
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Calculate crisis score
    let crisisScore = 0;
    const crisisIndicators: string[] = [];
    
    questions.forEach(question => {
      const response = responses[question.id];
      if (response) {
        const optionIndex = question.options.indexOf(response);
        const weight = (optionIndex + 1) * question.crisisWeight;
        crisisScore += weight;
        
        if (optionIndex >= 2) { // High risk responses
          crisisIndicators.push(question.id);
        }
      }
    });
    
    // Determine crisis level
    let crisisLevel: 'low' | 'medium' | 'high' | 'critical';
    if (crisisScore >= 80) {
      crisisLevel = 'critical';
      setCrisisDetected(true);
    } else if (crisisScore >= 60) {
      crisisLevel = 'high';
      setCrisisDetected(true);
    } else if (crisisScore >= 40) {
      crisisLevel = 'medium';
    } else {
      crisisLevel = 'low';
    }
    
    const result: TriageResult = {
      crisisLevel,
      crisisScore: Math.min(crisisScore, 100),
      crisisIndicators,
      recommendedServices: getRecommendedServices(crisisLevel, crisisIndicators),
      immediateActions: getImmediateActions(crisisLevel),
      carePlan: {
        immediateNeeds: getImmediateNeeds(crisisLevel),
        shortTermGoals: getShortTermGoals(crisisLevel),
        longTermGoals: getLongTermGoals(crisisLevel)
      }
    };
    
    setIsAnalyzing(false);
    onComplete(result);
  };

  const getRecommendedServices = (level: string, indicators: string[]) => {
    const services = [];
    
    if (indicators.includes('housing_status')) services.push('Housing Assistance');
    if (indicators.includes('safety_concerns')) services.push('Domestic Violence Support');
    if (indicators.includes('children_involved')) services.push('Child Welfare Services');
    if (indicators.includes('mental_health')) services.push('Mental Health Services');
    if (indicators.includes('substance_use')) services.push('Substance Abuse Treatment');
    if (indicators.includes('financial_situation')) services.push('Financial Assistance');
    
    return services;
  };

  const getImmediateActions = (level: string) => {
    switch (level) {
      case 'critical':
        return [
          'Contact emergency services immediately',
          'Initiate crisis intervention protocol',
          'Ensure safety of all involved',
          'Connect with emergency resources'
        ];
      case 'high':
        return [
          'Schedule immediate intake appointment',
          'Connect with crisis counselor',
          'Develop safety plan',
          'Monitor situation closely'
        ];
      case 'medium':
        return [
          'Schedule intake appointment within 24 hours',
          'Connect with appropriate services',
          'Begin care planning process'
        ];
      default:
        return [
          'Schedule intake appointment',
          'Connect with caseworker',
          'Begin service planning'
        ];
    }
  };

  const getImmediateNeeds = (level: string) => {
    switch (level) {
      case 'critical':
        return ['Safety', 'Emergency housing', 'Crisis intervention', 'Medical attention'];
      case 'high':
        return ['Safety planning', 'Emergency resources', 'Crisis counseling', 'Basic needs'];
      case 'medium':
        return ['Service connection', 'Resource coordination', 'Support planning'];
      default:
        return ['Service planning', 'Resource identification', 'Goal setting'];
    }
  };

  const getShortTermGoals = (level: string) => {
    switch (level) {
      case 'critical':
        return ['Stabilization', 'Safety assurance', 'Crisis resolution'];
      case 'high':
        return ['Crisis management', 'Safety planning', 'Resource connection'];
      case 'medium':
        return ['Service connection', 'Stabilization', 'Goal setting'];
      default:
        return ['Service planning', 'Resource coordination', 'Progress tracking'];
    }
  };

  const getLongTermGoals = (level: string) => {
    return ['Self-sufficiency', 'Independence', 'Long-term stability', 'Community integration'];
  };

  const getCrisisLevelColor = (level: string) => {
    switch (level) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      default: return 'bg-green-500';
    }
  };

  const getCrisisLevelIcon = (level: string) => {
    switch (level) {
      case 'critical': return <XCircle className="h-5 w-5" />;
      case 'high': return <AlertTriangle className="h-5 w-5" />;
      case 'medium': return <Clock className="h-5 w-5" />;
      default: return <CheckCircle className="h-5 w-5" />;
    }
  };

  if (isAnalyzing) {
    return (
      <Card className="w-full max-w-2xl mx-auto">
        <CardContent className="p-8 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <h3 className="text-lg font-semibold mb-2">Analyzing Assessment</h3>
          <p className="text-gray-600">Our AI is analyzing your responses to provide the best recommendations...</p>
        </CardContent>
      </Card>
    );
  }

  const currentQ = questions[currentQuestion];
  const progress = ((currentQuestion + 1) / questions.length) * 100;

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <span>AI-Powered Triage Assessment</span>
          <Badge variant="outline">Question {currentQuestion + 1} of {questions.length}</Badge>
        </CardTitle>
        <Progress value={progress} className="w-full" />
      </CardHeader>
      <CardContent className="space-y-6">
        <div>
          <h3 className="text-lg font-semibold mb-4">{currentQ.question}</h3>
          <div className="space-y-2">
            {currentQ.options.map((option, index) => (
              <Button
                key={index}
                variant={responses[currentQ.id] === option ? "default" : "outline"}
                className="w-full justify-start text-left h-auto p-4"
                onClick={() => handleResponse(currentQ.id, option)}
              >
                <div className="flex items-center gap-3">
                  <div className={`w-4 h-4 rounded-full border-2 ${
                    responses[currentQ.id] === option 
                      ? 'bg-blue-600 border-blue-600' 
                      : 'border-gray-300'
                  }`} />
                  <span>{option}</span>
                </div>
              </Button>
            ))}
          </div>
        </div>

        {crisisDetected && (
          <Alert className="border-red-200 bg-red-50">
            <AlertTriangle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-800">
              Crisis indicators detected. We will prioritize your case and connect you with immediate support.
            </AlertDescription>
          </Alert>
        )}

        <div className="flex justify-between">
          <Button
            variant="outline"
            onClick={handlePrevious}
            disabled={currentQuestion === 0}
          >
            Previous
          </Button>
          <Button
            onClick={handleNext}
            disabled={!responses[currentQ.id]}
          >
            {currentQuestion === questions.length - 1 ? 'Complete Assessment' : 'Next'}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default TriageAssessment;

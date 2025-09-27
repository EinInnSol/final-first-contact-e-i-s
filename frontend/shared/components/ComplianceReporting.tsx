"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  FileText, 
  CheckCircle, 
  AlertTriangle, 
  Download, 
  Upload,
  Calendar,
  Users,
  Home,
  Heart,
  Shield
} from 'lucide-react';

interface ComplianceReportingProps {
  onReportGenerated: (report: ComplianceReport) => void;
  language?: string;
}

interface ComplianceReport {
  reportId: string;
  reportType: 'HUD' | 'HMIS' | 'CES' | 'HIPAA';
  status: 'complete' | 'in_progress' | 'error';
  complianceScore: number;
  generatedAt: string;
  dataPoints: number;
  issues: ComplianceIssue[];
  recommendations: string[];
  downloadUrl?: string;
}

interface ComplianceIssue {
  id: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  category: string;
  description: string;
  recommendation: string;
  affectedRecords: number;
}

const ComplianceReporting: React.FC<ComplianceReportingProps> = ({ onReportGenerated, language = 'en' }) => {
  const [selectedReportType, setSelectedReportType] = useState<string>('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [reports, setReports] = useState<ComplianceReport[]>([]);
  const [complianceScore, setComplianceScore] = useState(0);

  const reportTypes = [
    {
      id: 'HUD',
      name: 'HUD Universal Data Elements',
      description: 'Housing and Urban Development compliance reporting',
      icon: <Home className="h-5 w-5" />,
      requirements: ['Client demographics', 'Housing status', 'Income verification', 'Service utilization']
    },
    {
      id: 'HMIS',
      name: 'HMIS Data Standards',
      description: 'Homeless Management Information System reporting',
      icon: <Users className="h-5 w-5" />,
      requirements: ['Client assessments', 'Service entries', 'Exit data', 'Program performance']
    },
    {
      id: 'CES',
      name: 'Coordinated Entry System',
      description: 'Coordinated Entry System compliance reporting',
      icon: <Heart className="h-5 w-5" />,
      requirements: ['Assessment scores', 'Priority rankings', 'Referral tracking', 'Outcome data']
    },
    {
      id: 'HIPAA',
      name: 'HIPAA Compliance',
      description: 'Health Insurance Portability and Accountability Act compliance',
      icon: <Shield className="h-5 w-5" />,
      requirements: ['Data encryption', 'Access controls', 'Audit logs', 'Privacy safeguards']
    }
  ];

  const generateReport = async (reportType: string) => {
    setIsGenerating(true);
    
    // Simulate AI report generation
    await new Promise(resolve => setTimeout(resolve, 3000));

    const mockReport: ComplianceReport = {
      reportId: `RPT-${reportType}-${Date.now()}`,
      reportType: reportType as 'HUD' | 'HMIS' | 'CES' | 'HIPAA',
      status: 'complete',
      complianceScore: Math.floor(Math.random() * 30) + 70, // 70-100
      generatedAt: new Date().toISOString(),
      dataPoints: Math.floor(Math.random() * 1000) + 500,
      issues: generateMockIssues(reportType),
      recommendations: generateMockRecommendations(reportType),
      downloadUrl: `/api/reports/${reportType}-${Date.now()}.pdf`
    };

    setReports(prev => [mockReport, ...prev]);
    setComplianceScore(mockReport.complianceScore);
    setIsGenerating(false);
    onReportGenerated(mockReport);
  };

  const generateMockIssues = (reportType: string): ComplianceIssue[] => {
    const issues: ComplianceIssue[] = [];
    
    if (reportType === 'HUD') {
      issues.push({
        id: 'hud-001',
        severity: 'medium',
        category: 'Data Quality',
        description: 'Missing income verification for 15 clients',
        recommendation: 'Update client records with current income documentation',
        affectedRecords: 15
      });
    }
    
    if (reportType === 'HMIS') {
      issues.push({
        id: 'hmis-001',
        severity: 'low',
        category: 'Service Entry',
        description: 'Incomplete service entry data for 8 clients',
        recommendation: 'Complete service entry forms for all active clients',
        affectedRecords: 8
      });
    }
    
    if (reportType === 'CES') {
      issues.push({
        id: 'ces-001',
        severity: 'high',
        category: 'Assessment Data',
        description: 'Missing assessment scores for 3 high-priority clients',
        recommendation: 'Complete priority assessments immediately',
        affectedRecords: 3
      });
    }
    
    if (reportType === 'HIPAA') {
      issues.push({
        id: 'hipaa-001',
        severity: 'critical',
        category: 'Access Controls',
        description: 'Unauthorized access detected in audit logs',
        recommendation: 'Review and update access controls immediately',
        affectedRecords: 0
      });
    }
    
    return issues;
  };

  const generateMockRecommendations = (reportType: string): string[] => {
    const recommendations = [
      'Implement automated data validation',
      'Schedule regular compliance training',
      'Update data collection procedures',
      'Enhance audit logging capabilities'
    ];
    
    if (reportType === 'HUD') {
      recommendations.unshift('Improve income verification process');
    }
    
    if (reportType === 'HMIS') {
      recommendations.unshift('Standardize service entry procedures');
    }
    
    if (reportType === 'CES') {
      recommendations.unshift('Implement real-time assessment tracking');
    }
    
    if (reportType === 'HIPAA') {
      recommendations.unshift('Strengthen data encryption protocols');
    }
    
    return recommendations;
  };

  const getComplianceColor = (score: number) => {
    if (score >= 90) return 'text-green-600 bg-green-100';
    if (score >= 80) return 'text-yellow-600 bg-yellow-100';
    if (score >= 70) return 'text-orange-600 bg-orange-100';
    return 'text-red-600 bg-red-100';
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'text-red-600 bg-red-100';
      case 'high': return 'text-orange-600 bg-orange-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      default: return 'text-blue-600 bg-blue-100';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical': return <AlertTriangle className="h-4 w-4" />;
      case 'high': return <AlertTriangle className="h-4 w-4" />;
      case 'medium': return <AlertTriangle className="h-4 w-4" />;
      default: return <CheckCircle className="h-4 w-4" />;
    }
  };

  useEffect(() => {
    // Calculate overall compliance score
    if (reports.length > 0) {
      const avgScore = reports.reduce((sum, report) => sum + report.complianceScore, 0) / reports.length;
      setComplianceScore(Math.round(avgScore));
    }
  }, [reports]);

  return (
    <div className="space-y-6">
      {/* Overall Compliance Score */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
            Overall Compliance Status
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-4">
            <div className="text-3xl font-bold">{complianceScore}%</div>
            <div className="flex-1">
              <Progress value={complianceScore} className="h-2" />
              <div className="text-sm text-gray-600 mt-1">
                {complianceScore >= 90 ? 'Excellent' : 
                 complianceScore >= 80 ? 'Good' : 
                 complianceScore >= 70 ? 'Needs Improvement' : 'Critical Issues'}
              </div>
            </div>
            <Badge className={`${getComplianceColor(complianceScore)} px-3 py-1`}>
              {complianceScore >= 90 ? 'Compliant' : 
               complianceScore >= 80 ? 'Mostly Compliant' : 
               complianceScore >= 70 ? 'Partially Compliant' : 'Non-Compliant'}
            </Badge>
          </div>
        </CardContent>
      </Card>

      {/* Report Generation */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            Generate Compliance Reports
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {reportTypes.map((report) => (
              <Card 
                key={report.id}
                className={`cursor-pointer transition-all ${
                  selectedReportType === report.id 
                    ? 'ring-2 ring-blue-500 bg-blue-50' 
                    : 'hover:bg-gray-50'
                }`}
                onClick={() => setSelectedReportType(report.id)}
              >
                <CardContent className="p-4">
                  <div className="flex items-start gap-3">
                    <div className="text-blue-600">{report.icon}</div>
                    <div className="flex-1">
                      <h3 className="font-semibold">{report.name}</h3>
                      <p className="text-sm text-gray-600 mb-2">{report.description}</p>
                      <div className="text-xs text-gray-500">
                        <div className="font-medium mb-1">Requirements:</div>
                        <ul className="list-disc list-inside space-y-1">
                          {report.requirements.map((req, index) => (
                            <li key={index}>{req}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          <Button 
            onClick={() => generateReport(selectedReportType)}
            disabled={!selectedReportType || isGenerating}
            className="w-full"
          >
            {isGenerating ? 'Generating Report...' : 'Generate Report'}
          </Button>
        </CardContent>
      </Card>

      {/* Report Generation Status */}
      {isGenerating && (
        <Card>
          <CardContent className="p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <h3 className="text-lg font-semibold mb-2">Generating Compliance Report</h3>
            <p className="text-gray-600">Our AI is analyzing data and generating your compliance report...</p>
          </CardContent>
        </Card>
      )}

      {/* Generated Reports */}
      {reports.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Generated Reports</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {reports.map((report) => (
              <div key={report.reportId} className="border rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <FileText className="h-5 w-5 text-blue-600" />
                    <div>
                      <h3 className="font-semibold">{report.reportType} Report</h3>
                      <p className="text-sm text-gray-600">
                        Generated {new Date(report.generatedAt).toLocaleString()}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge className={`${getComplianceColor(report.complianceScore)} px-2 py-1`}>
                      {report.complianceScore}%
                    </Badge>
                    <Button size="sm" variant="outline">
                      <Download className="h-4 w-4 mr-1" />
                      Download
                    </Button>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <div className="text-gray-600">Data Points</div>
                    <div className="font-semibold">{report.dataPoints.toLocaleString()}</div>
                  </div>
                  <div>
                    <div className="text-gray-600">Issues Found</div>
                    <div className="font-semibold">{report.issues.length}</div>
                  </div>
                  <div>
                    <div className="text-gray-600">Status</div>
                    <div className="font-semibold capitalize">{report.status}</div>
                  </div>
                </div>

                {report.issues.length > 0 && (
                  <div className="mt-4">
                    <h4 className="font-semibold mb-2">Issues Found:</h4>
                    <div className="space-y-2">
                      {report.issues.map((issue) => (
                        <div key={issue.id} className="flex items-start gap-2 p-2 bg-gray-50 rounded">
                          <div className={`${getSeverityColor(issue.severity)} p-1 rounded`}>
                            {getSeverityIcon(issue.severity)}
                          </div>
                          <div className="flex-1">
                            <div className="font-medium">{issue.description}</div>
                            <div className="text-sm text-gray-600">{issue.recommendation}</div>
                            <div className="text-xs text-gray-500">
                              {issue.affectedRecords} records affected
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {report.recommendations.length > 0 && (
                  <div className="mt-4">
                    <h4 className="font-semibold mb-2">Recommendations:</h4>
                    <ul className="space-y-1">
                      {report.recommendations.map((rec, index) => (
                        <li key={index} className="flex items-start gap-2 text-sm">
                          <span className="text-blue-500 mt-1">•</span>
                          <span>{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ComplianceReporting;

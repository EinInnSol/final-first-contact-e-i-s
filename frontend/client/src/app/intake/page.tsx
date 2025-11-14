"use client";

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import axios from 'axios';

interface Question {
  id: string;
  section: string;
  question: string;
  type: string;
  required: boolean;
  options?: string[];
  max_selections?: number;
  hud_field: string;
}

export default function IntakePage() {
  const searchParams = useSearchParams();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentSection, setCurrentSection] = useState(0);
  const [responses, setResponses] = useState<Record<string, any>>({});
  const [metadata, setMetadata] = useState<Record<string, string>>({});
  const [clientInfo, setClientInfo] = useState({
    first_name: '',
    last_name: '',
    date_of_birth: '',
    phone: '',
    email: ''
  });
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [caseworkerInfo, setCaseworkerInfo] = useState<any>(null);

  useEffect(() => {
    // Extract QR code metadata from URL
    const loc = searchParams.get('loc');
    const vendor = searchParams.get('vendor');
    const area = searchParams.get('area');
    const org = searchParams.get('org');
    const qr = searchParams.get('qr');

    if (loc || vendor || area) {
      setMetadata({
        location_id: loc || '',
        vendor_id: vendor || '',
        area_code: area || '',
        organization_id: org || 'lb',
        qr_hash: qr || ''
      });
    }

    // Load HUD 40 questions
    loadQuestions();
  }, [searchParams]);

  const loadQuestions = async () => {
    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/intakes/forms/hud40`);
      setQuestions(response.data.questions);
    } catch (error) {
      console.error('Error loading questions:', error);
    }
  };

  const sections = [...new Set(questions.map(q => q.section))];
  const currentQuestions = questions.filter(q => q.section === sections[currentSection]);
  const progress = ((currentSection + 1) / sections.length) * 100;

  const handleResponse = (questionId: string, value: any) => {
    setResponses(prev => ({
      ...prev,
      [questionId]: value
    }));
  };

  const handleMultiSelect = (questionId: string, option: string, maxSelections?: number) => {
    const current = responses[questionId] || [];
    const newValue = current.includes(option)
      ? current.filter((v: string) => v !== option)
      : maxSelections && current.length >= maxSelections
      ? current
      : [...current, option];

    handleResponse(questionId, newValue);
  };

  const handleNext = () => {
    if (currentSection < sections.length - 1) {
      setCurrentSection(currentSection + 1);
      window.scrollTo(0, 0);
    }
  };

  const handlePrevious = () => {
    if (currentSection > 0) {
      setCurrentSection(currentSection - 1);
      window.scrollTo(0, 0);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);

    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/intakes/submit`,
        {
          client_info: clientInfo,
          assessment_responses: responses,
          metadata: metadata
        }
      );

      setCaseworkerInfo(response.data);
      setSubmitted(true);
    } catch (error) {
      console.error('Error submitting intake:', error);
      alert('Error submitting form. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const renderQuestion = (question: Question) => {
    const value = responses[question.id];

    switch (question.type) {
      case 'select':
        return (
          <div className="space-y-2">
            {question.options?.map((option, index) => (
              <button
                key={index}
                onClick={() => handleResponse(question.id, option)}
                className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                  value === option
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                    value === option ? 'border-blue-500 bg-blue-500' : 'border-gray-300'
                  }`}>
                    {value === option && (
                      <div className="w-2 h-2 bg-white rounded-full"></div>
                    )}
                  </div>
                  <span className="text-gray-800">{option}</span>
                </div>
              </button>
            ))}
          </div>
        );

      case 'multi-select':
        const selectedValues = value || [];
        return (
          <div className="space-y-2">
            {question.max_selections && (
              <p className="text-sm text-gray-600 mb-2">
                Select up to {question.max_selections} options
              </p>
            )}
            {question.options?.map((option, index) => (
              <button
                key={index}
                onClick={() => handleMultiSelect(question.id, option, question.max_selections)}
                className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                  selectedValues.includes(option)
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className={`w-5 h-5 rounded border-2 flex items-center justify-center ${
                    selectedValues.includes(option) ? 'border-blue-500 bg-blue-500' : 'border-gray-300'
                  }`}>
                    {selectedValues.includes(option) && (
                      <svg className="w-3 h-3 text-white" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                        <path d="M5 13l4 4L19 7"></path>
                      </svg>
                    )}
                  </div>
                  <span className="text-gray-800">{option}</span>
                </div>
              </button>
            ))}
          </div>
        );

      case 'number':
        return (
          <input
            type="number"
            value={value || ''}
            onChange={(e) => handleResponse(question.id, e.target.value)}
            className="w-full p-4 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none"
            min="0"
          />
        );

      case 'text':
        return (
          <textarea
            value={value || ''}
            onChange={(e) => handleResponse(question.id, e.target.value)}
            className="w-full p-4 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none"
            rows={4}
            placeholder="Please share any additional information..."
          />
        );

      default:
        return null;
    }
  };

  if (submitted && caseworkerInfo) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center p-4">
        <div className="max-w-2xl w-full bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center">
            <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-10 h-10 text-green-600" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                <path d="M5 13l4 4L19 7"></path>
              </svg>
            </div>

            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              Thank You for Completing Your Assessment
            </h1>

            <div className="bg-blue-50 rounded-lg p-6 my-6">
              <p className="text-lg text-gray-800 mb-4">
                You have been assigned:
              </p>
              <h2 className="text-2xl font-bold text-blue-900 mb-2">
                {caseworkerInfo.caseworker?.name?.toUpperCase()}
              </h2>
              <p className="text-xl text-gray-700 mb-2">
                Phone: {caseworkerInfo.caseworker?.phone}
              </p>
              <p className="text-lg text-gray-600">
                Expect a call at: <span className="font-semibold text-gray-900">{caseworkerInfo.appointment_time}</span>
              </p>
            </div>

            <div className="bg-gray-50 rounded-lg p-6 text-left">
              <h3 className="font-semibold text-gray-900 mb-2">Your Case Information:</h3>
              <p className="text-gray-700">Case Number: <span className="font-mono">{caseworkerInfo.case_number}</span></p>
              <p className="text-gray-700">Crisis Level: <span className="capitalize">{caseworkerInfo.crisis_level}</span></p>
            </div>

            <p className="text-gray-600 mt-6">
              We're here to help you every step of the way. Your caseworker will contact you soon to discuss next steps.
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (currentSection === -1) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center p-4">
        <div className="max-w-2xl w-full bg-white rounded-2xl shadow-xl p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Welcome to First Contact EIS</h1>

          {metadata.location_id && (
            <div className="bg-blue-50 rounded-lg p-4 mb-6">
              <p className="text-sm text-blue-800">
                Starting intake from: <span className="font-semibold">{metadata.location_id.replace(/_/g, ' ')}</span>
              </p>
            </div>
          )}

          <p className="text-gray-700 mb-6">
            Before we begin the assessment, please provide your contact information:
          </p>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">First Name *</label>
              <input
                type="text"
                value={clientInfo.first_name}
                onChange={(e) => setClientInfo({...clientInfo, first_name: e.target.value})}
                className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Last Name *</label>
              <input
                type="text"
                value={clientInfo.last_name}
                onChange={(e) => setClientInfo({...clientInfo, last_name: e.target.value})}
                className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Date of Birth *</label>
              <input
                type="date"
                value={clientInfo.date_of_birth}
                onChange={(e) => setClientInfo({...clientInfo, date_of_birth: e.target.value})}
                className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Phone Number *</label>
              <input
                type="tel"
                value={clientInfo.phone}
                onChange={(e) => setClientInfo({...clientInfo, phone: e.target.value})}
                className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none"
                placeholder="(555) 555-5555"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email (optional)</label>
              <input
                type="email"
                value={clientInfo.email}
                onChange={(e) => setClientInfo({...clientInfo, email: e.target.value})}
                className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none"
                placeholder="your@email.com"
              />
            </div>
          </div>

          <button
            onClick={() => setCurrentSection(0)}
            disabled={!clientInfo.first_name || !clientInfo.last_name || !clientInfo.date_of_birth || !clientInfo.phone}
            className="w-full mt-6 bg-blue-600 text-white py-4 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            Begin Assessment
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white p-4 pb-20">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-2xl font-bold text-gray-900">HUD Coordinated Entry Assessment</h1>
            <span className="text-sm text-gray-600">
              Section {currentSection + 1} of {sections.length}
            </span>
          </div>

          {/* Progress bar */}
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>

          <p className="text-gray-600 mt-4">
            Current section: <span className="font-semibold">{sections[currentSection]}</span>
          </p>
        </div>

        {/* Questions */}
        <div className="space-y-6">
          {currentQuestions.map((question) => (
            <div key={question.id} className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                {question.question}
                {question.required && <span className="text-red-500 ml-1">*</span>}
              </h3>
              {renderQuestion(question)}
            </div>
          ))}
        </div>

        {/* Navigation */}
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 shadow-lg">
          <div className="max-w-3xl mx-auto flex justify-between gap-4">
            <button
              onClick={handlePrevious}
              disabled={currentSection === 0}
              className="px-6 py-3 border-2 border-gray-300 rounded-lg font-semibold text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Previous
            </button>

            {currentSection < sections.length - 1 ? (
              <button
                onClick={handleNext}
                className="px-8 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                Next Section
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="px-8 py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 disabled:bg-gray-400 transition-colors"
              >
                {loading ? 'Submitting...' : 'Submit Assessment'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

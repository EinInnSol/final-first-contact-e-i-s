"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { 
  Search, 
  MapPin, 
  Phone, 
  Clock, 
  Star, 
  Users,
  Home,
  Heart,
  Briefcase,
  Car,
  Shield,
  GraduationCap
} from 'lucide-react';

interface ResourceMatcherProps {
  onResourcesFound: (resources: Resource[]) => void;
  language?: string;
}

interface Resource {
  id: string;
  name: string;
  type: string;
  description: string;
  address: string;
  phone: string;
  email: string;
  website: string;
  distance: number;
  rating: number;
  availability: 'available' | 'limited' | 'waitlist' | 'unavailable';
  eligibility: string[];
  requirements: string[];
  hours: string;
  lastUpdated: string;
  matchScore: number;
}

const ResourceMatcher: React.FC<ResourceMatcherProps> = ({ onResourcesFound, language = 'en' }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [clientProfile, setClientProfile] = useState({
    needs: [] as string[],
    location: '',
    preferences: [] as string[],
    constraints: [] as string[]
  });
  const [isSearching, setIsSearching] = useState(false);
  const [resources, setResources] = useState<Resource[]>([]);
  const [selectedFilters, setSelectedFilters] = useState<string[]>([]);

  const resourceTypes = [
    { id: 'housing', name: 'Housing', icon: <Home className="h-4 w-4" /> },
    { id: 'healthcare', name: 'Healthcare', icon: <Heart className="h-4 w-4" /> },
    { id: 'employment', name: 'Employment', icon: <Briefcase className="h-4 w-4" /> },
    { id: 'transportation', name: 'Transportation', icon: <Car className="h-4 w-4" /> },
    { id: 'education', name: 'Education', icon: <GraduationCap className="h-4 w-4" /> },
    { id: 'legal', name: 'Legal Services', icon: <Shield className="h-4 w-4" /> }
  ];

  const mockResources: Resource[] = [
    {
      id: '1',
      name: 'Long Beach Housing Authority',
      type: 'housing',
      description: 'Emergency and transitional housing assistance for families and individuals',
      address: '1234 Pine Ave, Long Beach, CA 90813',
      phone: '(562) 570-6944',
      email: 'info@lbha.org',
      website: 'https://lbha.org',
      distance: 2.3,
      rating: 4.5,
      availability: 'available',
      eligibility: ['Low income', 'Homeless', 'At-risk families'],
      requirements: ['Income verification', 'ID', 'Proof of homelessness'],
      hours: 'Mon-Fri 8AM-5PM',
      lastUpdated: '2024-01-15',
      matchScore: 95
    },
    {
      id: '2',
      name: 'WomenShelter of Long Beach',
      type: 'housing',
      description: 'Emergency shelter and support services for domestic violence survivors',
      address: '4567 Ocean Blvd, Long Beach, CA 90803',
      phone: '(562) 437-4663',
      email: 'info@womenshelterlb.org',
      website: 'https://womenshelterlb.org',
      distance: 1.8,
      rating: 4.8,
      availability: 'limited',
      eligibility: ['Domestic violence survivors', 'Women and children'],
      requirements: ['Crisis assessment', 'Safety planning'],
      hours: '24/7 Crisis Line',
      lastUpdated: '2024-01-14',
      matchScore: 88
    },
    {
      id: '3',
      name: 'CalWORKs Long Beach',
      type: 'employment',
      description: 'Employment services, job training, and financial assistance',
      address: '7890 Atlantic Ave, Long Beach, CA 90804',
      phone: '(562) 570-3800',
      email: 'calworks@dss.ca.gov',
      website: 'https://calworks.ca.gov',
      distance: 3.1,
      rating: 4.2,
      availability: 'available',
      eligibility: ['Low income families', 'Unemployed', 'Underemployed'],
      requirements: ['Income verification', 'Work registration', 'Child care needs assessment'],
      hours: 'Mon-Fri 8AM-5PM',
      lastUpdated: '2024-01-16',
      matchScore: 92
    },
    {
      id: '4',
      name: 'Mental Health America of Long Beach',
      type: 'healthcare',
      description: 'Mental health counseling, crisis intervention, and support groups',
      address: '3210 Cherry Ave, Long Beach, CA 90807',
      phone: '(562) 435-2222',
      email: 'info@mhalb.org',
      website: 'https://mhalb.org',
      distance: 4.2,
      rating: 4.6,
      availability: 'available',
      eligibility: ['Mental health needs', 'Crisis situations', 'General public'],
      requirements: ['Intake assessment', 'Insurance verification'],
      hours: 'Mon-Fri 9AM-6PM, Sat 10AM-2PM',
      lastUpdated: '2024-01-13',
      matchScore: 87
    },
    {
      id: '5',
      name: 'Long Beach Transit',
      type: 'transportation',
      description: 'Public transportation services and reduced fare programs',
      address: '1963 E Anaheim St, Long Beach, CA 90813',
      phone: '(562) 591-2301',
      email: 'info@lbtransit.com',
      website: 'https://lbtransit.com',
      distance: 1.5,
      rating: 4.0,
      availability: 'available',
      eligibility: ['General public', 'Low income', 'Seniors', 'Disabled'],
      requirements: ['ID for reduced fare', 'Income verification for programs'],
      hours: 'Varies by route',
      lastUpdated: '2024-01-12',
      matchScore: 78
    }
  ];

  const searchResources = async () => {
    setIsSearching(true);
    
    // Simulate AI resource matching
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Filter resources based on search query and filters
    let filteredResources = mockResources;

    if (searchQuery) {
      filteredResources = filteredResources.filter(resource =>
        resource.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        resource.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        resource.type.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    if (selectedFilters.length > 0) {
      filteredResources = filteredResources.filter(resource =>
        selectedFilters.includes(resource.type)
      );
    }

    // Calculate match scores based on client profile
    const scoredResources = filteredResources.map(resource => {
      let matchScore = 0;
      
      // Base score
      matchScore += 50;
      
      // Distance scoring (closer is better)
      if (resource.distance < 2) matchScore += 20;
      else if (resource.distance < 5) matchScore += 15;
      else if (resource.distance < 10) matchScore += 10;
      
      // Availability scoring
      if (resource.availability === 'available') matchScore += 20;
      else if (resource.availability === 'limited') matchScore += 10;
      else if (resource.availability === 'waitlist') matchScore += 5;
      
      // Rating scoring
      matchScore += resource.rating * 2;
      
      // Eligibility matching
      const eligibilityMatches = resource.eligibility.filter(elig =>
        clientProfile.needs.some(need => 
          elig.toLowerCase().includes(need.toLowerCase())
        )
      ).length;
      matchScore += eligibilityMatches * 5;
      
      return {
        ...resource,
        matchScore: Math.min(matchScore, 100)
      };
    });

    // Sort by match score
    scoredResources.sort((a, b) => b.matchScore - a.matchScore);

    setResources(scoredResources);
    setIsSearching(false);
    onResourcesFound(scoredResources);
  };

  const getAvailabilityColor = (availability: string) => {
    switch (availability) {
      case 'available': return 'text-green-600 bg-green-100';
      case 'limited': return 'text-yellow-600 bg-yellow-100';
      case 'waitlist': return 'text-orange-600 bg-orange-100';
      default: return 'text-red-600 bg-red-100';
    }
  };

  const getTypeIcon = (type: string) => {
    const typeConfig = resourceTypes.find(t => t.id === type);
    return typeConfig ? typeConfig.icon : <Home className="h-4 w-4" />;
  };

  const getMatchScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600 bg-green-100';
    if (score >= 80) return 'text-blue-600 bg-blue-100';
    if (score >= 70) return 'text-yellow-600 bg-yellow-100';
    return 'text-orange-600 bg-orange-100';
  };

  const toggleFilter = (filterId: string) => {
    setSelectedFilters(prev =>
      prev.includes(filterId)
        ? prev.filter(id => id !== filterId)
        : [...prev, filterId]
    );
  };

  return (
    <div className="space-y-6">
      {/* Search Interface */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Search className="h-5 w-5" />
            AI Resource Matcher
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Search for resources:</label>
            <Input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by name, type, or description..."
              className="w-full"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Resource Types:</label>
            <div className="flex flex-wrap gap-2">
              {resourceTypes.map((type) => (
                <Button
                  key={type.id}
                  variant={selectedFilters.includes(type.id) ? "default" : "outline"}
                  size="sm"
                  onClick={() => toggleFilter(type.id)}
                  className="flex items-center gap-2"
                >
                  {type.icon}
                  {type.name}
                </Button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Client Needs (optional):</label>
            <Textarea
              value={clientProfile.needs.join(', ')}
              onChange={(e) => setClientProfile(prev => ({
                ...prev,
                needs: e.target.value.split(',').map(need => need.trim()).filter(Boolean)
              }))}
              placeholder="Enter client needs separated by commas (e.g., housing, mental health, employment)"
              className="w-full"
            />
          </div>

          <Button 
            onClick={searchResources}
            disabled={isSearching}
            className="w-full"
          >
            {isSearching ? 'Searching Resources...' : 'Find Resources'}
          </Button>
        </CardContent>
      </Card>

      {/* Search Status */}
      {isSearching && (
        <Card>
          <CardContent className="p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <h3 className="text-lg font-semibold mb-2">Matching Resources</h3>
            <p className="text-gray-600">Our AI is analyzing your needs and finding the best resources...</p>
          </CardContent>
        </Card>
      )}

      {/* Search Results */}
      {resources.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Found {resources.length} Resources</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {resources.map((resource) => (
              <div key={resource.id} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-start gap-3">
                    <div className="text-blue-600 mt-1">
                      {getTypeIcon(resource.type)}
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-lg">{resource.name}</h3>
                      <p className="text-gray-600 mb-2">{resource.description}</p>
                      <div className="flex items-center gap-4 text-sm text-gray-500">
                        <div className="flex items-center gap-1">
                          <MapPin className="h-4 w-4" />
                          {resource.distance} miles
                        </div>
                        <div className="flex items-center gap-1">
                          <Star className="h-4 w-4" />
                          {resource.rating}/5
                        </div>
                        <div className="flex items-center gap-1">
                          <Clock className="h-4 w-4" />
                          {resource.hours}
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="flex flex-col items-end gap-2">
                    <Badge className={`${getMatchScoreColor(resource.matchScore)} px-2 py-1`}>
                      {resource.matchScore}% Match
                    </Badge>
                    <Badge className={`${getAvailabilityColor(resource.availability)} px-2 py-1`}>
                      {resource.availability}
                    </Badge>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <div className="font-medium mb-1">Contact Information:</div>
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <MapPin className="h-4 w-4" />
                        {resource.address}
                      </div>
                      <div className="flex items-center gap-2">
                        <Phone className="h-4 w-4" />
                        {resource.phone}
                      </div>
                      {resource.email && (
                        <div className="flex items-center gap-2">
                          <span className="w-4 h-4">✉</span>
                          {resource.email}
                        </div>
                      )}
                    </div>
                  </div>
                  <div>
                    <div className="font-medium mb-1">Eligibility:</div>
                    <div className="flex flex-wrap gap-1">
                      {resource.eligibility.map((elig, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {elig}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>

                {resource.requirements.length > 0 && (
                  <div className="mt-3">
                    <div className="font-medium mb-1">Requirements:</div>
                    <ul className="text-sm text-gray-600">
                      {resource.requirements.map((req, index) => (
                        <li key={index} className="flex items-start gap-2">
                          <span className="text-blue-500 mt-1">•</span>
                          <span>{req}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                <div className="flex gap-2 mt-4">
                  <Button size="sm" variant="outline">
                    <Phone className="h-4 w-4 mr-1" />
                    Call
                  </Button>
                  <Button size="sm" variant="outline">
                    <MapPin className="h-4 w-4 mr-1" />
                    Directions
                  </Button>
                  <Button size="sm" variant="outline">
                    <Users className="h-4 w-4 mr-1" />
                    Refer Client
                  </Button>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {!isSearching && resources.length === 0 && searchQuery && (
        <Card>
          <CardContent className="p-8 text-center">
            <Search className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">No Resources Found</h3>
            <p className="text-gray-600">Try adjusting your search criteria or contact a caseworker for assistance.</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ResourceMatcher;

'use client'

import React, { useState } from 'react'
import { MapPin, TrendingUp, DollarSign, Users, Home, Calendar, Filter, Download } from 'lucide-react'

export function CityDashboard() {
  const [selectedMetric, setSelectedMetric] = useState('spending')
  const [timeRange, setTimeRange] = useState('month')

  // Mock data
  const metrics = [
    { id: 'spending', label: 'Total Spending', value: '$4.2M', change: '+12%', icon: DollarSign, color: 'primary' },
    { id: 'housed', label: 'People Housed', value: '127', change: '+24%', icon: Home, color: 'success' },
    { id: 'active', label: 'Active Cases', value: '1,834', change: '+8%', icon: Users, color: 'warning' },
    { id: 'utilization', label: 'Resource Use', value: '87%', change: '+15%', icon: TrendingUp, color: 'info' },
  ]

  const hotspots = [
    { name: 'MLK Park', intakes: 47, lat: 33.7701, lng: -118.1937, color: '#DC2626' },
    { name: 'Transit Center', intakes: 32, lat: 33.7683, lng: -118.1889, color: '#EA580C' },
    { name: 'Beach Blvd Shelter', intakes: 28, lat: 33.7665, lng: -118.1912, color: '#CA8A04' },
    { name: 'Pine Ave', intakes: 19, lat: 33.7695, lng: -118.1920, color: '#65A30D' },
  ]

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Top Navigation */}
      <nav className="bg-white border-b border-neutral-200 shadow-sm sticky top-0 z-50">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-11 h-11 bg-gradient-to-br from-info-600 to-info-700 rounded-lg flex items-center justify-center shadow-md">
                <span className="text-white font-bold text-xl">FC</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-neutral-900">First Contact E.I.S.</h1>
                <p className="text-sm text-neutral-500">City Analytics Dashboard</p>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <select 
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value)}
                className="px-4 py-2 border border-neutral-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-info-500"
              >
                <option value="week">Last Week</option>
                <option value="month">Last Month</option>
                <option value="quarter">Last Quarter</option>
                <option value="year">Last Year</option>
              </select>
              
              <button className="px-4 py-2 bg-info-600 text-white rounded-lg text-sm font-medium hover:bg-info-700 transition-colors flex items-center gap-2">
                <Download className="w-4 h-4" />
                Export Report
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* 3-PANEL LAYOUT WITH MAP IN CENTER */}
      <div className="flex h-[calc(100vh-89px)]">
        
        {/* LEFT PANEL: Metrics & Filters */}
        <div className="w-80 bg-white border-r border-neutral-200 flex flex-col overflow-hidden">
          {/* Key Metrics */}
          <div className="p-4 border-b border-neutral-200">
            <h2 className="text-sm font-semibold text-neutral-900 mb-3">Key Performance Indicators</h2>
            <div className="space-y-2">
              {metrics.map(metric => (
                <button
                  key={metric.id}
                  onClick={() => setSelectedMetric(metric.id)}
                  className={`w-full p-3 rounded-lg border transition-all ${
                    selectedMetric === metric.id
                      ? 'bg-info-50 border-info-300 shadow-sm'
                      : 'bg-white border-neutral-200 hover:border-neutral-300'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                      metric.color === 'primary' ? 'bg-primary-100 text-primary-600' :
                      metric.color === 'success' ? 'bg-success-100 text-success-600' :
                      metric.color === 'warning' ? 'bg-warning-100 text-warning-600' :
                      'bg-info-100 text-info-600'
                    }`}>
                      <metric.icon className="w-5 h-5" />
                    </div>
                    <div className="flex-1 text-left">
                      <div className="text-xs text-neutral-500">{metric.label}</div>
                      <div className="flex items-baseline gap-2">
                        <div className="text-lg font-bold text-neutral-900">{metric.value}</div>
                        <div className="text-xs text-success-600 font-medium">{metric.change}</div>
                      </div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Top Hotspots */}
          <div className="flex-1 overflow-y-auto p-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-semibold text-neutral-900">Service Hotspots</h2>
              <button className="text-xs text-info-600 hover:text-info-700 font-medium">View All</button>
            </div>
            <div className="space-y-2">
              {hotspots.map(spot => (
                <div key={spot.name} className="p-3 bg-neutral-50 border border-neutral-200 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <MapPin className="w-4 h-4" style={{ color: spot.color }} />
                    <div className="font-semibold text-sm text-neutral-900">{spot.name}</div>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="text-xs text-neutral-500">Intakes this month</div>
                    <div className="text-sm font-bold text-neutral-900">{spot.intakes}</div>
                  </div>
                  <div className="mt-2 h-2 bg-neutral-200 rounded-full overflow-hidden">
                    <div 
                      className="h-full rounded-full transition-all"
                      style={{ 
                        width: `${(spot.intakes / 50) * 100}%`,
                        backgroundColor: spot.color 
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* CENTER PANEL: INTERACTIVE MAP */}
        <div className="flex-1 bg-neutral-100 relative">
          {/* Map Container */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <MapPin className="w-24 h-24 text-neutral-300 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-neutral-900 mb-2">Interactive Map</h3>
              <p className="text-neutral-500 mb-4">Mapbox integration would render here</p>
              <div className="inline-block px-4 py-2 bg-info-100 text-info-700 rounded-lg text-sm font-medium">
                Showing {hotspots.length} service hotspots in Long Beach
              </div>
            </div>
          </div>

          {/* Map Legend (Bottom Left) */}
          <div className="absolute bottom-6 left-6 bg-white rounded-lg shadow-lg p-4 border border-neutral-200">
            <div className="text-xs font-semibold text-neutral-900 mb-2">Intake Volume</div>
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-red-600"></div>
                <div className="text-xs text-neutral-600">40+ intakes</div>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-orange-600"></div>
                <div className="text-xs text-neutral-600">30-39 intakes</div>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-yellow-600"></div>
                <div className="text-xs text-neutral-600">20-29 intakes</div>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-green-600"></div>
                <div className="text-xs text-neutral-600">10-19 intakes</div>
              </div>
            </div>
          </div>

          {/* Map Controls (Top Right) */}
          <div className="absolute top-6 right-6 flex flex-col gap-2">
            <button className="w-10 h-10 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow flex items-center justify-center border border-neutral-200">
              <span className="text-xl font-bold text-neutral-700">+</span>
            </button>
            <button className="w-10 h-10 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow flex items-center justify-center border border-neutral-200">
              <span className="text-xl font-bold text-neutral-700">−</span>
            </button>
          </div>
        </div>

        {/* RIGHT PANEL: Detailed Analytics */}
        <div className="w-96 bg-white border-l border-neutral-200 overflow-y-auto">
          <div className="p-6">
            <h2 className="text-lg font-bold text-neutral-900 mb-4">Detailed Analytics</h2>
            
            {/* Cost Breakdown */}
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-neutral-900 mb-3">Cost Per Outcome</h3>
              <div className="space-y-3">
                <div className="p-4 bg-neutral-50 rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <div className="text-sm text-neutral-600">Permanent Housing</div>
                    <div className="text-lg font-bold text-neutral-900">$18,400</div>
                  </div>
                  <div className="text-xs text-success-600 font-medium">↓ 42% vs last year</div>
                </div>

                <div className="p-4 bg-neutral-50 rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <div className="text-sm text-neutral-600">Temporary Shelter</div>
                    <div className="text-lg font-bold text-neutral-900">$4,200</div>
                  </div>
                  <div className="text-xs text-success-600 font-medium">↓ 28% vs last year</div>
                </div>

                <div className="p-4 bg-neutral-50 rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <div className="text-sm text-neutral-600">Average Per Client</div>
                    <div className="text-lg font-bold text-neutral-900">$21,300</div>
                  </div>
                  <div className="text-xs text-success-600 font-medium">↓ 52% vs last year</div>
                </div>
              </div>
            </div>

            {/* Program Efficiency */}
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-neutral-900 mb-3">Program Efficiency</h3>
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <div className="text-sm text-neutral-600">Housing Retention</div>
                  <div className="text-sm font-bold text-success-600">78%</div>
                </div>
                <div className="w-full h-2 bg-neutral-200 rounded-full overflow-hidden">
                  <div className="h-full bg-success-500 rounded-full" style={{ width: '78%' }} />
                </div>

                <div className="flex justify-between items-center mt-3">
                  <div className="text-sm text-neutral-600">Appointment Utilization</div>
                  <div className="text-sm font-bold text-info-600">87%</div>
                </div>
                <div className="w-full h-2 bg-neutral-200 rounded-full overflow-hidden">
                  <div className="h-full bg-info-500 rounded-full" style={{ width: '87%' }} />
                </div>

                <div className="flex justify-between items-center mt-3">
                  <div className="text-sm text-neutral-600">Document Completion</div>
                  <div className="text-sm font-bold text-warning-600">64%</div>
                </div>
                <div className="w-full h-2 bg-neutral-200 rounded-full overflow-hidden">
                  <div className="h-full bg-warning-500 rounded-full" style={{ width: '64%' }} />
                </div>
              </div>
            </div>

            {/* Recent Activity */}
            <div>
              <h3 className="text-sm font-semibold text-neutral-900 mb-3">Recent Activity</h3>
              <div className="space-y-2">
                {[
                  { time: '2 hours ago', text: '3 new housing placements', icon: Home },
                  { time: '5 hours ago', text: '47 intakes at MLK Park', icon: MapPin },
                  { time: 'Yesterday', text: '12 appointments optimized', icon: Calendar },
                ].map((activity, idx) => (
                  <div key={idx} className="flex items-start gap-3 p-3 bg-neutral-50 rounded-lg">
                    <activity.icon className="w-4 h-4 text-neutral-400 mt-0.5" />
                    <div className="flex-1">
                      <div className="text-sm text-neutral-900">{activity.text}</div>
                      <div className="text-xs text-neutral-500 mt-0.5">{activity.time}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  )
}

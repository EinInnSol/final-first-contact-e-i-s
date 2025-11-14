"use client";

import { useState, useEffect } from 'react';

interface VendorMetrics {
  id: string;
  name: string;
  contract_value: number;
  clients_served: number;
  success_rate: number;
  avg_time_to_housing: number;
  compliance_score: number;
  areas_covered: string[];
}

interface AreaMetrics {
  area_code: string;
  name: string;
  qr_scans: number;
  intakes_completed: number;
  crisis_level_avg: number;
  top_needs: string[];
}

export default function CityCommandCenter() {
  const [selectedView, setSelectedView] = useState<'overview' | 'vendors' | 'areas' | 'impact'>('overview');
  const [timeRange, setTimeRange] = useState<'24h' | '7d' | '30d' | '90d'>('30d');

  // Mock data - would come from API
  const systemMetrics = {
    total_clients: 1247,
    active_cases: 342,
    housing_placements: 89,
    avg_time_to_placement: 23,
    total_spend: 4250000,
    cost_per_placement: 47752,
    vendors_active: 12,
    compliance_rate: 98.5
  };

  const vendors: VendorMetrics[] = [
    {
      id: 'v1',
      name: 'Coastal Homeless Services',
      contract_value: 1200000,
      clients_served: 425,
      success_rate: 87,
      avg_time_to_housing: 21,
      compliance_score: 99,
      areas_covered: ['90802', '90806', '90813']
    },
    {
      id: 'v2',
      name: 'Pacific Housing Solutions',
      contract_value: 850000,
      clients_served: 312,
      success_rate: 92,
      avg_time_to_housing: 18,
      compliance_score: 98,
      areas_covered: ['90805', '90815']
    },
    {
      id: 'v3',
      name: 'Community Care Network',
      contract_value: 650000,
      clients_served: 245,
      success_rate: 84,
      avg_time_to_housing: 26,
      compliance_score: 97,
      areas_covered: ['90804', '90807']
    },
    {
      id: 'v4',
      name: 'Long Beach Family Services',
      contract_value: 550000,
      clients_served: 198,
      success_rate: 89,
      avg_time_to_housing: 22,
      compliance_score: 99,
      areas_covered: ['90802', '90803']
    }
  ];

  const areas: AreaMetrics[] = [
    {
      area_code: '90802',
      name: 'Downtown',
      qr_scans: 234,
      intakes_completed: 187,
      crisis_level_avg: 68,
      top_needs: ['Emergency Shelter', 'Food', 'Medical Care']
    },
    {
      area_code: '90806',
      name: 'Cambodia Town',
      qr_scans: 189,
      intakes_completed: 156,
      crisis_level_avg: 72,
      top_needs: ['Housing', 'Employment', 'Language Services']
    },
    {
      area_code: '90813',
      name: 'West Side',
      qr_scans: 156,
      intakes_completed: 132,
      crisis_level_avg: 65,
      top_needs: ['Housing', 'Childcare', 'Transportation']
    },
    {
      area_code: '90805',
      name: 'North Long Beach',
      qr_scans: 145,
      intakes_completed: 119,
      crisis_level_avg: 59,
      top_needs: ['Employment', 'Mental Health', 'Housing']
    },
    {
      area_code: '90815',
      name: 'East Side',
      qr_scans: 98,
      intakes_completed: 81,
      crisis_level_avg: 54,
      top_needs: ['Financial Assistance', 'Food', 'Healthcare']
    }
  ];

  const recentActivity = [
    { time: '2 min ago', event: 'New intake completed', area: 'Downtown (90802)', vendor: 'Coastal Homeless Services' },
    { time: '5 min ago', event: 'Housing placement confirmed', area: 'Cambodia Town (90806)', vendor: 'Pacific Housing Solutions' },
    { time: '12 min ago', event: 'Compliance report submitted', area: 'West Side (90813)', vendor: 'Coastal Homeless Services' },
    { time: '18 min ago', event: 'Crisis intervention initiated', area: 'Downtown (90802)', vendor: 'Community Care Network' },
    { time: '23 min ago', event: 'Case successfully closed', area: 'North Long Beach (90805)', vendor: 'Pacific Housing Solutions' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 text-white p-6">
      <div className="max-w-[1800px] mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-4xl font-bold mb-2">City Command Center</h1>
              <p className="text-blue-300">City of Long Beach - Homeless Services Oversight Dashboard</p>
            </div>
            <div className="flex gap-3">
              <select
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value as any)}
                className="bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white"
              >
                <option value="24h">Last 24 Hours</option>
                <option value="7d">Last 7 Days</option>
                <option value="30d">Last 30 Days</option>
                <option value="90d">Last 90 Days</option>
              </select>
              <button className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg font-semibold transition-colors">
                Export Report
              </button>
            </div>
          </div>

          {/* View Tabs */}
          <div className="flex gap-2">
            {(['overview', 'vendors', 'areas', 'impact'] as const).map((view) => (
              <button
                key={view}
                onClick={() => setSelectedView(view)}
                className={`px-6 py-3 rounded-t-lg font-semibold transition-colors ${
                  selectedView === view
                    ? 'bg-white/20 border-t-4 border-blue-400'
                    : 'bg-white/5 hover:bg-white/10'
                }`}
              >
                {view.charAt(0).toUpperCase() + view.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-4 gap-6 mb-8">
          <div className="bg-gradient-to-br from-blue-600 to-blue-800 rounded-xl p-6 shadow-2xl">
            <p className="text-blue-200 text-sm mb-2">Total Clients Served</p>
            <p className="text-5xl font-bold mb-2">{systemMetrics.total_clients.toLocaleString()}</p>
            <p className="text-green-300 text-sm">↑ 12% from last month</p>
          </div>

          <div className="bg-gradient-to-br from-purple-600 to-purple-800 rounded-xl p-6 shadow-2xl">
            <p className="text-purple-200 text-sm mb-2">Active Cases</p>
            <p className="text-5xl font-bold mb-2">{systemMetrics.active_cases}</p>
            <p className="text-yellow-300 text-sm">23 require urgent attention</p>
          </div>

          <div className="bg-gradient-to-br from-green-600 to-green-800 rounded-xl p-6 shadow-2xl">
            <p className="text-green-200 text-sm mb-2">Housing Placements</p>
            <p className="text-5xl font-bold mb-2">{systemMetrics.housing_placements}</p>
            <p className="text-green-300 text-sm">↑ 18% from last month</p>
          </div>

          <div className="bg-gradient-to-br from-orange-600 to-orange-800 rounded-xl p-6 shadow-2xl">
            <p className="text-orange-200 text-sm mb-2">Avg Time to Placement</p>
            <p className="text-5xl font-bold mb-2">{systemMetrics.avg_time_to_placement}<span className="text-2xl">d</span></p>
            <p className="text-green-300 text-sm">↓ 3 days from last month</p>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-6">
          {/* Main Content Area */}
          <div className="col-span-2 space-y-6">
            {/* Vendor Performance */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 shadow-2xl">
              <h2 className="text-2xl font-bold mb-6">Vendor Performance Overview</h2>
              <div className="space-y-4">
                {vendors.map((vendor, idx) => (
                  <div key={vendor.id} className="bg-white/5 rounded-lg p-4 hover:bg-white/10 transition-colors">
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h3 className="font-bold text-lg">{vendor.name}</h3>
                        <p className="text-sm text-gray-300">
                          Contract: ${(vendor.contract_value / 1000000).toFixed(2)}M | Areas: {vendor.areas_covered.join(', ')}
                        </p>
                      </div>
                      <div className={`px-3 py-1 rounded-full text-sm font-semibold ${
                        vendor.success_rate >= 90 ? 'bg-green-500/20 text-green-300' :
                        vendor.success_rate >= 85 ? 'bg-yellow-500/20 text-yellow-300' :
                        'bg-red-500/20 text-red-300'
                      }`}>
                        {vendor.success_rate}% Success Rate
                      </div>
                    </div>

                    <div className="grid grid-cols-4 gap-4">
                      <div>
                        <p className="text-xs text-gray-400 mb-1">Clients Served</p>
                        <p className="text-2xl font-bold">{vendor.clients_served}</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-400 mb-1">Avg Time to Housing</p>
                        <p className="text-2xl font-bold">{vendor.avg_time_to_housing}d</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-400 mb-1">Compliance Score</p>
                        <p className="text-2xl font-bold">{vendor.compliance_score}%</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-400 mb-1">Cost per Client</p>
                        <p className="text-2xl font-bold">${Math.round(vendor.contract_value / vendor.clients_served).toLocaleString()}</p>
                      </div>
                    </div>

                    {/* Performance Bar */}
                    <div className="mt-3">
                      <div className="w-full bg-gray-700 rounded-full h-2">
                        <div
                          className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full transition-all"
                          style={{ width: `${vendor.success_rate}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Geographic Heatmap Data */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 shadow-2xl">
              <h2 className="text-2xl font-bold mb-6">Geographic Distribution</h2>
              <div className="grid grid-cols-2 gap-4">
                {areas.map((area) => (
                  <div key={area.area_code} className="bg-white/5 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h3 className="font-bold">{area.name}</h3>
                        <p className="text-sm text-gray-400">ZIP: {area.area_code}</p>
                      </div>
                      <div className={`px-2 py-1 rounded text-xs font-semibold ${
                        area.crisis_level_avg >= 70 ? 'bg-red-500/20 text-red-300' :
                        area.crisis_level_avg >= 60 ? 'bg-orange-500/20 text-orange-300' :
                        'bg-yellow-500/20 text-yellow-300'
                      }`}>
                        Crisis: {area.crisis_level_avg}
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-3 mb-3">
                      <div>
                        <p className="text-xs text-gray-400">QR Scans</p>
                        <p className="text-xl font-bold">{area.qr_scans}</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-400">Intakes</p>
                        <p className="text-xl font-bold">{area.intakes_completed}</p>
                      </div>
                    </div>

                    <div>
                      <p className="text-xs text-gray-400 mb-1">Top Needs:</p>
                      <div className="flex flex-wrap gap-1">
                        {area.top_needs.map((need, idx) => (
                          <span key={idx} className="text-xs bg-blue-500/20 text-blue-300 px-2 py-1 rounded">
                            {need}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* System Health */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 shadow-2xl">
              <h2 className="text-xl font-bold mb-4">System Health</h2>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Compliance Rate</span>
                    <span className="font-semibold">{systemMetrics.compliance_rate}%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-green-500 h-2 rounded-full" style={{ width: `${systemMetrics.compliance_rate}%` }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Active Vendors</span>
                    <span className="font-semibold">{systemMetrics.vendors_active}/15</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${(systemMetrics.vendors_active / 15) * 100}%` }}></div>
                  </div>
                </div>

                <div className="pt-4 border-t border-white/20">
                  <p className="text-sm text-gray-400 mb-2">Total Contract Spend</p>
                  <p className="text-3xl font-bold">${(systemMetrics.total_spend / 1000000).toFixed(2)}M</p>
                  <p className="text-xs text-gray-400 mt-1">Cost per placement: ${systemMetrics.cost_per_placement.toLocaleString()}</p>
                </div>
              </div>
            </div>

            {/* Real-time Activity Feed */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 shadow-2xl">
              <h2 className="text-xl font-bold mb-4">Real-Time Activity</h2>
              <div className="space-y-3">
                {recentActivity.map((activity, idx) => (
                  <div key={idx} className="bg-white/5 rounded-lg p-3 text-sm">
                    <p className="text-gray-400 text-xs mb-1">{activity.time}</p>
                    <p className="font-semibold mb-1">{activity.event}</p>
                    <p className="text-xs text-blue-300">{activity.area}</p>
                    <p className="text-xs text-gray-400">{activity.vendor}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* AI Insights */}
            <div className="bg-gradient-to-br from-purple-600/20 to-blue-600/20 backdrop-blur-lg rounded-xl p-6 border border-purple-400/30 shadow-2xl">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <span>🤖</span>
                AI Insights
              </h2>
              <div className="space-y-3 text-sm">
                <div className="bg-white/10 rounded p-3">
                  <p className="font-semibold mb-1">⚡ Resource Optimization</p>
                  <p className="text-gray-300">Pacific Housing Solutions is outperforming with 92% success rate. Consider reallocating 15% budget from underperforming vendors.</p>
                </div>
                <div className="bg-white/10 rounded p-3">
                  <p className="font-semibold mb-1">📍 Geographic Trend</p>
                  <p className="text-gray-300">Cambodia Town (90806) showing elevated crisis levels. Deploy additional resources and QR codes.</p>
                </div>
                <div className="bg-white/10 rounded p-3">
                  <p className="font-semibold mb-1">💰 Cost Efficiency</p>
                  <p className="text-gray-300">Potential savings of $125K by optimizing vendor assignments based on geographic proximity.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

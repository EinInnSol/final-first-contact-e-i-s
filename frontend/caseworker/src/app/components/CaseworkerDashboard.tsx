'use client'

import React, { useState } from 'react'
import { Users, Bell, Filter, Search, Clock, CheckCircle2, AlertCircle, Activity } from 'lucide-react'
import { RecommendationsFeed } from './RecommendationsFeed'

export function CaseworkerDashboard() {
  const [selectedClient, setSelectedClient] = useState<string | null>(null)
  const [filterStatus, setFilterStatus] = useState('all')

  // Mock client data
  const clients = [
    { id: 'maria', name: 'Maria Rodriguez', status: 'active', urgency: 'high', lastContact: '2 hours ago', upcomingAppt: 'Today 2pm' },
    { id: 'robert', name: 'Robert Johnson', status: 'active', urgency: 'high', lastContact: '5 hours ago', upcomingAppt: 'Tomorrow 10am' },
    { id: 'sarah', name: 'Sarah Williams', status: 'pending', urgency: 'medium', lastContact: '1 day ago', upcomingAppt: 'None' },
    { id: 'james', name: 'James Davis', status: 'active', urgency: 'low', lastContact: '3 days ago', upcomingAppt: 'Next week' },
    { id: 'jennifer', name: 'Jennifer Garcia', status: 'inactive', urgency: 'low', lastContact: '1 week ago', upcomingAppt: 'None' },
  ]

  const filteredClients = filterStatus === 'all' 
    ? clients 
    : clients.filter(c => c.status === filterStatus)

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Top Navigation Bar */}
      <nav className="bg-white border-b border-neutral-200 shadow-sm sticky top-0 z-50">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-4">
              <div className="w-11 h-11 bg-gradient-to-br from-primary-600 to-primary-700 rounded-lg flex items-center justify-center shadow-md">
                <span className="text-white font-bold text-xl">FC</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-neutral-900">First Contact E.I.S.</h1>
                <p className="text-sm text-neutral-500">Caseworker Dashboard</p>
              </div>
            </div>

            {/* User Info */}
            <div className="flex items-center gap-4">
              <button className="relative p-2 text-neutral-600 hover:text-neutral-900 hover:bg-neutral-100 rounded-lg transition-colors">
                <Bell className="w-6 h-6" />
                <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-error-500 rounded-full ring-2 ring-white"></span>
              </button>
              <div className="flex items-center gap-3 pl-4 border-l border-neutral-200">
                <div className="text-right">
                  <div className="text-sm font-semibold text-neutral-900">Sarah Johnson</div>
                  <div className="text-xs text-neutral-500">Senior Caseworker</div>
                </div>
                <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center text-white font-semibold text-sm shadow-md">
                  SJ
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* 3-PANEL LAYOUT: Gmail Style */}
      <div className="flex h-[calc(100vh-89px)]">
        
        {/* LEFT PANEL: Filters & Client List */}
        <div className="w-80 bg-white border-r border-neutral-200 flex flex-col overflow-hidden">
          {/* Search Bar */}
          <div className="p-4 border-b border-neutral-200">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-400" />
              <input
                type="text"
                placeholder="Search clients..."
                className="w-full pl-10 pr-4 py-2 border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Filter Tabs */}
          <div className="flex gap-2 p-4 border-b border-neutral-200 bg-neutral-50">
            {[
              { value: 'all', label: 'All', count: clients.length },
              { value: 'active', label: 'Active', count: clients.filter(c => c.status === 'active').length },
              { value: 'pending', label: 'Pending', count: clients.filter(c => c.status === 'pending').length },
            ].map(filter => (
              <button
                key={filter.value}
                onClick={() => setFilterStatus(filter.value)}
                className={`flex-1 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  filterStatus === filter.value
                    ? 'bg-primary-600 text-white shadow-sm'
                    : 'bg-white text-neutral-700 hover:bg-neutral-100 border border-neutral-200'
                }`}
              >
                {filter.label} ({filter.count})
              </button>
            ))}
          </div>

          {/* Client List */}
          <div className="flex-1 overflow-y-auto">
            {filteredClients.map(client => (
              <button
                key={client.id}
                onClick={() => setSelectedClient(client.id)}
                className={`w-full p-4 border-b border-neutral-200 text-left hover:bg-neutral-50 transition-colors ${
                  selectedClient === client.id ? 'bg-primary-50 border-l-4 border-l-primary-600' : ''
                }`}
              >
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <div className="font-semibold text-neutral-900">{client.name}</div>
                    <div className="text-xs text-neutral-500 mt-0.5">ID: {client.id}</div>
                  </div>
                  {client.urgency === 'high' && (
                    <span className="px-2 py-0.5 text-xs font-semibold bg-error-100 text-error-700 rounded">
                      High
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-4 text-xs text-neutral-500">
                  <div className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {client.lastContact}
                  </div>
                  {client.upcomingAppt !== 'None' && (
                    <div className="flex items-center gap-1 text-primary-600">
                      <CheckCircle2 className="w-3 h-3" />
                      {client.upcomingAppt}
                    </div>
                  )}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* MIDDLE PANEL: Event Feed */}
        <div className="flex-1 bg-neutral-50 overflow-y-auto">
          <div className="p-6">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-neutral-900 mb-2">AI Recommendations</h2>
              <p className="text-neutral-600">Real-time coordination opportunities</p>
            </div>
            <RecommendationsFeed />
          </div>
        </div>

        {/* RIGHT PANEL: Details */}
        <div className="w-96 bg-white border-l border-neutral-200 overflow-y-auto">
          {selectedClient ? (
            <div className="p-6">
              <h3 className="text-lg font-bold text-neutral-900 mb-4">Client Details</h3>
              {/* Client details would go here */}
              <div className="space-y-4">
                <div className="p-4 bg-neutral-50 rounded-lg">
                  <div className="text-sm text-neutral-500 mb-1">Selected Client</div>
                  <div className="font-semibold text-neutral-900">
                    {clients.find(c => c.id === selectedClient)?.name}
                  </div>
                </div>
                <div className="text-sm text-neutral-600">
                  Full client profile, care plan, and history would display here in production.
                </div>
              </div>
            </div>
          ) : (
            <div className="h-full flex items-center justify-center p-6 text-center">
              <div>
                <Users className="w-16 h-16 text-neutral-300 mx-auto mb-4" />
                <h3 className="font-semibold text-neutral-900 mb-2">No Client Selected</h3>
                <p className="text-sm text-neutral-500">Select a client from the list to view details</p>
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  )
}

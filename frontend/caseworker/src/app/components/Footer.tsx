'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Heart, Shield, Clock } from 'lucide-react';

interface FooterProps {
  language: string;
  t: (key: string) => string;
}

export function Footer({ language, t }: FooterProps) {
  return (
    <footer className="bg-neutral-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">FC</span>
                </div>
                <div>
                  <h3 className="text-xl font-bold">First Contact EIS</h3>
                  <p className="text-neutral-400 text-sm">AI-Powered Case Management</p>
                </div>
              </div>
              <p className="text-neutral-300 mb-6 max-w-md">
                Transforming civic services through AI-powered client engagement, 
                intelligent case management, and compliance automation for vulnerable populations.
              </p>
              <div className="flex items-center space-x-2 text-sm text-neutral-400">
                <Shield className="w-4 h-4" />
                <span>HIPAA Compliant • HUD/HMIS Certified</span>
              </div>
            </motion.div>
          </div>

          {/* Quick Links */}
          <div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
              <ul className="space-y-2">
                <li>
                  <a href="#" className="text-neutral-300 hover:text-white transition-colors">
                    Case Management
                  </a>
                </li>
                <li>
                  <a href="#" className="text-neutral-300 hover:text-white transition-colors">
                    AI Assistant
                  </a>
                </li>
                <li>
                  <a href="#" className="text-neutral-300 hover:text-white transition-colors">
                    Compliance Reports
                  </a>
                </li>
                <li>
                  <a href="#" className="text-neutral-300 hover:text-white transition-colors">
                    Performance Metrics
                  </a>
                </li>
              </ul>
            </motion.div>
          </div>

          {/* Support */}
          <div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              <h4 className="text-lg font-semibold mb-4">Support</h4>
              <ul className="space-y-2">
                <li>
                  <a href="#" className="text-neutral-300 hover:text-white transition-colors">
                    Documentation
                  </a>
                </li>
                <li>
                  <a href="#" className="text-neutral-300 hover:text-white transition-colors">
                    Training Materials
                  </a>
                </li>
                <li>
                  <a href="#" className="text-neutral-300 hover:text-white transition-colors">
                    Contact Support
                  </a>
                </li>
                <li>
                  <a href="#" className="text-neutral-300 hover:text-white transition-colors">
                    System Status
                  </a>
                </li>
              </ul>
            </motion.div>
          </div>
        </div>

        {/* Bottom */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="border-t border-neutral-800 mt-8 pt-8"
        >
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-4 text-sm text-neutral-400 mb-4 md:mb-0">
              <span>© 2024 First Contact EIS</span>
              <span>•</span>
              <span>Long Beach Pilot Program</span>
              <span>•</span>
              <span>Version 1.0.0</span>
            </div>
            
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-2 text-sm text-neutral-400">
                <Clock className="w-4 h-4" />
                <span>24/7 Crisis Support</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-neutral-400">
                <Heart className="w-4 h-4 text-error-500" />
                <span>Made with care for our community</span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </footer>
  );
}

'use client';

import React from 'react';
import { Phone, Mail, MapPin, Globe, Shield, Heart } from 'lucide-react';

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
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">FC</span>
              </div>
              <div>
                <h3 className="text-xl font-bold">First Contact EIS</h3>
                <p className="text-sm text-neutral-400">Client Portal</p>
              </div>
            </div>
            <p className="text-neutral-300 mb-4 max-w-md">
              Your gateway to comprehensive social services in Long Beach. 
              We're here to help you access housing, employment, healthcare, 
              and other essential services.
            </p>
            <div className="flex items-center space-x-2 text-sm text-neutral-400">
              <Shield className="w-4 h-4" />
              <span>HIPAA Compliant • Secure • Confidential</span>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-neutral-300 hover:text-white transition-colors duration-200">
                  AI Chat Assistant
                </a>
              </li>
              <li>
                <a href="#" className="text-neutral-300 hover:text-white transition-colors duration-200">
                  My Cases
                </a>
              </li>
              <li>
                <a href="#" className="text-neutral-300 hover:text-white transition-colors duration-200">
                  Service Requests
                </a>
              </li>
              <li>
                <a href="#" className="text-neutral-300 hover:text-white transition-colors duration-200">
                  Resource Directory
                </a>
              </li>
              <li>
                <a href="#" className="text-neutral-300 hover:text-white transition-colors duration-200">
                  Profile Settings
                </a>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Contact Us</h4>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <Phone className="w-4 h-4 text-primary-400" />
                <span className="text-neutral-300">(562) 570-3800</span>
              </div>
              <div className="flex items-center space-x-3">
                <Mail className="w-4 h-4 text-primary-400" />
                <span className="text-neutral-300">help@firstcontact-eis.org</span>
              </div>
              <div className="flex items-start space-x-3">
                <MapPin className="w-4 h-4 text-primary-400 mt-1" />
                <span className="text-neutral-300">
                  333 W Ocean Blvd<br />
                  Long Beach, CA 90802
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Crisis Support */}
        <div className="mt-8 pt-8 border-t border-neutral-800">
          <div className="bg-red-900/20 border border-red-800 rounded-lg p-4">
            <div className="flex items-center space-x-3">
              <Heart className="w-5 h-5 text-red-400" />
              <div>
                <h5 className="font-semibold text-red-200">Crisis Support Available 24/7</h5>
                <p className="text-sm text-red-300">
                  If you're experiencing a crisis, call 988 for immediate help.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-8 pt-8 border-t border-neutral-800">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="flex items-center space-x-4 text-sm text-neutral-400">
              <span>© 2024 City of Long Beach</span>
              <span>•</span>
              <a href="#" className="hover:text-white transition-colors duration-200">
                Privacy Policy
              </a>
              <span>•</span>
              <a href="#" className="hover:text-white transition-colors duration-200">
                Terms of Service
              </a>
            </div>
            <div className="flex items-center space-x-2 text-sm text-neutral-400">
              <Globe className="w-4 h-4" />
              <span>Available in English, Spanish, Khmer, Tagalog, and Korean</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

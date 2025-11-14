"use client";

import { useState, useEffect } from 'react';
import axios from 'axios';

interface QRCode {
  qr_code_base64: string;
  qr_url: string;
  location_id: string;
  location_name?: string;
  address?: string;
  vendor_id?: string;
  area_code?: string;
}

export default function QRGeneratorPage() {
  const [qrCodes, setQrCodes] = useState<QRCode[]>([]);
  const [loading, setLoading] = useState(false);
  const [customQR, setCustomQR] = useState({
    location_id: '',
    vendor_id: '',
    area_code: ''
  });

  const generateBatchQRCodes = async () => {
    setLoading(true);
    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/intakes/qr/batch`,
        {
          vendor_id: 'demo_vendor',
          organization_id: 'lb',
          use_demo_locations: true
        }
      );

      setQrCodes(response.data.qr_codes);
    } catch (error) {
      console.error('Error generating QR codes:', error);
      alert('Error generating QR codes');
    } finally {
      setLoading(false);
    }
  };

  const generateCustomQR = async () => {
    if (!customQR.location_id) {
      alert('Please enter a location ID');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/intakes/qr/generate`,
        customQR
      );

      setQrCodes([response.data]);
    } catch (error) {
      console.error('Error generating QR code:', error);
      alert('Error generating QR code');
    } finally {
      setLoading(false);
    }
  };

  const printQRCode = (qr: QRCode) => {
    const printWindow = window.open('', '_blank');
    if (!printWindow) return;

    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
        <head>
          <title>QR Code - ${qr.location_name || qr.location_id}</title>
          <style>
            body {
              font-family: Arial, sans-serif;
              display: flex;
              justify-content: center;
              align-items: center;
              min-height: 100vh;
              margin: 0;
              background: white;
            }
            .qr-container {
              text-align: center;
              padding: 40px;
              border: 3px solid #2563eb;
              border-radius: 20px;
              max-width: 600px;
            }
            h1 {
              color: #1e40af;
              margin-bottom: 10px;
              font-size: 32px;
            }
            .subtitle {
              color: #64748b;
              font-size: 18px;
              margin-bottom: 30px;
            }
            img {
              max-width: 400px;
              height: auto;
              margin: 20px 0;
            }
            .location {
              font-size: 24px;
              font-weight: bold;
              color: #1e293b;
              margin: 20px 0;
            }
            .address {
              color: #64748b;
              font-size: 16px;
              margin-bottom: 20px;
            }
            .instructions {
              background: #f1f5f9;
              padding: 20px;
              border-radius: 10px;
              margin-top: 30px;
              text-align: left;
            }
            .instructions h2 {
              color: #1e40af;
              font-size: 20px;
              margin-bottom: 15px;
            }
            .instructions ol {
              margin: 0;
              padding-left: 25px;
            }
            .instructions li {
              margin: 10px 0;
              color: #334155;
              font-size: 16px;
            }
            @media print {
              body {
                margin: 0;
              }
              .qr-container {
                border: 3px solid #2563eb;
                page-break-after: always;
              }
            }
          </style>
        </head>
        <body>
          <div class="qr-container">
            <h1>🏠 First Contact E.I.S.</h1>
            <p class="subtitle">City of Long Beach - Early Intervention System</p>

            <div class="location">${qr.location_name || qr.location_id.replace(/_/g, ' ').toUpperCase()}</div>
            ${qr.address ? `<div class="address">${qr.address}</div>` : ''}

            <img src="${qr.qr_code_base64}" alt="QR Code" />

            <div class="instructions">
              <h2>📱 Need Help?</h2>
              <ol>
                <li>Scan this QR code with your phone camera</li>
                <li>Complete the short assessment form</li>
                <li>Get connected with a caseworker who can help</li>
              </ol>
              <p style="margin-top: 20px; color: #64748b; font-size: 14px;">
                Free | Confidential | Available 24/7 | Multilingual Support
              </p>
            </div>
          </div>
        </body>
      </html>
    `);

    printWindow.document.close();
    setTimeout(() => {
      printWindow.print();
    }, 250);
  };

  const printAllQRCodes = () => {
    const printWindow = window.open('', '_blank');
    if (!printWindow) return;

    const qrHTML = qrCodes.map(qr => `
      <div class="qr-container">
        <h1>🏠 First Contact E.I.S.</h1>
        <p class="subtitle">City of Long Beach - Early Intervention System</p>

        <div class="location">${qr.location_name || qr.location_id.replace(/_/g, ' ').toUpperCase()}</div>
        ${qr.address ? `<div class="address">${qr.address}</div>` : ''}

        <img src="${qr.qr_code_base64}" alt="QR Code" />

        <div class="instructions">
          <h2>📱 Need Help?</h2>
          <ol>
            <li>Scan this QR code with your phone camera</li>
            <li>Complete the short assessment form</li>
            <li>Get connected with a caseworker who can help</li>
          </ol>
          <p style="margin-top: 20px; color: #64748b; font-size: 14px;">
            Free | Confidential | Available 24/7 | Multilingual Support
          </p>
        </div>
      </div>
    `).join('');

    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
        <head>
          <title>First Contact EIS - QR Codes</title>
          <style>
            body {
              font-family: Arial, sans-serif;
              margin: 0;
              background: white;
            }
            .qr-container {
              text-align: center;
              padding: 40px;
              border: 3px solid #2563eb;
              border-radius: 20px;
              max-width: 600px;
              margin: 40px auto;
              page-break-after: always;
            }
            h1 {
              color: #1e40af;
              margin-bottom: 10px;
              font-size: 32px;
            }
            .subtitle {
              color: #64748b;
              font-size: 18px;
              margin-bottom: 30px;
            }
            img {
              max-width: 400px;
              height: auto;
              margin: 20px 0;
            }
            .location {
              font-size: 24px;
              font-weight: bold;
              color: #1e293b;
              margin: 20px 0;
            }
            .address {
              color: #64748b;
              font-size: 16px;
              margin-bottom: 20px;
            }
            .instructions {
              background: #f1f5f9;
              padding: 20px;
              border-radius: 10px;
              margin-top: 30px;
              text-align: left;
            }
            .instructions h2 {
              color: #1e40af;
              font-size: 20px;
              margin-bottom: 15px;
            }
            .instructions ol {
              margin: 0;
              padding-left: 25px;
            }
            .instructions li {
              margin: 10px 0;
              color: #334155;
              font-size: 16px;
            }
            @media print {
              .qr-container {
                border: 3px solid #2563eb;
              }
            }
          </style>
        </head>
        <body>
          ${qrHTML}
        </body>
      </html>
    `);

    printWindow.document.close();
    setTimeout(() => {
      printWindow.print();
    }, 250);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">QR Code Generator</h1>
          <p className="text-gray-600">Generate QR codes for client intake at various locations</p>
        </div>

        {/* Generation Options */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Batch Generation */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Batch Generation</h2>
            <p className="text-gray-600 mb-6">
              Generate QR codes for all 5 demo locations in Long Beach
            </p>
            <button
              onClick={generateBatchQRCodes}
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 rounded-lg transition-colors disabled:bg-gray-400"
            >
              {loading ? 'Generating...' : 'Generate Demo QR Codes'}
            </button>
          </div>

          {/* Custom Generation */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Custom Generation</h2>
            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Location ID *
                </label>
                <input
                  type="text"
                  value={customQR.location_id}
                  onChange={(e) => setCustomQR({...customQR, location_id: e.target.value})}
                  placeholder="downtown_library"
                  className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Vendor ID (optional)
                </label>
                <input
                  type="text"
                  value={customQR.vendor_id}
                  onChange={(e) => setCustomQR({...customQR, vendor_id: e.target.value})}
                  placeholder="coastal_homeless_services"
                  className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Area Code (optional)
                </label>
                <input
                  type="text"
                  value={customQR.area_code}
                  onChange={(e) => setCustomQR({...customQR, area_code: e.target.value})}
                  placeholder="90802"
                  className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none"
                />
              </div>
            </div>
            <button
              onClick={generateCustomQR}
              disabled={loading}
              className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-4 rounded-lg transition-colors disabled:bg-gray-400"
            >
              {loading ? 'Generating...' : 'Generate Custom QR Code'}
            </button>
          </div>
        </div>

        {/* Generated QR Codes */}
        {qrCodes.length > 0 && (
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                Generated QR Codes ({qrCodes.length})
              </h2>
              <button
                onClick={printAllQRCodes}
                className="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
              >
                🖨️ Print All
              </button>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {qrCodes.map((qr, idx) => (
                <div key={idx} className="border-2 border-gray-200 rounded-lg p-4 hover:border-blue-500 transition-colors">
                  <img
                    src={qr.qr_code_base64}
                    alt={`QR Code for ${qr.location_name || qr.location_id}`}
                    className="w-full h-auto mb-4"
                  />
                  <h3 className="font-bold text-lg text-gray-900 mb-1">
                    {qr.location_name || qr.location_id.replace(/_/g, ' ').toUpperCase()}
                  </h3>
                  {qr.address && (
                    <p className="text-sm text-gray-600 mb-2">{qr.address}</p>
                  )}
                  {qr.area_code && (
                    <p className="text-xs text-gray-500 mb-3">ZIP: {qr.area_code}</p>
                  )}
                  <div className="space-y-2">
                    <button
                      onClick={() => printQRCode(qr)}
                      className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition-colors"
                    >
                      🖨️ Print
                    </button>
                    <a
                      href={qr.qr_code_base64}
                      download={`qr-${qr.location_id}.png`}
                      className="block w-full bg-gray-600 hover:bg-gray-700 text-white font-semibold py-2 rounded-lg transition-colors text-center"
                    >
                      💾 Download
                    </a>
                  </div>
                  <div className="mt-3 p-2 bg-gray-50 rounded text-xs font-mono break-all text-gray-600">
                    {qr.qr_url}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

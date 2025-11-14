"""
QR Code Generation Service for First Contact EIS
Generates QR codes with metadata for location/vendor tracking
"""

import qrcode
import io
import base64
from typing import Optional, Dict
from datetime import datetime
import json
import hashlib


class QRCodeService:
    """Service for generating QR codes with embedded metadata"""

    def __init__(self, base_url: str = "https://firstcontact-eis.app"):
        self.base_url = base_url

    def generate_intake_qr(
        self,
        location_id: Optional[str] = None,
        vendor_id: Optional[str] = None,
        area_code: Optional[str] = None,
        organization_id: Optional[str] = None,
        custom_metadata: Optional[Dict] = None
    ) -> Dict[str, str]:
        """
        Generate a QR code for intake with embedded metadata

        Args:
            location_id: Geographic location identifier (e.g., "downtown_lb", "pier_area")
            vendor_id: Vendor/organization ID awarded contract
            area_code: Area code for geographic tracking
            organization_id: Organization ID for multi-tenant tracking
            custom_metadata: Additional custom metadata

        Returns:
            Dict containing QR code image (base64), URL, and metadata hash
        """
        # Create metadata object
        metadata = {
            "timestamp": datetime.utcnow().isoformat(),
            "location_id": location_id,
            "vendor_id": vendor_id,
            "area_code": area_code,
            "organization_id": organization_id or "lb",  # Default to Long Beach
        }

        if custom_metadata:
            metadata.update(custom_metadata)

        # Create metadata hash for verification
        metadata_str = json.dumps(metadata, sort_keys=True)
        metadata_hash = hashlib.sha256(metadata_str.encode()).hexdigest()[:16]

        # Build URL with encoded parameters
        params = []
        if location_id:
            params.append(f"loc={location_id}")
        if vendor_id:
            params.append(f"vendor={vendor_id}")
        if area_code:
            params.append(f"area={area_code}")
        if organization_id:
            params.append(f"org={organization_id}")
        params.append(f"qr={metadata_hash}")

        qr_url = f"{self.base_url}/intake?{'&'.join(params)}"

        # Generate QR code image
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_url)
        qr.make(fit=True)

        # Create image
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert to base64
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.read()).decode()

        return {
            "qr_code_base64": f"data:image/png;base64,{img_base64}",
            "qr_url": qr_url,
            "metadata": metadata,
            "metadata_hash": metadata_hash,
            "location_id": location_id,
            "vendor_id": vendor_id,
            "area_code": area_code,
        }

    def generate_batch_qr_codes(
        self,
        locations: list,
        vendor_id: Optional[str] = None,
        organization_id: Optional[str] = None
    ) -> list:
        """
        Generate multiple QR codes for different locations

        Args:
            locations: List of location dictionaries with id, name, area_code
            vendor_id: Vendor ID for all QR codes
            organization_id: Organization ID for all QR codes

        Returns:
            List of QR code data dictionaries
        """
        qr_codes = []

        for location in locations:
            qr_data = self.generate_intake_qr(
                location_id=location.get("id"),
                vendor_id=vendor_id,
                area_code=location.get("area_code"),
                organization_id=organization_id,
                custom_metadata={
                    "location_name": location.get("name"),
                    "address": location.get("address"),
                }
            )
            qr_data["location_name"] = location.get("name")
            qr_data["address"] = location.get("address")
            qr_codes.append(qr_data)

        return qr_codes


# Demo locations for Long Beach
DEMO_LOCATIONS = [
    {
        "id": "mlk_park",
        "name": "Martin Luther King Jr. Park",
        "area_code": "90805",
        "address": "1950 Lemon Ave, Long Beach, CA 90806"
    },
    {
        "id": "downtown_library",
        "name": "Long Beach Main Library",
        "area_code": "90802",
        "address": "101 Pacific Ave, Long Beach, CA 90802"
    },
    {
        "id": "homeless_shelter",
        "name": "Multi-Service Center",
        "area_code": "90813",
        "address": "1301 W 12th St, Long Beach, CA 90813"
    },
    {
        "id": "health_center",
        "name": "Long Beach Health Center",
        "area_code": "90806",
        "address": "2840 Long Beach Blvd, Long Beach, CA 90806"
    },
    {
        "id": "community_center",
        "name": "Houghton Park Community Center",
        "area_code": "90815",
        "address": "6301 Myrtle Ave, Long Beach, CA 90815"
    }
]

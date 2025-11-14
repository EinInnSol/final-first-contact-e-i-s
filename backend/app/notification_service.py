"""
Notification Service for First Contact EIS
Handles SMS, email, and push notifications for caseworkers and clients
"""

import os
import logging
from typing import Optional
from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for sending notifications via SMS, email, and push"""

    def __init__(self):
        self.demo_mode = os.getenv("DEMO_MODE", "true").lower() == "true"

        # Twilio configuration
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

        if not self.demo_mode and (not self.twilio_account_sid or not self.twilio_auth_token):
            logger.warning("Twilio credentials not configured. Running in demo mode for notifications.")
            self.demo_mode = True

        if not self.demo_mode:
            self.twilio_client = TwilioClient(
                self.twilio_account_sid,
                self.twilio_auth_token
            )
        else:
            self.twilio_client = None
            logger.info("Notification service running in DEMO MODE - will log instead of sending")

    async def send_caseworker_notification(
        self,
        caseworker_phone: str,
        client_name: str,
        case_number: str,
        appointment_time: str
    ) -> bool:
        """
        Send SMS notification to caseworker about new client assignment

        Args:
            caseworker_phone: Caseworker's phone number (format: 5626811431)
            client_name: Name of the new client
            case_number: Case number
            appointment_time: Suggested appointment time

        Returns:
            True if successful, False otherwise
        """
        # Format phone number
        if not caseworker_phone.startswith("+"):
            caseworker_phone = f"+1{caseworker_phone}"

        message = (
            f"🔔 First Contact EIS Alert\n\n"
            f"New client assigned: {client_name}\n"
            f"Case #: {case_number}\n"
            f"Suggested contact: {appointment_time}\n\n"
            f"Log in to your dashboard to review AI-suggested action plan and approve."
        )

        return await self._send_sms(caseworker_phone, message)

    async def send_compliance_notification(
        self,
        caseworker_phone: str,
        case_number: str,
        client_name: str
    ) -> bool:
        """
        Send SMS notification about compliance report ready for upload

        Args:
            caseworker_phone: Caseworker's phone number
            case_number: Case number
            client_name: Client name

        Returns:
            True if successful, False otherwise
        """
        # Format phone number
        if not caseworker_phone.startswith("+"):
            caseworker_phone = f"+1{caseworker_phone}"

        message = (
            f"📋 Compliance Report Ready\n\n"
            f"Case #: {case_number}\n"
            f"Client: {client_name}\n\n"
            f"HUD/HMIS compliance report is ready for review and upload. "
            f"Approve in your dashboard to proceed."
        )

        return await self._send_sms(caseworker_phone, message)

    async def send_client_confirmation(
        self,
        client_phone: str,
        caseworker_name: str,
        caseworker_phone: str,
        appointment_time: str
    ) -> bool:
        """
        Send SMS confirmation to client about caseworker assignment

        Args:
            client_phone: Client's phone number
            caseworker_name: Name of assigned caseworker
            caseworker_phone: Caseworker's phone number
            appointment_time: When caseworker will call

        Returns:
            True if successful, False otherwise
        """
        # Format phone number
        if not client_phone.startswith("+"):
            client_phone = f"+1{client_phone}"

        message = (
            f"✅ First Contact EIS Confirmation\n\n"
            f"Thank you for completing your intake assessment.\n\n"
            f"Your caseworker: {caseworker_name}\n"
            f"Phone: {caseworker_phone}\n"
            f"Expect a call at: {appointment_time}\n\n"
            f"We're here to help you every step of the way."
        )

        return await self._send_sms(client_phone, message)

    async def _send_sms(self, to_phone: str, message: str) -> bool:
        """
        Internal method to send SMS via Twilio

        Args:
            to_phone: Recipient phone number (E.164 format)
            message: Message content

        Returns:
            True if successful, False otherwise
        """
        if self.demo_mode:
            logger.info(f"[DEMO MODE] SMS to {to_phone}:")
            logger.info(f"Message: {message}")
            logger.info("=" * 60)
            return True

        try:
            message_obj = self.twilio_client.messages.create(
                body=message,
                from_=self.twilio_phone_number,
                to=to_phone
            )

            logger.info(f"SMS sent successfully. SID: {message_obj.sid}")
            return True

        except TwilioRestException as e:
            logger.error(f"Twilio error sending SMS to {to_phone}: {e}")
            return False

        except Exception as e:
            logger.error(f"Unexpected error sending SMS to {to_phone}: {e}")
            return False

    async def send_crisis_alert(
        self,
        caseworker_phone: str,
        client_name: str,
        crisis_indicators: list
    ) -> bool:
        """
        Send urgent crisis alert to caseworker

        Args:
            caseworker_phone: Caseworker's phone number
            client_name: Client name
            crisis_indicators: List of crisis indicators detected

        Returns:
            True if successful, False otherwise
        """
        # Format phone number
        if not caseworker_phone.startswith("+"):
            caseworker_phone = f"+1{caseworker_phone}"

        indicators_str = ", ".join(crisis_indicators)

        message = (
            f"🚨 CRISIS ALERT - First Contact EIS\n\n"
            f"Client: {client_name}\n"
            f"Crisis indicators: {indicators_str}\n\n"
            f"IMMEDIATE ACTION REQUIRED\n"
            f"Review case in dashboard NOW."
        )

        return await self._send_sms(caseworker_phone, message)

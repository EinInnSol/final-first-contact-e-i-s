"""
First Contact E.I.S. - Event Listener Service
THE SENSORS - Monitors all systems for events that trigger orchestration

Author: Claude (CTO, EINHARJER INNOVATIVE SOLUTIONS LLC)
Date: November 6, 2025
"""

from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
import asyncio
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class EventSource(Enum):
    """Source of the event"""
    FIRESTORE = "firestore"
    WEBHOOK = "webhook"
    DATABASE = "database"
    SCHEDULED = "scheduled"
    MANUAL = "manual"


@dataclass
class EventConfig:
    """Configuration for event monitoring"""
    event_type: str
    source: EventSource
    collection: Optional[str] = None
    webhook_path: Optional[str] = None
    schedule_cron: Optional[str] = None
    enabled: bool = True


class EventListenerService:
    """THE SENSORS - Monitors all systems for orchestration triggers"""
    
    def __init__(
        self,
        orchestrator,
        firestore_client=None,
        demo_mode: bool = True
    ):
        self.orchestrator = orchestrator
        self.firestore = firestore_client
        self.demo_mode = demo_mode
        
        self.events_detected = 0
        self.events_processed = 0
        self.events_ignored = 0
        self.listeners = []
        self.webhook_handlers = {}
        
        self.event_configs = self._initialize_event_configs()
        
        logger.info(f"Event Listener Service initialized (demo_mode={demo_mode})")
    
    def _initialize_event_configs(self) -> List[EventConfig]:
        """Initialize event monitoring configurations"""
        return [
            EventConfig(
                event_type="appointment_cancelled",
                source=EventSource.FIRESTORE,
                collection="appointments",
                enabled=True
            ),
            EventConfig(
                event_type="appointment_no_show",
                source=EventSource.FIRESTORE,
                collection="appointments",
                enabled=True
            ),
            EventConfig(
                event_type="housing_available",
                source=EventSource.WEBHOOK,
                webhook_path="/webhooks/housing-update",
                enabled=True
            ),
            EventConfig(
                event_type="documents_complete",
                source=EventSource.FIRESTORE,
                collection="clients",
                enabled=True
            ),
            EventConfig(
                event_type="deadline_approaching",
                source=EventSource.SCHEDULED,
                schedule_cron="0 9 * * *",
                enabled=True
            ),
        ]
    
    async def start(self):
        """Start all event listeners"""
        logger.info("Starting event listeners...")
        
        for config in self.event_configs:
            if not config.enabled:
                continue
            
            try:
                if config.source == EventSource.FIRESTORE:
                    await self._start_firestore_listener(config)
                elif config.source == EventSource.WEBHOOK:
                    self._register_webhook_handler(config)
                elif config.source == EventSource.SCHEDULED:
                    await self._start_scheduled_job(config)
                
                logger.info(f"Started listener: {config.event_type}")
            except Exception as e:
                logger.error(f"Failed to start listener {config.event_type}: {e}")
        
        logger.info(f"Event listeners started ({len(self.listeners)} active)")
    
    async def stop(self):
        """Stop all event listeners"""
        for listener in self.listeners:
            listener.unsubscribe()
        self.listeners.clear()
    
    async def _start_firestore_listener(self, config: EventConfig):
        """Start Firestore real-time listener"""
        if not self.firestore or self.demo_mode:
            logger.info(f"[DEMO] Would start Firestore listener for {config.collection}")
            return
        
        # TODO: Implement real Firestore listener
        pass
    
    def _register_webhook_handler(self, config: EventConfig):
        """Register webhook handler"""
        self.webhook_handlers[config.webhook_path] = config.event_type
        logger.info(f"Webhook handler registered: {config.webhook_path}")
    
    async def _start_scheduled_job(self, config: EventConfig):
        """Start scheduled job"""
        if self.demo_mode:
            logger.info(f"[DEMO] Would start scheduled job: {config.event_type}")
            return
        
        asyncio.create_task(self._run_scheduled_job(config))
    
    async def _run_scheduled_job(self, config: EventConfig):
        """Run scheduled job in loop"""
        while True:
            try:
                await asyncio.sleep(86400)  # 24 hours
                await self._execute_scheduled_check(config.event_type)
            except Exception as e:
                logger.error(f"Error in scheduled job {config.event_type}: {e}")
                await asyncio.sleep(3600)
    
    async def _execute_scheduled_check(self, event_type: str):
        """Execute a scheduled check"""
        if event_type == "deadline_approaching":
            await self._check_approaching_deadlines()
    
    async def _check_approaching_deadlines(self):
        """Check for approaching deadlines"""
        logger.info("Checking for approaching deadlines...")
        # TODO: Query database for deadlines
    
    async def handle_webhook(self, webhook_path: str, payload: Dict[str, Any]):
        """Handle incoming webhook from external system"""
        self.events_detected += 1
        
        event_type = self.webhook_handlers.get(webhook_path)
        if not event_type:
            logger.warning(f"Unknown webhook path: {webhook_path}")
            self.events_ignored += 1
            return
        
        try:
            from .orchestrator import Event
            
            event = Event(
                event_id=payload.get("id", f"webhook_{datetime.now().timestamp()}"),
                event_type=event_type,
                timestamp=datetime.now(),
                client_id=payload.get("client_id"),
                provider_id=payload.get("provider_id"),
                metadata=payload
            )
            
            await self._trigger_orchestration(event)
            
        except Exception as e:
            logger.error(f"Error handling webhook: {e}", exc_info=True)
    
    async def _trigger_orchestration(self, event):
        """Trigger orchestration engine with event"""
        try:
            logger.info(f"Triggering orchestration: {event.event_type}")
            
            recommendation = await self.orchestrator.handle_event(event)
            
            if recommendation:
                await self._store_recommendation(recommendation)
                self.events_processed += 1
            else:
                self.events_ignored += 1
            
        except Exception as e:
            logger.error(f"Error triggering orchestration: {e}", exc_info=True)
    
    async def _store_recommendation(self, recommendation):
        """Store recommendation in Firestore"""
        if not self.firestore or self.demo_mode:
            logger.info(f"[DEMO] Would store recommendation: {recommendation.recommendation_id}")
            return
        
        # TODO: Store in Firestore
    
    async def trigger_manual_event(
        self,
        event_type: str,
        client_id: Optional[str] = None,
        provider_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Manually trigger an event (for testing/demo)"""
        from .orchestrator import Event
        
        event = Event(
            event_id=f"manual_{datetime.now().timestamp()}",
            event_type=event_type,
            timestamp=datetime.now(),
            client_id=client_id,
            provider_id=provider_id,
            metadata=metadata or {}
        )
        
        await self._trigger_orchestration(event)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get event listener statistics"""
        return {
            "events_detected": self.events_detected,
            "events_processed": self.events_processed,
            "events_ignored": self.events_ignored,
            "active_listeners": len(self.listeners),
            "webhook_handlers": len(self.webhook_handlers),
            "processing_rate": (
                self.events_processed / max(self.events_detected, 1)
            ) * 100 if self.events_detected > 0 else 0
        }

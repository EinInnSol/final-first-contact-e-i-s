"""
First Contact E.I.S. - Execution Service
THE HANDS - Executes approved coordination plans across multiple systems

Author: Claude (CTO, EINHARJER INNOVATIVE SOLUTIONS LLC)
Date: November 6, 2025
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class ActionStatus(Enum):
    """Status of action execution"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class ActionResult:
    """Result of executing an action"""
    action_id: str
    status: ActionStatus
    started_at: datetime
    completed_at: Optional[datetime]
    result_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    retry_count: int = 0


@dataclass
class ExecutionResult:
    """Result of executing complete plan"""
    plan_id: str
    status: str
    actions_completed: int
    actions_failed: int
    total_duration_seconds: float
    action_results: List[ActionResult]
    rollback_performed: bool = False


class ExecutionService:
    """THE HANDS - Executes approved coordination plans"""
    
    def __init__(
        self, 
        db_session,
        notification_service,
        external_api_clients: Dict[str, Any],
        demo_mode: bool = True
    ):
        self.db = db_session
        self.notifications = notification_service
        self.api_clients = external_api_clients
        self.demo_mode = demo_mode
        
        self.executions_count = 0
        self.successful_executions = 0
        self.failed_executions = 0
        self.max_retries = 3
        self.retry_delay_seconds = 2
        
        logger.info(f"Execution Service initialized (demo_mode={demo_mode})")
    
    async def execute_plan(self, execution_plan, approved_by: str) -> ExecutionResult:
        """Execute an approved coordination plan"""
        logger.info(f"Executing plan: {execution_plan.plan_id}")
        start_time = datetime.now()
        
        action_results = []
        completed = 0
        failed = 0
        rollback_performed = False
        
        try:
            for action in execution_plan.actions:
                if not self._dependencies_met(action, action_results):
                    continue
                
                result = await self._execute_action(action)
                action_results.append(result)
                
                if result.status == ActionStatus.COMPLETED:
                    completed += 1
                elif result.status == ActionStatus.FAILED:
                    failed += 1
                    if self._is_critical_action(action):
                        rollback_performed = await self._rollback(action_results)
                        break
            
            if failed == 0:
                status = "success"
                self.successful_executions += 1
            elif completed > 0:
                status = "partial_success"
            else:
                status = "failed"
                self.failed_executions += 1
            
            self.executions_count += 1
            duration = (datetime.now() - start_time).total_seconds()
            
            await self._log_execution(execution_plan.plan_id, approved_by, status, action_results)
            
            return ExecutionResult(
                plan_id=execution_plan.plan_id,
                status=status,
                actions_completed=completed,
                actions_failed=failed,
                total_duration_seconds=duration,
                action_results=action_results,
                rollback_performed=rollback_performed
            )
        except Exception as e:
            logger.error(f"Error executing plan: {e}", exc_info=True)
            return ExecutionResult(
                plan_id=execution_plan.plan_id,
                status="failed",
                actions_completed=completed,
                actions_failed=failed + 1,
                total_duration_seconds=(datetime.now() - start_time).total_seconds(),
                action_results=action_results
            )
    
    async def _execute_action(self, action) -> ActionResult:
        """Execute a single action with retries"""
        action_id = f"{action.action_type}_{datetime.now().timestamp()}"
        started_at = datetime.now()
        
        for attempt in range(self.max_retries):
            try:
                if action.action_type == "cancel_appointment":
                    result_data = await self._cancel_appointment(action)
                elif action.action_type == "book_appointment":
                    result_data = await self._book_appointment(action)
                elif action.action_type == "update_transport":
                    result_data = await self._update_transport(action)
                elif action.action_type == "send_sms":
                    result_data = await self._send_sms(action)
                elif action.action_type == "notify_provider":
                    result_data = await self._notify_provider(action)
                elif action.action_type == "update_case":
                    result_data = await self._update_case(action)
                else:
                    raise ValueError(f"Unknown action type: {action.action_type}")
                
                return ActionResult(
                    action_id=action_id,
                    status=ActionStatus.COMPLETED,
                    started_at=started_at,
                    completed_at=datetime.now(),
                    result_data=result_data,
                    retry_count=attempt
                )
            except Exception as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay_seconds)
                else:
                    return ActionResult(
                        action_id=action_id,
                        status=ActionStatus.FAILED,
                        started_at=started_at,
                        completed_at=datetime.now(),
                        error_message=str(e),
                        retry_count=attempt + 1
                    )
    
    async def _cancel_appointment(self, action) -> Dict[str, Any]:
        params = action.parameters
        if self.demo_mode:
            logger.info(f"[DEMO] Cancelling appointment: {params}")
            await asyncio.sleep(0.5)
            return {"status": "cancelled", "confirmation": "DEMO-12345"}
        # TODO: Real implementation
        return {}
    
    async def _book_appointment(self, action) -> Dict[str, Any]:
        params = action.parameters
        if self.demo_mode:
            logger.info(f"[DEMO] Booking appointment: {params}")
            await asyncio.sleep(0.5)
            return {"status": "booked", "confirmation": "DEMO-67890"}
        # TODO: Real implementation
        return {}
    
    async def _update_transport(self, action) -> Dict[str, Any]:
        params = action.parameters
        if self.demo_mode:
            logger.info(f"[DEMO] Updating transport: {params}")
            await asyncio.sleep(0.3)
            return {"status": "updated", "route_id": "DEMO-ROUTE-001"}
        # TODO: Real implementation
        return {}
    
    async def _send_sms(self, action) -> Dict[str, Any]:
        params = action.parameters
        if self.demo_mode:
            logger.info(f"[DEMO] Sending SMS: {params['message']}")
            await asyncio.sleep(0.2)
            return {"status": "sent", "message_id": "DEMO-SMS-001"}
        # TODO: Real implementation
        return {}
    
    async def _notify_provider(self, action) -> Dict[str, Any]:
        params = action.parameters
        if self.demo_mode:
            logger.info(f"[DEMO] Notifying provider: {params['message']}")
            await asyncio.sleep(0.3)
            return {"status": "notified"}
        # TODO: Real implementation
        return {}
    
    async def _update_case(self, action) -> Dict[str, Any]:
        params = action.parameters
        if self.demo_mode:
            logger.info(f"[DEMO] Updating case: {params}")
            await asyncio.sleep(0.2)
            return {"status": "updated"}
        # TODO: Real database update
        return {}
    
    def _dependencies_met(self, action, completed_results: List[ActionResult]) -> bool:
        if not action.depends_on:
            return True
        completed_types = {
            result.action_id.split("_")[0] 
            for result in completed_results 
            if result.status == ActionStatus.COMPLETED
        }
        return all(dep in completed_types for dep in action.depends_on)
    
    def _is_critical_action(self, action) -> bool:
        critical_actions = ["book_appointment", "update_case", "cancel_appointment"]
        return action.action_type in critical_actions
    
    async def _rollback(self, action_results: List[ActionResult]) -> bool:
        logger.warning(f"Attempting rollback of {len(action_results)} actions")
        # TODO: Implement rollback logic
        return True
    
    async def _log_execution(self, plan_id: str, approved_by: str, status: str, action_results: List[ActionResult]):
        # TODO: Log to database for audit trail
        pass
    
    def get_statistics(self) -> Dict[str, Any]:
        return {
            "total_executions": self.executions_count,
            "successful": self.successful_executions,
            "failed": self.failed_executions,
            "success_rate": (self.successful_executions / max(self.executions_count, 1)) * 100
        }

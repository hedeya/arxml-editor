"""
Event Bus Implementation
Handles event publishing, subscription, and routing
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Callable, Type, Any, Optional
from collections import defaultdict
import threading
import logging
# DomainEvent will be imported when needed to avoid circular imports

logger = logging.getLogger(__name__)

class IEventBus(ABC):
    """Event bus interface"""
    
    @abstractmethod
    def subscribe(self, event_type: Type[Any], handler: Callable[[Any], None]) -> str:
        """Subscribe to an event type"""
        pass
    
    @abstractmethod
    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from events"""
        pass
    
    @abstractmethod
    def publish(self, event: Any) -> None:
        """Publish an event"""
        pass
    
    @abstractmethod
    def publish_async(self, event: Any) -> None:
        """Publish an event asynchronously"""
        pass
    
    @abstractmethod
    def get_subscribers(self, event_type: Type[Any]) -> List[Callable]:
        """Get all subscribers for an event type"""
        pass

class EventBus(IEventBus):
    """Synchronous event bus implementation"""
    
    def __init__(self):
        self._subscribers: Dict[Type[DomainEvent], List[Callable[[DomainEvent], None]]] = defaultdict(list)
        self._subscription_ids: Dict[str, Callable[[DomainEvent], None]] = {}
        self._lock = threading.RLock()
        self._next_subscription_id = 1
    
    def subscribe(self, event_type: Type[Any], handler: Callable[[Any], None]) -> str:
        """Subscribe to an event type"""
        with self._lock:
            subscription_id = f"sub_{self._next_subscription_id}"
            self._next_subscription_id += 1
            
            self._subscribers[event_type].append(handler)
            self._subscription_ids[subscription_id] = handler
            
            logger.debug(f"Subscribed {subscription_id} to {event_type.__name__}")
            return subscription_id
    
    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from events"""
        with self._lock:
            if subscription_id not in self._subscription_ids:
                return False
            
            handler = self._subscription_ids[subscription_id]
            
            # Remove from all event types
            for event_type, handlers in self._subscribers.items():
                if handler in handlers:
                    handlers.remove(handler)
            
            del self._subscription_ids[subscription_id]
            logger.debug(f"Unsubscribed {subscription_id}")
            return True
    
    def publish(self, event: Any) -> None:
        """Publish an event synchronously"""
        with self._lock:
            event_type = type(event)
            handlers = self._subscribers.get(event_type, [])
            
            logger.debug(f"Publishing {event_type.__name__} to {len(handlers)} subscribers")
            
            for handler in handlers:
                try:
                    handler(event)
                except Exception as e:
                    logger.error(f"Error in event handler for {event_type.__name__}: {e}")
    
    def publish_async(self, event: Any) -> None:
        """Publish an event asynchronously (same as sync for now)"""
        self.publish(event)
    
    def get_subscribers(self, event_type: Type[Any]) -> List[Callable]:
        """Get all subscribers for an event type"""
        with self._lock:
            return self._subscribers.get(event_type, []).copy()

class AsyncEventBus(IEventBus):
    """Asynchronous event bus implementation"""
    
    def __init__(self):
        self._subscribers: Dict[Type[DomainEvent], List[Callable[[DomainEvent], None]]] = defaultdict(list)
        self._subscription_ids: Dict[str, Callable[[DomainEvent], None]] = {}
        self._lock = threading.RLock()
        self._next_subscription_id = 1
        self._event_queue: List[DomainEvent] = []
        self._queue_lock = threading.Lock()
        self._worker_thread = None
        self._stop_event = threading.Event()
        self._start_worker()
    
    def _start_worker(self):
        """Start the background worker thread"""
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()
    
    def _worker_loop(self):
        """Background worker loop for processing events"""
        while not self._stop_event.is_set():
            events_to_process = []
            
            with self._queue_lock:
                if self._event_queue:
                    events_to_process = self._event_queue.copy()
                    self._event_queue.clear()
            
            for event in events_to_process:
                self._process_event(event)
            
            # Small sleep to prevent busy waiting
            self._stop_event.wait(0.01)
    
    def _process_event(self, event: Any):
        """Process a single event"""
        with self._lock:
            event_type = type(event)
            handlers = self._subscribers.get(event_type, [])
            
            logger.debug(f"Processing {event_type.__name__} with {len(handlers)} subscribers")
            
            for handler in handlers:
                try:
                    handler(event)
                except Exception as e:
                    logger.error(f"Error in async event handler for {event_type.__name__}: {e}")
    
    def subscribe(self, event_type: Type[Any], handler: Callable[[Any], None]) -> str:
        """Subscribe to an event type"""
        with self._lock:
            subscription_id = f"async_sub_{self._next_subscription_id}"
            self._next_subscription_id += 1
            
            self._subscribers[event_type].append(handler)
            self._subscription_ids[subscription_id] = handler
            
            logger.debug(f"Async subscribed {subscription_id} to {event_type.__name__}")
            return subscription_id
    
    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from events"""
        with self._lock:
            if subscription_id not in self._subscription_ids:
                return False
            
            handler = self._subscription_ids[subscription_id]
            
            # Remove from all event types
            for event_type, handlers in self._subscribers.items():
                if handler in handlers:
                    handlers.remove(handler)
            
            del self._subscription_ids[subscription_id]
            logger.debug(f"Async unsubscribed {subscription_id}")
            return True
    
    def publish(self, event: Any) -> None:
        """Publish an event (adds to queue for async processing)"""
        with self._queue_lock:
            self._event_queue.append(event)
            logger.debug(f"Queued {type(event).__name__} for async processing")
    
    def publish_async(self, event: Any) -> None:
        """Publish an event asynchronously"""
        self.publish(event)
    
    def get_subscribers(self, event_type: Type[Any]) -> List[Callable]:
        """Get all subscribers for an event type"""
        with self._lock:
            return self._subscribers.get(event_type, []).copy()
    
    def shutdown(self):
        """Shutdown the async event bus"""
        self._stop_event.set()
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=1.0)

class EventBusFactory:
    """Factory for creating event buses"""
    
    @staticmethod
    def create_sync_bus() -> IEventBus:
        """Create a synchronous event bus"""
        return EventBus()
    
    @staticmethod
    def create_async_bus() -> IEventBus:
        """Create an asynchronous event bus"""
        return AsyncEventBus()
    
    @staticmethod
    def create_bus(async_mode: bool = False) -> IEventBus:
        """Create an event bus with specified mode"""
        if async_mode:
            return EventBusFactory.create_async_bus()
        else:
            return EventBusFactory.create_sync_bus()
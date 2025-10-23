#!/usr/bin/env python3
"""
Detailed Event System Test
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_detailed_events():
    """Test detailed event functionality"""
    print("Testing detailed event functionality...")
    
    try:
        from src.core.domain_events import SwComponentTypeCreated, SwComponentTypeUpdated
        from src.core.domain_events.event_bus import EventBusFactory
        from src.core.models.autosar_elements import SwComponentType, SwComponentTypeCategory
        
        # Create event bus
        event_bus = EventBusFactory.create_sync_bus()
        
        # Track events
        received_events = []
        def event_handler(event):
            received_events.append(event)
            print(f"Received event: {event.event_type} - {getattr(event, 'component_name', 'N/A')}")
        
        event_bus.subscribe(SwComponentTypeCreated, event_handler)
        event_bus.subscribe(SwComponentTypeUpdated, event_handler)
        
        # Create component
        component = SwComponentType("TestComponent", SwComponentTypeCategory.APPLICATION, "Test Description")
        component.set_event_bus(event_bus)
        
        print(f"Component created: {component.short_name}")
        print(f"Component ID: {component.id}")
        print(f"Domain events before change: {len(component.get_domain_events())}")
        
        # Manually add a domain event to test
        from src.core.domain_events import SwComponentTypeCreated
        manual_event = SwComponentTypeCreated(
            component_id=component.id,
            component_name=component.short_name,
            category=component.category.value,
            source='ManualTest'
        )
        component.add_domain_event(manual_event)
        print(f"Domain events after manual add: {len(component.get_domain_events())}")
        
        # Change name
        print("Changing name...")
        component.change_name("NewComponentName")
        print(f"Domain events after change: {len(component.get_domain_events())}")
        
        # Publish events
        print("Publishing events...")
        component.publish_domain_events()
        print(f"Received events: {len(received_events)}")
        
        for i, event in enumerate(received_events):
            print(f"Event {i+1}: {event.event_type} - {getattr(event, 'component_name', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_detailed_events()
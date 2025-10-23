#!/usr/bin/env python3
"""
Simple Event System Test
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_simple_events():
    """Test basic event functionality"""
    print("Testing simple event functionality...")
    
    try:
        from src.core.domain_events import SwComponentTypeCreated
        from src.core.domain_events.event_bus import EventBusFactory
        from src.core.models.autosar_elements import SwComponentType, SwComponentTypeCategory
        
        # Create event bus
        event_bus = EventBusFactory.create_sync_bus()
        
        # Track events
        received_events = []
        def event_handler(event):
            received_events.append(event)
            print(f"Received event: {event.event_type} - {event.component_name}")
        
        event_bus.subscribe(SwComponentTypeCreated, event_handler)
        
        # Create component
        component = SwComponentType("TestComponent", SwComponentTypeCategory.APPLICATION, "Test Description")
        component.set_event_bus(event_bus)
        
        print(f"Component created: {component.short_name}")
        print(f"Domain events before change: {len(component.get_domain_events())}")
        
        # Change name
        component.change_name("NewComponentName")
        print(f"Domain events after change: {len(component.get_domain_events())}")
        
        # Publish events
        component.publish_domain_events()
        print(f"Received events: {len(received_events)}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_simple_events()
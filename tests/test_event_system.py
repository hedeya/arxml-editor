#!/usr/bin/env python3
"""
Event System Test
Tests the domain events system for loose coupling
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_domain_events():
    """Test domain event creation and serialization"""
    print("=" * 60)
    print("DOMAIN EVENTS TEST")
    print("=" * 60)
    
    try:
        from src.core.domain_events import (
            SwComponentTypeCreated, SwComponentTypeUpdated, SwComponentTypeDeleted,
            PortInterfaceCreated, DataElementAdded, DocumentLoaded,
            ValidationIssueDetected, SystemError, EventSeverity
        )
        
        # Test 1: Event Creation
        print("✓ Testing event creation...")
        event = SwComponentTypeCreated(
            component_id="comp_123",
            component_name="TestComponent",
            category="APPLICATION",
            source="TestSource"
        )
        
        assert event.event_id is not None
        assert event.component_name == "TestComponent"
        assert event.event_type == "SwComponentTypeCreated"
        assert event.severity == EventSeverity.INFO
        print("✅ Event creation working")
        
        # Test 2: Event Serialization
        print("✓ Testing event serialization...")
        event_dict = event.to_dict()
        assert 'event_id' in event_dict
        assert 'timestamp' in event_dict
        assert 'event_type' in event_dict
        assert 'data' in event_dict
        assert event_dict['data']['component_name'] == "TestComponent"
        print("✅ Event serialization working")
        
        # Test 3: Different Event Types
        print("✓ Testing different event types...")
        events = [
            PortInterfaceCreated("TestInterface", "Test Interface", False),
            DataElementAdded("iface_123", "TestInterface", "TestElement", "string"),
            DocumentLoaded("/path/to/file.arxml", "doc_123"),
            ValidationIssueDetected("issue_123", "elem_123", "SwComponentType", "Test error"),
            SystemError("TestError", "Test error message", "stack trace")
        ]
        
        for event in events:
            assert event.event_id is not None
            assert event.event_type is not None
            assert event.timestamp is not None
        
        print("✅ Different event types working")
        
        return True
        
    except Exception as e:
        print(f"❌ Domain events test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_event_bus():
    """Test event bus functionality"""
    print("\n✓ Testing event bus...")
    
    try:
        from src.core.domain_events.event_bus import EventBusFactory
        from src.core.domain_events import SwComponentTypeCreated, PortInterfaceCreated
        
        # Create event bus
        event_bus = EventBusFactory.create_sync_bus()
        
        # Test 1: Event Subscription
        print("✓ Testing event subscription...")
        received_events = []
        
        def event_handler(event):
            received_events.append(event)
        
        subscription_id = event_bus.subscribe(SwComponentTypeCreated, event_handler)
        assert subscription_id is not None
        print("✅ Event subscription working")
        
        # Test 2: Event Publishing
        print("✓ Testing event publishing...")
        event = SwComponentTypeCreated(
            component_name="TestComponent",
            component_id="comp_123",
            category="APPLICATION"
        )
        
        event_bus.publish(event)
        assert len(received_events) == 1
        assert received_events[0].component_name == "TestComponent"
        print("✅ Event publishing working")
        
        # Test 3: Multiple Subscribers
        print("✓ Testing multiple subscribers...")
        second_handler_events = []
        
        def second_handler(event):
            second_handler_events.append(event)
        
        event_bus.subscribe(SwComponentTypeCreated, second_handler)
        
        event2 = SwComponentTypeCreated(
            component_name="TestComponent2",
            component_id="comp_456",
            category="ATOMIC"
        )
        
        event_bus.publish(event2)
        assert len(received_events) == 2
        assert len(second_handler_events) == 1
        print("✅ Multiple subscribers working")
        
        # Test 4: Unsubscription
        print("✓ Testing unsubscription...")
        success = event_bus.unsubscribe(subscription_id)
        assert success
        
        event3 = SwComponentTypeCreated(
            component_name="TestComponent3",
            component_id="comp_789",
            category="COMPOSITION"
        )
        
        event_bus.publish(event3)
        assert len(received_events) == 2  # Should not increase
        assert len(second_handler_events) == 2  # Should increase
        print("✅ Unsubscription working")
        
        return True
        
    except Exception as e:
        print(f"❌ Event bus test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_event_handlers():
    """Test event handlers"""
    print("\n✓ Testing event handlers...")
    
    try:
        from src.core.domain_events.handlers import (
            LoggingEventHandler, AuditEventHandler, ValidationEventHandler,
            UINotificationHandler, MetricsEventHandler, EventHandlerRegistry
        )
        from src.core.domain_events import SwComponentTypeCreated, ValidationIssueDetected
        
        # Test 1: Individual Handlers
        print("✓ Testing individual handlers...")
        
        # Logging handler
        logging_handler = LoggingEventHandler()
        event = SwComponentTypeCreated(component_id="TestComponent", component_name="comp_123", category="APPLICATION")
        logging_handler.handle(event)
        assert logging_handler.handled_events == 1
        print("✅ Logging handler working")
        
        # Audit handler
        audit_handler = AuditEventHandler()
        audit_handler.handle(event)
        assert len(audit_handler.audit_log) == 1
        print("✅ Audit handler working")
        
        # Validation handler
        validation_handler = ValidationEventHandler()
        validation_event = ValidationIssueDetected(issue_id="issue_123", element_id="elem_123", element_type="SwComponentType", message="Test error")
        validation_handler.handle(validation_event)
        assert len(validation_handler.validation_issues) == 1
        print("✅ Validation handler working")
        
        # Metrics handler
        metrics_handler = MetricsEventHandler()
        metrics_handler.handle(event)
        metrics_handler.handle(validation_event)
        metrics = metrics_handler.get_metrics()
        assert metrics['total_events'] == 2
        assert 'SwComponentTypeCreated' in metrics['events_by_type']
        print("✅ Metrics handler working")
        
        # Test 2: Handler Registry
        print("✓ Testing handler registry...")
        registry = EventHandlerRegistry()
        registry.register_handler(logging_handler)
        registry.register_handler(audit_handler)
        registry.register_handler(validation_handler)
        registry.register_handler(metrics_handler)
        
        assert len(registry.get_all_handlers()) == 4
        
        # Test handler selection
        handlers = registry.get_handlers_for_event(event)
        assert len(handlers) == 4  # All handlers can handle any event
        
        handlers = registry.get_handlers_for_event(validation_event)
        assert len(handlers) == 4
        
        print("✅ Handler registry working")
        
        return True
        
    except Exception as e:
        print(f"❌ Event handlers test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_domain_models_with_events():
    """Test domain models with event publishing"""
    print("\n✓ Testing domain models with events...")
    
    try:
        from src.core.domain_events.event_bus import EventBusFactory
        from src.core.domain_events import SwComponentTypeCreated, SwComponentTypeUpdated
        from src.core.models.autosar_elements import SwComponentType, SwComponentTypeCategory
        
        # Create event bus
        event_bus = EventBusFactory.create_sync_bus()
        
        # Track events
        received_events = []
        def event_handler(event):
            received_events.append(event)
        
        event_bus.subscribe(SwComponentTypeCreated, event_handler)
        event_bus.subscribe(SwComponentTypeUpdated, event_handler)
        
        # Test 1: Component Creation with Events
        print("✓ Testing component creation with events...")
        component = SwComponentType("TestComponent", SwComponentTypeCategory.APPLICATION, "Test Description")
        component.set_event_bus(event_bus)
        
        # Initially no events
        assert len(component.get_domain_events()) == 0
        
        # Change name should create event
        component.change_name("NewComponentName")
        assert len(component.get_domain_events()) == 1
        
        # Publish events
        component.publish_domain_events()
        assert len(received_events) == 1
        assert received_events[0].component_name == "NewComponentName"
        print("✅ Component creation with events working")
        
        # Test 2: Component Updates with Events
        print("✓ Testing component updates with events...")
        component.change_category(SwComponentTypeCategory.ATOMIC)
        component.publish_domain_events()
        
        assert len(received_events) == 2
        assert received_events[1].changes['category']['new'] == 'AtomicSwComponentType'
        print("✅ Component updates with events working")
        
        return True
        
    except Exception as e:
        print(f"❌ Domain models with events test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_application_services_with_events():
    """Test application services with event publishing"""
    print("\n✓ Testing application services with events...")
    
    try:
        from src.core.container import setup_container
        from src.core.domain_events import SwComponentTypeCreated, PortInterfaceCreated
        from src.core.application_services import ISwComponentTypeApplicationService, IPortInterfaceApplicationService
        
        # Setup container with event system
        container = setup_container()
        
        # Get application services
        sw_service = container.get(ISwComponentTypeApplicationService)
        port_service = container.get(IPortInterfaceApplicationService)
        
        # Track events
        received_events = []
        event_bus = container.get(container._registrations[ISwComponentTypeApplicationService][1].__globals__['IEventBus'])
        
        def event_handler(event):
            received_events.append(event)
        
        event_bus.subscribe(SwComponentTypeCreated, event_handler)
        event_bus.subscribe(PortInterfaceCreated, event_handler)
        
        # Test 1: Component Creation
        print("✓ Testing component creation through application service...")
        result = sw_service.create_component_type("TestComponent", "APPLICATION", "Test Description")
        assert result.success
        assert len(received_events) == 1
        assert received_events[0].component_name == "TestComponent"
        print("✅ Component creation through application service working")
        
        # Test 2: Interface Creation
        print("✓ Testing interface creation through application service...")
        result = port_service.create_port_interface("TestInterface", False, "Test Description")
        assert result.success
        assert len(received_events) == 2
        assert received_events[1].interface_name == "TestInterface"
        print("✅ Interface creation through application service working")
        
        return True
        
    except Exception as e:
        print(f"❌ Application services with events test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Test full integration of event system"""
    print("\n✓ Testing full integration...")
    
    try:
        from src.core.container import setup_container
        from src.core.application import ARXMLEditorApp
        from src.core.domain_events import DocumentCreated, SwComponentTypeCreated
        
        # Create application with DI
        container = setup_container()
        app = ARXMLEditorApp(container)
        
        # Track events
        received_events = []
        event_bus = container.get(container._registrations[ISwComponentTypeApplicationService][1].__globals__['IEventBus'])
        
        def event_handler(event):
            received_events.append(event)
        
        event_bus.subscribe(DocumentCreated, event_handler)
        event_bus.subscribe(SwComponentTypeCreated, event_handler)
        
        # Test 1: Document Creation
        print("✓ Testing document creation with events...")
        document = app.new_document()
        assert document is not None
        print("✅ Document creation with events working")
        
        # Test 2: Component Creation through Application
        print("✓ Testing component creation through application...")
        if app.sw_component_service:
            result = app.sw_component_service.create_component_type("IntegrationTest", "APPLICATION")
            assert result.success
            print("✅ Component creation through application working")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all event system tests"""
    print("Testing Event System Implementation")
    print("=" * 60)
    
    tests = [
        ("Domain Events", test_domain_events),
        ("Event Bus", test_event_bus),
        ("Event Handlers", test_event_handlers),
        ("Domain Models with Events", test_domain_models_with_events),
        ("Application Services with Events", test_application_services_with_events),
        ("Full Integration", test_integration)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n[{test_name}]")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            failed += 1
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 60)
    print("EVENT SYSTEM TEST RESULTS")
    print("=" * 60)
    print(f"✅ PASSED: {passed}")
    print(f"❌ FAILED: {failed}")
    print(f"📊 SUCCESS RATE: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL EVENT SYSTEM TESTS PASSED!")
        print("   - Domain events implemented")
        print("   - Event bus working")
        print("   - Event handlers functional")
        print("   - Domain models publishing events")
        print("   - Application services publishing events")
        print("   - Full integration working")
        print("\n🚀 Event System provides:")
        print("   - Loose coupling between components")
        print("   - Better separation of concerns")
        print("   - Improved DDD compliance")
        print("   - Enhanced testability")
        print("   - Audit and logging capabilities")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the implementation.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
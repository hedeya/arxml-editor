"""
UI Event Adapter
Bridges the core UIEventBus to Qt signals so legacy UI code can connect to QObject signals.
"""
from PyQt6.QtCore import QObject, pyqtSignal
from typing import Any

class UIEventAdapter(QObject):
    """Adapter that exposes Qt signals for UI events published on UIEventBus"""

    element_changed = pyqtSignal(object)

    def __init__(self, ui_event_bus):
        super().__init__()
        self._ui_event_bus = ui_event_bus
        # Subscribe to event bus
        try:
            self._ui_event_bus.subscribe('element_changed', self._on_element_changed)
        except Exception:
            pass

    def _on_element_changed(self, payload: Any) -> None:
        try:
            self.element_changed.emit(payload)
        except Exception:
            pass

    def dispose(self) -> None:
        try:
            self._ui_event_bus.unsubscribe('element_changed', self._on_element_changed)
        except Exception:
            pass

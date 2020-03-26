import psutil

from opentelemetry import metrics
from opentelemetry.sdk.metrics import LabelSet
from opentelemetry.sdk.metrics.export.controller import PushController


class SystemMetrics:
    # Callback to gather RAM memory usage
    def get_memory_available(self, observer):
        system_memory = psutil.virtual_memory()
        observer.observe(system_memory.available, LabelSet({"memory": "available"}))

    def __init__(self, exporter):
        self.meter = metrics.get_meter(__name__)
        self.controller = PushController(
            meter=self.meter, exporter=exporter, interval=10
        )

        self.meter.register_observer(
            callback=self.get_memory_available,
            name="mem.available",
            description="Memory available",
            unit="1",
            value_type=int,
            label_keys=("host"),
        )

import gc
import os
import typing

import psutil

from opentelemetry import metrics
from opentelemetry.sdk.metrics.export import MetricsExporter
from opentelemetry.sdk.metrics.export.controller import PushController


_DEFAULT_INTERVAL = 30


# TODO: add unit tests
class SystemMetrics:
    def _get_cpu_total(self, observer):
        cpu_times = psutil.cpu_times()
        usage = cpu_times.user + cpu_times.system
        metrics = [
            "nice",
            "iowait",
            "irq",
            "softirq",
            "steal",
            "idle",
        ]
        for m in metrics:
            if hasattr(cpu_times, m):
                usage += getattr(cpu_times, m)

        observer.observe(usage, self._labels)

    def _get_cpu_usage(self, observer):
        cpu_times = psutil.cpu_times()
        usage = cpu_times.user + cpu_times.system
        metrics = [
            "nice",
            "iowait",
            "irq",
            "softirq",
            "steal",
        ]
        for m in metrics:
            if hasattr(cpu_times, m):
                usage += getattr(cpu_times, m)

        observer.observe(usage, self._labels)

    def _get_memory_available(self, observer):
        system_memory = psutil.virtual_memory()
        observer.observe(system_memory.available, self._labels)

    def _get_memory_total(self, observer):
        system_memory = psutil.virtual_memory()
        observer.observe(system_memory.total, self._labels)

    def _get_cpu_user(self, observer):
        cpu_times = psutil.cpu_times()
        observer.observe(cpu_times.user, self._labels)

    def _get_cpu_nice(self, observer):
        cpu_times = psutil.cpu_times()
        observer.observe(cpu_times.nice, self._labels)

    def _get_cpu_system(self, observer):
        cpu_times = psutil.cpu_times()
        observer.observe(cpu_times.system, self._labels)

    def _get_cpu_idle(self, observer):
        cpu_times = psutil.cpu_times()
        observer.observe(cpu_times.idle, self._labels)

    def _get_network_bytes_received(self, observer):
        net_io = psutil.net_io_counters()
        observer.observe(net_io.bytes_recv, self._labels)

    def _get_network_bytes_sent(self, observer):
        net_io = psutil.net_io_counters()
        observer.observe(net_io.bytes_sent, self._labels)

    def _get_runtime_memory_rss(self, observer):
        observer.observe(self._proc.memory_info().rss, self._labels)

    def _get_runtime_gc_count0(self, observer):
        gc_count = gc.get_count()
        observer.observe(gc_count[0], self._labels)

    def _get_runtime_gc_count1(self, observer):
        gc_count = gc.get_count()
        observer.observe(gc_count[1], self._labels)

    def _get_runtime_gc_count2(self, observer):
        gc_count = gc.get_count()
        observer.observe(gc_count[2], self._labels)

    def __init__(
        self,
        exporter: MetricsExporter,
        interval: int = _DEFAULT_INTERVAL,
        labels: typing.Dict[str, str] = {},
    ):
        self.meter = metrics.get_meter(__name__)
        self.controller = PushController(
            meter=self.meter, exporter=exporter, interval=interval
        )
        self._proc = psutil.Process(os.getpid())
        self._labels = labels

        self.meter.register_observer(
            callback=self._get_memory_available,
            name="mem.available",
            description="Memory available",
            unit="bytes",
            value_type=int,
            label_keys=self._labels.keys(),
        )

        self.meter.register_observer(
            callback=self._get_memory_total,
            name="mem.total",
            description="Memory total",
            unit="bytes",
            value_type=int,
            label_keys=self._labels.keys(),
        )

        self.meter.register_observer(
            callback=self._get_cpu_user,
            name="cpu.user",
            description="CPU user metrics",
            unit="seconds",
            value_type=float,
            label_keys=self._labels.keys(),
        )

        self.meter.register_observer(
            callback=self._get_cpu_nice,
            name="cpu.nice",
            description="CPU nice metrics",
            unit="seconds",
            value_type=float,
            label_keys=self._labels.keys(),
        )

        self.meter.register_observer(
            callback=self._get_cpu_system,
            name="cpu.sys",
            description="CPU system metrics",
            unit="seconds",
            value_type=float,
            label_keys=self._labels.keys(),
        )

        self.meter.register_observer(
            callback=self._get_cpu_idle,
            name="cpu.idle",
            description="CPU idle metrics",
            unit="seconds",
            value_type=float,
            label_keys=self._labels.keys(),
        )

        self.meter.register_observer(
            callback=self._get_cpu_usage,
            name="cpu.usage",
            description="CPU usage metrics",
            unit="seconds",
            value_type=float,
            label_keys=self._labels.keys(),
        )

        self.meter.register_observer(
            callback=self._get_cpu_total,
            name="cpu.total",
            description="CPU total metrics",
            unit="seconds",
            value_type=float,
            label_keys=self._labels.keys(),
        )

        self.meter.register_observer(
            callback=self._get_network_bytes_sent,
            name="net.bytes_sent",
            description="Network:bytes sent",
            unit="bytes",
            value_type=int,
            label_keys=self._labels.keys(),
        )

        self.meter.register_observer(
            callback=self._get_network_bytes_received,
            name="net.bytes_recv",
            description="Network:bytes received",
            unit="bytes",
            value_type=int,
            label_keys=self._labels.keys(),
        )

        self.meter.register_observer(
            callback=self._get_runtime_memory_rss,
            name="runtime.python.mem.rss",
            description="Runtime: memory rss",
            unit="bytes",
            value_type=int,
            label_keys=self._labels.keys(),
        )

        self.meter.register_observer(
            callback=self._get_runtime_gc_count0,
            name="runtime.python.gc.count.gen0",
            description="Runtime: gc objects gen0",
            unit="objects",
            value_type=int,
            label_keys=self._labels.keys(),
        )

        self.meter.register_observer(
            callback=self._get_runtime_gc_count1,
            name="runtime.python.gc.count.gen1",
            description="Runtime: gc objects gen1",
            unit="objects",
            value_type=int,
            label_keys=self._labels.keys(),
        )

        self.meter.register_observer(
            callback=self._get_runtime_gc_count2,
            name="runtime.python.gc.count.gen2",
            description="Runtime: gc objects gen2",
            unit="objects",
            value_type=int,
            label_keys=self._labels.keys(),
        )

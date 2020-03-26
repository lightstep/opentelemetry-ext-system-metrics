# System Metrics Extension for Python
This is an OpenTelemetry extension to collect system metrics, which can then be exported via an OpenTelemetry metrics exporter

## Install

```bash
pip install opentelemetry-ext-system-metrics
```

## Initialize

```python
exporter = ConsoleMetricsExporter()
SystemMetrics(exporter)
```
from prometheus_client import Counter, Histogram

class PrometheusService:
    def __init__(self):
        self.request_count = Counter(
            'user_request_count', 'Total Request Count', ['method', 'route', 'status']
        )
        self.request_latency = Histogram(
            'user_request_latency_seconds', 'Request latency', ['method', 'route']
        )
        
    def log_request(self, method, route, status):
        self.request_count.labels(method=method, route=route, status=status).inc()
        #self.request_latency.labels(method=method, route=route).observe([0.1, 0.5, 1.0, 1.5, 2.0])
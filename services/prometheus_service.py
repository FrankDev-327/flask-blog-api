from prometheus_client import Counter, Histogram

class PrometheusService:
    def __init__(self):
        self.counter = self.request_count = Counter(
            'user_request_count', 'Total Request Count', ['method', 'route', 'status']
        )
        self.histogram = self.request_latency = Histogram(
            'user_request_latency_seconds', 'Request latency', ['method', 'route']
        )
        
        self.register_metrics()
    
    """"  
    def register_metrics(self): 
        from prometheus_client import REGISTRY
        REGISTRY.register(self.request_count)
        REGISTRY.register(self.request_latency)
    """
                
    def log_count_request(self, method, route, status):
        self.counter.labels(method=method, route=route, status=status).inc()
        
    """def log_request_latency(self, method, route, latency):
        self.histogram .labels(method=method, route=route).observe(latency)
    """
        
        
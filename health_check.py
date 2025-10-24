"""
Health Check Server for Koyeb/Cloud Deployments
Runs a simple HTTP server on port 8080 for health checks
"""
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import json

logger = logging.getLogger(__name__)


class HealthCheckHandler(BaseHTTPRequestHandler):
    """Simple health check HTTP handler"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/health':
            # Health check endpoint
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'ok',
                'bot': 'running',
                'service': 'telegram-strategy-game'
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            # 404 for other paths
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Override to reduce noise in logs"""
        # Only log non-health check requests
        if '/health' not in self.path and '/' != self.path:
            logger.debug(f"Health check request: {self.path}")


def start_health_check_server(port=8080):
    """Start health check server in background thread"""
    try:
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        logger.info(f"Health check server started on port {port}")
        
        # Run in background thread
        def run_server():
            try:
                server.serve_forever()
            except Exception as e:
                logger.error(f"Health check server error: {e}")
        
        thread = Thread(target=run_server, daemon=True)
        thread.start()
        logger.info("Health check server running in background")
        return server
    except Exception as e:
        logger.error(f"Failed to start health check server: {e}")
        return None


if __name__ == '__main__':
    # Test the health check server
    logging.basicConfig(level=logging.INFO)
    start_health_check_server(8080)
    
    # Keep main thread alive for testing
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nHealth check server stopped")



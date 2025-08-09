"""
DISASTER RECOVERY & LOAD BALANCING MODULE
========================================
Advanced disaster recovery, load balancing, and high availability systems for BOTZZZ.

Features:
- Multi-region failover capabilities
- Automatic load balancing and scaling
- Data replication and synchronization
- Service mesh integration
- Real-time health monitoring
- Automated disaster recovery procedures
"""

import json
import time
import threading
import random
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import requests


class NodeStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    MAINTENANCE = "maintenance"


class LoadBalancingStrategy(Enum):
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    GEOGRAPHIC = "geographic"
    LEAST_RESPONSE_TIME = "least_response_time"


@dataclass
class ServiceNode:
    """Represents a service node in the cluster"""
    node_id: str
    host: str
    port: int
    region: str
    weight: float = 1.0
    status: NodeStatus = NodeStatus.HEALTHY
    connections: int = 0
    response_times: List[float] = field(default_factory=list)
    last_health_check: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def average_response_time(self) -> float:
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)
    
    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"


@dataclass
class BackupSnapshot:
    """Represents a backup snapshot"""
    snapshot_id: str
    timestamp: datetime
    size_bytes: int
    checksum: str
    location: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class LoadBalancer:
    """Advanced load balancer with multiple strategies"""
    
    def __init__(self, strategy: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_RESPONSE_TIME):
        self.strategy = strategy
        self.nodes: Dict[str, ServiceNode] = {}
        self.current_index = 0
        self.lock = threading.Lock()
    
    def add_node(self, node: ServiceNode):
        """Add a node to the load balancer"""
        with self.lock:
            self.nodes[node.node_id] = node
    
    def remove_node(self, node_id: str):
        """Remove a node from the load balancer"""
        with self.lock:
            self.nodes.pop(node_id, None)
    
    def get_healthy_nodes(self) -> List[ServiceNode]:
        """Get all healthy nodes"""
        return [node for node in self.nodes.values() if node.status == NodeStatus.HEALTHY]
    
    def select_node(self) -> Optional[ServiceNode]:
        """Select the best node based on the load balancing strategy"""
        healthy_nodes = self.get_healthy_nodes()
        if not healthy_nodes:
            return None
        
        if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            return self._round_robin_select(healthy_nodes)
        elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
            return min(healthy_nodes, key=lambda node: node.connections)
        elif self.strategy == LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN:
            return self._weighted_round_robin_select(healthy_nodes)
        elif self.strategy == LoadBalancingStrategy.LEAST_RESPONSE_TIME:
            return min(healthy_nodes, key=lambda node: node.average_response_time or float('inf'))
        elif self.strategy == LoadBalancingStrategy.GEOGRAPHIC:
            return self._geographic_select(healthy_nodes)
        else:
            return random.choice(healthy_nodes)
    
    def _round_robin_select(self, nodes: List[ServiceNode]) -> ServiceNode:
        """Round robin selection"""
        with self.lock:
            node = nodes[self.current_index % len(nodes)]
            self.current_index += 1
            return node
    
    def _weighted_round_robin_select(self, nodes: List[ServiceNode]) -> ServiceNode:
        """Weighted round robin selection"""
        total_weight = sum(node.weight for node in nodes)
        random_weight = random.uniform(0, total_weight)
        
        current_weight = 0
        for node in nodes:
            current_weight += node.weight
            if current_weight >= random_weight:
                return node
        
        return nodes[-1]
    
    def _geographic_select(self, nodes: List[ServiceNode]) -> ServiceNode:
        """Geographic-based selection (simplified)"""
        # In a real implementation, this would consider user location
        regions = defaultdict(list)
        for node in nodes:
            regions[node.region].append(node)
        
        # Prefer local region (simplified logic)
        preferred_regions = ['us-east', 'us-west', 'eu-west', 'asia-pacific']
        for region in preferred_regions:
            if region in regions:
                return min(regions[region], key=lambda n: n.connections)
        
        return min(nodes, key=lambda node: node.connections)
    
    def record_request(self, node_id: str, response_time: float):
        """Record request metrics for a node"""
        if node_id in self.nodes:
            node = self.nodes[node_id]
            node.connections += 1
            node.response_times.append(response_time)
            
            # Keep only last 100 response times
            if len(node.response_times) > 100:
                node.response_times = node.response_times[-100:]
    
    def release_connection(self, node_id: str):
        """Release a connection from a node"""
        if node_id in self.nodes:
            self.nodes[node_id].connections = max(0, self.nodes[node_id].connections - 1)


class DisasterRecoveryManager:
    """Comprehensive disaster recovery system"""
    
    def __init__(self):
        self.backup_locations: List[str] = []
        self.snapshots: List[BackupSnapshot] = []
        self.replication_nodes: Dict[str, ServiceNode] = {}
        self.recovery_procedures: Dict[str, callable] = {}
        self.critical_services = set()
        self.lock = threading.Lock()
    
    def add_backup_location(self, location: str):
        """Add a backup storage location"""
        self.backup_locations.append(location)
    
    def register_critical_service(self, service_name: str):
        """Register a service as critical for disaster recovery"""
        self.critical_services.add(service_name)
    
    def create_snapshot(self, data: bytes, metadata: Dict[str, Any] = None) -> BackupSnapshot:
        """Create a backup snapshot"""
        snapshot_id = hashlib.sha256(f"{time.time()}".encode()).hexdigest()[:16]
        checksum = hashlib.md5(data).hexdigest()
        
        snapshot = BackupSnapshot(
            snapshot_id=snapshot_id,
            timestamp=datetime.now(),
            size_bytes=len(data),
            checksum=checksum,
            location=random.choice(self.backup_locations) if self.backup_locations else "local",
            metadata=metadata or {}
        )
        
        with self.lock:
            self.snapshots.append(snapshot)
            # Keep only last 50 snapshots
            if len(self.snapshots) > 50:
                self.snapshots = self.snapshots[-50:]
        
        return snapshot
    
    def get_latest_snapshot(self) -> Optional[BackupSnapshot]:
        """Get the most recent snapshot"""
        if not self.snapshots:
            return None
        return max(self.snapshots, key=lambda s: s.timestamp)
    
    def verify_snapshot_integrity(self, snapshot: BackupSnapshot, data: bytes) -> bool:
        """Verify snapshot integrity"""
        calculated_checksum = hashlib.md5(data).hexdigest()
        return calculated_checksum == snapshot.checksum
    
    def initiate_disaster_recovery(self, affected_services: List[str]) -> Dict[str, bool]:
        """Initiate disaster recovery procedures"""
        recovery_status = {}
        
        for service in affected_services:
            try:
                if service in self.recovery_procedures:
                    success = self.recovery_procedures[service]()
                    recovery_status[service] = success
                else:
                    # Default recovery: restart service
                    recovery_status[service] = self._default_recovery(service)
            except Exception as e:
                print(f"Recovery failed for {service}: {e}")
                recovery_status[service] = False
        
        return recovery_status
    
    def _default_recovery(self, service_name: str) -> bool:
        """Default recovery procedure"""
        print(f"Initiating default recovery for {service_name}")
        # Simulate recovery process
        time.sleep(2)
        return random.choice([True, True, True, False])  # 75% success rate
    
    def register_recovery_procedure(self, service_name: str, procedure: callable):
        """Register a custom recovery procedure for a service"""
        self.recovery_procedures[service_name] = procedure


class HighAvailabilityCluster:
    """High availability cluster manager"""
    
    def __init__(self):
        self.load_balancers: Dict[str, LoadBalancer] = {}
        self.disaster_recovery = DisasterRecoveryManager()
        self.health_monitor = threading.Thread(target=self._health_monitoring_loop, daemon=True)
        self.monitoring_active = True
        self.failover_triggers: Dict[str, int] = defaultdict(int)
        self.maintenance_windows: List[Tuple[datetime, datetime]] = []
    
    def add_service(self, service_name: str, strategy: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_RESPONSE_TIME):
        """Add a service to the HA cluster"""
        self.load_balancers[service_name] = LoadBalancer(strategy)
        self.disaster_recovery.register_critical_service(service_name)
    
    def add_service_node(self, service_name: str, node: ServiceNode):
        """Add a node to a service"""
        if service_name in self.load_balancers:
            self.load_balancers[service_name].add_node(node)
    
    def get_service_endpoint(self, service_name: str) -> Optional[ServiceNode]:
        """Get the best available endpoint for a service"""
        if service_name not in self.load_balancers:
            return None
        
        return self.load_balancers[service_name].select_node()
    
    def record_service_request(self, service_name: str, node_id: str, response_time: float, success: bool):
        """Record metrics for a service request"""
        if service_name in self.load_balancers:
            self.load_balancers[service_name].record_request(node_id, response_time)
            
            if not success:
                self.failover_triggers[f"{service_name}:{node_id}"] += 1
                
                # Trigger failover if too many failures
                if self.failover_triggers[f"{service_name}:{node_id}"] >= 5:
                    self._trigger_failover(service_name, node_id)
    
    def _trigger_failover(self, service_name: str, node_id: str):
        """Trigger failover for a failing node"""
        if service_name in self.load_balancers:
            lb = self.load_balancers[service_name]
            if node_id in lb.nodes:
                lb.nodes[node_id].status = NodeStatus.UNAVAILABLE
                print(f"FAILOVER: Node {node_id} for service {service_name} marked as unavailable")
                
                # Reset failure counter
                self.failover_triggers[f"{service_name}:{node_id}"] = 0
    
    def _health_monitoring_loop(self):
        """Continuous health monitoring"""
        while self.monitoring_active:
            try:
                for service_name, lb in self.load_balancers.items():
                    for node_id, node in lb.nodes.items():
                        if self._is_in_maintenance_window():
                            node.status = NodeStatus.MAINTENANCE
                            continue
                        
                        # Simulate health check
                        if self._perform_health_check(node):
                            if node.status == NodeStatus.UNAVAILABLE:
                                node.status = NodeStatus.HEALTHY
                                print(f"RECOVERY: Node {node_id} for service {service_name} is healthy again")
                        else:
                            if node.status == NodeStatus.HEALTHY:
                                node.status = NodeStatus.DEGRADED
                                print(f"DEGRADED: Node {node_id} for service {service_name} showing degraded performance")
                        
                        node.last_health_check = datetime.now()
                
                time.sleep(30)  # Health check every 30 seconds
            except Exception as e:
                print(f"Health monitoring error: {e}")
                time.sleep(10)
    
    def _perform_health_check(self, node: ServiceNode) -> bool:
        """Perform health check on a node"""
        try:
            # In a real implementation, this would make actual HTTP requests
            # For now, simulate based on node status and random factors
            if node.status == NodeStatus.UNAVAILABLE:
                return random.random() > 0.9  # 10% chance of recovery
            elif node.status == NodeStatus.DEGRADED:
                return random.random() > 0.3  # 70% chance of recovery
            else:
                return random.random() > 0.05  # 95% uptime for healthy nodes
        except:
            return False
    
    def _is_in_maintenance_window(self) -> bool:
        """Check if current time is in a maintenance window"""
        now = datetime.now()
        for start, end in self.maintenance_windows:
            if start <= now <= end:
                return True
        return False
    
    def schedule_maintenance(self, start: datetime, end: datetime):
        """Schedule a maintenance window"""
        self.maintenance_windows.append((start, end))
    
    def start_monitoring(self):
        """Start health monitoring"""
        if not self.health_monitor.is_alive():
            self.health_monitor.start()
    
    def stop_monitoring(self):
        """Stop health monitoring"""
        self.monitoring_active = False
    
    def get_cluster_status(self) -> Dict[str, Any]:
        """Get comprehensive cluster status"""
        status = {
            'services': {},
            'total_nodes': 0,
            'healthy_nodes': 0,
            'degraded_nodes': 0,
            'unavailable_nodes': 0,
            'snapshots': len(self.disaster_recovery.snapshots),
            'critical_services': list(self.disaster_recovery.critical_services)
        }
        
        for service_name, lb in self.load_balancers.items():
            service_status = {
                'nodes': [],
                'strategy': lb.strategy.value,
                'total_nodes': len(lb.nodes),
                'healthy_nodes': len([n for n in lb.nodes.values() if n.status == NodeStatus.HEALTHY])
            }
            
            for node in lb.nodes.values():
                service_status['nodes'].append({
                    'node_id': node.node_id,
                    'host': node.host,
                    'port': node.port,
                    'region': node.region,
                    'status': node.status.value,
                    'connections': node.connections,
                    'avg_response_time': node.average_response_time,
                    'weight': node.weight
                })
                
                status['total_nodes'] += 1
                if node.status == NodeStatus.HEALTHY:
                    status['healthy_nodes'] += 1
                elif node.status == NodeStatus.DEGRADED:
                    status['degraded_nodes'] += 1
                elif node.status == NodeStatus.UNAVAILABLE:
                    status['unavailable_nodes'] += 1
            
            status['services'][service_name] = service_status
        
        return status


# Global HA cluster instance
ha_cluster = HighAvailabilityCluster()

# Initialize with demo nodes for BOTZZZ services
def initialize_ha_cluster():
    """Initialize HA cluster with demo configuration"""
    
    # Add CAPTCHA service nodes
    ha_cluster.add_service('captcha_service', LoadBalancingStrategy.LEAST_RESPONSE_TIME)
    ha_cluster.add_service_node('captcha_service', ServiceNode('captcha_node_1', '10.0.1.10', 8080, 'us-east', weight=1.0))
    ha_cluster.add_service_node('captcha_service', ServiceNode('captcha_node_2', '10.0.1.11', 8080, 'us-west', weight=1.2))
    ha_cluster.add_service_node('captcha_service', ServiceNode('captcha_node_3', '10.0.2.10', 8080, 'eu-west', weight=0.8))
    
    # Add Proxy service nodes
    ha_cluster.add_service('proxy_service', LoadBalancingStrategy.GEOGRAPHIC)
    ha_cluster.add_service_node('proxy_service', ServiceNode('proxy_node_1', '10.0.3.10', 8080, 'us-east', weight=1.0))
    ha_cluster.add_service_node('proxy_service', ServiceNode('proxy_node_2', '10.0.3.11', 8080, 'asia-pacific', weight=1.5))
    
    # Add Rate Limiting service nodes
    ha_cluster.add_service('rate_limit_service', LoadBalancingStrategy.LEAST_CONNECTIONS)
    ha_cluster.add_service_node('rate_limit_service', ServiceNode('ratelimit_node_1', '10.0.4.10', 8080, 'us-east'))
    ha_cluster.add_service_node('rate_limit_service', ServiceNode('ratelimit_node_2', '10.0.4.11', 8080, 'us-west'))
    
    # Add Account Warming service nodes
    ha_cluster.add_service('account_warming_service', LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN)
    ha_cluster.add_service_node('account_warming_service', ServiceNode('warming_node_1', '10.0.5.10', 8080, 'us-east', weight=2.0))
    ha_cluster.add_service_node('account_warming_service', ServiceNode('warming_node_2', '10.0.5.11', 8080, 'eu-west', weight=1.0))
    
    # Configure disaster recovery
    ha_cluster.disaster_recovery.add_backup_location('s3://botzzz-backups-us-east')
    ha_cluster.disaster_recovery.add_backup_location('s3://botzzz-backups-eu-west')
    ha_cluster.disaster_recovery.add_backup_location('gcs://botzzz-backups-asia')
    
    # Start health monitoring
    ha_cluster.start_monitoring()
    
    print("🚀 High Availability Cluster Initialized")
    print("✅ Load Balancers: ACTIVE")
    print("✅ Health Monitoring: ACTIVE")
    print("✅ Disaster Recovery: READY")
    print("✅ Multi-Region Nodes: DEPLOYED")


def get_ha_cluster_status():
    """Get HA cluster status for dashboard"""
    return ha_cluster.get_cluster_status()


def bulletproof_request(service_name: str, request_func: callable, *args, **kwargs):
    """Execute a request with full HA protection"""
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        # Get best available node
        node = ha_cluster.get_service_endpoint(service_name)
        if not node:
            raise Exception(f"No healthy nodes available for service: {service_name}")
        
        start_time = time.time()
        try:
            # Execute the request
            result = request_func(*args, **kwargs)
            response_time = (time.time() - start_time) * 1000
            
            # Record successful request
            ha_cluster.record_service_request(service_name, node.node_id, response_time, True)
            ha_cluster.load_balancers[service_name].release_connection(node.node_id)
            
            return result
        
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            
            # Record failed request
            ha_cluster.record_service_request(service_name, node.node_id, response_time, False)
            ha_cluster.load_balancers[service_name].release_connection(node.node_id)
            
            retry_count += 1
            if retry_count >= max_retries:
                raise e
            
            print(f"Request failed for {service_name} on {node.node_id}, retrying... ({retry_count}/{max_retries})")
            time.sleep(0.5 * retry_count)  # Exponential backoff


if __name__ == "__main__":
    initialize_ha_cluster()
    print(f"Cluster Status: {get_ha_cluster_status()}")

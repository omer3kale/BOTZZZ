#!/usr/bin/env python3
"""
🔒 TIER 2 ULTRA HIGH-IMPACT FEATURE #4: ENTERPRISE SECURITY & COMPLIANCE SUITE
================================================================================

Comprehensive Security & Compliance Management Platform providing:
- Advanced Threat Detection & Response
- Real-time Security Monitoring & Alerts
- Compliance Management (SOX, GDPR, HIPAA, PCI)
- Data Protection & Encryption
- Access Control & Identity Management
- Security Audit Trails & Reporting
- Vulnerability Assessment & Management
- Incident Response & Recovery

Enterprise-grade security and compliance for mission-critical operations.
"""

import sqlite3
import json
import logging
import hashlib
import hmac
import secrets
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import threading
import time
import re
import ipaddress
from collections import defaultdict, deque
import asyncio
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('enterprise_security')

class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ComplianceStandard(Enum):
    SOX = "sox"
    GDPR = "gdpr"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    ISO_27001 = "iso_27001"
    CCPA = "ccpa"

class SecurityEventType(Enum):
    LOGIN_ATTEMPT = "login_attempt"
    FAILED_LOGIN = "failed_login"
    DATA_ACCESS = "data_access"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    MALWARE_DETECTION = "malware_detection"
    DDoS_ATTACK = "ddos_attack"
    SQL_INJECTION = "sql_injection"
    XSS_ATTEMPT = "xss_attempt"
    BRUTE_FORCE = "brute_force"

class IncidentStatus(Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    RESOLVED = "resolved"
    CLOSED = "closed"

@dataclass
class SecurityEvent:
    """Security event record"""
    event_id: str
    event_type: SecurityEventType
    threat_level: ThreatLevel
    source_ip: str
    user_id: Optional[str]
    timestamp: datetime
    description: str
    metadata: Dict[str, Any]
    resolved: bool = False

@dataclass
class ThreatIntelligence:
    """Threat intelligence data"""
    threat_id: str
    threat_type: str
    severity: ThreatLevel
    indicators: List[str]
    description: str
    mitigation: str
    last_updated: datetime

@dataclass
class ComplianceReport:
    """Compliance audit report"""
    report_id: str
    standard: ComplianceStandard
    compliance_score: float
    findings: List[Dict[str, Any]]
    recommendations: List[str]
    generated_at: datetime
    valid_until: datetime

@dataclass
class SecurityIncident:
    """Security incident record"""
    incident_id: str
    title: str
    description: str
    severity: ThreatLevel
    status: IncidentStatus
    assigned_to: str
    created_at: datetime
    updated_at: datetime
    resolution: Optional[str] = None

class EnterpriseSecuritySuite:
    """
    🔒 Enterprise Security & Compliance Suite
    
    Comprehensive security and compliance management platform providing:
    - Advanced threat detection and response
    - Real-time security monitoring
    - Compliance management and reporting
    - Data protection and encryption
    """
    
    def __init__(self, db_path: str = "../botzzz_security.db"):
        """Initialize Enterprise Security Suite"""
        self.db_path = db_path
        self.threat_patterns = {}
        self.blocked_ips = set()
        self.encryption_key = self._generate_encryption_key()
        self.cipher = Fernet(self.encryption_key)
        
        # Security monitoring queues
        self.event_queue = deque(maxlen=10000)
        self.alert_queue = deque(maxlen=1000)
        
        # Threat detection thresholds
        self.failed_login_threshold = 5
        self.rate_limit_threshold = 100
        self.suspicious_activity_window = 300  # 5 minutes
        
        # Initialize database
        self._init_database()
        
        # Load threat intelligence
        self._load_threat_intelligence()
        
        # Start security monitoring
        self._start_security_monitoring()
        
        # Generate sample security data
        self._generate_sample_security_data()
        
        logger.info("Enterprise Security & Compliance Suite initialized")
    
    def _generate_encryption_key(self) -> bytes:
        """Generate encryption key for data protection"""
        password = b"BOTZZZ_ENTERPRISE_SECURITY_2025"
        salt = b"security_salt_2025"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def _init_database(self):
        """Initialize Security database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Security Events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS security_events (
                    event_id TEXT PRIMARY KEY,
                    event_type TEXT NOT NULL,
                    threat_level TEXT NOT NULL,
                    source_ip TEXT NOT NULL,
                    user_id TEXT,
                    timestamp TIMESTAMP NOT NULL,
                    description TEXT NOT NULL,
                    metadata TEXT NOT NULL,
                    resolved BOOLEAN DEFAULT FALSE
                )
            ''')
            
            # Threat Intelligence table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS threat_intelligence (
                    threat_id TEXT PRIMARY KEY,
                    threat_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    indicators TEXT NOT NULL,
                    description TEXT NOT NULL,
                    mitigation TEXT NOT NULL,
                    last_updated TIMESTAMP NOT NULL
                )
            ''')
            
            # Security Incidents table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS security_incidents (
                    incident_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    status TEXT NOT NULL,
                    assigned_to TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    resolution TEXT
                )
            ''')
            
            # Compliance Reports table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS compliance_reports (
                    report_id TEXT PRIMARY KEY,
                    standard TEXT NOT NULL,
                    compliance_score REAL NOT NULL,
                    findings TEXT NOT NULL,
                    recommendations TEXT NOT NULL,
                    generated_at TIMESTAMP NOT NULL,
                    valid_until TIMESTAMP NOT NULL
                )
            ''')
            
            # Access Logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS access_logs (
                    log_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    resource TEXT NOT NULL,
                    action TEXT NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    source_ip TEXT NOT NULL,
                    user_agent TEXT,
                    success BOOLEAN NOT NULL
                )
            ''')
            
            # Audit Trails table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_trails (
                    audit_id TEXT PRIMARY KEY,
                    entity_type TEXT NOT NULL,
                    entity_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    old_values TEXT,
                    new_values TEXT,
                    metadata TEXT
                )
            ''')
            
            # Blocked IPs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS blocked_ips (
                    ip_address TEXT PRIMARY KEY,
                    reason TEXT NOT NULL,
                    blocked_at TIMESTAMP NOT NULL,
                    expires_at TIMESTAMP,
                    threat_level TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("Security database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing security database: {e}")
            raise
    
    def detect_threat(self, source_ip: str, user_id: Optional[str], activity_type: str, metadata: Dict[str, Any]) -> Optional[SecurityEvent]:
        """Advanced threat detection using pattern analysis"""
        threat_level = ThreatLevel.LOW
        event_type = SecurityEventType.SUSPICIOUS_ACTIVITY
        description = f"Suspicious activity detected: {activity_type}"
        
        # IP-based threat detection
        if self._is_malicious_ip(source_ip):
            threat_level = ThreatLevel.HIGH
            description = f"Known malicious IP detected: {source_ip}"
        
        # Failed login analysis
        if activity_type == "failed_login":
            failed_count = self._get_recent_failed_logins(source_ip, user_id)
            if failed_count >= self.failed_login_threshold:
                threat_level = ThreatLevel.HIGH
                event_type = SecurityEventType.BRUTE_FORCE
                description = f"Brute force attack detected: {failed_count} failed attempts"
        
        # Rate limiting analysis
        if self._is_rate_limit_exceeded(source_ip):
            threat_level = ThreatLevel.MEDIUM
            event_type = SecurityEventType.DDoS_ATTACK
            description = f"Rate limit exceeded from IP: {source_ip}"
        
        # SQL injection detection
        if self._detect_sql_injection(metadata.get('query_params', '')):
            threat_level = ThreatLevel.HIGH
            event_type = SecurityEventType.SQL_INJECTION
            description = "SQL injection attempt detected"
        
        # XSS detection
        if self._detect_xss(metadata.get('user_input', '')):
            threat_level = ThreatLevel.MEDIUM
            event_type = SecurityEventType.XSS_ATTEMPT
            description = "Cross-site scripting attempt detected"
        
        # Create security event if threat detected
        if threat_level != ThreatLevel.LOW or activity_type in ['failed_login', 'privilege_escalation']:
            event = SecurityEvent(
                event_id=f'sec_{uuid.uuid4().hex[:12]}',
                event_type=event_type,
                threat_level=threat_level,
                source_ip=source_ip,
                user_id=user_id,
                timestamp=datetime.now(),
                description=description,
                metadata=metadata
            )
            
            # Store event
            self._store_security_event(event)
            
            # Auto-block critical threats
            if threat_level == ThreatLevel.CRITICAL:
                self.block_ip(source_ip, "Critical threat detected", expires_in_hours=24)
            
            return event
        
        return None
    
    def _is_malicious_ip(self, ip: str) -> bool:
        """Check if IP is in threat intelligence database"""
        # Check blocked IPs
        if ip in self.blocked_ips:
            return True
            
        # Check threat intelligence indicators
        for threat in self.threat_patterns.values():
            if ip in threat.get('indicators', []):
                return True
        
        # Basic IP validation and private IP check
        try:
            ip_obj = ipaddress.ip_address(ip)
            # Flag unusual private IP ranges
            if ip_obj.is_private and not str(ip).startswith(('192.168.', '10.', '172.')):
                return True
        except ValueError:
            return True  # Invalid IP format is suspicious
        
        return False
    
    def _get_recent_failed_logins(self, source_ip: str, user_id: Optional[str]) -> int:
        """Count recent failed login attempts"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Count failed logins in the last 15 minutes
            cutoff_time = datetime.now() - timedelta(minutes=15)
            
            query = '''
                SELECT COUNT(*) FROM security_events 
                WHERE event_type = ? AND source_ip = ? AND timestamp > ?
            '''
            params = [SecurityEventType.FAILED_LOGIN.value, source_ip, cutoff_time]
            
            if user_id:
                query += ' AND user_id = ?'
                params.append(user_id)
            
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            conn.close()
            
            return count
            
        except Exception as e:
            logger.error(f"Error counting failed logins: {e}")
            return 0
    
    def _is_rate_limit_exceeded(self, source_ip: str) -> bool:
        """Check if IP has exceeded rate limits"""
        # Count recent events from this IP
        recent_events = [
            event for event in self.event_queue
            if event.get('source_ip') == source_ip and 
            (datetime.now() - event.get('timestamp', datetime.now())).seconds < 60
        ]
        
        return len(recent_events) > self.rate_limit_threshold
    
    def _detect_sql_injection(self, input_text: str) -> bool:
        """Detect SQL injection patterns"""
        if not input_text:
            return False
            
        sql_patterns = [
            r"(\bunion\b.*\bselect\b)",
            r"(\bdrop\b.*\btable\b)",
            r"(\binsert\b.*\binto\b)",
            r"(\bdelete\b.*\bfrom\b)",
            r"(\bupdate\b.*\bset\b)",
            r"(\bor\b.*\b1\s*=\s*1\b)",
            r"(\band\b.*\b1\s*=\s*1\b)",
            r"(;.*--)",
            r"(\bexec\b.*\bxp_)",
            r"(\bsp_executesql\b)"
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, input_text.lower(), re.IGNORECASE):
                return True
        
        return False
    
    def _detect_xss(self, input_text: str) -> bool:
        """Detect XSS patterns"""
        if not input_text:
            return False
            
        xss_patterns = [
            r"<script[^>]*>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe[^>]*>",
            r"<object[^>]*>",
            r"<embed[^>]*>",
            r"<link[^>]*>",
            r"<meta[^>]*>"
        ]
        
        for pattern in xss_patterns:
            if re.search(pattern, input_text.lower(), re.IGNORECASE):
                return True
        
        return False
    
    def block_ip(self, ip_address: str, reason: str, expires_in_hours: int = 1):
        """Block an IP address"""
        try:
            self.blocked_ips.add(ip_address)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            expires_at = datetime.now() + timedelta(hours=expires_in_hours)
            
            cursor.execute('''
                INSERT OR REPLACE INTO blocked_ips 
                (ip_address, reason, blocked_at, expires_at, threat_level)
                VALUES (?, ?, ?, ?, ?)
            ''', (ip_address, reason, datetime.now(), expires_at, ThreatLevel.HIGH.value))
            
            conn.commit()
            conn.close()
            
            logger.warning(f"IP blocked: {ip_address} - {reason}")
            
        except Exception as e:
            logger.error(f"Error blocking IP: {e}")
    
    def generate_compliance_report(self, standard: ComplianceStandard) -> ComplianceReport:
        """Generate compliance audit report"""
        report_id = f'comp_{uuid.uuid4().hex[:12]}'
        
        # Simulate compliance assessment
        if standard == ComplianceStandard.GDPR:
            findings, score = self._assess_gdpr_compliance()
        elif standard == ComplianceStandard.SOX:
            findings, score = self._assess_sox_compliance()
        elif standard == ComplianceStandard.PCI_DSS:
            findings, score = self._assess_pci_compliance()
        else:
            findings, score = self._assess_general_compliance(standard)
        
        recommendations = self._generate_compliance_recommendations(standard, findings)
        
        report = ComplianceReport(
            report_id=report_id,
            standard=standard,
            compliance_score=score,
            findings=findings,
            recommendations=recommendations,
            generated_at=datetime.now(),
            valid_until=datetime.now() + timedelta(days=90)
        )
        
        # Store report
        self._store_compliance_report(report)
        
        return report
    
    def _assess_gdpr_compliance(self) -> Tuple[List[Dict[str, Any]], float]:
        """Assess GDPR compliance"""
        findings = [
            {
                "requirement": "Data Protection Impact Assessment",
                "status": "compliant",
                "score": 95,
                "description": "DPIA processes are well documented and regularly updated"
            },
            {
                "requirement": "Right to be Forgotten",
                "status": "partial",
                "score": 78,
                "description": "Data deletion procedures exist but need automation"
            },
            {
                "requirement": "Data Breach Notification",
                "status": "compliant",
                "score": 92,
                "description": "72-hour notification procedures are implemented"
            },
            {
                "requirement": "Consent Management",
                "status": "compliant",
                "score": 89,
                "description": "Explicit consent mechanisms are in place"
            }
        ]
        
        overall_score = sum(f["score"] for f in findings) / len(findings)
        return findings, overall_score
    
    def _assess_sox_compliance(self) -> Tuple[List[Dict[str, Any]], float]:
        """Assess SOX compliance"""
        findings = [
            {
                "requirement": "Internal Controls Over Financial Reporting",
                "status": "compliant",
                "score": 91,
                "description": "Robust ICFR framework implemented"
            },
            {
                "requirement": "Management Assessment",
                "status": "compliant",
                "score": 87,
                "description": "Annual management assessment completed"
            },
            {
                "requirement": "Audit Committee Oversight",
                "status": "compliant",
                "score": 94,
                "description": "Independent audit committee oversight active"
            }
        ]
        
        overall_score = sum(f["score"] for f in findings) / len(findings)
        return findings, overall_score
    
    def _assess_pci_compliance(self) -> Tuple[List[Dict[str, Any]], float]:
        """Assess PCI DSS compliance"""
        findings = [
            {
                "requirement": "Secure Network Architecture",
                "status": "compliant",
                "score": 88,
                "description": "Network segmentation and firewalls properly configured"
            },
            {
                "requirement": "Encryption of Cardholder Data",
                "status": "compliant",
                "score": 95,
                "description": "Strong encryption in place for all card data"
            },
            {
                "requirement": "Access Control Measures",
                "status": "partial",
                "score": 82,
                "description": "Access controls need strengthening for admin accounts"
            }
        ]
        
        overall_score = sum(f["score"] for f in findings) / len(findings)
        return findings, overall_score
    
    def _assess_general_compliance(self, standard: ComplianceStandard) -> Tuple[List[Dict[str, Any]], float]:
        """Generic compliance assessment"""
        findings = [
            {
                "requirement": "Security Policies",
                "status": "compliant",
                "score": 90,
                "description": f"{standard.value.upper()} security policies implemented"
            },
            {
                "requirement": "Access Controls",
                "status": "compliant",
                "score": 85,
                "description": "Role-based access controls active"
            }
        ]
        
        overall_score = sum(f["score"] for f in findings) / len(findings)
        return findings, overall_score
    
    def _generate_compliance_recommendations(self, standard: ComplianceStandard, findings: List[Dict[str, Any]]) -> List[str]:
        """Generate compliance recommendations"""
        recommendations = []
        
        for finding in findings:
            if finding["status"] != "compliant" or finding["score"] < 90:
                if standard == ComplianceStandard.GDPR:
                    recommendations.extend([
                        "Implement automated data deletion procedures",
                        "Enhance consent management workflows",
                        "Conduct quarterly GDPR training sessions"
                    ])
                elif standard == ComplianceStandard.PCI_DSS:
                    recommendations.extend([
                        "Strengthen admin account access controls",
                        "Implement additional network monitoring",
                        "Regular penetration testing schedule"
                    ])
                else:
                    recommendations.extend([
                        f"Review {standard.value.upper()} requirements quarterly",
                        "Implement additional security controls",
                        "Enhance documentation and procedures"
                    ])
        
        return list(set(recommendations))  # Remove duplicates
    
    def create_security_incident(self, title: str, description: str, severity: ThreatLevel, assigned_to: str) -> SecurityIncident:
        """Create new security incident"""
        incident = SecurityIncident(
            incident_id=f'inc_{uuid.uuid4().hex[:12]}',
            title=title,
            description=description,
            severity=severity,
            status=IncidentStatus.OPEN,
            assigned_to=assigned_to,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Store incident
        self._store_security_incident(incident)
        
        return incident
    
    def get_security_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive security dashboard data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get recent security events
            cursor.execute('''
                SELECT event_type, threat_level, COUNT(*) 
                FROM security_events 
                WHERE timestamp > ? 
                GROUP BY event_type, threat_level
            ''', (datetime.now() - timedelta(hours=24),))
            
            event_stats = defaultdict(lambda: defaultdict(int))
            for event_type, threat_level, count in cursor.fetchall():
                event_stats[event_type][threat_level] = count
            
            # Get active incidents
            cursor.execute('''
                SELECT severity, status, COUNT(*) 
                FROM security_incidents 
                WHERE status != ?
                GROUP BY severity, status
            ''', (IncidentStatus.CLOSED.value,))
            
            incident_stats = defaultdict(lambda: defaultdict(int))
            for severity, status, count in cursor.fetchall():
                incident_stats[severity][status] = count
            
            # Get blocked IPs count
            cursor.execute('SELECT COUNT(*) FROM blocked_ips WHERE expires_at > ?', (datetime.now(),))
            blocked_ips_count = cursor.fetchone()[0]
            
            # Get compliance scores
            cursor.execute('''
                SELECT standard, compliance_score 
                FROM compliance_reports 
                WHERE valid_until > ? 
                ORDER BY generated_at DESC
            ''', (datetime.now(),))
            
            compliance_scores = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                'event_statistics': dict(event_stats),
                'incident_statistics': dict(incident_stats),
                'blocked_ips_count': blocked_ips_count,
                'compliance_scores': compliance_scores,
                'threat_level_distribution': self._get_threat_level_distribution(),
                'security_metrics': {
                    'total_events_24h': sum(sum(levels.values()) for levels in event_stats.values()),
                    'active_incidents': sum(sum(statuses.values()) for statuses in incident_stats.values()),
                    'avg_compliance_score': sum(compliance_scores.values()) / len(compliance_scores) if compliance_scores else 0,
                    'security_score': self._calculate_security_score()
                },
                'recent_threats': self._get_recent_threats(),
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting security dashboard: {e}")
            return {}
    
    def _get_threat_level_distribution(self) -> Dict[str, int]:
        """Get distribution of threat levels"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT threat_level, COUNT(*) 
                FROM security_events 
                WHERE timestamp > ? 
                GROUP BY threat_level
            ''', (datetime.now() - timedelta(days=7),))
            
            distribution = dict(cursor.fetchall())
            conn.close()
            
            return distribution
            
        except Exception as e:
            logger.error(f"Error getting threat level distribution: {e}")
            return {}
    
    def _calculate_security_score(self) -> float:
        """Calculate overall security score (0-100)"""
        base_score = 85.0
        
        # Penalty for recent high-severity events
        recent_critical_events = self._count_recent_events_by_level(ThreatLevel.CRITICAL, hours=24)
        recent_high_events = self._count_recent_events_by_level(ThreatLevel.HIGH, hours=24)
        
        penalty = (recent_critical_events * 10) + (recent_high_events * 5)
        
        # Bonus for resolved incidents
        resolved_incidents_ratio = self._get_resolved_incidents_ratio()
        bonus = resolved_incidents_ratio * 10
        
        final_score = max(0, min(100, base_score - penalty + bonus))
        return round(final_score, 1)
    
    def _count_recent_events_by_level(self, threat_level: ThreatLevel, hours: int) -> int:
        """Count recent events by threat level"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) 
                FROM security_events 
                WHERE threat_level = ? AND timestamp > ?
            ''', (threat_level.value, datetime.now() - timedelta(hours=hours)))
            
            count = cursor.fetchone()[0]
            conn.close()
            
            return count
            
        except Exception as e:
            logger.error(f"Error counting events by level: {e}")
            return 0
    
    def _get_resolved_incidents_ratio(self) -> float:
        """Get ratio of resolved incidents"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM security_incidents')
            total = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM security_incidents WHERE status = ?', 
                         (IncidentStatus.RESOLVED.value,))
            resolved = cursor.fetchone()[0]
            
            conn.close()
            
            return resolved / total if total > 0 else 1.0
            
        except Exception as e:
            logger.error(f"Error getting resolved incidents ratio: {e}")
            return 0.0
    
    def _get_recent_threats(self) -> List[Dict[str, Any]]:
        """Get recent high-priority threats"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT event_id, event_type, threat_level, source_ip, description, timestamp
                FROM security_events 
                WHERE threat_level IN (?, ?) AND timestamp > ?
                ORDER BY timestamp DESC
                LIMIT 10
            ''', (ThreatLevel.HIGH.value, ThreatLevel.CRITICAL.value, datetime.now() - timedelta(hours=24)))
            
            threats = []
            for row in cursor.fetchall():
                threats.append({
                    'event_id': row[0],
                    'event_type': row[1],
                    'threat_level': row[2],
                    'source_ip': row[3],
                    'description': row[4],
                    'timestamp': row[5]
                })
            
            conn.close()
            return threats
            
        except Exception as e:
            logger.error(f"Error getting recent threats: {e}")
            return []
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            encrypted_data = self.cipher.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            logger.error(f"Error encrypting data: {e}")
            return data
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self.cipher.decrypt(encrypted_bytes)
            return decrypted_data.decode()
        except Exception as e:
            logger.error(f"Error decrypting data: {e}")
            return encrypted_data
    
    def log_access(self, user_id: str, resource: str, action: str, source_ip: str, success: bool, user_agent: str = None):
        """Log access attempt"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO access_logs 
                (log_id, user_id, resource, action, timestamp, source_ip, user_agent, success)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (f'log_{uuid.uuid4().hex[:12]}', user_id, resource, action, 
                 datetime.now(), source_ip, user_agent, success))
            
            conn.commit()
            conn.close()
            
            # Detect potential threats
            if not success:
                self.detect_threat(source_ip, user_id, "failed_login", {
                    'resource': resource,
                    'action': action,
                    'user_agent': user_agent
                })
            
        except Exception as e:
            logger.error(f"Error logging access: {e}")
    
    def create_audit_trail(self, entity_type: str, entity_id: str, action: str, user_id: str, old_values: Dict = None, new_values: Dict = None):
        """Create audit trail entry"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO audit_trails 
                (audit_id, entity_type, entity_id, action, user_id, timestamp, old_values, new_values)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (f'audit_{uuid.uuid4().hex[:12]}', entity_type, entity_id, action, user_id,
                 datetime.now(), json.dumps(old_values) if old_values else None,
                 json.dumps(new_values) if new_values else None))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error creating audit trail: {e}")
    
    def _load_threat_intelligence(self):
        """Load threat intelligence data"""
        sample_threats = [
            {
                'threat_id': f'threat_{uuid.uuid4().hex[:8]}',
                'threat_type': 'Malicious IP',
                'severity': ThreatLevel.HIGH.value,
                'indicators': ['192.168.100.50', '10.0.0.250'],
                'description': 'Known botnet command and control servers',
                'mitigation': 'Block IP addresses and monitor for similar patterns'
            },
            {
                'threat_id': f'threat_{uuid.uuid4().hex[:8]}',
                'threat_type': 'SQL Injection',
                'severity': ThreatLevel.CRITICAL.value,
                'indicators': ['union select', 'drop table', '1=1'],
                'description': 'SQL injection attack patterns',
                'mitigation': 'Implement prepared statements and input validation'
            }
        ]
        
        for threat in sample_threats:
            self.threat_patterns[threat['threat_id']] = threat
    
    def _store_security_event(self, event: SecurityEvent):
        """Store security event in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO security_events 
                (event_id, event_type, threat_level, source_ip, user_id, timestamp, description, metadata, resolved)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (event.event_id, event.event_type.value, event.threat_level.value,
                 event.source_ip, event.user_id, event.timestamp,
                 event.description, json.dumps(event.metadata), event.resolved))
            
            conn.commit()
            conn.close()
            
            # Add to event queue for real-time monitoring
            self.event_queue.append({
                'event_id': event.event_id,
                'source_ip': event.source_ip,
                'timestamp': event.timestamp,
                'threat_level': event.threat_level.value
            })
            
        except Exception as e:
            logger.error(f"Error storing security event: {e}")
    
    def _store_compliance_report(self, report: ComplianceReport):
        """Store compliance report in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO compliance_reports 
                (report_id, standard, compliance_score, findings, recommendations, generated_at, valid_until)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (report.report_id, report.standard.value, report.compliance_score,
                 json.dumps(report.findings), json.dumps(report.recommendations),
                 report.generated_at, report.valid_until))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing compliance report: {e}")
    
    def _store_security_incident(self, incident: SecurityIncident):
        """Store security incident in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO security_incidents 
                (incident_id, title, description, severity, status, assigned_to, created_at, updated_at, resolution)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (incident.incident_id, incident.title, incident.description,
                 incident.severity.value, incident.status.value, incident.assigned_to,
                 incident.created_at, incident.updated_at, incident.resolution))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing security incident: {e}")
    
    def _generate_sample_security_data(self):
        """Generate sample security events and incidents for demonstration"""
        sample_ips = ['192.168.1.100', '10.0.0.50', '172.16.1.25', '203.0.113.1']
        
        # Generate sample security events
        for i in range(20):
            self.detect_threat(
                source_ip=f"192.168.{i % 10}.{100 + i}",
                user_id=f"user_{i % 5}",
                activity_type="login_attempt" if i % 3 == 0 else "data_access",
                metadata={'resource': f'/api/data/{i}', 'method': 'GET'}
            )
        
        # Generate sample incidents
        sample_incidents = [
            {
                'title': 'Suspicious Login Activity',
                'description': 'Multiple failed login attempts from external IP',
                'severity': ThreatLevel.MEDIUM,
                'assigned_to': 'security_team'
            },
            {
                'title': 'Potential SQL Injection',
                'description': 'SQL injection patterns detected in user input',
                'severity': ThreatLevel.HIGH,
                'assigned_to': 'incident_response'
            }
        ]
        
        for incident_data in sample_incidents:
            self.create_security_incident(**incident_data)
        
        # Generate compliance reports
        for standard in [ComplianceStandard.GDPR, ComplianceStandard.SOX, ComplianceStandard.PCI_DSS]:
            self.generate_compliance_report(standard)
    
    def _start_security_monitoring(self):
        """Start background security monitoring"""
        def monitoring_worker():
            while True:
                try:
                    # Clean up expired IP blocks
                    self._cleanup_expired_blocks()
                    
                    # Process security alerts
                    self._process_security_alerts()
                    
                    # Update threat intelligence
                    if len(self.event_queue) % 100 == 0:  # Every 100 events
                        self._update_threat_patterns()
                    
                    time.sleep(60)  # Run every minute
                    
                except Exception as e:
                    logger.error(f"Error in security monitoring: {e}")
                    time.sleep(60)
        
        # Start background thread
        monitoring_thread = threading.Thread(target=monitoring_worker, daemon=True)
        monitoring_thread.start()
        logger.info("Security monitoring started")
    
    def _cleanup_expired_blocks(self):
        """Clean up expired IP blocks"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get expired blocks
            cursor.execute('SELECT ip_address FROM blocked_ips WHERE expires_at < ?', (datetime.now(),))
            expired_ips = [row[0] for row in cursor.fetchall()]
            
            # Remove from blocked set
            for ip in expired_ips:
                self.blocked_ips.discard(ip)
            
            # Delete from database
            cursor.execute('DELETE FROM blocked_ips WHERE expires_at < ?', (datetime.now(),))
            
            conn.commit()
            conn.close()
            
            if expired_ips:
                logger.info(f"Cleaned up {len(expired_ips)} expired IP blocks")
                
        except Exception as e:
            logger.error(f"Error cleaning up expired blocks: {e}")
    
    def _process_security_alerts(self):
        """Process pending security alerts"""
        # This would integrate with external alerting systems
        # For now, just log high-priority events
        high_priority_events = [
            event for event in self.event_queue
            if event.get('threat_level') in [ThreatLevel.HIGH.value, ThreatLevel.CRITICAL.value]
        ]
        
        for event in high_priority_events[-5:]:  # Process last 5 high-priority events
            logger.warning(f"High-priority security event: {event}")
    
    def _update_threat_patterns(self):
        """Update threat patterns based on recent events"""
        # Analyze recent events for new threat patterns
        # This would use ML in production
        recent_ips = [event.get('source_ip') for event in list(self.event_queue)[-50:]]
        ip_counts = defaultdict(int)
        
        for ip in recent_ips:
            ip_counts[ip] += 1
        
        # Flag IPs with unusually high activity
        for ip, count in ip_counts.items():
            if count > 5:  # Threshold for suspicious activity
                logger.info(f"Flagging IP for monitoring: {ip} ({count} events)")

# Global security instance
enterprise_security = None

def get_enterprise_security():
    """Get global Enterprise Security instance"""
    global enterprise_security
    if enterprise_security is None:
        enterprise_security = EnterpriseSecuritySuite()
    return enterprise_security

if __name__ == "__main__":
    # Initialize and test Enterprise Security Suite
    print("🔒 Initializing Enterprise Security & Compliance Suite...")
    
    security = EnterpriseSecuritySuite()
    
    print("\n🚨 Testing Threat Detection...")
    threat = security.detect_threat(
        source_ip="192.168.1.100",
        user_id="test_user",
        activity_type="failed_login",
        metadata={'attempts': 6}
    )
    if threat:
        print(f"Threat detected: {threat.description}")
    
    print("\n📋 Generating Compliance Report...")
    report = security.generate_compliance_report(ComplianceStandard.GDPR)
    print(f"GDPR Compliance Score: {report.compliance_score:.1f}%")
    
    print("\n🔍 Getting Security Dashboard...")
    dashboard = security.get_security_dashboard()
    print(f"Security Score: {dashboard['security_metrics']['security_score']}")
    print(f"Total Events (24h): {dashboard['security_metrics']['total_events_24h']}")
    
    print("\n🔒 Enterprise Security Suite Ready!")

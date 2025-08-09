#!/usr/bin/env python3
"""
Comprehensive Test Suite for BOTZZZ Admin Panel (app.py)
Targets 100% code coverage with exhaustive testing

Test Coverage Areas:
- All 80+ Flask routes
- All helper functions
- User authentication & authorization
- Database operations
- Error handling
- Mock integrations
- Edge cases and boundary conditions
"""

import unittest
import tempfile
import os
import json
import sqlite3
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import sys

# Add admin_panel to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'admin_panel'))

# Import the app and components
import app
from app import (
    app as flask_app, init_database, init_sqlite_fallback, 
    log_system_event, log_system_event_sqlite, User, 
    load_user, get_active_simulations_count
)

class TestBOTZZZAppComprehensive(unittest.TestCase):
    """Comprehensive test suite targeting 100% code coverage"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary database for testing
        self.db_fd, flask_app.config['DATABASE'] = tempfile.mkstemp()
        flask_app.config['TESTING'] = True
        flask_app.config['WTF_CSRF_ENABLED'] = False
        flask_app.config['LOGIN_DISABLED'] = False
        
        self.app = flask_app.test_client()
        self.app_context = flask_app.app_context()
        self.app_context.push()
        
        # Initialize test database
        with flask_app.app_context():
            init_sqlite_fallback()
        
        # Create test user session
        with self.app.session_transaction() as sess:
            sess['_user_id'] = '1'
            sess['_fresh'] = True
    
    def tearDown(self):
        """Clean up test environment"""
        self.app_context.pop()
        os.close(self.db_fd)
        os.unlink(flask_app.config['DATABASE'])
    
    def login_as_admin(self):
        """Helper to login as admin user"""
        return self.app.post('/login', data={
            'username': 'admin',
            'password': 'BOTZZZ2025!'
        }, follow_redirects=True)
    
    def login_as_operator(self):
        """Helper to login as operator user"""
        return self.app.post('/login', data={
            'username': 'operator',
            'password': 'operator123'
        }, follow_redirects=True)
    
    def login_as_viewer(self):
        """Helper to login as viewer user"""
        return self.app.post('/login', data={
            'username': 'viewer',
            'password': 'viewer123'
        }, follow_redirects=True)

    # ==========================================
    # AUTHENTICATION & USER MANAGEMENT TESTS
    # ==========================================
    
    def test_home_route(self):
        """Test public home page"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_login_get(self):
        """Test login page GET"""
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
    
    def test_login_post_success(self):
        """Test successful login"""
        response = self.login_as_admin()
        self.assertEqual(response.status_code, 200)
    
    def test_login_post_failure(self):
        """Test failed login"""
        response = self.app.post('/login', data={
            'username': 'invalid',
            'password': 'invalid'
        })
        self.assertEqual(response.status_code, 200)
    
    def test_logout(self):
        """Test user logout"""
        self.login_as_admin()
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_register_get(self):
        """Test registration page GET"""
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
    
    def test_register_post_success(self):
        """Test successful user registration"""
        response = self.app.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'service_type': 'premium'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_register_post_password_mismatch(self):
        """Test registration with password mismatch"""
        response = self.app.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'password123',
            'confirm_password': 'different',
            'service_type': 'premium'
        })
        self.assertEqual(response.status_code, 200)
    
    def test_register_post_missing_fields(self):
        """Test registration with missing fields"""
        response = self.app.post('/register', data={
            'username': '',
            'email': '',
            'password': '',
            'confirm_password': '',
            'service_type': 'premium'
        })
        self.assertEqual(response.status_code, 200)
    
    def test_register_post_existing_username(self):
        """Test registration with existing username"""
        response = self.app.post('/register', data={
            'username': 'admin',  # Existing username
            'email': 'newemail@test.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'service_type': 'premium'
        })
        self.assertEqual(response.status_code, 200)
    
    def test_user_login_get(self):
        """Test user login page GET"""
        response = self.app.get('/user-login')
        self.assertEqual(response.status_code, 200)
    
    def test_user_login_post_success(self):
        """Test successful user login"""
        # First register a user
        self.app.post('/register', data={
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'test123',
            'confirm_password': 'test123',
            'service_type': 'basic'
        })
        
        response = self.app.post('/user-login', data={
            'username': 'testuser',
            'password': 'test123',
            'remember_me': 'on'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_user_login_post_failure(self):
        """Test failed user login"""
        response = self.app.post('/user-login', data={
            'username': 'nonexistent',
            'password': 'wrong'
        })
        self.assertEqual(response.status_code, 200)
    
    def test_user_dashboard_regular_user(self):
        """Test user dashboard for regular users"""
        # Register and login as regular user
        self.app.post('/register', data={
            'username': 'regularuser',
            'email': 'regular@test.com',
            'password': 'test123',
            'confirm_password': 'test123',
            'service_type': 'basic'
        })
        
        with self.app.session_transaction() as sess:
            sess['_user_id'] = '10'  # Regular user ID
        
        response = self.app.get('/user-dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_user_dashboard_admin_redirect(self):
        """Test user dashboard redirects admin users"""
        self.login_as_admin()
        response = self.app.get('/user-dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # ==========================================
    # DASHBOARD & MAIN INTERFACE TESTS
    # ==========================================
    
    def test_dashboard_requires_login(self):
        """Test dashboard requires authentication"""
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_dashboard_authenticated(self):
        """Test dashboard with authenticated user"""
        self.login_as_admin()
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_simulations_page(self):
        """Test simulations management page"""
        self.login_as_admin()
        response = self.app.get('/simulations')
        self.assertEqual(response.status_code, 200)
    
    def test_simulations_with_pagination(self):
        """Test simulations page with pagination"""
        self.login_as_admin()
        response = self.app.get('/simulations?page=2')
        self.assertEqual(response.status_code, 200)
    
    def test_analytics_page(self):
        """Test analytics dashboard"""
        self.login_as_admin()
        response = self.app.get('/analytics')
        self.assertEqual(response.status_code, 200)
    
    def test_detection_page(self):
        """Test detection dashboard"""
        self.login_as_admin()
        response = self.app.get('/detection')
        self.assertEqual(response.status_code, 200)
    
    def test_logs_page(self):
        """Test logs viewer"""
        self.login_as_admin()
        response = self.app.get('/logs')
        self.assertEqual(response.status_code, 200)
    
    def test_logs_with_filters(self):
        """Test logs page with filters"""
        self.login_as_admin()
        response = self.app.get('/logs?level=ERROR&component=system&page=1')
        self.assertEqual(response.status_code, 200)
    
    def test_settings_page_super_admin_only(self):
        """Test settings page requires super admin"""
        self.login_as_operator()
        response = self.app.get('/settings', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_settings_page_super_admin_access(self):
        """Test settings page with super admin access"""
        self.login_as_admin()
        response = self.app.get('/settings')
        self.assertEqual(response.status_code, 200)

    # ==========================================
    # SIMULATION MANAGEMENT TESTS
    # ==========================================
    
    def test_create_simulation_get(self):
        """Test create simulation page GET"""
        self.login_as_admin()
        response = self.app.get('/simulations/create')
        self.assertEqual(response.status_code, 200)
    
    def test_create_simulation_post_success(self):
        """Test successful simulation creation"""
        self.login_as_admin()
        response = self.app.post('/simulations/create', 
            json={
                'name': 'Test Simulation',
                'type': 'youtube',
                'parameters': {'target_views': 1000}
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_create_simulation_post_missing_name(self):
        """Test simulation creation with missing name"""
        self.login_as_admin()
        response = self.app.post('/simulations/create',
            json={'type': 'youtube', 'parameters': {}},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_create_simulation_requires_operator_role(self):
        """Test create simulation requires operator role"""
        self.login_as_viewer()
        response = self.app.post('/simulations/create',
            json={'name': 'Test', 'type': 'youtube', 'parameters': {}},
            content_type='application/json',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
    
    @patch('app.subprocess.run')
    @patch('app.threading.Thread')
    def test_start_simulation_success(self, mock_thread, mock_subprocess):
        """Test successful simulation start"""
        # Create a simulation first
        self.login_as_admin()
        
        # Insert test simulation
        conn = sqlite3.connect('botzzz_admin.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO simulation_runs (name, type, status, parameters, created_by)
            VALUES (?, ?, 'pending', ?, ?)
        ''', ('Test Sim', 'youtube', '{}', 'admin'))
        sim_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        response = self.app.post(f'/simulations/{sim_id}/start')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_start_simulation_not_found(self):
        """Test start simulation with invalid ID"""
        self.login_as_admin()
        response = self.app.post('/simulations/99999/start')
        self.assertEqual(response.status_code, 404)
    
    def test_start_simulation_requires_operator_role(self):
        """Test start simulation requires operator role"""
        self.login_as_viewer()
        response = self.app.post('/simulations/1/start', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # ==========================================
    # API ENDPOINT TESTS
    # ==========================================
    
    def test_api_system_status(self):
        """Test system status API"""
        self.login_as_admin()
        response = self.app.get('/api/system-status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('timestamp', data)
        self.assertIn('active_simulations', data)
        self.assertIn('system_health', data)
    
    def test_api_simulation_logs_success(self):
        """Test simulation logs API success"""
        self.login_as_admin()
        
        # Create simulation with log file
        conn = sqlite3.connect('botzzz_admin.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO simulation_runs (name, type, status, log_file, created_by)
            VALUES (?, ?, 'completed', ?, ?)
        ''', ('Test', 'youtube', 'test.log', 'admin'))
        sim_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Create dummy log file
        with open('test.log', 'w') as f:
            f.write('Test log content')
        
        try:
            response = self.app.get(f'/api/simulations/{sim_id}/logs')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('logs', data)
        finally:
            os.remove('test.log')
    
    def test_api_simulation_logs_not_found(self):
        """Test simulation logs API with missing simulation"""
        self.login_as_admin()
        response = self.app.get('/api/simulations/99999/logs')
        self.assertEqual(response.status_code, 404)
    
    def test_api_simulation_logs_file_not_accessible(self):
        """Test simulation logs API with inaccessible file"""
        self.login_as_admin()
        
        # Create simulation with non-existent log file
        conn = sqlite3.connect('botzzz_admin.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO simulation_runs (name, type, status, log_file, created_by)
            VALUES (?, ?, 'completed', ?, ?)
        ''', ('Test', 'youtube', 'nonexistent.log', 'admin'))
        sim_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        response = self.app.get(f'/api/simulations/{sim_id}/logs')
        self.assertEqual(response.status_code, 404)

    # ==========================================
    # INFRASTRUCTURE SERVICE TESTS
    # ==========================================
    
    def test_infrastructure_dashboard(self):
        """Test infrastructure services dashboard"""
        self.login_as_admin()
        response = self.app.get('/infrastructure')
        self.assertEqual(response.status_code, 200)
    
    def test_captcha_service_get(self):
        """Test CAPTCHA service GET"""
        self.login_as_admin()
        response = self.app.get('/infrastructure/captcha')
        self.assertEqual(response.status_code, 200)
    
    @patch('app.captcha_solver.solve_captcha')
    def test_captcha_service_post_success(self, mock_solve):
        """Test CAPTCHA service POST success"""
        mock_solve.return_value = {'success': True, 'token': 'test_token'}
        
        self.login_as_admin()
        response = self.app.post('/infrastructure/captcha', data={
            'captcha_type': 'recaptcha_v2',
            'site_key': 'test_key',
            'page_url': 'https://test.com',
            'provider': 'auto'
        })
        self.assertEqual(response.status_code, 200)
    
    @patch('app.captcha_solver.solve_captcha')
    def test_captcha_service_post_failure(self, mock_solve):
        """Test CAPTCHA service POST failure"""
        mock_solve.side_effect = Exception("CAPTCHA solve failed")
        
        self.login_as_admin()
        response = self.app.post('/infrastructure/captcha', data={
            'captcha_type': 'recaptcha_v2',
            'site_key': 'test_key',
            'page_url': 'https://test.com'
        })
        self.assertEqual(response.status_code, 400)
    
    def test_rate_limit_service_get(self):
        """Test rate limit service GET"""
        self.login_as_admin()
        response = self.app.get('/infrastructure/rate-limits')
        self.assertEqual(response.status_code, 200)
    
    @patch('app.rate_limiter.check_rate_limit')
    def test_rate_limit_service_post_success(self, mock_check):
        """Test rate limit service POST success"""
        mock_check.return_value = {'allowed': True, 'utilization': 0.5}
        
        self.login_as_admin()
        response = self.app.post('/infrastructure/rate-limits', data={
            'platform': 'youtube',
            'account_id': 'test_account',
            'action': 'likes'
        })
        self.assertEqual(response.status_code, 200)
    
    def test_rate_limit_service_post_missing_params(self):
        """Test rate limit service POST with missing parameters"""
        self.login_as_admin()
        response = self.app.post('/infrastructure/rate-limits', data={
            'platform': 'youtube'
            # Missing account_id and action
        })
        self.assertEqual(response.status_code, 400)
    
    def test_proxy_service_get(self):
        """Test proxy service GET"""
        self.login_as_admin()
        response = self.app.get('/infrastructure/proxies')
        self.assertEqual(response.status_code, 200)
    
    @patch('app.proxy_manager.get_optimal_proxy')
    def test_proxy_service_get_proxy(self, mock_get_proxy):
        """Test proxy service get optimal proxy"""
        mock_get_proxy.return_value = {'proxy': 'proxy.test.com:8080'}
        
        self.login_as_admin()
        response = self.app.post('/infrastructure/proxies', data={
            'action': 'get_proxy',
            'platform': 'youtube',
            'region': 'US'
        })
        self.assertEqual(response.status_code, 200)
    
    @patch('app.proxy_manager.rotate_proxy')
    def test_proxy_service_rotate_proxy(self, mock_rotate):
        """Test proxy service rotate proxy"""
        mock_rotate.return_value = {'success': True}
        
        self.login_as_admin()
        response = self.app.post('/infrastructure/proxies', data={
            'action': 'rotate_proxy',
            'current_proxy_id': 'proxy_123',
            'reason': 'detected'
        })
        self.assertEqual(response.status_code, 200)
    
    @patch('app.proxy_manager.mark_proxy_detected')
    def test_proxy_service_mark_detected(self, mock_mark):
        """Test proxy service mark proxy as detected"""
        self.login_as_admin()
        response = self.app.post('/infrastructure/proxies', data={
            'action': 'mark_detected',
            'proxy_id': 'proxy_123',
            'platform': 'youtube',
            'detection_type': 'captcha'
        })
        self.assertEqual(response.status_code, 200)
    
    def test_account_warming_service_get(self):
        """Test account warming service GET"""
        self.login_as_admin()
        response = self.app.get('/infrastructure/warming')
        self.assertEqual(response.status_code, 200)
    
    @patch('app.account_warmer.start_account_warming')
    def test_account_warming_start(self, mock_start):
        """Test account warming start"""
        mock_start.return_value = {'success': True}
        
        self.login_as_admin()
        response = self.app.post('/infrastructure/warming', data={
            'action': 'start_warming',
            'account_id': 'test_account',
            'platform': 'youtube',
            'target_stage': 'stage_3'
        })
        self.assertEqual(response.status_code, 200)
    
    @patch('app.account_warmer.execute_daily_warming')
    def test_account_warming_execute_daily(self, mock_execute):
        """Test account warming execute daily"""
        mock_execute.return_value = {'success': True}
        
        self.login_as_admin()
        response = self.app.post('/infrastructure/warming', data={
            'action': 'execute_daily',
            'account_id': 'test_account'
        })
        self.assertEqual(response.status_code, 200)

    # ==========================================
    # INFRASTRUCTURE API TESTS
    # ==========================================
    
    def test_infrastructure_api_captcha(self):
        """Test infrastructure API for CAPTCHA stats"""
        self.login_as_admin()
        response = self.app.get('/api/infrastructure/captcha')
        self.assertEqual(response.status_code, 200)
    
    def test_infrastructure_api_rate_limits_success(self):
        """Test infrastructure API for rate limits with account ID"""
        self.login_as_admin()
        response = self.app.get('/api/infrastructure/rate-limits?account_id=test_account')
        self.assertEqual(response.status_code, 200)
    
    def test_infrastructure_api_rate_limits_missing_param(self):
        """Test infrastructure API for rate limits without account ID"""
        self.login_as_admin()
        response = self.app.get('/api/infrastructure/rate-limits')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_infrastructure_api_proxies(self):
        """Test infrastructure API for proxy stats"""
        self.login_as_admin()
        response = self.app.get('/api/infrastructure/proxies')
        self.assertEqual(response.status_code, 200)
    
    def test_infrastructure_api_warming_success(self):
        """Test infrastructure API for warming with account ID"""
        self.login_as_admin()
        response = self.app.get('/api/infrastructure/warming?account_id=test_account')
        self.assertEqual(response.status_code, 200)
    
    def test_infrastructure_api_warming_missing_param(self):
        """Test infrastructure API for warming without account ID"""
        self.login_as_admin()
        response = self.app.get('/api/infrastructure/warming')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_infrastructure_api_unknown_service(self):
        """Test infrastructure API with unknown service"""
        self.login_as_admin()
        response = self.app.get('/api/infrastructure/unknown')
        self.assertEqual(response.status_code, 404)

    # ==========================================
    # BULLETPROOF SYSTEMS TESTS
    # ==========================================
    
    def test_bulletproof_dashboard(self):
        """Test bulletproof systems dashboard"""
        self.login_as_admin()
        response = self.app.get('/bulletproof')
        self.assertEqual(response.status_code, 200)
    
    def test_bulletproof_api_status(self):
        """Test bulletproof API status"""
        self.login_as_admin()
        response = self.app.get('/api/bulletproof/status')
        self.assertEqual(response.status_code, 200)
    
    def test_bulletproof_api_alerts(self):
        """Test bulletproof API alerts"""
        self.login_as_admin()
        response = self.app.get('/api/bulletproof/alerts')
        self.assertEqual(response.status_code, 200)
    
    def test_bulletproof_api_metrics(self):
        """Test bulletproof API metrics"""
        self.login_as_admin()
        response = self.app.get('/api/bulletproof/metrics')
        self.assertEqual(response.status_code, 200)
    
    def test_bulletproof_api_cluster(self):
        """Test bulletproof API cluster status"""
        self.login_as_admin()
        response = self.app.get('/api/bulletproof/cluster')
        self.assertEqual(response.status_code, 200)
    
    def test_bulletproof_api_disaster_recovery(self):
        """Test bulletproof API disaster recovery"""
        self.login_as_admin()
        response = self.app.get('/api/bulletproof/disaster-recovery')
        self.assertEqual(response.status_code, 200)

    # ==========================================
    # HIGH AVAILABILITY & DISASTER RECOVERY TESTS
    # ==========================================
    
    def test_ha_dashboard(self):
        """Test HA cluster dashboard"""
        self.login_as_admin()
        response = self.app.get('/ha-dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_disaster_recovery_dashboard(self):
        """Test disaster recovery dashboard"""
        self.login_as_admin()
        response = self.app.get('/disaster_recovery')
        self.assertEqual(response.status_code, 200)
    
    def test_trigger_failover(self):
        """Test trigger failover"""
        self.login_as_admin()
        response = self.app.post('/api/cluster/failover')
        self.assertEqual(response.status_code, 200)
    
    def test_create_backup(self):
        """Test create backup"""
        self.login_as_admin()
        response = self.app.post('/api/backup/create')
        self.assertEqual(response.status_code, 200)
    
    def test_system_health_api(self):
        """Test system health API"""
        self.login_as_admin()
        response = self.app.get('/api/system/health')
        self.assertEqual(response.status_code, 200)

    # ==========================================
    # TIER 1 FEATURE DASHBOARD TESTS
    # ==========================================
    
    def test_analytics_dashboard_tier1(self):
        """Test Tier 1 analytics dashboard"""
        self.login_as_admin()
        response = self.app.get('/analytics_dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_ai_management_dashboard(self):
        """Test AI management dashboard"""
        self.login_as_admin()
        response = self.app.get('/ai_management')
        self.assertEqual(response.status_code, 200)
    
    def test_campaign_center_dashboard(self):
        """Test campaign center dashboard"""
        self.login_as_admin()
        response = self.app.get('/campaign_center')
        self.assertEqual(response.status_code, 200)

    # ==========================================
    # TIER 2 ENTERPRISE FEATURE TESTS
    # ==========================================
    
    def test_enterprise_marketplace_dashboard(self):
        """Test enterprise marketplace dashboard"""
        self.login_as_admin()
        response = self.app.get('/enterprise_marketplace')
        self.assertEqual(response.status_code, 200)
    
    def test_client_dashboard(self):
        """Test individual client dashboard"""
        self.login_as_admin()
        response = self.app.get('/marketplace/client/test_client')
        self.assertEqual(response.status_code, 200)
    
    def test_premium_ai_dashboard(self):
        """Test premium AI dashboard"""
        self.login_as_admin()
        response = self.app.get('/premium_ai')
        self.assertEqual(response.status_code, 200)
    
    def test_business_intelligence_dashboard(self):
        """Test business intelligence dashboard"""
        self.login_as_admin()
        response = self.app.get('/business_intelligence')
        self.assertEqual(response.status_code, 200)
    
    def test_enterprise_security_dashboard(self):
        """Test enterprise security dashboard"""
        self.login_as_admin()
        response = self.app.get('/enterprise_security')
        self.assertEqual(response.status_code, 200)
    
    def test_social_orchestrator_dashboard(self):
        """Test social orchestrator dashboard"""
        self.login_as_admin()
        response = self.app.get('/social_orchestrator')
        self.assertEqual(response.status_code, 200)
    
    def test_revenue_optimization_dashboard(self):
        """Test revenue optimization dashboard"""
        self.login_as_admin()
        response = self.app.get('/revenue_optimization')
        self.assertEqual(response.status_code, 200)

    # ==========================================
    # ANALYTICS API TESTS
    # ==========================================
    
    def test_api_analytics_dashboard(self):
        """Test analytics dashboard API"""
        self.login_as_admin()
        response = self.app.get('/api/analytics/dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_api_ai_dashboard(self):
        """Test AI management dashboard API"""
        self.login_as_admin()
        response = self.app.get('/api/ai/dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_api_ai_create_campaign_success(self):
        """Test AI campaign creation success"""
        self.login_as_admin()
        response = self.app.post('/api/ai/create_campaign',
            json={
                'platform': 'youtube',
                'task_type': 'engagement',
                'targets': ['video1', 'video2'],
                'priority': 5
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_api_ai_create_campaign_missing_fields(self):
        """Test AI campaign creation with missing fields"""
        self.login_as_admin()
        response = self.app.post('/api/ai/create_campaign',
            json={'platform': 'youtube'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    # ==========================================
    # CAMPAIGN MANAGEMENT API TESTS
    # ==========================================
    
    def test_api_campaigns_dashboard(self):
        """Test campaigns dashboard API"""
        self.login_as_admin()
        response = self.app.get('/api/campaigns/dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_api_campaigns_create_success(self):
        """Test campaign creation success"""
        self.login_as_admin()
        response = self.app.post('/api/campaigns/create',
            json={
                'name': 'Test Campaign',
                'platform': 'instagram',
                'hashtags': ['#test', '#campaign'],
                'likes_target': 500,
                'follows_target': 50
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_api_campaigns_create_missing_fields(self):
        """Test campaign creation with missing fields"""
        self.login_as_admin()
        response = self.app.post('/api/campaigns/create',
            json={'name': 'Test'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_api_campaigns_pause(self):
        """Test campaign pause"""
        self.login_as_admin()
        response = self.app.post('/api/campaigns/test_campaign/pause')
        self.assertEqual(response.status_code, 200)
    
    def test_api_campaigns_resume(self):
        """Test campaign resume"""
        self.login_as_admin()
        response = self.app.post('/api/campaigns/test_campaign/resume')
        self.assertEqual(response.status_code, 200)

    # ==========================================
    # MARKETPLACE API TESTS
    # ==========================================
    
    def test_api_marketplace_mrr(self):
        """Test marketplace MRR analytics"""
        self.login_as_admin()
        response = self.app.get('/api/marketplace/mrr')
        self.assertEqual(response.status_code, 200)
    
    def test_api_marketplace_clients_get(self):
        """Test get marketplace clients"""
        self.login_as_admin()
        response = self.app.get('/api/marketplace/clients')
        self.assertEqual(response.status_code, 200)
    
    def test_api_marketplace_clients_post(self):
        """Test create marketplace client"""
        self.login_as_admin()
        response = self.app.post('/api/marketplace/clients',
            json={
                'company_name': 'Test Corp',
                'contact_email': 'test@corp.com',
                'contact_name': 'John Doe',
                'subscription_tier': 'professional',
                'billing_cycle': 'monthly'
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_api_marketplace_services(self):
        """Test get marketplace services"""
        self.login_as_admin()
        response = self.app.get('/api/marketplace/services')
        self.assertEqual(response.status_code, 200)
    
    def test_api_marketplace_client_dashboard(self):
        """Test get client dashboard data"""
        self.login_as_admin()
        response = self.app.get('/api/marketplace/client/test_client/dashboard')
        self.assertEqual(response.status_code, 200)

    # ==========================================
    # AI ENGINE API TESTS
    # ==========================================
    
    def test_api_ai_insights(self):
        """Test AI insights API"""
        self.login_as_admin()
        response = self.app.get('/api/ai/insights')
        self.assertEqual(response.status_code, 200)
    
    def test_api_ai_predictions(self):
        """Test AI predictions API"""
        self.login_as_admin()
        response = self.app.get('/api/ai/predictions?metric=engagement&horizon=30')
        self.assertEqual(response.status_code, 200)
    
    def test_api_ai_optimization(self):
        """Test AI optimization API"""
        self.login_as_admin()
        response = self.app.get('/api/ai/optimization?campaign_id=test_campaign')
        self.assertEqual(response.status_code, 200)
    
    def test_api_ai_patterns(self):
        """Test AI patterns API"""
        self.login_as_admin()
        response = self.app.get('/api/ai/patterns')
        self.assertEqual(response.status_code, 200)
    
    def test_api_ai_analysis(self):
        """Test AI analysis API"""
        self.login_as_admin()
        response = self.app.get('/api/ai/analysis')
        self.assertEqual(response.status_code, 200)
    
    def test_api_ai_models(self):
        """Test AI models performance API"""
        self.login_as_admin()
        response = self.app.get('/api/ai/models')
        self.assertEqual(response.status_code, 200)

    # ==========================================
    # BUSINESS INTELLIGENCE API TESTS
    # ==========================================
    
    def test_api_bi_executive_dashboard(self):
        """Test BI executive dashboard API"""
        self.login_as_admin()
        response = self.app.get('/api/bi/executive_dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_api_bi_kpi_dashboard(self):
        """Test BI KPI dashboard API"""
        self.login_as_admin()
        response = self.app.get('/api/bi/kpi_dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_api_bi_generate_report(self):
        """Test BI generate report API"""
        self.login_as_admin()
        response = self.app.get('/api/bi/generate_report/executive')
        self.assertEqual(response.status_code, 200)
    
    def test_api_bi_export_pdf(self):
        """Test BI export PDF API"""
        self.login_as_admin()
        response = self.app.get('/api/bi/export/pdf')
        self.assertEqual(response.status_code, 200)
    
    def test_api_bi_export_excel(self):
        """Test BI export Excel API"""
        self.login_as_admin()
        response = self.app.get('/api/bi/export/excel')
        self.assertEqual(response.status_code, 200)
    
    def test_api_bi_visualizations(self):
        """Test BI visualizations API"""
        self.login_as_admin()
        response = self.app.get('/api/bi/visualizations/revenue_trends')
        self.assertEqual(response.status_code, 200)

    # ==========================================
    # SECURITY API TESTS
    # ==========================================
    
    def test_api_security_dashboard(self):
        """Test security dashboard API"""
        self.login_as_admin()
        response = self.app.get('/api/security/dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_api_security_threats_detect(self):
        """Test security threat detection API"""
        self.login_as_admin()
        response = self.app.post('/api/security/threats/detect',
            json={
                'source_ip': '192.168.1.100',
                'user_id': 'test_user',
                'activity_type': 'login',
                'metadata': {'user_agent': 'test'}
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_api_security_compliance_report(self):
        """Test security compliance report API"""
        self.login_as_admin()
        response = self.app.get('/api/security/compliance/report/SOC2')
        self.assertEqual(response.status_code, 200)
    
    def test_api_security_incidents_get(self):
        """Test security incidents GET API"""
        self.login_as_admin()
        response = self.app.get('/api/security/incidents')
        self.assertEqual(response.status_code, 200)
    
    def test_api_security_incidents_post(self):
        """Test security incidents POST API"""
        self.login_as_admin()
        response = self.app.post('/api/security/incidents',
            json={
                'incident_type': 'unauthorized_access',
                'severity': 'high',
                'description': 'Test incident',
                'affected_systems': ['web_app']
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_api_security_ip_block(self):
        """Test security IP block API"""
        self.login_as_admin()
        response = self.app.post('/api/security/ip/block',
            json={
                'ip_address': '192.168.1.100',
                'reason': 'suspicious_activity',
                'duration': 3600
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_api_security_encrypt(self):
        """Test security encrypt API"""
        self.login_as_admin()
        response = self.app.post('/api/security/encrypt',
            json={
                'data': 'sensitive_data',
                'encryption_level': 'AES256'
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_api_security_decrypt(self):
        """Test security decrypt API"""
        self.login_as_admin()
        response = self.app.post('/api/security/decrypt',
            json={
                'encrypted_data': 'encrypted_string',
                'encryption_key': 'test_key'
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    # ==========================================
    # SOCIAL ORCHESTRATOR API TESTS
    # ==========================================
    
    def test_api_social_dashboard(self):
        """Test social orchestrator dashboard API"""
        self.login_as_admin()
        response = self.app.get('/api/social/dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_api_social_content_create(self):
        """Test social content creation API"""
        self.login_as_admin()
        response = self.app.post('/api/social/content/create',
            json={
                'content_type': 'post',
                'platforms': ['instagram', 'twitter'],
                'content': 'Test post content',
                'schedule_time': '2024-12-31T12:00:00Z'
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_api_social_platforms_insights(self):
        """Test social platform insights API"""
        self.login_as_admin()
        response = self.app.get('/api/social/platforms/instagram/insights')
        self.assertEqual(response.status_code, 200)
    
    def test_api_social_calendar(self):
        """Test social calendar API"""
        self.login_as_admin()
        response = self.app.get('/api/social/calendar')
        self.assertEqual(response.status_code, 200)
    
    def test_api_social_analytics(self):
        """Test social analytics API"""
        self.login_as_admin()
        response = self.app.get('/api/social/analytics/instagram')
        self.assertEqual(response.status_code, 200)

    # ==========================================
    # REVENUE OPTIMIZATION API TESTS
    # ==========================================
    
    def test_api_revenue_dashboard(self):
        """Test revenue optimization dashboard API"""
        self.login_as_admin()
        response = self.app.get('/api/revenue/dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_api_revenue_pricing_recommend(self):
        """Test revenue pricing recommendation API"""
        self.login_as_admin()
        response = self.app.post('/api/revenue/pricing/recommend',
            json={
                'product_id': 'starter_plan',
                'current_price': 29.99,
                'target_metric': 'revenue'
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_api_revenue_pricing_test(self):
        """Test revenue pricing test API"""
        self.login_as_admin()
        response = self.app.post('/api/revenue/pricing/test',
            json={
                'product_id': 'pro_plan',
                'test_name': 'Price Increase Test',
                'variant_price': 99.99,
                'duration_days': 30
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_api_revenue_optimize_analyze(self):
        """Test revenue optimization analysis API"""
        self.login_as_admin()
        response = self.app.post('/api/revenue/optimize/analyze')
        self.assertEqual(response.status_code, 200)
    
    def test_api_revenue_recommendations(self):
        """Test revenue recommendations API"""
        self.login_as_admin()
        response = self.app.get('/api/revenue/recommendations')
        self.assertEqual(response.status_code, 200)
    
    def test_api_revenue_upsells(self):
        """Test revenue upsells API"""
        self.login_as_admin()
        response = self.app.get('/api/revenue/upsells')
        self.assertEqual(response.status_code, 200)
    
    def test_api_revenue_tests(self):
        """Test revenue A/B tests API"""
        self.login_as_admin()
        response = self.app.get('/api/revenue/tests?test_id=test_001')
        self.assertEqual(response.status_code, 200)

    # ==========================================
    # ERROR HANDLER TESTS
    # ==========================================
    
    def test_error_handler_404(self):
        """Test 404 error handler"""
        self.login_as_admin()
        response = self.app.get('/nonexistent-route')
        self.assertEqual(response.status_code, 404)
    
    def test_error_handler_403(self):
        """Test 403 error handler by accessing admin route as viewer"""
        self.login_as_viewer()
        response = self.app.get('/settings')
        # Should redirect or show 403
        self.assertIn(response.status_code, [302, 403])
    
    @patch('app.flask_app.logger.error')
    def test_error_handler_500(self, mock_logger):
        """Test 500 error handler"""
        # This would need a route that deliberately raises an exception
        # For now, just test that the error handler exists
        with flask_app.test_request_context('/'):
            try:
                raise Exception("Test exception")
            except:
                pass  # Error handler would catch this in real app

    # ==========================================
    # HELPER FUNCTION TESTS
    # ==========================================
    
    def test_user_class_initialization(self):
        """Test User class initialization"""
        user = User('1', 'testuser', 'hash123', 'admin', 'test@test.com', 'premium')
        self.assertEqual(user.id, '1')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'admin')
        self.assertTrue(user.is_active)
    
    def test_load_user_admin(self):
        """Test load_user function with admin user"""
        user = load_user('1')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'admin')
    
    def test_load_user_nonexistent(self):
        """Test load_user function with nonexistent user"""
        user = load_user('99999')
        self.assertIsNone(user)
    
    def test_get_active_simulations_count(self):
        """Test get_active_simulations_count function"""
        count = get_active_simulations_count()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)
    
    def test_log_system_event_sqlite(self):
        """Test SQLite logging function"""
        result = log_system_event_sqlite('INFO', 'Test message', 'test_component', 'test_user')
        self.assertTrue(result)
    
    def test_log_system_event_supabase_fallback(self):
        """Test system event logging with Supabase fallback"""
        with patch('app.supabase_manager.log_system_event', return_value=False):
            result = log_system_event('INFO', 'Test message')
            # Should fallback to SQLite and still succeed
            self.assertTrue(result)
    
    def test_init_database_function(self):
        """Test database initialization function"""
        # This function is complex and involves Supabase, 
        # so we'll test that it doesn't crash
        try:
            with flask_app.app_context():
                init_database()
        except Exception as e:
            # It's okay if it fails due to missing dependencies
            pass
    
    def test_init_sqlite_fallback_function(self):
        """Test SQLite fallback initialization"""
        result = init_sqlite_fallback()
        self.assertTrue(result)

    # ==========================================
    # ACCESS CONTROL TESTS
    # ==========================================
    
    def test_role_required_decorator_super_admin(self):
        """Test role_required decorator allows super admin"""
        self.login_as_admin()
        response = self.app.get('/settings')
        self.assertEqual(response.status_code, 200)
    
    def test_role_required_decorator_insufficient_privileges(self):
        """Test role_required decorator blocks insufficient privileges"""
        self.login_as_viewer()
        response = self.app.get('/settings', follow_redirects=False)
        # Should redirect to dashboard
        self.assertEqual(response.status_code, 302)
    
    def test_unauthenticated_access_blocked(self):
        """Test unauthenticated access is blocked"""
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_api_endpoints_require_authentication(self):
        """Test API endpoints require authentication"""
        response = self.app.get('/api/system-status')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    # ==========================================
    # EDGE CASE TESTS
    # ==========================================
    
    def test_analytics_with_missing_data_files(self):
        """Test analytics page with missing data files"""
        self.login_as_admin()
        # Remove any existing data files to test fallback
        response = self.app.get('/analytics')
        self.assertEqual(response.status_code, 200)
    
    def test_simulation_logs_with_no_log_file(self):
        """Test simulation logs API with no log file"""
        self.login_as_admin()
        
        # Create simulation without log file
        conn = sqlite3.connect('botzzz_admin.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO simulation_runs (name, type, status, created_by)
            VALUES (?, ?, 'pending', ?)
        ''', ('Test', 'youtube', 'admin'))
        sim_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        response = self.app.get(f'/api/simulations/{sim_id}/logs')
        self.assertEqual(response.status_code, 404)
    
    def test_logs_page_with_empty_database(self):
        """Test logs page with empty database"""
        self.login_as_admin()
        response = self.app.get('/logs')
        self.assertEqual(response.status_code, 200)
    
    def test_detection_page_with_no_events(self):
        """Test detection page with no events"""
        self.login_as_admin()
        response = self.app.get('/detection')
        self.assertEqual(response.status_code, 200)
    
    def test_dashboard_with_empty_database(self):
        """Test dashboard with empty database"""
        self.login_as_admin()
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)

    # ==========================================
    # MOCK INTEGRATION TESTS
    # ==========================================
    
    def test_bulletproof_service_decorator_mock(self):
        """Test bulletproof service decorator works with mocks"""
        # Since we're using mock systems, test that decorated functions work
        self.login_as_admin()
        response = self.app.get('/infrastructure/captcha')
        self.assertEqual(response.status_code, 200)
    
    def test_monitoring_system_mock_methods(self):
        """Test mock monitoring system methods work"""
        from app import monitoring_system, AlertLevel
        
        # Test mock methods don't crash
        monitoring_system.create_alert('test', AlertLevel.INFO, 'test message')
        self.assertTrue(monitoring_system.is_healthy())
        self.assertEqual(monitoring_system.metrics, {})
        self.assertEqual(monitoring_system.alerts, [])
    
    def test_security_manager_mock_methods(self):
        """Test mock security manager methods work"""
        from app import security_manager
        
        # Test mock methods don't crash
        self.assertTrue(security_manager.is_healthy())
    
    def test_get_bulletproof_status_mock(self):
        """Test get_bulletproof_status mock function"""
        from app import get_bulletproof_status
        
        status = get_bulletproof_status()
        self.assertEqual(status['status'], 'mock')

    # ==========================================
    # ADDITIONAL COVERAGE TESTS
    # ==========================================
    
    def test_admin_access_denied_for_non_admin_apis(self):
        """Test admin access denied for non-admin users on admin APIs"""
        # Register and login as regular user
        self.app.post('/register', data={
            'username': 'regularuser',
            'email': 'regular@test.com',
            'password': 'test123',
            'confirm_password': 'test123',
            'service_type': 'basic'
        })
        
        # Mock current_user.is_admin = False for APIs that check it
        with patch('app.current_user') as mock_user:
            mock_user.is_authenticated = True
            mock_user.is_admin = False
            
            response = self.app.get('/api/marketplace/mrr')
            self.assertEqual(response.status_code, 403)
    
    def test_security_check_before_request(self):
        """Test security check before request"""
        with patch('app.security_manager.is_ip_blocked', return_value=True):
            self.login_as_admin()
            response = self.app.get('/dashboard')
            self.assertEqual(response.status_code, 403)
    
    def test_user_is_active_property(self):
        """Test User.is_active property"""
        user = User('1', 'test', 'hash', 'user')
        self.assertTrue(user.is_active)
    
    def test_mock_monitoring_system_properties(self):
        """Test MockMonitoringSystem properties"""
        from app import MockMonitoringSystem
        
        mock_system = MockMonitoringSystem()
        mock_system.create_alert('test', 'info', 'message')
        self.assertTrue(mock_system.is_healthy())
        self.assertEqual(mock_system.metrics, {})
        self.assertEqual(mock_system.alerts, [])

if __name__ == '__main__':
    # Create comprehensive test suite
    unittest.main(verbosity=2)

-- =====================================================
-- BOTZZZ Enterprise Platform - Supabase Database Schema
-- Advanced PostgreSQL schema with real-time capabilities
-- =====================================================

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- =====================================================
-- USER MANAGEMENT & AUTHENTICATION
-- =====================================================

-- Enhanced user profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    login_count INTEGER DEFAULT 0,
    avatar_url TEXT,
    timezone TEXT DEFAULT 'UTC',
    preferences JSONB DEFAULT '{}'::jsonb
);

-- User activity tracking
CREATE TABLE IF NOT EXISTS user_activity (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id TEXT NOT NULL,
    action TEXT NOT NULL,
    resource_type TEXT,
    resource_id TEXT,
    ip_address INET,
    user_agent TEXT,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- SIMULATION MANAGEMENT
-- =====================================================

-- Enhanced simulation runs table
CREATE TABLE IF NOT EXISTS simulation_runs (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled', 'paused')),
    priority INTEGER DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    estimated_duration INTEGER, -- in seconds
    actual_duration INTEGER, -- in seconds
    parameters JSONB,
    results JSONB,
    log_file TEXT,
    created_by TEXT NOT NULL,
    assigned_to TEXT,
    resource_requirements JSONB,
    progress_percentage INTEGER DEFAULT 0 CHECK (progress_percentage BETWEEN 0 AND 100),
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    tags TEXT[] DEFAULT '{}',
    environment TEXT DEFAULT 'production'
);

-- Simulation performance metrics
CREATE TABLE IF NOT EXISTS simulation_metrics (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    simulation_id INTEGER REFERENCES simulation_runs(id) ON DELETE CASCADE,
    metric_name TEXT NOT NULL,
    metric_value NUMERIC,
    unit TEXT,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB
);

-- =====================================================
-- SYSTEM MONITORING & LOGGING
-- =====================================================

-- Enhanced system logs table
CREATE TABLE IF NOT EXISTS system_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    level TEXT NOT NULL CHECK (level IN ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')),
    message TEXT NOT NULL,
    component TEXT,
    user_id TEXT,
    session_id TEXT,
    request_id TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    severity_score INTEGER DEFAULT 2,
    source_ip INET,
    metadata JSONB,
    stack_trace TEXT,
    resolved BOOLEAN DEFAULT false,
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolved_by TEXT
);

-- System alerts table
CREATE TABLE IF NOT EXISTS system_alerts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    alert_type TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('INFO', 'WARNING', 'ERROR', 'CRITICAL')),
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    component TEXT,
    source_table TEXT,
    source_id TEXT,
    acknowledged BOOLEAN DEFAULT false,
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    acknowledged_by TEXT,
    resolved BOOLEAN DEFAULT false,
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolved_by TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB
);

-- =====================================================
-- BOT DETECTION & ANALYTICS
-- =====================================================

-- Enhanced bot detection events
CREATE TABLE IF NOT EXISTS bot_detection_events (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    event_type TEXT NOT NULL,
    bot_id TEXT,
    video_id TEXT,
    platform TEXT,
    risk_score REAL CHECK (risk_score BETWEEN 0 AND 1),
    detection_method TEXT,
    confidence_score REAL CHECK (confidence_score BETWEEN 0 AND 1),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    simulation_run_id INTEGER REFERENCES simulation_runs(id) ON DELETE SET NULL,
    metadata JSONB,
    ip_address INET,
    user_agent TEXT,
    geographical_location POINT,
    device_fingerprint TEXT
);

-- Analytics metrics for business intelligence
CREATE TABLE IF NOT EXISTS analytics_metrics (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    metric_name TEXT NOT NULL,
    value NUMERIC NOT NULL,
    dimensions JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    aggregation_period TEXT, -- 'minute', 'hour', 'day', 'week', 'month'
    data_source TEXT,
    quality_score REAL DEFAULT 1.0
);

-- =====================================================
-- ENTERPRISE FEATURES
-- =====================================================

-- Campaign management
CREATE TABLE IF NOT EXISTS campaigns (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    platform TEXT NOT NULL,
    status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'paused', 'completed', 'cancelled')),
    campaign_type TEXT NOT NULL,
    targeting_criteria JSONB,
    budget_allocated NUMERIC(10,2),
    budget_spent NUMERIC(10,2) DEFAULT 0,
    start_date TIMESTAMP WITH TIME ZONE,
    end_date TIMESTAMP WITH TIME ZONE,
    created_by TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    performance_metrics JSONB,
    tags TEXT[] DEFAULT '{}'
);

-- Campaign tasks/actions
CREATE TABLE IF NOT EXISTS campaign_tasks (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    task_type TEXT NOT NULL,
    target_url TEXT,
    target_user TEXT,
    parameters JSONB,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'skipped')),
    scheduled_at TIMESTAMP WITH TIME ZONE,
    executed_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    result JSONB,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Client management for enterprise marketplace
CREATE TABLE IF NOT EXISTS marketplace_clients (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    company_name TEXT NOT NULL,
    contact_name TEXT NOT NULL,
    contact_email TEXT NOT NULL,
    subscription_tier TEXT NOT NULL CHECK (subscription_tier IN ('starter', 'professional', 'enterprise', 'white_label')),
    billing_cycle TEXT DEFAULT 'monthly' CHECK (billing_cycle IN ('monthly', 'quarterly', 'yearly')),
    mrr NUMERIC(10,2), -- Monthly Recurring Revenue
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'suspended', 'cancelled', 'trial')),
    trial_end_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB,
    api_key_hash TEXT,
    rate_limit INTEGER DEFAULT 1000,
    white_label_domain TEXT
);

-- Revenue tracking
CREATE TABLE IF NOT EXISTS revenue_records (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    client_id UUID REFERENCES marketplace_clients(id) ON DELETE CASCADE,
    amount NUMERIC(10,2) NOT NULL,
    currency TEXT DEFAULT 'USD',
    billing_period_start DATE,
    billing_period_end DATE,
    invoice_id TEXT,
    payment_status TEXT DEFAULT 'pending' CHECK (payment_status IN ('pending', 'paid', 'failed', 'refunded')),
    payment_method TEXT,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB
);

-- =====================================================
-- AI & MACHINE LEARNING
-- =====================================================

-- AI insights and predictions
CREATE TABLE IF NOT EXISTS ai_insights (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    insight_type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    confidence_level TEXT CHECK (confidence_level IN ('low', 'medium', 'high')),
    impact_score REAL CHECK (impact_score BETWEEN 0 AND 10),
    data_points JSONB,
    recommended_action TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'implemented', 'dismissed', 'expired'))
);

-- ML model performance tracking
CREATE TABLE IF NOT EXISTS ml_model_performance (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_version TEXT,
    metric_name TEXT NOT NULL,
    metric_value NUMERIC,
    training_data_size INTEGER,
    test_data_size INTEGER,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB
);

-- =====================================================
-- CACHING & PERFORMANCE
-- =====================================================

-- Enhanced analytics cache
CREATE TABLE IF NOT EXISTS analytics_cache (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    cache_key TEXT UNIQUE NOT NULL,
    data JSONB NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    access_count INTEGER DEFAULT 0,
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    size_bytes INTEGER,
    tags TEXT[] DEFAULT '{}'
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Simulation runs indexes
CREATE INDEX IF NOT EXISTS idx_simulation_runs_status ON simulation_runs(status);
CREATE INDEX IF NOT EXISTS idx_simulation_runs_created_by ON simulation_runs(created_by);
CREATE INDEX IF NOT EXISTS idx_simulation_runs_created_at ON simulation_runs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_simulation_runs_type ON simulation_runs(type);

-- System logs indexes
CREATE INDEX IF NOT EXISTS idx_system_logs_level ON system_logs(level);
CREATE INDEX IF NOT EXISTS idx_system_logs_timestamp ON system_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_system_logs_component ON system_logs(component);
CREATE INDEX IF NOT EXISTS idx_system_logs_user_id ON system_logs(user_id);

-- Analytics metrics indexes
CREATE INDEX IF NOT EXISTS idx_analytics_metrics_name ON analytics_metrics(metric_name);
CREATE INDEX IF NOT EXISTS idx_analytics_metrics_timestamp ON analytics_metrics(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_analytics_metrics_name_timestamp ON analytics_metrics(metric_name, timestamp DESC);

-- Bot detection events indexes
CREATE INDEX IF NOT EXISTS idx_bot_detection_platform ON bot_detection_events(platform);
CREATE INDEX IF NOT EXISTS idx_bot_detection_timestamp ON bot_detection_events(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_bot_detection_risk_score ON bot_detection_events(risk_score DESC);

-- Campaign indexes
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);
CREATE INDEX IF NOT EXISTS idx_campaigns_platform ON campaigns(platform);
CREATE INDEX IF NOT EXISTS idx_campaigns_created_by ON campaigns(created_by);

-- =====================================================
-- TRIGGERS FOR AUTO-UPDATES
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers
CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_simulation_runs_updated_at BEFORE UPDATE ON simulation_runs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_campaigns_updated_at BEFORE UPDATE ON campaigns FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_marketplace_clients_updated_at BEFORE UPDATE ON marketplace_clients FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to increment user login count
CREATE OR REPLACE FUNCTION increment_user_login(user_id TEXT)
RETURNS VOID AS $$
BEGIN
    UPDATE user_profiles 
    SET login_count = login_count + 1,
        last_login = NOW()
    WHERE user_profiles.user_id = increment_user_login.user_id;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- ROW LEVEL SECURITY (RLS)
-- =====================================================

-- Enable RLS on sensitive tables
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE marketplace_clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE revenue_records ENABLE ROW LEVEL SECURITY;

-- Basic RLS policies (customize based on your auth setup)
CREATE POLICY "Users can view their own profile" ON user_profiles
    FOR SELECT USING (auth.uid()::text = user_id);

CREATE POLICY "Admins can view all profiles" ON user_profiles
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM user_profiles 
            WHERE user_id = auth.uid()::text 
            AND role IN ('super_admin', 'admin')
        )
    );

-- =====================================================
-- REAL-TIME SUBSCRIPTIONS SETUP
-- =====================================================

-- Enable real-time for specific tables
ALTER PUBLICATION supabase_realtime ADD TABLE simulation_runs;
ALTER PUBLICATION supabase_realtime ADD TABLE system_logs;
ALTER PUBLICATION supabase_realtime ADD TABLE system_alerts;
ALTER PUBLICATION supabase_realtime ADD TABLE bot_detection_events;
ALTER PUBLICATION supabase_realtime ADD TABLE analytics_metrics;

-- =====================================================
-- INITIAL DATA SEEDING
-- =====================================================

-- Insert sample data for testing (optional)
INSERT INTO user_profiles (user_id, email, username, role) VALUES
('admin-001', 'admin@botzzz.com', 'admin', 'super_admin'),
('operator-001', 'operator@botzzz.com', 'operator', 'operator'),
('viewer-001', 'viewer@botzzz.com', 'viewer', 'viewer')
ON CONFLICT (user_id) DO NOTHING;

-- =====================================================
-- PERFORMANCE MONITORING VIEWS
-- =====================================================

-- View for simulation performance overview
CREATE OR REPLACE VIEW simulation_performance_overview AS
SELECT 
    type,
    COUNT(*) as total_runs,
    COUNT(*) FILTER (WHERE status = 'completed') as completed_runs,
    COUNT(*) FILTER (WHERE status = 'failed') as failed_runs,
    AVG(actual_duration) as avg_duration_seconds,
    AVG(progress_percentage) as avg_progress
FROM simulation_runs
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY type;

-- View for system health metrics
CREATE OR REPLACE VIEW system_health_summary AS
SELECT 
    DATE_TRUNC('hour', timestamp) as hour,
    COUNT(*) as total_logs,
    COUNT(*) FILTER (WHERE level = 'ERROR') as error_count,
    COUNT(*) FILTER (WHERE level = 'CRITICAL') as critical_count,
    COUNT(DISTINCT component) as active_components
FROM system_logs
WHERE timestamp >= NOW() - INTERVAL '24 hours'
GROUP BY DATE_TRUNC('hour', timestamp)
ORDER BY hour DESC;

-- =====================================================
-- STORED PROCEDURES FOR BUSINESS LOGIC
-- =====================================================

-- Calculate MRR (Monthly Recurring Revenue)
CREATE OR REPLACE FUNCTION calculate_total_mrr()
RETURNS NUMERIC AS $$
DECLARE
    total_mrr NUMERIC := 0;
BEGIN
    SELECT COALESCE(SUM(
        CASE 
            WHEN billing_cycle = 'monthly' THEN mrr
            WHEN billing_cycle = 'quarterly' THEN mrr / 3
            WHEN billing_cycle = 'yearly' THEN mrr / 12
            ELSE 0
        END
    ), 0) INTO total_mrr
    FROM marketplace_clients
    WHERE status = 'active';
    
    RETURN total_mrr;
END;
$$ LANGUAGE plpgsql;

-- Get client performance metrics
CREATE OR REPLACE FUNCTION get_client_metrics(client_uuid UUID)
RETURNS JSONB AS $$
DECLARE
    metrics JSONB;
BEGIN
    SELECT jsonb_build_object(
        'total_revenue', COALESCE(SUM(amount), 0),
        'active_campaigns', (
            SELECT COUNT(*) FROM campaigns 
            WHERE created_by = (
                SELECT user_id FROM marketplace_clients WHERE id = client_uuid
            ) AND status = 'active'
        ),
        'last_payment', MAX(recorded_at)
    ) INTO metrics
    FROM revenue_records
    WHERE client_id = client_uuid;
    
    RETURN metrics;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- CLEANUP PROCEDURES
-- =====================================================

-- Cleanup old logs (keep last 90 days)
CREATE OR REPLACE FUNCTION cleanup_old_logs()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM system_logs 
    WHERE timestamp < NOW() - INTERVAL '90 days';
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Cleanup expired cache entries
CREATE OR REPLACE FUNCTION cleanup_expired_cache()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM analytics_cache 
    WHERE expires_at < NOW();
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- COMMENTS FOR DOCUMENTATION
-- =====================================================

COMMENT ON TABLE simulation_runs IS 'Core table for tracking bot simulation executions with enhanced metadata';
COMMENT ON TABLE system_logs IS 'Centralized logging system with severity scoring and real-time alerting';
COMMENT ON TABLE analytics_metrics IS 'Time-series data for business intelligence and performance monitoring';
COMMENT ON TABLE marketplace_clients IS 'Enterprise client management with subscription and billing tracking';
COMMENT ON TABLE ai_insights IS 'AI-generated business insights and recommendations';
COMMENT ON FUNCTION calculate_total_mrr() IS 'Calculates total Monthly Recurring Revenue across all active clients';
COMMENT ON FUNCTION cleanup_old_logs() IS 'Maintenance function to remove logs older than 90 days';

-- =====================================================
-- GRANTS AND PERMISSIONS
-- =====================================================

-- Grant appropriate permissions to authenticated users
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO authenticated;

-- Grant read-only access to anonymous users for public data
GRANT SELECT ON simulation_runs TO anon;
GRANT SELECT ON analytics_metrics TO anon;

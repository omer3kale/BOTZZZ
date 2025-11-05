/**
 * Admin Features Integration Tests
 * Tests for Add Manual Payment and Add Provider functionality
 * 
 * Run: node tests/admin-features.test.js
 */

const BASE_URL = process.env.TEST_URL || 'http://localhost:8888';

// ANSI color codes for terminal output
const colors = {
    reset: '\x1b[0m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m'
};

const ADMIN_EMAIL = process.env.ADMIN_EMAIL || 'botzzz773@gmail.com';
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'Mariogomez33*';

let testResults = {
    passed: 0,
    failed: 0,
    total: 0
};

// Helper function to make API calls
async function apiCall(endpoint, options = {}) {
    const url = `${BASE_URL}/.netlify/functions/${endpoint}`;
    console.log(`${colors.cyan}📡 ${options.method || 'GET'} ${url}${colors.reset}`);
    
    const response = await fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
            ...(options.headers?.Authorization ? { 'authorization': options.headers.Authorization } : {})
        },
        ...options
    });
    
    const data = await response.json();
    console.log(`${colors.blue}📥 Response (${response.status}):${colors.reset}`, JSON.stringify(data, null, 2));
    
    return { response, data };
}

// Test helper
async function test(name, fn) {
    testResults.total++;
    console.log(`\n${colors.magenta}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}`);
    console.log(`${colors.yellow}🧪 TEST ${testResults.total}: ${name}${colors.reset}`);
    console.log(`${colors.magenta}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}`);
    
    try {
        await fn();
        testResults.passed++;
        console.log(`${colors.green}✅ PASSED: ${name}${colors.reset}`);
        return true;
    } catch (error) {
        testResults.failed++;
        console.log(`${colors.red}❌ FAILED: ${name}${colors.reset}`);
        console.log(`${colors.red}Error: ${error.message}${colors.reset}`);
        console.error(error.stack);
        return false;
    }
}

// Assert helper
function assert(condition, message) {
    if (!condition) {
        throw new Error(message || 'Assertion failed');
    }
}

// Main test suite
async function runTests() {
    console.log(`${colors.cyan}╔════════════════════════════════════════════════════════╗${colors.reset}`);
    console.log(`${colors.cyan}║     Admin Features Integration Test Suite             ║${colors.reset}`);
    console.log(`${colors.cyan}╚════════════════════════════════════════════════════════╝${colors.reset}`);
    console.log(`${colors.blue}Base URL: ${BASE_URL}${colors.reset}\n`);

    let adminToken = null;
    let testUserId = null;
    let testProviderId = null;
    let adminUser = null;

    // Setup: Login as admin
    await test('Admin Login', async () => {
        const { response, data } = await apiCall('auth', {
            method: 'POST',
            body: JSON.stringify({
                action: 'login',
                email: ADMIN_EMAIL,
                password: ADMIN_PASSWORD
            })
        });

        assert(response.ok, `Login failed with status ${response.status}`);
        assert(data.success, 'Login should return success');
        assert(data.token, 'Login should return token');
        assert(data.user.role === 'admin', 'User should have admin role');

        adminToken = data.token;
        adminUser = data.user;
        testUserId = adminUser.id; // use admin account for testing
        console.log(`${colors.green}✓ Admin token obtained${colors.reset}`);
    });

    if (!adminToken) {
        console.log(`${colors.red}⚠️  Cannot continue tests without admin token${colors.reset}`);
        return;
    }

    await test('Admin Token Valid', async () => {
        assert(adminUser && adminUser.id, 'Admin user data missing from login response');
        console.log(`${colors.green}✓ Using admin account for manual payment tests (${adminUser.email})${colors.reset}`);
    });

    // TEST 1: Add Manual Payment - Completed
    await test('Add Manual Payment (Completed)', async () => {
        const amount = 100.00;
        const { response, data } = await apiCall('payments', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${adminToken}`
            },
            body: JSON.stringify({
                action: 'admin-add-payment',
                userId: testUserId,
                amount: amount,
                method: 'payeer',
                transactionId: `TEST-${Date.now()}`,
                status: 'completed',
                memo: 'Automated test payment'
            })
        });

        assert(response.ok, `Add payment failed with status ${response.status}: ${data.error}`);
        assert(data.success, `Add payment should succeed: ${data.error}`);
        assert(data.payment, 'Response should include payment object');
        assert(data.payment.amount == amount, `Payment amount should be ${amount}`);
        assert(data.payment.status === 'completed', 'Payment status should be completed');
        assert(data.message, 'Response should include success message');

        console.log(`${colors.green}✓ Payment created: $${amount}${colors.reset}`);
        console.log(`${colors.green}✓ ${data.message}${colors.reset}`);
    });

    // TEST 2: Add Manual Payment - Pending
    await test('Add Manual Payment (Pending)', async () => {
        const amount = 50.00;
        const { response, data } = await apiCall('payments', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${adminToken}`
            },
            body: JSON.stringify({
                action: 'admin-add-payment',
                userId: testUserId,
                amount: amount,
                method: 'stripe',
                transactionId: `TEST-PENDING-${Date.now()}`,
                status: 'pending',
                memo: 'Test pending payment'
            })
        });

        assert(response.ok, `Add pending payment failed with status ${response.status}: ${data.error}`);
        assert(data.success, `Add pending payment should succeed: ${data.error}`);
        assert(data.payment.status === 'pending', 'Payment status should be pending');

        console.log(`${colors.green}✓ Pending payment created: $${amount}${colors.reset}`);
    });

    // TEST 3: Add Manual Payment - Missing Required Fields
    await test('Add Manual Payment - Validation (should fail)', async () => {
        const { response, data } = await apiCall('payments', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${adminToken}`
            },
            body: JSON.stringify({
                action: 'admin-add-payment',
                userId: testUserId,
                // Missing amount, method, status
            })
        });

        assert(!response.ok || !data.success, 'Should fail validation');
        assert(data.error, 'Should return error message');
        assert(data.error.includes('required'), 'Error should mention required fields');

        console.log(`${colors.green}✓ Validation working correctly${colors.reset}`);
    });

    // TEST 4: Add New Provider
    await test('Add New Provider', async () => {
        const providerName = `TestProvider-${Date.now()}`;
        const { response, data } = await apiCall('providers', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${adminToken}`
            },
            body: JSON.stringify({
                action: 'create',
                name: providerName,
                apiUrl: 'https://test-provider.example.com/api',
                apiKey: 'test-api-key-' + Date.now(),
                markup: 15.5,
                status: 'active'
            })
        });

        assert(response.ok, `Add provider failed with status ${response.status}: ${data.error}`);
        assert(data.success, `Add provider should succeed: ${data.error}`);
        assert(data.provider, 'Response should include provider object');
        assert(data.provider.name === providerName, `Provider name should be ${providerName}`);
        assert(data.provider.markup == 15.5, 'Provider markup should be 15.5');

        testProviderId = data.provider.id;
        console.log(`${colors.green}✓ Provider created: ${providerName} (${testProviderId})${colors.reset}`);
    });

    // TEST 5: Add Provider - Missing Required Fields
    await test('Add Provider - Validation (should fail)', async () => {
        const { response, data } = await apiCall('providers', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${adminToken}`
            },
            body: JSON.stringify({
                action: 'create',
                // Missing name and apiKey
                apiUrl: 'https://test.com'
            })
        });

        assert(!response.ok || !data.success, 'Should fail validation');
        assert(data.error, 'Should return error message');

        console.log(`${colors.green}✓ Provider validation working correctly${colors.reset}`);
    });

    // TEST 6: Add Provider - Without action field (should fail)
    await test('Add Provider - Missing action field (should fail)', async () => {
        const { response, data } = await apiCall('providers', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${adminToken}`
            },
            body: JSON.stringify({
                // Missing action field
                name: 'Test Provider',
                apiUrl: 'https://test.com',
                apiKey: 'test-key'
            })
        });

        assert(!response.ok || !data.success, 'Should fail without action field');
        assert(data.error, 'Should return error message');
        assert(data.error.includes('action'), 'Error should mention action field');

        console.log(`${colors.green}✓ Action field validation working${colors.reset}`);
    });

    // TEST 7: Unauthorized Payment Addition (should fail)
    await test('Add Payment - Unauthorized (should fail)', async () => {
        const { response, data } = await apiCall('payments', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer invalid-token'
            },
            body: JSON.stringify({
                action: 'admin-add-payment',
                userId: testUserId,
                amount: 100,
                method: 'payeer',
                status: 'completed'
            })
        });

        assert(!response.ok, 'Should fail with invalid token');
        assert(response.status === 401 || response.status === 403, 'Should return 401 or 403');

        console.log(`${colors.green}✓ Authorization check working${colors.reset}`);
    });

    // Print summary
    console.log(`\n${colors.cyan}╔════════════════════════════════════════════════════════╗${colors.reset}`);
    console.log(`${colors.cyan}║                   TEST SUMMARY                         ║${colors.reset}`);
    console.log(`${colors.cyan}╚════════════════════════════════════════════════════════╝${colors.reset}`);
    console.log(`${colors.green}✅ Passed: ${testResults.passed}${colors.reset}`);
    console.log(`${colors.red}❌ Failed: ${testResults.failed}${colors.reset}`);
    console.log(`📊 Total:  ${testResults.total}`);
    console.log(`📈 Success Rate: ${((testResults.passed / testResults.total) * 100).toFixed(1)}%\n`);

    if (testResults.failed === 0) {
        console.log(`${colors.green}🎉 All tests passed!${colors.reset}\n`);
        process.exit(0);
    } else {
        console.log(`${colors.red}⚠️  Some tests failed!${colors.reset}\n`);
        process.exit(1);
    }
}

// Run tests
runTests().catch(error => {
    console.error(`${colors.red}Fatal error running tests:${colors.reset}`, error);
    process.exit(1);
});

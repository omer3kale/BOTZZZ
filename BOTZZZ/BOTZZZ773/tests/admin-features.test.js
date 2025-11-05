/**
 * Admin Features Integration Tests
 * Tests for Add Manual Payment and Add Provider functionality
 * 
 * Run: node tests/admin-features.test.js
 */

const BASE_URL = (process.env.TEST_URL || 'https://botzzz773.pro').replace(/\/$/, '');

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

// Test data from screenshots
const PAYMENT_USER_EMAIL = 'eyuphans@gmail.com';  // Gandalfpapa user
const PAYMENT_AMOUNT = 100;
const PAYMENT_METHOD = 'payeer';
const PAYMENT_TRANSACTION_ID = '123132';
const PAYMENT_MEMO = 'test';
const PAYMENT_STATUS = 'completed';

const PROVIDER_NAME = 'g1618';
const PROVIDER_API_URL = 'https://g1618.com';
const PROVIDER_API_KEY = 'dedd4dac6d44f5523caf0c';
const PROVIDER_MARKUP = 0;
const PROVIDER_STATUS = 'active';

let testResults = {
    passed: 0,
    failed: 0,
    total: 0
};

// Helper function to make API calls
async function apiCall(endpoint, options = {}) {
    const url = `${BASE_URL}/.netlify/functions/${endpoint}`;
    console.log(`${colors.cyan}📡 ${options.method || 'GET'} ${url}${colors.reset}`);
    
    const { method, headers, body, ...rest } = options;
    const customHeaders = headers || {};
    const authHeader = customHeaders.Authorization || customHeaders.authorization;
    const response = await fetch(url, {
        method: method || 'GET',
        headers: {
            'Content-Type': 'application/json',
            ...customHeaders,
            ...(authHeader ? { Authorization: authHeader, authorization: authHeader } : {})
        },
        body,
        ...rest
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

    await test('Load Test User (Gandalfpapa)', async () => {
        assert(adminUser && adminUser.id, 'Admin user data missing from login response');
        console.log(`${colors.green}✓ Admin account verified (${adminUser.email})${colors.reset}`);

        const { response, data } = await apiCall('users', {
            headers: {
                'authorization': `Bearer ${adminToken}`
            }
        });

        assert(response.ok, `Get users failed with status ${response.status}`);
        assert(Array.isArray(data.users), 'Response should include users array');

        const targetUser = data.users.find(u => (u.email || '').toLowerCase() === PAYMENT_USER_EMAIL.toLowerCase());
        assert(targetUser, `User with email ${PAYMENT_USER_EMAIL} not found`);

        testUserId = targetUser.id;
        console.log(`${colors.green}✓ Using test user: ${targetUser.username || targetUser.email} (${testUserId})${colors.reset}`);
    });

    // TEST 1: Add Manual Payment - Completed
    await test('Add Manual Payment (Completed)', async () => {
        const amount = 100.00;
        const { response, data } = await apiCall('payments', {
            method: 'POST',
            headers: {
                'authorization': `Bearer ${adminToken}`
            },
            body: JSON.stringify({
                action: 'admin-add-payment',
                userId: testUserId,
                amount: PAYMENT_AMOUNT,
                method: PAYMENT_METHOD,
                transactionId: `${PAYMENT_TRANSACTION_ID}-${Date.now()}`,
                status: PAYMENT_STATUS,
                memo: PAYMENT_MEMO
            })
        });

        assert(response.ok, `Add payment failed with status ${response.status}: ${data.error}`);
        assert(data.success, `Add payment should succeed: ${data.error}`);
        assert(data.payment, 'Response should include payment object');
        assert(Number(data.payment.amount) === PAYMENT_AMOUNT, `Payment amount should be ${PAYMENT_AMOUNT}`);
        assert((data.payment.status || '').toLowerCase() === PAYMENT_STATUS, `Payment status should be ${PAYMENT_STATUS}`);
        assert(data.message, 'Response should include success message');

        console.log(`${colors.green}✓ Payment created: $${PAYMENT_AMOUNT}${colors.reset}`);
        console.log(`${colors.green}✓ ${data.message}${colors.reset}`);
    });

    // TEST 2: Add Manual Payment - Pending
    await test('Add Manual Payment (Pending)', async () => {
        const { response, data } = await apiCall('payments', {
            method: 'POST',
            headers: {
                'authorization': `Bearer ${adminToken}`
            },
            body: JSON.stringify({
                action: 'admin-add-payment',
                userId: testUserId,
                amount: PAYMENT_AMOUNT,
                method: PAYMENT_METHOD,
                transactionId: `PENDING-${PAYMENT_TRANSACTION_ID}-${Date.now()}`,
                status: 'pending',
                memo: `${PAYMENT_MEMO}-pending`
            })
        });

        assert(response.ok, `Add pending payment failed with status ${response.status}: ${data.error}`);
        assert(data.success, `Add pending payment should succeed: ${data.error}`);
        assert(data.payment.status === 'pending', 'Payment status should be pending');

        console.log(`${colors.green}✓ Pending payment created${colors.reset}`);
    });

    // TEST 3: Add Manual Payment - Missing Required Fields
    await test('Add Manual Payment - Validation (should fail)', async () => {
        const { response, data } = await apiCall('payments', {
            method: 'POST',
            headers: {
                'authorization': `Bearer ${adminToken}`
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
        const { response, data } = await apiCall('providers', {
            method: 'POST',
            headers: {
                'authorization': `Bearer ${adminToken}`
            },
            body: JSON.stringify({
                action: 'create',
                name: `${PROVIDER_NAME}-${Date.now()}`,
                apiUrl: PROVIDER_API_URL,
                apiKey: `${PROVIDER_API_KEY}-${Date.now()}`,
                markup: PROVIDER_MARKUP,
                status: PROVIDER_STATUS
            })
        });

        assert(response.ok, `Add provider failed with status ${response.status}: ${data.error}`);
        assert(data.success, `Add provider should succeed: ${data.error}`);
        assert(data.provider, 'Response should include provider object');
        assert(data.provider.markup == PROVIDER_MARKUP, `Provider markup should be ${PROVIDER_MARKUP}`);

        testProviderId = data.provider.id;
        console.log(`${colors.green}✓ Provider created: ${data.provider.name} (${testProviderId})${colors.reset}`);
    });

    // TEST 5: Add Provider - Missing Required Fields
    await test('Add Provider - Validation (should fail)', async () => {
        const { response, data } = await apiCall('providers', {
            method: 'POST',
            headers: {
                'authorization': `Bearer ${adminToken}`
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
                'authorization': `Bearer ${adminToken}`
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

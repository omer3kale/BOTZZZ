// API Client Tests
// Run these tests in browser console or with a test framework

class APIClientTests {
    constructor() {
        this.results = [];
        this.api = new APIClient();
    }

    // Test runner
    async runAll() {
        console.log('🧪 Starting API Client Tests...\n');
        
        await this.testAuthEndpoints();
        await this.testUserEndpoints();
        await this.testServiceEndpoints();
        await this.testOrderEndpoints();
        await this.testPaymentEndpoints();
        await this.testTicketEndpoints();
        
        this.printResults();
    }

    // Test helpers
    async test(name, fn) {
        try {
            console.log(`Testing: ${name}...`);
            await fn();
            this.results.push({ name, status: 'PASS', error: null });
            console.log(`✅ PASS: ${name}\n`);
        } catch (error) {
            this.results.push({ name, status: 'FAIL', error: error.message });
            console.error(`❌ FAIL: ${name}`, error.message, '\n');
        }
    }

    // Auth tests
    async testAuthEndpoints() {
        console.log('\n📝 Testing Authentication Endpoints...\n');

        await this.test('Signup - should create new user', async () => {
            const testUser = {
                email: `test${Date.now()}@test.com`,
                password: 'Test1234!',
                username: `testuser${Date.now()}`,
                firstName: 'Test',
                lastName: 'User'
            };

            const result = await this.api.signup(
                testUser.email,
                testUser.password,
                testUser.username,
                testUser.firstName,
                testUser.lastName
            );

            if (!result.success || !result.token || !result.user) {
                throw new Error('Signup failed or missing required fields');
            }

            // Store for later tests
            this.testToken = result.token;
            this.testUser = result.user;
        });

        await this.test('Login - should authenticate user', async () => {
            const result = await this.api.login('admin@botzzz.com', 'admin123');
            
            if (!result.success || !result.token || !result.user) {
                throw new Error('Login failed');
            }
        });

        await this.test('Verify Token - should validate token', async () => {
            if (!this.testToken) {
                throw new Error('No token available for testing');
            }

            const result = await this.api.verifyToken(this.testToken);
            
            if (!result.success || !result.user) {
                throw new Error('Token verification failed');
            }
        });
    }

    // User tests
    async testUserEndpoints() {
        console.log('\n👤 Testing User Endpoints...\n');

        await this.test('Get User - should fetch user data', async () => {
            const result = await this.api.getUser();
            
            if (!result.user) {
                throw new Error('Failed to fetch user');
            }
        });

        await this.test('Update User - should update user data', async () => {
            if (!this.testUser) {
                console.log('⏭️  Skipping: No test user available');
                return;
            }

            const result = await this.api.updateUser(this.testUser.id, {
                first_name: 'Updated',
                last_name: 'Name'
            });
            
            if (!result.success) {
                throw new Error('Failed to update user');
            }
        });
    }

    // Service tests
    async testServiceEndpoints() {
        console.log('\n🛍️  Testing Service Endpoints...\n');

        await this.test('Get Services - should fetch all services', async () => {
            const result = await this.api.getServices();
            
            if (!Array.isArray(result.services)) {
                throw new Error('Services should be an array');
            }
        });
    }

    // Order tests
    async testOrderEndpoints() {
        console.log('\n📦 Testing Order Endpoints...\n');

        await this.test('Get Orders - should fetch orders', async () => {
            const result = await this.api.getOrders();
            
            if (!Array.isArray(result.orders)) {
                throw new Error('Orders should be an array');
            }
        });
    }

    // Payment tests
    async testPaymentEndpoints() {
        console.log('\n💳 Testing Payment Endpoints...\n');

        await this.test('Get Payment History - should fetch payment history', async () => {
            const result = await this.api.getPaymentHistory();
            
            if (!Array.isArray(result.payments)) {
                throw new Error('Payments should be an array');
            }
        });
    }

    // Ticket tests
    async testTicketEndpoints() {
        console.log('\n🎫 Testing Ticket Endpoints...\n');

        await this.test('Get Tickets - should fetch tickets', async () => {
            const result = await this.api.getTickets();
            
            if (!Array.isArray(result.tickets)) {
                throw new Error('Tickets should be an array');
            }
        });

        await this.test('Create Ticket - should create new ticket', async () => {
            const result = await this.api.createTicket(
                'Test Ticket',
                'orders',
                'medium',
                'This is a test ticket message'
            );
            
            if (!result.success || !result.ticket) {
                throw new Error('Failed to create ticket');
            }

            this.testTicketId = result.ticket.id;
        });

        await this.test('Reply to Ticket - should add reply', async () => {
            if (!this.testTicketId) {
                console.log('⏭️  Skipping: No test ticket available');
                return;
            }

            const result = await this.api.replyTicket(
                this.testTicketId,
                'This is a test reply'
            );
            
            if (!result.success) {
                throw new Error('Failed to reply to ticket');
            }
        });
    }

    // Print results
    printResults() {
        console.log('\n' + '='.repeat(50));
        console.log('📊 TEST RESULTS SUMMARY');
        console.log('='.repeat(50));

        const passed = this.results.filter(r => r.status === 'PASS').length;
        const failed = this.results.filter(r => r.status === 'FAIL').length;
        const total = this.results.length;

        console.log(`\nTotal Tests: ${total}`);
        console.log(`✅ Passed: ${passed}`);
        console.log(`❌ Failed: ${failed}`);
        console.log(`Success Rate: ${((passed / total) * 100).toFixed(1)}%\n`);

        if (failed > 0) {
            console.log('Failed Tests:');
            this.results
                .filter(r => r.status === 'FAIL')
                .forEach(r => {
                    console.log(`  ❌ ${r.name}: ${r.error}`);
                });
        }

        console.log('\n' + '='.repeat(50) + '\n');
    }
}

// Auto-run tests if in test mode
if (typeof window !== 'undefined' && window.location.search.includes('test=true')) {
    window.addEventListener('DOMContentLoaded', async () => {
        const tests = new APIClientTests();
        await tests.runAll();
    });
}

// Export for manual testing
if (typeof window !== 'undefined') {
    window.APIClientTests = APIClientTests;
}

// Usage in console:
// const tests = new APIClientTests();
// tests.runAll();

// Test Runner - Executes all test suites
// Run with: node tests/run-all-tests.js

const { spawn } = require('child_process');
const path = require('path');

const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m'
};

function log(color, message) {
  console.log(colors[color] + message + colors.reset);
}

class TestRunner {
  constructor() {
    this.results = {
      suites: [],
      totalTests: 0,
      passedTests: 0,
      failedTests: 0,
      startTime: Date.now()
    };
  }

  async runTestSuite(name, scriptPath) {
    log('magenta', `\n${'='.repeat(60)}`);
    log('magenta', `Running ${name}...`);
    log('magenta', '='.repeat(60));

    return new Promise((resolve) => {
      const testProcess = spawn('node', [scriptPath], {
        stdio: 'inherit',
        cwd: path.dirname(scriptPath)
      });

      testProcess.on('close', (code) => {
        const result = {
          name,
          passed: code === 0,
          exitCode: code
        };
        
        this.results.suites.push(result);
        
        if (code === 0) {
          log('green', `✓ ${name} completed successfully`);
        } else {
          log('red', `✗ ${name} failed with exit code ${code}`);
        }
        
        resolve(result);
      });

      testProcess.on('error', (error) => {
        log('red', `Error running ${name}: ${error.message}`);
        this.results.suites.push({
          name,
          passed: false,
          error: error.message
        });
        resolve({ name, passed: false, error: error.message });
      });
    });
  }

  async runAll() {
    log('yellow', '\n╔════════════════════════════════════════════════════════╗');
    log('yellow', '║        BOTZZZ Comprehensive Test Suite Runner         ║');
    log('yellow', '╚════════════════════════════════════════════════════════╝\n');

    const testSuites = [
      {
        name: 'API Tests',
        path: path.join(__dirname, 'api-tests.js')
      },
      {
        name: 'Integration Tests',
        path: path.join(__dirname, 'integration-tests.js')
      }
    ];

    // Run each test suite
    for (const suite of testSuites) {
      try {
        await this.runTestSuite(suite.name, suite.path);
      } catch (error) {
        log('red', `Failed to run ${suite.name}: ${error.message}`);
      }
    }

    // Print final summary
    this.printSummary();

    // Exit with appropriate code
    const allPassed = this.results.suites.every(s => s.passed);
    process.exit(allPassed ? 0 : 1);
  }

  printSummary() {
    const duration = ((Date.now() - this.results.startTime) / 1000).toFixed(2);
    
    log('yellow', '\n╔════════════════════════════════════════════════════════╗');
    log('yellow', '║              Final Test Results Summary                ║');
    log('yellow', '╚════════════════════════════════════════════════════════╝\n');

    // Suite results
    this.results.suites.forEach(suite => {
      const icon = suite.passed ? '✓' : '✗';
      const color = suite.passed ? 'green' : 'red';
      log(color, `${icon} ${suite.name}`);
    });

    // Overall stats
    const passedSuites = this.results.suites.filter(s => s.passed).length;
    const totalSuites = this.results.suites.length;
    
    log('blue', `\n📊 Test Suites: ${passedSuites}/${totalSuites} passed`);
    log('blue', `⏱️  Duration: ${duration}s`);

    if (passedSuites === totalSuites) {
      log('green', '\n🎉 All test suites passed!');
      log('green', '✨ Your code is ready for production!');
    } else {
      log('red', '\n⚠️  Some test suites failed.');
      log('yellow', 'Please review the errors above and fix the issues.');
    }
  }
}

// Run tests
const runner = new TestRunner();
runner.runAll().catch(error => {
  log('red', `Fatal error: ${error.message}`);
  console.error(error);
  process.exit(1);
});

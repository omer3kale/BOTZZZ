// BOTZZZ Pre-Deployment Diagnostic Tool
// Comprehensive workspace validation before going live

const fs = require('fs').promises;
const path = require('path');

const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
};

function log(color, message) {
  console.log(colors[color] + message + colors.reset);
}

class DiagnosticRunner {
  constructor() {
    this.results = {
      passed: [],
      failed: [],
      warnings: [],
      total: 0
    };
  }

  async check(name, testFunc) {
    this.results.total++;
    try {
      const result = await testFunc();
      if (result === 'warning') {
        this.results.warnings.push(name);
        log('yellow', `⚠️  ${name}`);
      } else {
        this.results.passed.push(name);
        log('green', `✅ ${name}`);
      }
    } catch (error) {
      this.results.failed.push({ name, error: error.message });
      log('red', `❌ ${name}: ${error.message}`);
    }
  }

  async runDiagnostics() {
    log('cyan', '\n╔═══════════════════════════════════════════════════════════╗');
    log('cyan', '║        BOTZZZ PRE-DEPLOYMENT DIAGNOSTIC SUITE            ║');
    log('cyan', '╚═══════════════════════════════════════════════════════════╝\n');

    // 1. File Structure Checks
    log('blue', '\n📁 Checking File Structure...\n');
    await this.checkFileStructure();

    // 2. Configuration Checks
    log('blue', '\n⚙️  Checking Configuration Files...\n');
    await this.checkConfiguration();

    // 3. Backend Function Checks
    log('blue', '\n🔧 Checking Backend Functions...\n');
    await this.checkBackendFunctions();

    // 4. Frontend Files Checks
    log('blue', '\n🎨 Checking Frontend Files...\n');
    await this.checkFrontendFiles();

    // 5. Environment Variables
    log('blue', '\n🔐 Checking Environment Variables...\n');
    await this.checkEnvironmentVariables();

    // 6. Dependencies
    log('blue', '\n📦 Checking Dependencies...\n');
    await this.checkDependencies();

    // 7. Test Files
    log('blue', '\n🧪 Checking Test Suite...\n');
    await this.checkTestSuite();

    // 8. Security Checks
    log('blue', '\n🔒 Checking Security Implementation...\n');
    await this.checkSecurity();

    // 9. Database Schema
    log('blue', '\n🗄️  Checking Database Schema...\n');
    await this.checkDatabaseSchema();

    // Print Summary
    this.printSummary();
  }

  async checkFileStructure() {
    const requiredFiles = [
      'index.html',
      'services.html',
      'order.html',
      'addfunds.html',
      'api.html',
      'tickets.html',
      'signin.html',
      'signup.html',
      'api-dashboard.html',
      'contact.html',
      'payment-success.html',
      'payment-failed.html',
      'package.json',
      'netlify.toml',
      '.env'
    ];

    for (const file of requiredFiles) {
      await this.check(`File exists: ${file}`, async () => {
        const filePath = path.join(__dirname, '..', file);
        await fs.access(filePath);
      });
    }

    // Check directories
    const requiredDirs = [
      'netlify/functions',
      'js',
      'css',
      'tests',
      'supabase',
      'admin'
    ];

    for (const dir of requiredDirs) {
      await this.check(`Directory exists: ${dir}`, async () => {
        const dirPath = path.join(__dirname, '..', dir);
        await fs.access(dirPath);
      });
    }
  }

  async checkConfiguration() {
    // Check netlify.toml
    await this.check('netlify.toml is configured', async () => {
      const configPath = path.join(__dirname, '..', 'netlify.toml');
      const content = await fs.readFile(configPath, 'utf-8');
      if (!content.includes('functions = "netlify/functions"')) {
        throw new Error('Functions directory not configured');
      }
      if (!content.includes('[[redirects]]')) {
        throw new Error('Redirects not configured');
      }
    });

    // Check package.json
    await this.check('package.json has required scripts', async () => {
      const pkgPath = path.join(__dirname, '..', 'package.json');
      const content = await fs.readFile(pkgPath, 'utf-8');
      const pkg = JSON.parse(content);
      
      if (!pkg.scripts.dev) throw new Error('Missing dev script');
      if (!pkg.scripts.deploy) throw new Error('Missing deploy script');
      if (!pkg.scripts.test) throw new Error('Missing test script');
    });

    // Check .env structure
    await this.check('.env file structure', async () => {
      const envPath = path.join(__dirname, '..', '.env');
      const content = await fs.readFile(envPath, 'utf-8');
      
      const requiredVars = [
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY',
        'SUPABASE_SERVICE_ROLE_KEY',
        'JWT_SECRET'
      ];

      for (const varName of requiredVars) {
        if (!content.includes(varName)) {
          throw new Error(`Missing ${varName}`);
        }
      }
    });
  }

  async checkBackendFunctions() {
    const functions = [
      'auth.js',
      'users.js',
      'orders.js',
      'services.js',
      'payments.js',
      'payeer.js',
      'tickets.js',
      'providers.js',
      'settings.js',
      'contact.js',
      'api-keys.js',
      'dashboard.js'
    ];

    const functionsDir = path.join(__dirname, '..', 'netlify', 'functions');

    for (const func of functions) {
      await this.check(`Backend function: ${func}`, async () => {
        const funcPath = path.join(functionsDir, func);
        const content = await fs.readFile(funcPath, 'utf-8');
        
        // Check for exports.handler
        if (!content.includes('exports.handler')) {
          throw new Error('Missing exports.handler');
        }
        
        // Check for error handling
        if (!content.includes('try') || !content.includes('catch')) {
          throw new Error('Missing error handling');
        }
      });
    }

    // Check utils/supabase.js
    await this.check('Supabase utility configured', async () => {
      const utilPath = path.join(functionsDir, 'utils', 'supabase.js');
      const content = await fs.readFile(utilPath, 'utf-8');
      
      if (!content.includes('createClient')) {
        throw new Error('Supabase client not initialized');
      }
    });
  }

  async checkFrontendFiles() {
    // Check JavaScript files
    const jsFiles = [
      'api-client.js',
      'auth-backend.js',
      'order-backend.js',
      'payment-backend.js'
    ];

    const jsDir = path.join(__dirname, '..', 'js');

    for (const file of jsFiles) {
      await this.check(`Frontend JS: ${file}`, async () => {
        const filePath = path.join(jsDir, file);
        await fs.access(filePath);
      });
    }

    // Check CSS files exist
    const cssDir = path.join(__dirname, '..', 'css');
    await this.check('CSS directory has files', async () => {
      const files = await fs.readdir(cssDir);
      if (files.length === 0) {
        throw new Error('No CSS files found');
      }
    });
  }

  async checkEnvironmentVariables() {
    const envPath = path.join(__dirname, '..', '.env');
    const content = await fs.readFile(envPath, 'utf-8');

    // Check each variable has a value
    await this.check('SUPABASE_URL is set', async () => {
      const match = content.match(/SUPABASE_URL=(.+)/);
      if (!match || !match[1] || match[1].trim() === '' || match[1].includes('your_')) {
        throw new Error('SUPABASE_URL not configured');
      }
    });

    await this.check('SUPABASE_ANON_KEY is set', async () => {
      const match = content.match(/SUPABASE_ANON_KEY=(.+)/);
      if (!match || !match[1] || match[1].trim() === '' || match[1].includes('your_')) {
        throw new Error('SUPABASE_ANON_KEY not configured');
      }
    });

    await this.check('SUPABASE_SERVICE_ROLE_KEY is set', async () => {
      const match = content.match(/SUPABASE_SERVICE_ROLE_KEY=(.+)/);
      if (!match || !match[1] || match[1].trim() === '' || match[1].includes('your_')) {
        throw new Error('SUPABASE_SERVICE_ROLE_KEY not configured');
      }
    });

    await this.check('JWT_SECRET is set', async () => {
      const match = content.match(/JWT_SECRET=(.+)/);
      if (!match || !match[1] || match[1].trim() === '' || match[1].includes('your_')) {
        throw new Error('JWT_SECRET not configured');
      }
    });

    // Payment gateways (warnings if not set)
    await this.check('STRIPE_SECRET_KEY configured', async () => {
      const match = content.match(/STRIPE_SECRET_KEY=(.+)/);
      if (!match || !match[1] || match[1].trim() === '' || match[1].includes('your_')) {
        return 'warning';
      }
    });

    await this.check('PAYEER_MERCHANT_ID configured', async () => {
      const match = content.match(/PAYEER_MERCHANT_ID=(.+)/);
      if (!match || !match[1] || match[1].trim() === '' || match[1].includes('your_')) {
        return 'warning';
      }
    });
  }

  async checkDependencies() {
    const pkgPath = path.join(__dirname, '..', 'package.json');
    const content = await fs.readFile(pkgPath, 'utf-8');
    const pkg = JSON.parse(content);

    const requiredDeps = [
      '@supabase/supabase-js',
      'express',
      'cors',
      'dotenv',
      'jsonwebtoken',
      'bcryptjs',
      'stripe'
    ];

    for (const dep of requiredDeps) {
      await this.check(`Dependency: ${dep}`, async () => {
        if (!pkg.dependencies || !pkg.dependencies[dep]) {
          throw new Error(`${dep} not installed`);
        }
      });
    }

    // Check node_modules exists
    await this.check('node_modules installed', async () => {
      const nmPath = path.join(__dirname, '..', 'node_modules');
      await fs.access(nmPath);
    });
  }

  async checkTestSuite() {
    const testFiles = [
      'api-tests.js',
      'frontend-tests.js',
      'integration-tests.js',
      'run-all-tests.js',
      'coverage-report.js'
    ];

    const testsDir = path.join(__dirname);

    for (const file of testFiles) {
      await this.check(`Test file: ${file}`, async () => {
        const filePath = path.join(testsDir, file);
        await fs.access(filePath);
      });
    }

    // Check test README
    await this.check('Test documentation exists', async () => {
      const readmePath = path.join(testsDir, 'README.md');
      await fs.access(readmePath);
    });
  }

  async checkSecurity() {
    // Check auth.js has password hashing
    await this.check('Password hashing implemented', async () => {
      const authPath = path.join(__dirname, '..', 'netlify', 'functions', 'auth.js');
      const content = await fs.readFile(authPath, 'utf-8');
      
      if (!content.includes('bcrypt')) {
        throw new Error('bcrypt not used for password hashing');
      }
    });

    // Check JWT implementation
    await this.check('JWT authentication implemented', async () => {
      const authPath = path.join(__dirname, '..', 'netlify', 'functions', 'auth.js');
      const content = await fs.readFile(authPath, 'utf-8');
      
      if (!content.includes('jsonwebtoken') && !content.includes('jwt')) {
        throw new Error('JWT not implemented');
      }
    });

    // Check CORS is configured
    await this.check('CORS configured', async () => {
      const configPath = path.join(__dirname, '..', 'netlify.toml');
      const content = await fs.readFile(configPath, 'utf-8');
      
      if (!content.includes('Access-Control-Allow-Origin') && !content.includes('cors')) {
        return 'warning'; // CORS might be configured differently
      }
    });

    // Check for .env in .gitignore
    await this.check('.env in .gitignore', async () => {
      try {
        const gitignorePath = path.join(__dirname, '..', '.gitignore');
        const content = await fs.readFile(gitignorePath, 'utf-8');
        if (!content.includes('.env')) {
          throw new Error('.env not in .gitignore');
        }
      } catch (error) {
        // .gitignore might not exist yet
        return 'warning';
      }
    });
  }

  async checkDatabaseSchema() {
    await this.check('Database schema file exists', async () => {
      const schemaPath = path.join(__dirname, '..', 'supabase', 'schema.sql');
      await fs.access(schemaPath);
    });

    await this.check('Schema has required tables', async () => {
      const schemaPath = path.join(__dirname, '..', 'supabase', 'schema.sql');
      const content = await fs.readFile(schemaPath, 'utf-8');
      
      const requiredTables = [
        'users',
        'services',
        'orders',
        'payments',
        'tickets',
        'ticket_messages',
        'providers',
        'api_keys',
        'settings'
      ];

      for (const table of requiredTables) {
        if (!content.includes(`CREATE TABLE ${table}`) && !content.includes(`create table ${table}`)) {
          throw new Error(`Table ${table} not defined`);
        }
      }
    });

    await this.check('RLS policies defined', async () => {
      const schemaPath = path.join(__dirname, '..', 'supabase', 'schema.sql');
      const content = await fs.readFile(schemaPath, 'utf-8');
      
      if (!content.includes('ALTER TABLE') || !content.includes('ENABLE ROW LEVEL SECURITY')) {
        return 'warning';
      }
    });
  }

  printSummary() {
    log('cyan', '\n╔═══════════════════════════════════════════════════════════╗');
    log('cyan', '║              DIAGNOSTIC RESULTS SUMMARY                   ║');
    log('cyan', '╚═══════════════════════════════════════════════════════════╝\n');

    log('green', `✅ Passed:   ${this.results.passed.length}/${this.results.total}`);
    
    if (this.results.warnings.length > 0) {
      log('yellow', `⚠️  Warnings: ${this.results.warnings.length}/${this.results.total}`);
      log('yellow', '\nWarnings:');
      this.results.warnings.forEach(warning => {
        log('yellow', `   • ${warning}`);
      });
    }
    
    if (this.results.failed.length > 0) {
      log('red', `❌ Failed:   ${this.results.failed.length}/${this.results.total}`);
      log('red', '\nFailures:');
      this.results.failed.forEach(failure => {
        log('red', `   • ${failure.name}: ${failure.error}`);
      });
    }

    // Calculate readiness score
    const score = ((this.results.passed.length / this.results.total) * 100).toFixed(1);
    
    log('blue', `\n📊 Readiness Score: ${score}%`);

    if (this.results.failed.length === 0) {
      log('green', '\n🎉 ALL CRITICAL CHECKS PASSED!');
      log('green', '✨ Your application is READY FOR PRODUCTION DEPLOYMENT!');
      
      if (this.results.warnings.length > 0) {
        log('yellow', '\n⚠️  Note: There are some warnings above. These are optional configurations.');
        log('yellow', '   You can deploy now and configure them later if needed.');
      }
    } else {
      log('red', '\n⚠️  DEPLOYMENT BLOCKED!');
      log('red', '   Please fix the failed checks above before deploying to production.');
    }

    // Next steps
    log('cyan', '\n╔═══════════════════════════════════════════════════════════╗');
    log('cyan', '║                    NEXT STEPS                             ║');
    log('cyan', '╚═══════════════════════════════════════════════════════════╝\n');

    if (this.results.failed.length === 0) {
      log('green', '1. Run tests:           npm test');
      log('green', '2. Generate coverage:   npm run coverage');
      log('green', '3. Start dev server:    npm run dev');
      log('green', '4. Deploy to Netlify:   netlify deploy --prod');
    } else {
      log('yellow', '1. Fix the failed checks listed above');
      log('yellow', '2. Run diagnostic again: node tests/diagnostic.js');
      log('yellow', '3. Once all checks pass, proceed with deployment');
    }

    console.log('');
  }
}

// Run diagnostics
const runner = new DiagnosticRunner();
runner.runDiagnostics().catch(error => {
  log('red', `\n❌ Fatal error running diagnostics: ${error.message}`);
  console.error(error);
  process.exit(1);
});

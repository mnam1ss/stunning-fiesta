# Security Report

## Vulnerabilities Found and Fixed

### 1. XML External Entity (XXE) Vulnerability - FIXED ✓
**Severity**: Medium  
**Location**: `scripts/news_bot.py` (parse_rss function)  
**Issue**: The script used `xml.etree.ElementTree.fromstring()` to parse RSS feeds, which is vulnerable to XML External Entity (XXE) attacks and XML bombs.

**Fix Applied**: 
- Updated to use `defusedxml.ElementTree` which provides protection against XXE attacks
- Added fallback with warning if defusedxml is not installed
- Created `requirements.txt` to document the dependency

**Recommendation**: Install defusedxml with `pip install defusedxml`

### 2. Exposed Supabase API Key - REQUIRES ACTION ⚠️
**Severity**: High  
**Location**: `_includes/bot-tracker.html` (config object)  
**Issue**: Supabase API key is hardcoded in client-side JavaScript and exposed in public repository.

**Current Status**: 
- This appears to be a Supabase "anon" key which is designed for client-side use
- However, the key has been exposed in the repository history

**Actions Required**:
1. **Immediately rotate the Supabase API key** in your Supabase dashboard
2. Verify that Row-Level Security (RLS) policies are properly configured on all tables
3. Consider using environment variables via Jekyll configuration
4. For sensitive operations, use server-side Supabase functions with service role keys

**Temporary Mitigation**:
- Changed debug mode from `true` to `false` to prevent information leakage
- Added security warnings in code comments

### 3. Debug Mode Enabled - FIXED ✓
**Severity**: Low  
**Location**: `_includes/bot-tracker.html` (config object)  
**Issue**: Debug mode was enabled, potentially leaking information in production.

**Fix Applied**: Changed `debug: true` to `debug: false`

## Recommendations

1. **Rotate API Keys**: Any API key committed to a public repository should be considered compromised
2. **Use Environment Variables**: Store sensitive configuration in environment variables, not in code
3. **Implement Proper Secret Management**: Use tools like GitHub Secrets for CI/CD workflows
4. **Regular Security Audits**: Run security scanners regularly
5. **Install Security Dependencies**: Run `pip install -r requirements.txt` to ensure secure XML parsing

## Security Best Practices

- Never commit API keys, passwords, or tokens to version control
- Use `.env` files (and add them to `.gitignore`) for local development
- Use environment variables or secret management systems in production
- Regularly scan dependencies for known vulnerabilities
- Keep all dependencies up to date
- Enable and properly configure Row-Level Security (RLS) for databases

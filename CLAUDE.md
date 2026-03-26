# Project Instructions for Claude

This is the jira-discovery project containing the JC CLI tool.

## Shell Preference
Always use PowerShell 7 (pwsh) for Windows commands in this project.
Command format: `pwsh -Command "..."`

## Project Context
- JC CLI tool for Jira & Confluence
- Main file: jc.py
- User's PowerShell 7 profile has JC alias installed
- Location: C:\Users\kevin.mbuluko\projects\jira-discovery\

## Development Best Practices (CRITICAL - READ THIS FIRST)

### Test-Driven Development (TDD)
**ALWAYS follow these testing practices when developing new features:**

1. **Write Tests FIRST or IMMEDIATELY After Implementation**
   - For new features: Write tests before or immediately after implementing
   - For bug fixes: Add a test that reproduces the bug before fixing it
   - Never consider a feature "complete" without tests

2. **Run Tests After Writing Them**
   - ALWAYS run tests immediately after writing them to verify they work
   - Use: `pwsh -Command "python -m pytest test_jc.py::TestClassName::test_method_name -v"`
   - For full suite: `pwsh -Command "python -m pytest test_jc.py -v"`
   - Never assume tests work without running them

3. **Test Coverage Requirements**
   - All new functions must have unit tests
   - All new CLI commands must have integration tests
   - All edge cases and error conditions must be tested
   - Aim for >90% code coverage

4. **Test Quality Standards**
   - Tests must be descriptive: `test_<feature>_<scenario>`
   - Use Arrange-Act-Assert pattern
   - Mock external dependencies (API calls, file system)
   - Include both positive and negative test cases

### Code Quality Best Practices

1. **SOLID Principles**
   - Single Responsibility: Each function/class should do one thing well
   - Open/Closed: Open for extension, closed for modification
   - Don't Repeat Yourself (DRY): Extract common logic into reusable functions

2. **Error Handling**
   - Always handle edge cases explicitly
   - Provide clear, user-friendly error messages
   - Never let exceptions crash the CLI silently

3. **Code Review Checklist (Review Your Own Code)**
   - ✓ Does it follow existing patterns in the codebase?
   - ✓ Are variable/function names clear and descriptive?
   - ✓ Is there duplicated code that should be extracted?
   - ✓ Are there error cases that aren't handled?
   - ✓ Is the code testable?
   - ✓ Are tests written and passing?

4. **Documentation**
   - Update CLI_README.md for user-facing features
   - Update TESTING.md when adding new test categories
   - Add docstrings to all new functions
   - Keep CHEATSHEET.md updated with new commands

### Development Workflow

1. **Before implementing a feature:**
   ```
   1. Understand the requirement fully
   2. Check existing code for similar patterns
   3. Design the solution (consider edge cases)
   4. Write tests first (TDD) or plan tests immediately
   ```

2. **While implementing:**
   ```
   1. Follow existing code patterns and structure
   2. Keep functions small and focused
   3. Add comments for complex logic only (code should be self-documenting)
   4. Handle errors gracefully
   ```

3. **After implementing:**
   ```
   1. Write tests if not done yet (REQUIRED)
   2. Run tests and verify they pass
   3. Test the feature manually with real data
   4. Update documentation (README, TESTING.md)
   5. Review your own code against the checklist above
   ```

### Testing Commands Quick Reference
```bash
# Run specific test
pwsh -Command "python -m pytest test_jc.py::TestClassName::test_method -v"

# Run all tests for a class
pwsh -Command "python -m pytest test_jc.py::TestClassName -v"

# Run tests matching a pattern
pwsh -Command "python -m pytest test_jc.py -k 'pattern' -v"

# Run full suite
pwsh -Command "python -m pytest test_jc.py -v"

# Run with coverage
pwsh -Command "python -m pytest test_jc.py --cov=jc --cov-report=term-missing"
```

### Common Mistakes to Avoid

1. ❌ **Implementing features without tests**
   - ✅ Always write tests - they catch bugs and document behavior

2. ❌ **Not running tests after writing them**
   - ✅ Run tests immediately to verify they work correctly

3. ❌ **Copying code without understanding patterns**
   - ✅ Study existing code structure before adding new features

4. ❌ **Adding features without updating documentation**
   - ✅ Update README and relevant docs as part of the feature

5. ❌ **Ignoring edge cases and error conditions**
   - ✅ Think through and test edge cases explicitly

6. ❌ **Creating duplicate code instead of reusing**
   - ✅ Extract common functionality into shared utilities

### When in Doubt
- Look at existing similar features for patterns
- Write tests to clarify expected behavior
- Ask questions before implementing if requirements are unclear
- Keep it simple - don't over-engineer

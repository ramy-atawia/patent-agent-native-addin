# Tests Directory - Clean & Simple

## 📁 **Current Structure**

```
tests/
├── functional/
│   └── comprehensive_test_quick.py    # Core functionality tests (3 tests)
├── performance/
│   └── test_multiple_scenarios.py     # Performance tests (2 scenarios)
├── data/                              # Test data and archives
├── logs/                              # Test execution logs
└── README.md                          # This file
```

## 🎯 **What Each Test Does**

### **Functional Tests** (`tests/functional/`)
- **`comprehensive_test_quick.py`** - Tests core system functionality
  - Basic conversation handling
  - Tool execution (patent drafting)
  - Context awareness across messages

### **Performance Tests** (`tests/performance/`)
- **`test_multiple_scenarios.py`** - Tests system performance and reliability
  - AI patent scenario (complex algorithms)
  - Software patent scenario (user interface)

## 🚀 **How to Run Tests**

### **Run All Tests:**
```bash
python3 run_tests_simple.py
```

### **Run Individual Test Categories:**
```bash
# Core functionality only
python3 tests/functional/comprehensive_test_quick.py

# Performance only  
python3 tests/performance/test_multiple_scenarios.py
```

## 🧹 **What Was Removed**

The following **old, complex, and conflicting** test files were removed:
- ❌ `comprehensive_test.py` (1005 lines - overly complex)
- ❌ `expanded_comprehensive_test.py` (826 lines - redundant)
- ❌ `legal_tech_scenarios_test.py` (557 lines - not focused)
- ❌ `tests/scripts/` directory (unnecessary abstraction)
- ❌ `tests/config/` directory (over-engineered configuration)

## 💡 **Why This Structure?**

1. **Simple**: Only essential tests, no complexity
2. **Fast**: 5-15 minutes total execution time
3. **Clear**: Each test has a specific purpose
4. **Maintainable**: Easy to understand and modify
5. **Reliable**: No race conditions or orchestration issues

## 📊 **Expected Results**

- **Total Tests**: 5 (3 functional + 2 performance)
- **Success Rate**: 90%+ (core functionality should work)
- **Execution Time**: 5-15 minutes
- **Output**: Clear pass/fail for each test

The new structure focuses on **testing what matters most** without the complexity that was causing timeouts and failures.

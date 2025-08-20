#!/usr/bin/env python3
"""
Simple Test Runner for Patent Drafting System
============================================

Clean, simple test runner that focuses on essential functionality
without the complexity of the orchestrator system.
"""

import subprocess
import sys
import time
from pathlib import Path

def run_test(test_name, script_path, timeout=300):
    """Run a single test with timeout."""
    print(f"\n🧪 Running: {test_name}")
    print(f"📁 Script: {script_path}")
    print(f"⏱️  Timeout: {timeout}s")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            ["python3", str(script_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=Path(__file__).parent.parent
        )
        
        duration = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ {test_name} PASSED ({duration:.1f}s)")
            return True
        else:
            print(f"❌ {test_name} FAILED ({duration:.1f}s)")
            print(f"   Return Code: {result.returncode}")
            if result.stdout:
                print(f"   Stdout: {result.stdout[-500:]}...")
            if result.stderr:
                print(f"   Stderr: {result.stderr[:500]}...")
            return False
            
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        print(f"⏰ {test_name} TIMEOUT after {duration:.1f}s")
        return False
    except Exception as e:
        duration = time.time() - start_time
        print(f"💥 {test_name} ERROR after {duration:.1f}s: {e}")
        return False

def main():
    """Run essential tests."""
    print("🚀 Patent Drafting System - Comprehensive Test Suite")
    print("=" * 70)
    print("🎯 Testing core functionality + edge cases + performance + advanced tech + quality")
    print("⏱️  Expected time: 25-45 minutes")
    print("=" * 70)
    
    # Define test phases
    phases = [
        {
            "name": "Phase 1: Session Management & Regression",
            "script": "tests/regression/test_session_regression.py",
            "timeout": 300,  # 5 minutes
            "description": "Session management, multi-turn conversations, session persistence"
        },
        {
            "name": "Phase 2: Draft Claims Regression",
            "script": "tests/regression/test_draft_claims_regression.py",
            "timeout": 300,  # 5 minutes
            "description": "Patent claim drafting, claim generation, claim quality"
        },
        {
            "name": "Phase 3: Review Claims Regression",
            "script": "tests/regression/test_review_claims_regression.py",
            "timeout": 300,  # 5 minutes
            "description": "Claim review, validation, error detection"
        },
        {
            "name": "Phase 4: Software Engineering & Telecom",
            "script": "tests/software_networking_test.py",
            "timeout": 900,  # 15 minutes
            "description": "Software architecture, networking protocols, 5G telecom, cybersecurity"
        },
        {
            "name": "Phase 5: Confidence Threshold & Memory",
            "script": "tests/regression/test_confidence_threshold.py",
            "timeout": 300,  # 5 minutes
            "description": "Confidence scoring, conversation memory, context awareness"
        }
    ]
    
    # Check if test files exist
    for phase in phases:
        if not Path(phase["script"]).exists():
            print(f"❌ Test script not found: {phase['script']}")
            sys.exit(1)
    
    print(f"\n🔄 Starting {len(phases)} test phases...")
    start_time = time.time()
    
    # Run test phases
    results = []
    for i, phase in enumerate(phases, 1):
        print(f"\n{'='*70}")
        print(f"🚀 PHASE {i}: {phase['name']}")
        print(f"📝 {phase['description']}")
        print(f"{'='*70}")
        
        success = run_test(phase["name"], phase["script"], phase["timeout"])
        results.append((phase["name"], success))
        
        # Brief pause between phases
        if i < len(phases):
            print("⏸️  Pausing 3 seconds between phases...")
            time.sleep(3)
    
    # Summary
    total_time = time.time() - start_time
    passed = sum(1 for _, success in results if success)
    failed = len(results) - passed
    
    print(f"\n{'='*70}")
    print(f"📊 COMPREHENSIVE TEST SUMMARY")
    print(f"{'='*70}")
    print(f"✅ Passed: {passed}/{len(results)} phases")
    print(f"❌ Failed: {failed}/{len(results)} phases")
    print(f"📈 Success Rate: {(passed/len(results)*100):.1f}%")
    print(f"⏱️  Total Time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
    
    # Phase-by-phase results
    print(f"\n📋 Phase Results:")
    for i, (phase_name, success) in enumerate(results, 1):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   Phase {i}: {status} - {phase_name}")
    
    # Overall assessment
    if failed == 0:
        print(f"\n🎉 All test phases passed!")
        print(f"✅ System is ready for production use")
        print(f"🚀 Advanced technical capabilities validated")
        print(f"🎯 Patent claim quality assessed and validated")
        sys.exit(0)
    elif passed >= len(results) * 0.8:  # At least 4/5 phases passed
        print(f"\n⚠️  Most test phases passed")
        print(f"✅ Core functionality is working")
        print(f"🔧 Some advanced features need attention")
        sys.exit(1)
    else:
        print(f"\n❌ Multiple test phases failed")
        print(f"🔧 Core functionality needs investigation")
        sys.exit(1)

if __name__ == "__main__":
    main()

"""Run all four tasks' tests: python test_homework.py"""

from pathlib import Path
import sys
import unittest


def run_tests(task_number=None):
    """Run one task's tests, or all tasks, and return a failing exit code on failure."""
    project_directory = str(Path(__file__).resolve().parent)
    pattern = "test_task_*.py" if task_number is None else f"test_task_{task_number}.py"
    label = "All tasks" if task_number is None else f"Task {task_number}"
    print(f"\n{label}: running tests...", flush=True)
    suite = unittest.defaultTestLoader.discover(
        start_dir=project_directory,
        pattern=pattern,
    )
    if suite.countTestCases() == 0:
        print(f"FAIL: no tests found for {label}.")
        raise SystemExit(1)
    result = unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(suite)
    if result.wasSuccessful():
        print(f"PASS: {label} - all {result.testsRun} tests passed.")
    else:
        print(f"FAIL: {label} - see the failed checks above.")
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    run_tests()

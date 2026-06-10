"""
╔══════════════════════════════════════════════════════════════════╗
║  CodeToAGI — Episode 19: Context Managers                        ║
║  CHALLENGE SOLUTION: Thread-Safe Lock Manager                    ║
║                                                                  ║
║  Challenge: Build a @contextmanager that wraps threading.Lock    ║
║  and prove no race condition with 3 threads × 1000 writes each  ║
╚══════════════════════════════════════════════════════════════════╝
"""

from contextlib import contextmanager
import threading
import time


# ════════════════════════════════════════════════════════════════
#  PART 1 — The Context Manager
# ════════════════════════════════════════════════════════════════

@contextmanager
def locked(lock):
    """
    A context manager that acquires a threading.Lock on entry
    and releases it on exit — guaranteed even if an exception occurs.

    Usage:
        my_lock = threading.Lock()
        with locked(my_lock):
            # only one thread runs this block at a time
            shared_list.append(value)
    """
    lock.acquire()
    try:
        yield lock          # yield the lock itself (optional — rarely needed)
    finally:
        lock.release()      # ALWAYS releases — even on exception


# ════════════════════════════════════════════════════════════════
#  PART 2 — Proving It Works: 3 threads × 1000 writes
# ════════════════════════════════════════════════════════════════

shared_list = []
my_lock     = threading.Lock()
WRITES_PER_THREAD = 1000


def worker(thread_id):
    """Each thread appends 1000 items to shared_list under the lock."""
    for i in range(WRITES_PER_THREAD):
        with locked(my_lock):
            shared_list.append(f"T{thread_id}-item{i}")


def run_demo():
    print("=" * 55)
    print("  CodeToAGI EP19 — Thread-Safe Lock Manager Challenge")
    print("=" * 55)

    # ── Without lock (to show the problem) ──────────────────
    print("\n[ WITHOUT lock — race condition possible ]\n")
    unsafe_list = []

    def unsafe_worker(tid):
        for i in range(WRITES_PER_THREAD):
            unsafe_list.append(f"T{tid}-item{i}")   # no lock

    threads = [threading.Thread(target=unsafe_worker, args=(i,)) for i in range(3)]
    start = time.perf_counter()
    for t in threads: t.start()
    for t in threads: t.join()
    elapsed = time.perf_counter() - start

    print(f"  Threads: 3   Writes/thread: {WRITES_PER_THREAD}")
    print(f"  Expected total: {3 * WRITES_PER_THREAD}")
    print(f"  Actual total:   {len(unsafe_list)}")
    note = "✓ OK (list.append is GIL-safe in CPython)" if len(unsafe_list) == 3000 \
           else "✗ Race condition detected!"
    print(f"  Note: {note}")
    print(f"  Time: {elapsed:.4f}s\n")

    # ── With our locked() context manager ───────────────────
    print("[ WITH locked() context manager — guaranteed safe ]\n")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
    start = time.perf_counter()
    for t in threads: t.start()
    for t in threads: t.join()
    elapsed = time.perf_counter() - start

    expected = 3 * WRITES_PER_THREAD
    actual   = len(shared_list)
    status   = "✓ PASS" if actual == expected else "✗ FAIL"

    print(f"  Threads: 3   Writes/thread: {WRITES_PER_THREAD}")
    print(f"  Expected total: {expected}")
    print(f"  Actual total:   {actual}   {status}")
    print(f"  Time: {elapsed:.4f}s")

    # Verify ordering sanity — first 5 and last 5
    print(f"\n  First 5 entries: {shared_list[:5]}")
    print(f"  Last  5 entries: {shared_list[-5:]}")

    print("\n" + "=" * 55)
    print("  Context Manager Protocol recap:")
    print("  lock.acquire()  ←→  __enter__")
    print("  yield           ←→  body of with block")
    print("  lock.release()  ←→  __exit__  (always runs)")
    print("=" * 55)


# ════════════════════════════════════════════════════════════════
#  PART 3 — BONUS: reusable LockManager class (class-based)
# ════════════════════════════════════════════════════════════════

class LockManager:
    """
    Class-based version of the same pattern — for comparison.
    Shows __enter__ and __exit__ explicitly.
    """

    def __init__(self, lock):
        self.lock = lock

    def __enter__(self):
        self.lock.acquire()
        return self.lock          # returned as the 'as' value

    def __exit__(self, exc_type, exc_val, tb):
        self.lock.release()
        return False              # don't suppress exceptions


def run_class_based_demo():
    print("\n[ BONUS — Class-based LockManager ]\n")
    results = []
    lock    = threading.Lock()

    def class_worker(tid):
        for i in range(500):
            with LockManager(lock):
                results.append(f"T{tid}-{i}")

    threads = [threading.Thread(target=class_worker, args=(i,)) for i in range(3)]
    for t in threads: t.start()
    for t in threads: t.join()

    expected = 3 * 500
    status   = "✓ PASS" if len(results) == expected else "✗ FAIL"
    print(f"  Class-based LockManager: {len(results)}/{expected}  {status}")


# ════════════════════════════════════════════════════════════════
#  PART 4 — BONUS: exception safety test
# ════════════════════════════════════════════════════════════════

def run_exception_safety_test():
    """Prove the lock is ALWAYS released even when an exception is raised."""
    print("\n[ BONUS — Exception Safety Test ]\n")
    lock = threading.Lock()

    print("  Acquiring lock inside locked() then raising an exception...")
    try:
        with locked(lock):
            raise ValueError("Simulated crash inside with block!")
    except ValueError as e:
        print(f"  Exception caught: {e}")

    # If lock was not released, this acquire would block forever
    acquired = lock.acquire(blocking=False)
    if acquired:
        lock.release()
        print("  ✓ Lock was released despite the exception — finally block worked!")
    else:
        print("  ✗ Lock was NOT released — bug in implementation!")


# ════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_demo()
    run_class_based_demo()
    run_exception_safety_test()

    print("\n  Challenge complete! 🎉")
    print("  Drop your version in the comments @CodeToAGI")

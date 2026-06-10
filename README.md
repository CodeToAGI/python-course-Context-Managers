# CodeToAGI — Episode 19: Context Managers

> **Series:** Python to Agentic AI — Free Complete Course  
> **Channel:** [@CodeToAGI](https://youtube.com/@CodeToAGI) · Mahaz Abbasi  
> **Episode:** 19 / ongoing  
> **Topic:** `with` statement · `__enter__` · `__exit__` · `@contextmanager` · `contextlib`

---

## 📺 Watch the Episode

**[▶ Python Context Managers Explained in 10 Minutes | Ep 19](https://youtube.com/@CodeToAGI)**

---

## 🗂 What's in This Repo

```
ep19/
├── ep19_challenge_solution.py   ← Full challenge solution with 3 bonus tests
├── README.md                    ← This file
└── examples/
    ├── 01_with_vs_without.py    ← Resource leak demo
    ├── 02_class_based.py        ← ManagedFile with __enter__ / __exit__
    ├── 03_contextmanager.py     ← @contextmanager generator approach
    ├── 04_nested_with.py        ← Multiple context managers
    ├── 05_suppress.py           ← contextlib.suppress
    ├── 06_timer.py              ← Timer context manager
    └── 07_db_transaction.py     ← Mini project: DB transaction manager
```

---

## 📖 What You Will Learn

| Concept | What It Does |
|---|---|
| `with` statement | Automatic setup + teardown — no resource leaks |
| `__enter__` | Called on entry — returns the `as` value |
| `__exit__` | Called on exit — ALWAYS runs, even on exception |
| `@contextmanager` | Turn a generator function into a context manager |
| `yield` | Split point: code before = enter, code after = exit |
| `contextlib.suppress` | Silence specific exceptions in one line |
| Nested `with` | Multiple managers — close in LIFO order |
| Real patterns | Files, DB transactions, locks, timers, HTTP sessions |

---

## 🏆 Episode Challenge

**Build a Thread-Safe Lock Manager using `@contextmanager`**

### Your task:

```python
from contextlib import contextmanager
import threading

@contextmanager
def locked(lock):
    # YOUR CODE HERE
    # Step 1: acquire the lock
    # Step 2: yield
    # Step 3: release in finally (so it ALWAYS releases)
    pass

# Test it:
shared_list = []
my_lock = threading.Lock()

def worker(thread_id):
    for i in range(1000):
        with locked(my_lock):
            shared_list.append(f"T{thread_id}-item{i}")

# Run 3 threads
threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
for t in threads: t.start()
for t in threads: t.join()

print(len(shared_list))   # Should be exactly 3000
```

### Requirements:
- ✅ `locked()` acquires the lock in `__enter__` (before `yield`)
- ✅ `locked()` releases the lock in `finally` (after `yield`)
- ✅ Lock is released even if exception is raised inside `with` block
- ✅ 3 threads × 1000 writes = exactly 3000 items, no race condition
- ⭐ **Bonus:** also implement the class-based version with `__enter__` / `__exit__`
- ⭐ **Bonus:** write an exception safety test that proves the lock releases on crash

---

## 💡 Stuck? Try It Yourself First!

The challenge is designed to be solved with only the concepts from this episode:

1. `@contextmanager` from `contextlib`
2. `yield` as the boundary
3. `try / finally` for cleanup guarantee
4. `threading.Lock()` — just two methods: `.acquire()` and `.release()`

**Spend at least 20 minutes trying before looking at the solution.**  
The struggle is where the learning happens.

---

## ✅ Full Solution

The complete solution with 4 parts is in [`ep19_challenge_solution.py`](./ep19_challenge_solution.py):

- **Part 1** — `locked()` context manager implementation
- **Part 2** — 3-thread race condition proof (3000 writes)
- **Part 3** — Bonus: class-based `LockManager` with `__enter__` / `__exit__`
- **Part 4** — Bonus: exception safety test

Run it:
```bash
python ep19_challenge_solution.py
```

Expected output:
```
===================================================
  CodeToAGI EP19 — Thread-Safe Lock Manager Challenge
===================================================

[ WITHOUT lock — race condition possible ]
  Expected total: 3000
  Actual total:   3000
  Note: ✓ OK (list.append is GIL-safe in CPython)

[ WITH locked() context manager — guaranteed safe ]
  Expected total: 3000
  Actual total:   3000   ✓ PASS

[ BONUS — Exception Safety Test ]
  Exception caught: Simulated crash inside with block!
  ✓ Lock was released despite the exception — finally block worked!
```

---

## 🗺 Course Roadmap

| Episode | Topic | Status |
|---|---|---|
| EP15 | OOP Part 2 | ✅ Done |
| EP16 | Iterators & Generators | ✅ Done |
| EP17 | Decorators | ✅ Done |
| EP18 | Async & Await | ✅ Done |
| **EP19** | **Context Managers** | **← You are here** |
| EP20 | Testing with pytest | 🔜 Next |
| EP21 | Type Hints | 🔜 Coming |
| ... | → Agentic AI | 🎯 Goal |

---

## 🔗 Links

- 📺 **YouTube:** [youtube.com/@CodeToAGI](https://youtube.com/@CodeToAGI)
- 💻 **GitHub:** [github.com/CodeToAGI](https://github.com/CodeToAGI)
- 💬 **Comments:** Drop your solution on the video — Mahaz replies to every one

---

## ⚙️ Requirements

```bash
pip install contextlib2   # optional — contextlib is built-in in Python 3.x
```

All code in this episode uses **Python standard library only** — no installs needed.

```
Python 3.8+  ✅
```

---

*CodeToAGI — Python to Agentic AI, one episode at a time.*

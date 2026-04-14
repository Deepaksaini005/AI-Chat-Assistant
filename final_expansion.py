"""Final data expansion to reach 500+ examples"""
import json

def load_data():
    with open('chat_history.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def add_all_unique():
    data = load_data()
    existing_users = set()
    for ex in data:
        for msg in ex['messages']:
            if msg['role'] == 'user':
                existing_users.add(msg['content'].lower().strip())
    
    # New variations not yet in dataset
    new_examples = [
        ("Explain variables", "Variables are named containers storing values. They have type, scope, and lifecycle. Essential for any program."),
        ("What is a loop?", "Loops repeat block of code. For loop over sequences, while loop for conditions. Essential for processing collections."),
        ("What is an if statement?", "Conditional execution. Code runs if condition is true. Chains with elif and else. Foundation of logic."),
        ("What are functions?", "Reusable code blocks. Take parameters, return values. Reduce repetition. Essential for organization."),
        ("What are modules?", "Files containing Python code. Contain functions, classes, variables. Import to reuse. Organize large projects."),
        ("What is standard library?", "Built-in Python modules (os, sys, random, math). No installation needed. Extensive functionality."),
        ("What is pip?", "Package installer for Python. Download from PyPI. pip install package-name. Manage dependencies in requirements.txt."),
        ("What is virtualenv?", "Isolated Python environments. Different projects can use different versions. Python 3 includes venv built-in."),
        ("What is Jupyter?", "Interactive Python notebooks. Code, text, visualizations in one file. Great for data science, learning, sharing."),
        ("What is numpy?", "Numerical Python library. Arrays, mathematical functions. Foundation of scientific Python stack."),
        ("What is pandas?", "Data analysis library. DataFrames like Excel sheets. Clean, transform, analyze data easily."),
        ("What is matplotlib?", "Plotting library for visualizations. Line charts, scatter plots, histograms. Pair with pandas for analysis."),
        ("What is scikit-learn?", "Machine learning library. Classification, regression, clustering algorithms. Simple API, production-ready."),
        ("What is TensorFlow?", "Deep learning framework by Google. Neural networks, large-scale computation. PyTorch alternative."),
        ("What is PyTorch?", "Deep learning framework by Facebook. Dynamic computation graphs. Popular for research and production."),
        ("What is Keras?", "High-level deep learning API. Runs on TensorFlow. Easier API for beginners. Model training simplified."),
        ("What is Flask?", "Lightweight web framework. Minimal dependencies. Great for learning web development. Build REST APIs easily."),
        ("What is Django?", "Full-featured web framework. Includes ORM, admin, forms. Heavy but complete. Good for large projects."),
        ("What is SQLAlchemy?", "ORM for Python. Works with SQL databases. Abstract SQL, write Python. Production-ready."),
        ("What is pytest?", "Testing framework. Simple syntax. Fixtures for setup/teardown. Plugin ecosystem. Industry standard."),
        ("What is black?", "Code formatter for Python. Opinionated, less arguments. Enforces consistency. Zero configuration."),
        ("What is pylint?", "Code analyzer and linter. Checks style and errors. Configurable rules. Integrated with IDEs."),
        ("What is type checking?", "Validating types at development time. mypy for Python. Catches errors early. Optional type hints."),
        ("Why use type hints?", "Improves code readability. Enables better IDE support. Catches type errors early. Optional but recommended."),
        ("What is a decorator?", "Wrapper around function/class. Modifies behavior. @decorator_name syntax. Powerful and elegant."),
        ("What does *args do?", "Allows variable number of arguments. Collected as tuple. Used for flexible function signatures."),
        ("What does **kwargs do?", "Allows variable keyword arguments. Collected as dictionary. Useful for default values and options."),
        ("What is a generator?", "Function yielding values lazily. Memory efficient for large data. Enables elegant iteration."),
        ("What is list comprehension?", "Concise syntax for creating lists. [x*2 for x in range(5)]. More readable than loops."),
        ("What is dictionary comprehension?", "{k: v for...}. Concise syntax for dictionaries. Pairs well with zip()."),
        ("What is lambda?", "Anonymous function. lambda x: x*2. Used with map, filter, sort. Short one-liners only."),
        ("What is map?", "Apply function to every item. map(func, iterable). Returns iterator. Use comprehension usually better."),
        ("What is filter?", "Select items matching condition. filter(func, iterable). Returns iterator. Syntactic clarity varies."),
        ("What is any?", "Returns True if any element is truthy. Useful for conditions. Short-circuit evaluation."),
        ("What is all?", "Returns True if all elements are truthy. Useful for validation. Short-circuit evaluation."),
        ("What is enumerate?", "Get index and value in loop. [(i, val) for i, val enumerate(list)]. Cleaner than range(len())."),
        ("What is zip?", "Combine multiple iterables. zip(list1, list2). Iterate in parallel. Creates tuples of elements."),
        ("Tell me about immutability", "Immutable objects cannot change. Tuples, strings, numbers. Hashable, can be dict keys. Thread-safe."),
        ("Explain mutable vs immutable", "Mutable: lists, dicts can change. Immutable: tuples, strings cannot. Affects equality and hashing."),
        ("What is method chaining?", "Calling methods on return values. obj.method1().method2(). Readable and elegant. Requires returning self."),
        ("What is a context manager?", "with statement managing resources. __enter__ and __exit__ methods. Automatic cleanup. Used with files, locks."),
        ("What is assert?", "Statement for debugging. Raises AssertionError if false. Should not be production logic. Help find bugs."),
        ("What is debugging tools?", "pdb is Python debugger. Set breakpoints, step through code, inspect variables. Built-in, no install needed."),
        ("What is profiling?", "Measuring program performance. cProfile for timing. memory_profiler for memory. Find bottlenecks."),
        ("What is garbage collection?", "Automatic memory cleanup. Python removes unreferenced objects. Prevents memory leaks. Manual control possible."),
        ("What is serialization?", "Converting objects to bytes/string. pickle for Python objects, json for text. Enables storage and transmission."),
        ("Explain dependency injection", "Passing dependencies rather than creating. Functions take what they need. Improves testability and flexibility."),
        ("What is singleton pattern?", "Class with single instance. Shared globally. Useful for connection pools, logging. Can complicate testing."),
        ("What is factory pattern?", "Creating objects without specifying exact classes. Abstracts creation logic. Enables polymorphism in creation."),
        ("What is observer pattern?", "Subjects notify observers of changes. Loose coupling. Used in event systems and MVC. Complex can get messy."),
        ("What is strategy pattern?", "Encapsulating algorithms. Switching strategies at runtime. Avoids conditionals. Elegant solution for variants."),
        ("What is async programming?", "Non-blocking concurrent code. async/await syntax. Handles I/O efficiently. Single threaded but async."),
        ("What is a coroutine?", "Function pausing and resuming. async def creates coroutine. Enables efficient async. Different from threads."),
        ("What is event loop?", "Manages coroutines. asyncio.run() starts event loop. Switches between ready coroutines. Single threaded."),
        ("What is await?", "Pauses coroutine until result. Only in async functions. Returns immediately if result ready. Enables concurrent waits."),
        ("What is a future?", "Placeholder for eventual result. Can be resolved later. Base for promises in JavaScript. asyncio.Future."),
        ("What is thread safety?", "Code works correctly with multiple threads. Needs synchronization for shared data. Locks, semaphores, queues."),
        ("What is deadlock?", "Threads waiting on each other infinitely. Prevents progress. Avoid with careful lifecycle and timeouts."),
        ("What is race condition?", "Outcome depends on execution order. Unpredictable behavior. Synchronize shared data access."),
        ("What is livelock?", "Threads keep changing state but make no progress. Avoid with backoff strategies. Less common than deadlock."),
        ("What is a process?", "Independent Python interpreter. IPC for communication. Heavier than threads. True parallelism possible."),
        ("What is multiprocessing?", "Running multiple processes. Bypasses GIL for true parallelism. More complex than threading."),
        ("What is the GIL?", "Global Interpreter Lock in Python. Ensures thread safety internally. Only one thread executes bytecode at once."),
        ("How to get around GIL?", "Multiprocessing for true parallelism. asyncio for I/O bound. Threads still good for I/O. Numpy releases GIL."),
        ("What is a memory leak?", "Retained references preventing garbage collection. Causes growing memory usage. Circular references, caches, listeners."),
        ("How to detect memory leaks?", "Monitor memory over time. memory_profiler on specific functions. tracemalloc for traces. Check for reference cycles."),
        ("What is CPU profiling?", "Measuring function execution time. cProfile built-in. Line profiler for line-by-line. Finds bottlenecks."),
        ("What is memory profiling?", "Measuring memory usage per line. memory_profiler package. Enables tracking allocations. Find inefficiencies."),
        ("What is benchmarking?", "Measuring and comparing performance. Controlled test repeated multiple times. timeit standard library. Compare approaches."),
        ("What is optimization strategy?", "Measure first (profile). Find real bottlenecks. Try simple fixes first. Batch operations. Cache results."),
        ("What is premature optimization?", "Optimizing without measurement. Most code not bottleneck. Makes code complex. Focus on correctness first."),
        ("What is big data?", "Data too large for single machine. Requires distributed processing. Hadoop, Spark, cloud platforms. Challenges storage and processing."),
        ("What is machine learning workflow?", "Define problem, gather data, explore, preprocess, select model, train, evaluate, tune, deploy, monitor."),
        ("What is overfitting?", "Model memorizes training data. High train accuracy, low test. More complex model, not enough data, too many features."),
        ("What is underfitting?", "Model too simple for data. Low accuracy on both train and test. Add features, complex model, train longer."),
        ("What is cross validation?", "Splitting data into train/test folds. Evaluates on multiple splits. Better generalization estimate. Avoid lucky splits."),
        ("What is regularization?", "Preventing overfitting by limiting model. L1/L2 penalties. Dropout in neural networks. Simple often better than complex."),
    ]
    
    added = 0
    for user_text, asst_text in new_examples:
        user_lower = user_text.lower().strip()
        if user_lower not in existing_users:
            data.append({
                "id": f"final-{added}",
                "messages": [
                    {"role": "user", "content": user_text},
                    {"role": "assistant", "content": asst_text}
                ]
            })
            added += 1
    
    with open('chat_history.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Added {added} new examples")
    print(f"✓ Total: {len(data)} examples")
    return len(data)

if __name__ == "__main__":
    total = add_all_unique()
    pct = round(total / 500 * 100)
    print(f"\n📊 Dataset size: {total}/500 ({pct}%)")
    if total >= 500:
        print("🎉 TARGET REACHED!")
    else:
        print(f"📌 Need {500 - total} more examples")

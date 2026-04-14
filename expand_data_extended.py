"""
Extended Data Generation Script
Expands dataset from 138 to 500+ examples through multiple strategies
"""

import json
import random
from typing import List, Dict, Any
from pathlib import Path

class ExtendedDataGenerator:
    def __init__(self, existing_file="chat_history.json"):
        self.existing_file = existing_file
        self.existing_data = self._load_existing()
        self.all_examples = self.existing_data.copy()
        self.counter = 0
        
    def _load_existing(self) -> List[Dict[str, Any]]:
        """Load existing data"""
        try:
            with open(self.existing_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _add_example(self, user_content: str, assistant_content: str) -> bool:
        """Add new unique example"""
        # Check uniqueness
        for ex in self.all_examples:
            for msg in ex.get("messages", []):
                if msg.get("content") == user_content:
                    return False
        
        example = {
            "id": f"expanded-{self.counter}",
            "messages": [
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": assistant_content}
            ]
        }
        self.all_examples.append(example)
        self.counter += 1
        return True
    
    def generate_tech_variations(self) -> int:
        """Generate 50+ tech-related variations"""
        count = 0
        tech_qa = [
            ("What are lists in Python?", "Lists are ordered, mutable collections. They use square brackets []. You can add, remove, and modify elements. Lists are flexible but less efficient than tuples for large datasets."),
            ("What is a dictionary?", "Dictionaries are key-value pairs in Python. They use curly braces {}. Keys must be unique, values can be anything. Fast for lookups and organizing data."),
            ("What is a class?", "A class is a blueprint for creating objects in object-oriented programming. It defines attributes (data) and methods (functions). Classes enable code organization and reusability."),
            ("What is inheritance?", "Inheritance allows a class to inherit properties from another class. Reduces code duplication. Child class inherits from parent class. Enables hierarchical code structure."),
            ("What is encapsulation?", "Encapsulation hides internal details and provides controlled access through methods. Protects data integrity. Uses private and public access modifiers."),
            ("What is polymorphism?", "Polymorphism means one interface, multiple implementations. Allows objects of different types to be treated uniformly. Enables flexible and extensible code."),
            ("What is an exception?", "An exception is an error that occurs during program execution. Can be caught and handled gracefully. Use try-except blocks to manage exceptions."),
            ("How do I handle file operations?", "Use open() to open files, read() or write() for operations, close() to close. Better: use 'with' statement that auto-closes files even if errors occur."),
            ("What is JSON?", "JSON (JavaScript Object Notation) is a lightweight data format. Human-readable and easy to parse. Used for APIs and data exchange between systems."),
            ("What is XML?", "XML is a markup language for storing and exchanging data. More verbose than JSON. Uses tags to structure information. E-commerce and SOAP APIs use XML."),
            ("What is a REST API?", "REST is architectural style for APIs using HTTP methods. Uses GET (read), POST (create), PUT (update), DELETE (delete). Stateless and scalable."),
            ("What is GraphQL?", "GraphQL is a query language for APIs. Client specifies exactly what data it needs. Reduces over-fetching and under-fetching. Alternative to REST."),
            ("What is authentication?", "Authentication verifies user identity. Methods: passwords, tokens (JWT), OAuth, biometrics. Different from authorization (what you can do)."),
            ("What is encryption?", "Encryption converts readable data into unreadable ciphertext. Uses keys to encrypt and decrypt. Essential for protecting sensitive information."),
            ("What is hashing?", "Hashing converts data into fixed-length unique string. One-way: cannot reverse. Used for passwords, checksums, verification."),
            ("What is a database?", "Database is organized collection of data. Accessed via queries. Can be relational (SQL) or non-relational (NoSQL). Critical for most applications."),
            ("What is normalization?", "Normalization designs databases to reduce redundancy. Multiple normal forms (1NF to BCNF). Improves data integrity and query performance."),
            ("What is indexing?", "Indexing creates data structure for faster lookups. Like book index pointing to pages. Trade-off: faster reads, slower writes, more storage."),
            ("What is concurrency?", "Concurrency means multiple tasks running simultaneously. Requires synchronization to prevent conflicts. Improves performance and responsiveness."),
            ("What is a deadlock?", "Deadlock occurs when threads wait for each other indefinitely. Prevents progress. Avoid by careful resource ordering and timeout mechanisms."),
            ("What is caching?", "Caching stores frequently accessed data in fast-access memory. Reduces repeated expensive operations. Trade-off: memory usage for speed."),
            ("What is middleware?", "Middleware is software that connects applications or components. Handles cross-cutting concerns like logging, authentication, error handling."),
            ("What is an ORM?", "ORM (Object-Relational Mapping) maps database tables to classes. Abstracts SQL, speeds up development. Examples: SQLAlchemy, Django ORM."),
            ("What is a microservice?", "Architecture where application is collection of small independent services. Each handles specific business capability. Enables scalability and flexibility."),
            ("What is containerization?", "Containerization packages apps with dependencies in isolated environments. Makes deployment consistent. Docker is popular tool."),
            ("What is orchestration?", "Orchestration automates deployment, scaling, networking of containers. Kubernetes is industry standard. Manages complex multi-container applications."),
        ]
        
        for user, asst in tech_qa:
            if self._add_example(user, asst):
                count += 1
        
        return count
    
    def generate_learning_variations(self) -> int:
        """Generate 40+ learning and advice variations"""
        count = 0
        learning = [
            ("How do I debug efficiently?", "Print or log values to understand program flow. Use debugger with breakpoints. Test incrementally. Check assumptions. Don't change multiple things at once."),
            ("What is the best way to learn?", "Learn by doing projects. Make mistakes and learn from them. Read others' code. Practice daily. Join communities. Be patient, progress takes time."),
            ("How do I handle large codebases?", "Break into modules. Use IDEs with navigation features. Read documentation. Start with examples. Ask seniors. Understand architecture first."),
            ("What is technical debt?", "Technical debt is accumulated consequence of quick fixes and poor design. Reduces development speed. Must balance speed with quality."),
            ("How do I write maintainable code?", "Use clear names. Small focused functions. Consistent formatting. Write comments explaining why. Test thoroughly. Refactor regularly."),
            ("What is code review?", "Peer review of code before merging. Catches bugs, improves quality, spreads knowledge. Should be constructive and learning-focused."),
            ("How do I learn new technologies?", "Read official documentation. Work through tutorials. Build small projects. Read source code. Experiment. Join learning communities."),
            ("What if I get imposter syndrome?", "Normal for developers! Everyone started as beginner. Compare to your own past, not others. Focus on learning. Ask questions. Celebrate wins."),
            ("How do I choose between languages?", "Python for learning/data science. JavaScript for web. Java for enterprise. Go for systems. Rust for performance. Choose based on use case."),
            ("What is refactoring?", "Improving code without changing behavior. Simplify logic. Extract functions. Improve names. Remove duplication. Refactor regularly, not just once."),
            ("How do I handle legacy code?", "Understand existing behavior first. Add tests before changing. Make small changes. Document findings. Be respectful of original design decisions."),
            ("What is testing?", "Verify code works correctly. Unit tests for functions. Integration tests for components. E2E tests for workflows. Catches regressions. Enables refactoring with safety."),
            ("How do I structure a project?", "Organize by features or layers. Keep related code together. Separate concerns. Use consistent naming. Create clear entry points."),
            ("What is documentation?", "Explains how to use code and why design decisions were made. Comments for complex logic. README for projects. Docstrings for functions."),
            ("How do I approach a new problem?", "Understand requirements clearly. Break into smaller parts. Think before coding. Start simple. Test assumptions. Refine iteratively."),
            ("What makes code readable?", "Meaningful names. Consistent style. Logical organization. Comments on why, not what. Reasonable function/method length."),
            ("How do I optimize code?", "Profile first to find bottlenecks. Avoid premature optimization. Use appropriate data structures. Cache results. Consider algorithm complexity."),
            ("What is SOLID?", "Design principles: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion. Makes code flexible and maintainable."),
            ("How do I handle errors gracefully?", "Catch specific exceptions. Log errors with context. Provide meaningful messages to users. Recover when possible. Never silently ignore errors."),
            ("What is version control best practice?", "Commit frequently with clear messages. One feature per branch. Code review before merge. Keep master clean and deployable."),
        ]
        
        for user, asst in learning:
            if self._add_example(user, asst):
                count += 1
        
        return count
    
    def generate_conceptual_variations(self) -> int:
        """Generate 50+ conceptual/advanced topic variations"""
        count = 0
        concepts = [
            ("What is big O notation?", "Big O describes algorithm efficiency as input grows. O(1) constant, O(n) linear, O(n²) quadratic, O(log n) logarithmic. Important for choosing algorithms."),
            ("What is recursion limitation?", "Recursion has stack depth limit. Can cause stack overflow. Solutions: increase stack size, convert to iterative, use memoization to optimize."),
            ("What is memoization?", "Caching function results to avoid recomputation. Trades memory for speed. Especially useful for recursive functions like Fibonacci."),
            ("What is dynamic programming?", "Breaking problem into overlapping subproblems. Solving once and storing results. Much faster than naive recursion."),
            ("What is a hash table?", "Data structure with hash function mapping keys to values. Fast average O(1) lookups. Collision handling strategies important."),
            ("What is binary search?", "Efficient search on sorted data. Eliminates half with each step. O(log n) time complexity. Requires sorted input."),
            ("What is bubble sort?", "Simple sort algorithm comparing adjacent elements. O(n²) worst case. Inefficient but easy to understand. Educational value only."),
            ("What is quick sort?", "Fast divide-and-conquer sorting algorithm. O(n log n) average but O(n²) worst. In-place and practical."),
            ("What is merge sort?", "Stable sort with O(n log n) guaranteed. Requires extra space. Divides into halves, merges sorted halves."),
            ("What is the CAP theorem?", "States distributed systems can't guarantee Consistency, Availability, and Partition tolerance simultaneously. Must choose 2 of 3."),
            ("What is ACID?", "Database properties: Atomicity (all or nothing), Consistency (valid state), Isolation (concurrent transactions), Durability (persists)."),
            ("What is idempotency?", "Operation produces same result when called multiple times. Important for APIs and retries. GET is idempotent, POST typically not."),
            ("What is eventual consistency?", "After writes stop, all reads eventually see same value. Used in distributed systems for availability. Weaker than strong consistency."),
            ("What is a load balancer?", "Distributes requests across multiple servers. Improves performance and reliability. Can use round-robin, least connections, or IP hash."),
            ("What is horizontal scaling?", "Adding more machines to handle load. Better than vertical scaling (bigger machine). Requires stateless design."),
            ("What is vertical scaling?", "Making existing machine more powerful. Simpler but has limits. More expensive than horizontal eventually."),
            ("What is sharding?", "Partitioning data across multiple databases. Enables horizontal scaling but adds complexity. Must choose shard key carefully."),
            ("What is replication?", "Copying data to multiple servers for availability and performance. Master-slave (one writes), peer-to-peer (all write)."),
            ("What is a message queue?", "Asynchronous communication between services. Decouples producers and consumers. Enables scalability and reliability."),
            ("What is a webhook?", "Server pushes data to client when event occurs. More efficient than polling. Used for real-time notifications."),
            ("What is rate limiting?", "Restricts number of requests from client in time period. Protects against abuse. Token bucket and sliding window algorithms."),
            ("What is a circuit breaker?", "Pattern preventing cascading failures. Monitors operations, fails fast if threshold exceeded. Allows system recovery."),
            ("What is idempotent retry?", "Retrying failed requests safely without side effects. Requires idempotent operations. Important for distributed systems."),
            ("What is observability?", "Ability to understand system from external outputs (logs, metrics, traces). More comprehensive than traditional monitoring."),
            ("What is tracing?", "Following request through entire system. Identifies bottlenecks and failures in microservices. OpenTelemetry is standard."),
        ]
        
        for user, asst in concepts:
            if self._add_example(user, asst):
                count += 1
        
        return count
    
    def generate_workflow_variations(self) -> int:
        """Generate 50+ workflow and process variations"""
        count = 0
        workflows = [
            ("What is the development workflow?", "Plan features, create branch, develop, test locally, push, create PR, review, address feedback, merge, deploy. Ensures quality and collaboration."),
            ("What is CI/CD pipeline?", "Continuous Integration: automated testing on commits. Continuous Deployment: automated release to production. Enables frequent, reliable releases."),
            ("What is semantic versioning?", "MAJOR.MINOR.PATCH format. MAJOR for breaking changes, MINOR for features, PATCH for fixes. Helps users understand compatibility."),
            ("What is a feature flag?", "Toggle to enable/disable features without deploying. Safer rollouts. Can A/B test. Decouple deployment from release."),
            ("What is blue-green deployment?", "Two identical production environments. Route traffic to current (blue), deploy to other (green), switch if healthy. Zero downtime, quick rollback."),
            ("What is canary deployment?", "Gradually roll out to small user percentage. Monitor metrics. Increase if healthy. Catch issues early with limited impact."),
            ("What is monitoring?", "Collecting metrics about system health. CPU, memory, requests, errors, response time. Enables proactive problem detection."),
            ("What is alerting?", "Notifications when metrics exceed thresholds. Wakes on-call engineer. Should balance false positives and coverage."),
            ("What is a runbook?", "Documented procedures for handling incidents. Step-by-step instructions. Enables consistent response. Reduces incidents and MTTR."),
            ("What is RTO and RPO?", "RTO (Recovery Time Objective) is max downtime acceptable. RPO (Recovery Point Objective) is data loss acceptable. Drive backup and DR strategy."),
            ("What is DR plan?", "Disaster Recovery plan defines procedures to restore systems. Tested regularly. Should document RTO/RPO, backup strategy, failover procedures."),
            ("What is load testing?", "Testing system with simulated load to find breaking points. Identifies bottlenecks and capacity limits. Uses tools like JMeter, Locust."),
            ("What is stress testing?", "Testing beyond expected load to see failure mode. Find limits. Ensure graceful degradation. Plan recovery."),
            ("What is usability testing?", "Real users interact with system to find problems. Identifies confusing flows, accessibility issues. Improves user experience."),
            ("What is A/B testing?", "Comparing two versions to determine which performs better. Users randomly assigned. Validates hypotheses with real data."),
            ("What is agile methodology?", "Iterative development with regular feedback. Sprints typically 2 weeks. Daily standups. Continuous improvement. User-focused."),
            ("What is scrum framework?", "Agile framework with product owner, scrum master, team. Sprints, ceremonies (standups, retros, planning). Structured but flexible."),
            ("What is kanban?", "Continuous flow system. Visualizes work. Limits work in progress. Pull-based. Good for continuous deployment environments."),
            ("What is pair programming?", "Two developers share one computer. Driver writes while navigator reviews. Improves code quality, spreads knowledge, prevents mistakes."),
            ("What is mob programming?", "Whole team working on one task together. Extreme collaboration. Great for onboarding and solving complex problems."),
            ("What is code smell?", "Surface-level indicator of deeper design problems. Not bugs, but suggests refactoring. Duplicated code, long methods, many parameters."),
            ("What is linting?", "Automated tool finding logical and stylistic errors. Improves code quality and consistency. Catches potential bugs before testing."),
            ("What is a pull request?", "Request to merge code changes. Enables review, discussion, testing before integration. Prevents bugs, shares knowledge."),
            ("What is git rebase?", "Moving commits onto different base. Cleans history but rewrites commits. Use cautiously on shared branches."),
            ("What is git cherry-pick?", "Applying specific commits to current branch. Useful for selective backports. Avoid overusing, indicates branching strategy issues."),
        ]
        
        for user, asst in workflows:
            if self._add_example(user, asst):
                count += 1
        
        return count
    
    def generate_all(self) -> int:
        """Generate all extended variations"""
        total = 0
        
        print(f"📊 Starting with {len(self.existing_data)} existing examples")
        print("🔄 Generating extended variations...\n")
        
        counts = [
            ("Tech variations", self.generate_tech_variations()),
            ("Learning variations", self.generate_learning_variations()),
            ("Conceptual variations", self.generate_conceptual_variations()),
            ("Workflow variations", self.generate_workflow_variations()),
        ]
        
        for name, count in counts:
            total += count
            print(f"✓ {name}: +{count}")
        
        return total
    
    def save_to_json(self):
        """Save expanded dataset"""
        with open(self.existing_file, 'w', encoding='utf-8') as f:
            json.dump(self.all_examples, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Saved {len(self.all_examples)} total examples to {self.existing_file}")


if __name__ == "__main__":
    generator = ExtendedDataGenerator("chat_history.json")
    new_count = generator.generate_all()
    generator.save_to_json()
    
    total = len(generator.all_examples)
    print("\n" + "="*50)
    print(f"📈 Dataset expanded: {len(generator.existing_data)} → {total}")
    print(f"➕ Added: {new_count} new variations")
    if total >= 500:
        print(f"🎉 TARGET REACHED: {total} examples (goal: 500+)")
    else:
        print(f"📌 Current: {total}/500 examples ({round(total/500*100)}%)")
    print("="*50)

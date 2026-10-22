# Cause → remedy chains

Use this to go from a finding to a treatment. Read each row left to right:
**smell (symptom)** → **techniques (in order)** → **pattern it may converge to** → **only if...**
(the condition that justifies going all the way to the pattern). If the condition is not met,
stop at the techniques.

## Smell → technique → pattern

| Smell | Techniques (typical order) | Possible pattern | Only if... |
|---|---|---|---|
| Switch Statements on type | Extract Method → Move Method → Replace Type Code with Subclasses / State/Strategy → Replace Conditional with Polymorphism | Strategy | the variants are algorithms chosen by client/config, and the switch is duplicated or grows |
| Switch on object's lifecycle status | Replace Type Code with State/Strategy → Replace Conditional with Polymorphism | State | behavior depends on a status that changes at runtime, with transitions spread around |
| Switch picking which class to instantiate | Replace Constructor with Factory Method → (map of constructors) | Factory Method / Abstract Factory | creation logic is duplicated or clients must not know concrete types |
| Switch on node type across many operations | Extract Method per operation → Move to visitor | Visitor | node types are stable and new operations are frequent |
| `if (x == null)` repeated | Introduce Null Object | Null Object (Strategy-like) | the default behavior is the same everywhere |
| Long Method, entangled temps | Replace Temp with Query → Replace Method with Method Object → Extract Method | Command | the operation must be queued, logged, retried or undone |
| Long Methods with same skeleton in siblings | Extract Method (identical/different parts) → Pull Up Method → Form Template Method | Template Method | the skeleton is stable and only steps vary |
| Duplicate Code, different algorithms same goal | Substitute Algorithm → Extract Method | Strategy | the algorithm must be chosen at runtime |
| Large Class / Divergent Change | Extract Class per responsibility → Move Method/Field | Facade (keep entry point) / Strategy / Bridge | callers need a single entry point / a dimension varies / two dimensions vary independently |
| Large Class coordinating many peers | Extract Class → Move Method | Mediator | components call each other in a many-to-many web |
| Shotgun Surgery | Move Method/Field → Inline Class | Facade / Observer | a subsystem is called from many places / many parts react to the same event |
| Parallel Inheritance Hierarchies | Move Method/Field → collapse one hierarchy | Bridge / Abstract Factory | both dimensions really vary independently / families must match |
| Refused Bequest | Replace Inheritance with Delegation / Push Down | Decorator / Strategy / Bridge | behavior needs to be combined or swapped at runtime |
| Combinatorial subclasses (`LoggedCachedX`, `CachedX`...) | Replace Inheritance with Delegation → Extract Interface | Decorator | features stack in different combinations |
| Alternative Classes with Different Interfaces (one external) | Rename/Move Method; wrap the external one | Adapter | the third-party interface cannot change |
| Incomplete Library Class | Introduce Foreign Method → Introduce Local Extension | Adapter / Decorator | many additions, used widely |
| Message Chains | Hide Delegate | Facade | chains cross a subsystem boundary |
| Middle Man | Remove Middle Man / Inline Method | (remove a fake Proxy/Facade) | — |
| Primitive Obsession (domain values) | Replace Data Value with Object | Value Object | rules/validation duplicated around the primitive |
| Primitive Obsession (many identical immutable objects in memory) | Change Reference to Value / share instances | Flyweight | memory pressure is measured, not guessed |
| Long Parameter List for construction | Introduce Parameter Object | Builder | many optional parts, step-wise or different representations |
| Telescoping constructors | Replace Constructor with Factory Method | Builder / Factory Method | many valid combinations |
| Costly object setup copied by hand | Extract Method (clone) | Prototype | copies of configured objects are needed with unknown concrete class |
| Callbacks / hard-wired notifications to many listeners | Extract Interface → Move Method | Observer | listeners vary at runtime, sender must not know them |
| Sequential `if` handlers with fallthrough | Extract Method per handler → Extract Class | Chain of Responsibility | handlers and order vary, or are configured |
| UI actions duplicating business calls | Extract Method → Extract Class per action | Command | actions need undo/queue/macro/menus+shortcuts reuse |
| Undo by snapshotting fields from outside | Encapsulate Field → Extract Class (snapshot) | Memento | encapsulation must be preserved |
| Client knowing collection internals | Encapsulate Collection | Iterator | several traversal strategies or lazy/huge collections |
| Global mutable state accessed everywhere | Pass dependency explicitly / Introduce Parameter | (remove Singleton) | — |
| Lazy access control/caching mixed into business code | Extract Class → Extract Interface | Proxy | the concern is orthogonal and the interface stays the same |
| Speculative Generality | Collapse Hierarchy / Inline Class / Inline Method / Remove Parameter | (remove the pattern) | — |

## Reverse index: pattern ← refactorings that build it

| Pattern | Refactorings that usually lead there |
|---|---|
| Factory Method | Replace Constructor with Factory Method, Replace Type Code with Subclasses, Extract Method + Pull Up |
| Abstract Factory | Extract Interface over several factory methods, Extract Class |
| Builder | Introduce Parameter Object, Replace Constructor with Factory Method, Extract Class |
| Prototype | Extract Method (copy), Extract Interface |
| Singleton | (rarely a target) — usually remove it: Introduce Parameter, Move Method to the composition root |
| Adapter | Extract Interface, Introduce Local Extension (wrapper), Move Method |
| Bridge | Replace Inheritance with Delegation, Extract Interface, Extract Class |
| Composite | Extract Interface, Extract Superclass, Replace Conditional with Polymorphism |
| Decorator | Replace Inheritance with Delegation, Extract Interface, Introduce Local Extension |
| Facade | Extract Class, Hide Delegate, Move Method |
| Flyweight | Change Reference to Value, Extract Class (intrinsic state) |
| Proxy | Extract Interface, Extract Class, Hide Delegate |
| Chain of Responsibility | Extract Class per handler, Replace Conditional with Polymorphism |
| Command | Replace Method with Method Object, Extract Class, Extract Interface |
| Iterator | Encapsulate Collection, Extract Class |
| Mediator | Extract Class, Move Method, Change Bidirectional Association to Unidirectional |
| Memento | Encapsulate Field, Extract Class |
| Observer | Duplicate Observed Data, Extract Interface, Replace callbacks with subscribe API |
| State | Replace Type Code with State/Strategy, Replace Conditional with Polymorphism, Move Method |
| Strategy | Replace Type Code with State/Strategy, Replace Conditional with Polymorphism, Substitute Algorithm, Extract Interface |
| Template Method | Form Template Method, Extract Method, Pull Up Method |
| Visitor | Extract Method per operation, Move Method into visitor, Introduce double dispatch |

## Reverse index: pattern → refactorings that remove it (over-engineering)

| Over-engineered structure | Simplify with |
|---|---|
| Strategy/State with one implementation | Inline Class, Collapse Hierarchy (keep a function) |
| Factory returning one concrete type | Inline Method (call the constructor) |
| Abstract Factory with one family | Collapse Hierarchy → plain factory functions |
| Interface with one implementation, no seam need | Collapse Hierarchy / remove interface |
| Proxy/Decorator/Facade that only forwards | Remove Middle Man |
| Visitor over a hierarchy that keeps changing | Move Method back into elements (polymorphism) |
| Observer with one fixed listener | Replace with direct call |
| Singleton | Pass the instance explicitly; let DI/composition root own lifecycle |
| Builder for 2–3 required fields | Constructor / named arguments |
| Template Method with one subclass | Collapse Hierarchy |

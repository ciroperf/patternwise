# Pattern catalog and recognition guide

Recognize patterns by **roles and relationships**, never by class names. A name like
`OrderFactory` is a hint to check, not evidence. Open the specific file for verdict criteria.

Each pattern file has: Intent · Problem it solves · Roles · Recognize it · Red flags
(misapplied / name only) · Don't use when · Idiomatic forms · Path to it · Trade-offs · Related.

## Creational — how objects get created
| Pattern | One-line intent | Structural signature to look for | File |
|---|---|---|---|
| Factory Method | Let subclasses/implementations decide which product to create | Overridable creation method returning an abstract product, used by the creator's own logic | `creational/factory-method.md` |
| Abstract Factory | Create families of related products without naming concrete classes | Interface with several `createX()` methods; one implementation per family | `creational/abstract-factory.md` |
| Builder | Construct complex objects step by step | Object accumulating parts via chained/step methods, then `build()`; optional Director | `creational/builder.md` |
| Prototype | Create objects by copying an existing instance | `clone()`/copy method on the object itself; registry of prototypes | `creational/prototype.md` |
| Singleton | Ensure one instance with a global access point | Private constructor + static accessor/instance; module-level instance | `creational/singleton.md` |

## Structural — how objects are composed
| Pattern | One-line intent | Structural signature | File |
|---|---|---|---|
| Adapter | Make an incompatible interface usable by a client | Class implementing client's interface and translating calls to a wrapped adaptee | `structural/adapter.md` |
| Bridge | Split abstraction and implementation into two hierarchies varying independently | Abstraction holds a reference to an implementation interface; both sides have subclasses | `structural/bridge.md` |
| Composite | Treat trees of objects and single objects uniformly | Component interface; leaf and container both implement it; container holds children of component type and delegates recursively | `structural/composite.md` |
| Decorator | Add behavior by wrapping objects with the same interface | Wrapper implements the same interface as the wrapped object and holds one; wrappers stack | `structural/decorator.md` |
| Facade | Simple interface to a complex subsystem | One class whose methods orchestrate several subsystem objects; clients use only it | `structural/facade.md` |
| Flyweight | Share common state among many fine-grained objects | Factory/cache returning shared immutable objects; extrinsic state passed in | `structural/flyweight.md` |
| Proxy | Control access to an object through a stand-in with the same interface | Same interface as the service; holds/creates it; adds lazy-load, access check, cache, remote call, logging | `structural/proxy.md` |

## Behavioral — how objects distribute responsibility and communicate
| Pattern | One-line intent | Structural signature | File |
|---|---|---|---|
| Chain of Responsibility | Pass a request along handlers until one (or all) process it | Handlers with common interface and a `next` link or ordered list; each decides to handle/pass | `behavioral/chain-of-responsibility.md` |
| Command | Turn a request into an object | Objects with `execute()` (and maybe `undo()`) holding receiver + params; invoker stores/queues them | `behavioral/command.md` |
| Iterator | Traverse a collection without exposing its structure | Separate object/generator with `next/hasNext` or language iteration protocol | `behavioral/iterator.md` |
| Mediator | Centralize communication between components | Components reference only a mediator; mediator knows them and routes interactions | `behavioral/mediator.md` |
| Memento | Snapshot and restore state without breaking encapsulation | Originator creates opaque snapshot objects; caretaker stores them | `behavioral/memento.md` |
| Observer | Notify subscribers about events | Publisher keeps a list of subscribers behind an interface; `subscribe/unsubscribe/notify` | `behavioral/observer.md` |
| State | Change behavior when internal state changes | Context delegates to a current state object; states trigger transitions by replacing it | `behavioral/state.md` |
| Strategy | Make interchangeable algorithms | Context holds a reference to an algorithm interface; clients choose/swap the implementation | `behavioral/strategy.md` |
| Template Method | Fix an algorithm's skeleton, let subclasses redefine steps | Base method calling abstract/hook steps in fixed order; subclasses override steps only | `behavioral/template-method.md` |
| Visitor | Add operations to a stable object structure without changing it | Elements with `accept(visitor)` calling `visitor.visitX(this)`; visitors per operation | `behavioral/visitor.md` |

## Telling similar patterns apart
- **Strategy vs State**: same shape. Strategy is chosen by the client and strategies do not know
  each other; State objects know about each other (or the context) and trigger transitions.
- **Adapter vs Decorator vs Proxy vs Facade**: Adapter *changes* the interface; Decorator *keeps* it
  and adds behavior, stackable, client-controlled; Proxy *keeps* it and controls access/lifecycle,
  usually managing the service itself; Facade *defines a new simpler* interface over many objects.
- **Bridge vs Strategy**: Bridge is designed up-front to separate two dimensions of a whole
  hierarchy; Strategy swaps one algorithm in one context.
- **Factory Method vs Abstract Factory vs "simple factory"**: Factory Method relies on overriding
  in subclasses; Abstract Factory is an object producing a family; a static method that picks a
  class from a parameter is a *simple factory* (fine, not GoF — report as such, not as misuse).
- **Command vs Strategy**: Command packages *what to do* (any action, often with undo/queue);
  Strategy packages *how to do* one specific job.
- **Chain of Responsibility vs Decorator**: CoR handlers may stop the chain; decorators always
  delegate (they extend, never short-circuit the main job — a decorator that sometimes doesn't
  delegate is a CoR or a Proxy).
- **Mediator vs Observer vs Facade**: Mediator coordinates peers that know only it (two-way);
  Observer is one-way dynamic subscription; Facade simplifies access but subsystem classes do not
  know it.
- **Composite vs Decorator**: Composite has many children and aggregates results; Decorator has one
  wrapped object and adds behavior.
- **Template Method vs Strategy**: inheritance and compile-time steps vs composition and runtime swap.

## Frequent "name only" cases (verify before labeling)
- `*Factory` that is a static helper with one product → simple factory or just a constructor wrapper.
- `*Manager`, `*Handler`, `*Processor`, `*Service` → no pattern implied; check for God object.
- `*Strategy` with one implementation and a `switch` inside → not Strategy.
- `*Adapter` that only renames methods 1:1 for an interface you control → Middle Man.
- `*Proxy` / `*Wrapper` that forwards everything with no added control → Middle Man.
- `*Builder` with a single `build(a, b, c)` call → constructor with extra steps.
- `*Observer`/`*Listener` interface with exactly one hard-wired implementation → indirection only.
- `*Singleton` / `getInstance()` holding mutable global state → misapplied Singleton.
- `*Visitor` that is a generic tree walker with `instanceof` inside → not Visitor (no double dispatch).
- `*Command` objects that are plain DTOs handled by a big switch → message objects, not Command.

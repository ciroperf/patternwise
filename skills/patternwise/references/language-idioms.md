# Adapting patterns to the language

Pattern descriptions are written in classic class-based OO. Translate the **intent** and the
**roles**, not the class diagram. Recognize idiomatic forms as the pattern (do not report them
as "missing the pattern"), and do not introduce class-heavy versions where the idiom exists.

## General rules
- **First-class functions** (Python, JS/TS, Kotlin, Swift, Go, Rust, C#, Java 8+, Scala):
  Strategy, Command, Template-Method-with-hooks, Observer callbacks, Factory Method are
  often just functions/lambdas/closures. A dict/map of functions replaces a switch.
- **Modules as singletons**: a module-level instance (Python module, ES module, Go package
  var) is the idiomatic single instance. Prefer passing dependencies explicitly anyway.
- **Sum types / sealed hierarchies + exhaustive matching** (Rust enums, Kotlin/Java sealed,
  Scala, TS discriminated unions, F#, Swift enums): `match` over a closed set is idiomatic and
  checked by the compiler; it plays the role of Visitor. Do not flag it as Switch Statements
  unless the same match is duplicated and the set of variants grows often.
- **Structural typing / duck typing** (Go interfaces, TS, Python protocols): interfaces are
  defined by the consumer and need no explicit `implements`; Extract Interface may be a
  type/Protocol declaration only.
- **Language-native patterns**: iterators/generators (Iterator), decorators/annotations and
  middleware (Decorator/Chain of Responsibility), `with`/`using`/`defer`/RAII (resource Proxy),
  copy/clone traits (Prototype), events/signals/RxJS/Flow (Observer), `@dataclass`/records/
  data classes (Value Object, Data Class). Prefer them over hand-rolled versions.
- **Frameworks own some patterns**: DI containers (Factory/Singleton lifecycle), ORMs (Proxy,
  Unit of Work, Identity Map), web middleware (Chain of Responsibility), UI frameworks
  (Observer, Composite, Command). Use the framework mechanism; report hand-rolled duplicates.

## Per language notes

### Python
- Strategy/Command: functions or callables; `typing.Protocol` for the contract if needed.
- Decorator: function decorators for cross-cutting behavior on functions; object Decorator
  still valid for wrapping objects. Do not confuse the two in the report.
- Singleton: module-level object or `functools.cache` on a factory; avoid metaclass singletons.
- Value objects: `@dataclass(frozen=True)`, `NamedTuple`, `enum.Enum` for type codes.
- Iterator: generators. Template Method: base class with hook methods, or pass functions.
- Visitor: `functools.singledispatch` or `match` (3.10+).
- Verify: `pytest`, `python -m unittest`, `mypy`/`pyright`, `ruff`.

### JavaScript / TypeScript
- Strategy/Command/Factory: functions and object literals; maps of handlers.
- Observer: EventEmitter, DOM events, RxJS, framework state (React hooks, Vue reactivity).
- Decorator: higher-order functions/components; TS decorators are a different feature.
- Type codes: string literal unions + discriminated unions with exhaustive `switch` +
  `never` check (idiomatic; do not replace with class hierarchies by default).
- Singleton: ES module export. Value objects: `readonly` types, branded types.
- Verify: `npm test`, `tsc --noEmit`, `eslint`.

### Java / C# / Kotlin
- Classic GoF shapes are idiomatic, but prefer lambdas/functional interfaces (`Function`,
  `Supplier`, `Func<>`, `Action<>`) for single-method Strategies/Commands.
- Records (Java 16+, C# `record`, Kotlin `data class`) for value objects/DTOs.
- Sealed interfaces + `switch` pattern matching (Java 21, Kotlin `when`, C# switch expressions).
- Singleton/Factory lifecycle usually belongs to the DI container (Spring, .NET DI, Dagger).
- Kotlin: `object` is the singleton; extension functions solve Incomplete Library Class;
  delegation `by` implements Decorator/Proxy with little code.
- Verify: `mvn -q test`, `gradle test`, `dotnet build && dotnet test`.

### Go
- Small consumer-defined interfaces; no inheritance: Template Method → pass functions or
  embed + interface; Refused Bequest becomes over-embedding.
- Strategy: function types (`type PriceFn func(Order) Money`). Decorator: middleware
  `func(http.Handler) http.Handler`. Options pattern (functional options) instead of Builder.
- Singleton: package var + `sync.Once` only when lazy init is required.
- Verify: `go build ./... && go vet ./... && go test ./...`.

### Rust
- Enums + `match` are the default for closed variation; traits + `Box<dyn Trait>` for open
  variation. Builder is idiomatic for complex construction. Newtype pattern for Primitive
  Obsession. `Clone` for Prototype. `Iterator` trait. RAII guards for Proxy-like resources.
- Ownership makes Observer/Mediator awkward: prefer channels or callbacks owned by one side.
- Verify: `cargo build && cargo clippy && cargo test`.

### C++
- Templates/concepts give compile-time Strategy (policy-based design); `std::function` for
  runtime. RAII. CRTP as static Template Method. `std::variant` + `std::visit` as Visitor.
- Verify: project build (CMake/Make) + ctest.

### PHP / Ruby
- PHP: interfaces + DI container (Laravel/Symfony); enums (8.1+) for type codes; readonly
  classes for value objects. Ruby: blocks/procs for Strategy/Command; modules (mixins) for
  shared behavior — watch for Refused Bequest via over-included modules.
- Verify: `phpunit`/`pest`, `rspec`/`rake test`.

### Functional-first code (Elixir, Clojure, Haskell, F#, Scala FP)
- Most GoF patterns dissolve into functions, higher-order functions, data, and protocols/
  typeclasses. Analyze smells (duplication, long functions, data clumps, feature envy across
  modules) but be careful with OO-centric pattern verdicts; state uncertainty.

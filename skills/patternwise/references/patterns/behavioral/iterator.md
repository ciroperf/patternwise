# Iterator (Behavioral)

**Intent**: traverse elements of a collection without exposing its underlying representation
(list, tree, graph, paginated API, stream).

## Problem it solves
- Clients depend on a collection's internals (indexes, nodes, pages) to loop over it; traversal
  code is duplicated; several traversal orders (depth-first, breadth-first, filtered) are needed.
- Lazy traversal over large/remote data.

## Roles
- **Iterator** interface: `next()`, `hasNext()` (or language protocol).
- **Concrete Iterators**: keep traversal state per algorithm.
- **Iterable Collection**: `createIterator()`; concrete collections return their iterators.

## Recognize it
- Language iteration protocols (`__iter__/__next__`, `Iterable`, `Symbol.iterator`, `IEnumerable`,
  Rust `Iterator`), generators (`yield`), cursors, paginators.

## Red flags
- Hand-rolled iterator classes where a generator would do → extra code.
- Collection returning its internal mutable list (Encapsulate Collection missing).
- Iterator invalidated by concurrent modification without detection.

## Don't use when
- A plain list is fine and no encapsulation is needed.

## Idiomatic forms
- Always prefer the language protocol + generators; library combinators (`map/filter`, LINQ,
  streams) over custom classes.

## Path to it
Encapsulate Collection → Extract Method for traversal loops → expose a generator/iterator
method on the collection → callers use it.

## Trade-offs
+ SRP for traversal, multiple simultaneous traversals, lazy evaluation. − Overkill for simple
collections; may be slower than direct access.

## Related
Traverses Composite trees; Factory Method creates matching iterators; Memento can capture
iteration state; Visitor + Iterator to apply operations over complex structures.

# Composite (Structural)

**Intent**: compose objects into tree structures and let clients treat individual objects and
compositions uniformly.

## Problem it solves
- The domain is genuinely a tree (files/folders, UI widgets, org charts, order boxes containing
  products and boxes, expression trees) and clients write type checks + recursion to compute
  totals or apply operations.

## Roles
- **Component** interface: operations meaningful for both leaves and containers.
- **Leaf**: does the actual work.
- **Composite/Container**: holds child Components, delegates to them and aggregates results.
- **Client**: works through Component.

## Recognize it
- A container class holding a list typed as the same interface it implements; recursive methods
  (`getPrice()` summing children); `add/remove/children` methods.

## Red flags
- Client code still doing `if (x instanceof Folder)` → uniformity not achieved.
- Child-management methods on Leaf that throw → an ISP trade-off; acceptable if documented, but
  check whether clients need them on Component at all.
- Cycles allowed in what should be a tree; parent pointers out of sync.
- Forced on data that is not hierarchical.

## Don't use when
- The structure is flat or fixed-depth; a list or two classes are clearer.

## Idiomatic forms
- Recursive algebraic data types (`enum Node { Leaf(..), Group(Vec<Node>) }`) + recursion;
  UI component trees provided by frameworks.

## Path to it
Extract Interface for the shared operations → make container and leaf implement it → Replace
Conditional with Polymorphism for the type checks in clients → move recursion into the container.

## Trade-offs
+ Uniform client code, easy to add element types (OCP). − Overly general Component interface;
hard to restrict which children a container accepts.

## Related
Built with Builder; traversed with Iterator; operations added with Visitor; leaves shared with
Flyweight; Chain of Responsibility often travels up the tree to parents. Decorator has the same
recursive shape but one child.

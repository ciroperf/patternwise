# Composing Methods

Most problems start with methods that are too long. These techniques shrink methods, remove
duplication and make intent visible. They are mostly local and low-risk: do them first.

Format: **When** · **Steps** · **Watch out** · **Treats**.

## Extract Method
- **When**: a fragment can be grouped and named; a comment explains a block; duplicated fragment.
- **Steps**: 1) create a new function named after *what* the fragment does; 2) copy the
  fragment; 3) variables read but not modified become parameters; variables declared inside
  stay local; a single variable modified and used afterwards becomes the return value (more
  than one → return a small object, or first apply Replace Temp with Query / Split Temporary
  Variable); 4) replace the fragment with a call; 5) test.
- **Watch out**: too many parameters means a poor boundary or a need for Method Object.
- **Treats**: Long Method, Duplicate Code, Comments, Feature Envy, Switch Statements, Message
  Chains, Data Class (usually as prelude to Move Method).

## Inline Method
- **When**: the body is as clear as the name; a method only delegates; after over-splitting.
- **Steps**: ensure it is not overridden; replace every call with the body; delete the method.
- **Treats**: Speculative Generality, Middle Man.

## Extract Variable
- **When**: an expression is hard to read (complex conditions, long arithmetic).
- **Steps**: put a sub-expression in a well-named immutable local; replace occurrences.
- **Watch out**: prefer Extract Method if the expression is useful elsewhere.
- **Treats**: Comments, Long Method (as prelude).

## Inline Temp
- **When**: a temp holds a simple expression and gets in the way of other refactorings.
- **Steps**: check it is assigned once; replace reads with the expression; delete it.
- **Watch out**: do not inline expensive or side-effecting expressions used repeatedly.

## Replace Temp with Query
- **When**: a temp stores an expression result that other methods could also use.
- **Steps**: ensure single assignment; extract the expression into a side-effect-free method;
  replace the temp's uses with calls; remove the temp.
- **Watch out**: performance in hot loops (measure; usually negligible).
- **Treats**: Long Method, Duplicate Code; unlocks Extract Method.

## Split Temporary Variable
- **When**: one local is reused for different purposes (not a loop counter/accumulator).
- **Steps**: rename at the first assignment to a purpose-specific name (make it final/const);
  update reads until the next assignment; repeat for each assignment.
- **Treats**: confusing code, blocks Extract Method.

## Remove Assignments to Parameters
- **When**: a parameter is reassigned inside the body.
- **Steps**: introduce a local initialized from the parameter; replace assignments and later
  reads with the local.
- **Watch out**: in pass-by-reference languages, check that callers did not rely on the change.

## Replace Method with Method Object
- **When**: a long method whose locals are so entangled that Extract Method is impractical.
- **Steps**: create a class; its fields are the original object (if needed), parameters and
  locals; constructor takes them; move the body into a `compute/run/execute` method; replace
  the original body with `new X(...).compute()`; now extract freely inside the new class.
- **Leads to**: Command (if the object is later queued, logged or undone).
- **Treats**: Long Method, Temporary Field.

## Substitute Algorithm
- **When**: a simpler/clearer algorithm (or a library call) does the same thing.
- **Steps**: simplify/decompose the old one first if possible; write the new one; run the
  same tests on both (or compare outputs on many inputs); replace.
- **Watch out**: identical results on edge cases (ordering, duplicates, nulls, precision).
- **Treats**: Duplicate Code, Long Method. Leads to Strategy if both algorithms must remain.

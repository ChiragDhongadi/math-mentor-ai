# Probability Rules for JEE Mathematics

## 1. Basic Probability Concept

Probability measures the likelihood of an event occurring.

If an experiment has n equally likely outcomes and m favorable outcomes for event A:

P(A) = m / n

Where:

0 ≤ P(A) ≤ 1

---

## 2. Sample Space and Events

Sample Space (S)

The set of all possible outcomes.

Example:

Tossing a coin

S = {H, T}

Event

A subset of the sample space.

Example:

Event A = getting head

A = {H}

---

## 3. Types of Events

### Simple Event

An event with a single outcome.

Example:

Rolling a 3 on a die.

---

### Compound Event

An event with more than one outcome.

Example:

Rolling an even number on a die.

---

### Complementary Events

For event A:

P(A') = 1 − P(A)

Where A' is the complement of A.

Example:

Probability of not getting a head.

---

## 4. Addition Rule of Probability

For two events A and B:

P(A ∪ B) = P(A) + P(B) − P(A ∩ B)

If A and B are mutually exclusive:

P(A ∩ B) = 0

Then:

P(A ∪ B) = P(A) + P(B)

---

## 5. Multiplication Rule

For two events A and B:

P(A ∩ B) = P(A) × P(B | A)

Where:

P(B | A) is conditional probability.

---

## 6. Conditional Probability

Conditional probability of B given A:

P(B | A) = P(A ∩ B) / P(A)

Provided:

P(A) ≠ 0

---

## 7. Independent Events

Events A and B are independent if:

P(A ∩ B) = P(A) × P(B)

Also:

P(A | B) = P(A)

P(B | A) = P(B)

Example:

Two independent coin tosses.

---

## 8. Bayes' Theorem

Used to find reverse probability.

If A1, A2, A3 ... An are mutually exclusive and exhaustive events:

P(Ak | B) = [P(Ak) × P(B | Ak)] / Σ [P(Ai) × P(B | Ai)]

This is commonly used in JEE probability questions.

---

## 9. Permutations

Number of ways to arrange r objects from n distinct objects:

nPr = n! / (n − r)!

Example:

Arranging 3 letters from 5 letters.

5P3 = 5! / 2!

---

## 10. Combinations

Number of ways to select r objects from n objects:

nCr = n! / [r!(n − r)!]

Example:

Choosing 2 students from 5.

5C2 = 10

---

## 11. Relation Between Permutations and Combinations

nPr = nCr × r!

---

## 12. Random Variable

A random variable assigns numerical values to outcomes of an experiment.

Example:

Number of heads in 3 coin tosses.

---

## 13. Probability Distribution

If random variable X takes values:

x1, x2, x3 ...

with probabilities:

p1, p2, p3 ...

Then:

Σ pi = 1

---

## 14. Expected Value (Mean)

Expected value of random variable:

E(X) = Σ xi × pi

This represents the average outcome.

---

## 15. Variance

Variance measures spread of distribution.

Var(X) = E(X²) − [E(X)]²

Standard deviation:

σ = √Var(X)

---

## 16. Binomial Distribution

Used when:

1. Fixed number of trials
2. Only two outcomes (success/failure)
3. Trials are independent
4. Probability of success remains constant

Probability formula:

P(X = r) = nCr × p^r × (1 − p)^(n − r)

Where:

n = number of trials
r = number of successes
p = probability of success

---

## 17. Important Binomial Results

Mean:

E(X) = np

Variance:

Var(X) = np(1 − p)

Standard deviation:

σ = √(np(1 − p))

---

## 18. Law of Total Probability

If events A1, A2, ... An partition the sample space:

P(B) = Σ P(Ai)P(B | Ai)

Used frequently with Bayes theorem.

---

## 19. Common Probability Techniques in JEE

Counting favorable outcomes
Using symmetry
Using complementary probability
Using conditional probability
Breaking complex problems into simpler events

---

## 20. Complement Trick (Very Important)

Often easier to compute:

P(A') instead of P(A)

Then:

P(A) = 1 − P(A')

Example:

Probability of at least one success.

---

End of Probability Knowledge Base

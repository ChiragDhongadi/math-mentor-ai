# Calculus Rules for JEE Mathematics

## 1. Limits – Basic Concepts

The limit of a function f(x) as x approaches a value a is written as:

lim (x → a) f(x)

A limit exists if the left-hand limit and right-hand limit are equal.

Left-hand limit:

lim (x → a⁻) f(x)

Right-hand limit:

lim (x → a⁺) f(x)

If both are equal, the limit exists.

---

## 2. Standard Limits (Important for JEE)

lim (x → 0) (sin x / x) = 1

lim (x → 0) ((1 − cos x) / x²) = 1/2

lim (x → 0) (tan x / x) = 1

lim (x → 0) ((e^x − 1) / x) = 1

lim (x → 0) ((a^x − 1) / x) = ln(a)

lim (x → ∞) (1 + 1/x)^x = e

These limits are frequently used to simplify indeterminate forms.

---

## 3. Indeterminate Forms

Common indeterminate forms:

0/0
∞/∞
0 × ∞
∞ − ∞
0^0
∞^0
1^∞

These forms require algebraic manipulation or special techniques.

---

## 4. Techniques to Evaluate Limits

Common methods:

Factorization
Rationalization
Substitution
Using standard limits
Series approximation (for small x)

Example:

lim (x → 0) (sin x / x)

Using standard limit → result = 1

---

## 5. Definition of Derivative

The derivative of a function f(x) is defined as:

f'(x) = lim (h → 0) [f(x + h) − f(x)] / h

It represents the **rate of change** of the function.

Geometrically, it represents the **slope of the tangent** to the curve.

---

## 6. Basic Derivative Formulas

d/dx (c) = 0

d/dx (x^n) = n x^(n−1)

d/dx (e^x) = e^x

d/dx (a^x) = a^x ln(a)

d/dx (ln x) = 1/x

d/dx (log_a x) = 1 / (x ln a)

---

## 7. Trigonometric Derivatives

d/dx (sin x) = cos x

d/dx (cos x) = −sin x

d/dx (tan x) = sec² x

d/dx (cot x) = −cosec² x

d/dx (sec x) = sec x tan x

d/dx (cosec x) = −cosec x cot x

---

## 8. Derivative Rules

### Sum Rule

d/dx [f(x) + g(x)] = f'(x) + g'(x)

### Product Rule

d/dx [f(x)g(x)] = f'(x)g(x) + f(x)g'(x)

### Quotient Rule

d/dx [f(x)/g(x)] = [f'(x)g(x) − f(x)g'(x)] / g(x)^2

### Chain Rule

If y = f(g(x)):

dy/dx = f'(g(x)) × g'(x)

---

## 9. Implicit Differentiation

Used when variables cannot be separated easily.

Example:

x² + y² = 1

Differentiate both sides:

2x + 2y(dy/dx) = 0

dy/dx = −x/y

---

## 10. Higher Order Derivatives

Second derivative:

d²y/dx²

Represents **rate of change of slope**.

Used to determine:

Concavity
Maxima and minima

---

## 11. Increasing and Decreasing Functions

If:

f'(x) > 0 → function is increasing

f'(x) < 0 → function is decreasing

Critical points occur when:

f'(x) = 0

---

## 12. Maxima and Minima (Optimization)

Steps to find maxima/minima:

1. Compute derivative f'(x)
2. Solve f'(x) = 0
3. Find critical points
4. Use second derivative test

Second derivative test:

If f''(x) > 0 → local minimum

If f''(x) < 0 → local maximum

---

## 13. Tangent and Normal

Slope of tangent at point x = a:

m = f'(a)

Equation of tangent:

y − y₁ = m(x − x₁)

Normal line slope:

m_normal = −1 / m

---

## 14. Rolle's Theorem

If function f(x):

1. is continuous on [a, b]
2. differentiable on (a, b)
3. f(a) = f(b)

Then there exists a point c in (a, b) such that:

f'(c) = 0

---

## 15. Mean Value Theorem

If f(x) is:

continuous on [a, b]
differentiable on (a, b)

Then there exists c such that:

f'(c) = [f(b) − f(a)] / (b − a)

---

## 16. L'Hôpital's Rule

Used for limits of form:

0/0 or ∞/∞

If:

lim (x → a) f(x)/g(x)

is indeterminate, then:

lim (x → a) f(x)/g(x) = lim (x → a) f'(x)/g'(x)

(if the limit exists)

---

## 17. Simple Optimization Problems

Common JEE optimization problems:

Maximum area
Minimum distance
Maximum volume

Steps:

1. Express quantity in terms of one variable
2. Differentiate
3. Set derivative = 0
4. Verify using second derivative

---

## 18. Important Calculus Identities

Derivative of inverse functions:

d/dx (sin⁻¹ x) = 1 / √(1 − x²)

d/dx (cos⁻¹ x) = −1 / √(1 − x²)

d/dx (tan⁻¹ x) = 1 / (1 + x²)

---

End of Calculus Knowledge Base

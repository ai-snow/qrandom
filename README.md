# qrandom
A random number generator framework designed with testing in mind.

# Problem qrandom Solves
When modellers run their simulations, generating random numbers is essential.  What is also essential is that when you add/change/remove functionality, you want to be able to see how your simulations changed as a result of these operations.  However, there is a glaring issue when it comes to generating random numbers: **order really matters**.  So, in a traditional random number generator, if you were to add functionality in the middle of your process utiliting random numbers from your generator, you indirectly impact the entire remainder of the simulation, even the parts that didn't change!  Here's an example:

```python
import random

random.seed(1)

process_A_quantile = random.random()
process_B_quantile = random.random()

print(f'A: {process_A_quantile}')
print(f'B: {process_B_quantile}')
```

The above outputs:

```
A: 0.13436424411240122
B: 0.8474337369372327
```

Now, let's say we realize we need a third process (process_C_quantile)  and it needs to run after process A but before process B:
```python
import random

random.seed(1)

process_A_quantile = random.random()
process_C_quantile = random.random()
process_B_quantile = random.random()

print(f'A: {process_A_quantile}')
print(f'C: {process_C_quantile}')
print(f'B: {process_B_quantile}')
```
The above outputs:
```
A: 0.13436424411240122
C: 0.8474337369372327
B: 0.763774618976614
```
Adding process C and not touching process B still caused a change to process B!  The quantiles are in a first-come-first-served manner.  If you want to be able to regression test your code/model, good luck!

# QRandom's Solution
Let's bring some sanity back to testing simulaltions.

qrandom works off a backend buffer and a collection of quantiles composed of a coupling of index queues.  That may sound confusing, but it's not too important if you want to just consume the functionality.

Here's the same problem as the previous section, but implemented with qrandom's QRandom object:
```python
from random import Random
from qrandom.qrandom import QRandom

q = QRandom(Random(), 1) # First parameter is RNG to use; second is the seed value

process_A_quantile_1 = q.q('process_A_quantile')
process_B_quantile_1 = q.q('process_B_quantile')

q.save('./tmp/rng.q')

q = QRandom.restore('./tmp/rng.q')

process_A_quantile_2 = q.q('process_A_quantile')
process_C_quantile_2 = q.q('process_C_quantile')
process_B_quantile_2 = q.q('process_B_quantile')

print(process_A_quantile_1 == process_A_quantile_2)
print(process_B_quantile_1 == process_B_quantile_2)
```
The above outputs:
```
True
True
```
The state of process B was unchanged! Woot!

The process is quite straight-forward.  You need to wrap your RNG in a QRandom object like so:
```python
q = QRandom(Random(), 1) # First parameter is RNG to use; second is the seed value
```
Then anywhere you want to generate a quantile (random number between 0 and 1, you write:
```python
x = q.q('x')
```
where 'x' is an ID/name of the quantile you are asking for.  Moreover, anytime you try to get an attribute on a QRandom object that begins with 'q_', it treats the rest of the name of the attribute as the name of the quantile you want to generate. Note that the variable name of the left of the assignment doesn't have to match the quantile name, it's just convenient to do so.
```python
dummy = q.q_x  # this is equivalent to: dummy = q.q('x')
```
Loops are a common mechanism in simulations.  The order in which quantiles are accessed multiple times (as in multiple passes through a loop) is also preserved
```python
for i in range(10):
    x = q.q_x
    y = q.q_y
    print(x)
    print(y)
```
The above will print 10 unique quantiles for both x and y (a total of 20 quantiles).  If you were to place `z = q.q_z` in between the assignments of x and y, you would be happy to know that the quantiles for x and y will not change (given, obviously, that you saved the state of the QRandom object and restored that state).
```python
q.reset() # in-memory equivalent to doing a save/restore set of operations (for testing, mainly)
for i in range(10):
    x = q.q_x
    z = q.q_z
    y = q.q_y
    print(x)
    print(z)
    print(y)
```
It is important to note that if you plan on using a quantile multiple times in the same equation, the following would be incorrect:
```python
something = q.q_x + (1 + q.q_x) ** 2
```
This equation would return different values for each call to q_x.  The appropriate way to correct this would be:
```python
x = q.q_x
something = x + (1 + x) ** 2
```
Happy coding!

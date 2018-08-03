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

process_A_quantile_1 = q.q_process_A_quantile
process_B_quantile_1 = q.q_process_B_quantile

q.save('./tmp/rng.q')

q = QRandom.restore('./tmp/rng.q')

process_A_quantile_2 = q.q_process_A_quantile
process_C_quantile_2 = q.q_process_C_quantile
process_B_quantile_2 = q.q_process_B_quantile

print(process_A_quantile_1 == process_A_quantile_2)
print(process_B_quantile_1 == process_B_quantile_2)
```
The above outputs:
```
True
True
```
The state of process B was unchanged! Woot!

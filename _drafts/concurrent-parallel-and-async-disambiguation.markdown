---
layout: post
title:  "An easy to remember disambiguation between concurrent, parallel and asynchronous"
date:   2019-02-24 18:26:00 +0000
categories: jekyll update
---

Concurrent programming is confusing as it is, but it can get even worse
without a clear idea of what the terms concurrent, parallel and asynchronous
mean.
While these are all somewhat related concepts they mean different things.
My plan for this post is to provide an easy to remember example that I hope
can help visualise the difference in daily dealings with concurrent
programs.

<!--
First define
- task
- thread
- core
-->

<!--
Define an order:
- sequential
- concurrent
    - parallel
    - asynchronous
-->

## Concurrent execution

Concurrent, parallel, asynchronous are all terms to describe the execution of
tasks. However, the most basic tasks are sequential ones: these are composed of
a number of steps and are executed in order.

An example of such process is tying a shoe, illustrated below

| t1 | t2 | t3 | t4 |
|----|----|----|----|
| Put shoe on | Create overhand knot | Finish basic shoe knot | Create double knot (for safety!) |

<!--
put as footnote, or cursive (and maybe gray) caption to table the description of processes
-->

The process is composed of four subtasks (we assume throughout the post that
time is subdivised into equal time slots and that subtasks take 1 or multiple
time slots to execute) which have to be executed strictly in
this specific order. Scrambling steps wouldn’t make much sense.

In general these strong restrictions are too limiting to describe many
processes, especially real-life ones involving many interacting
agents.
To see this you only have to go as far as considering tying both of your shoes.
The straightforward way would be:

| t1 | t2 | t3 | t4 | t5 | t6 | t7 | t8 |
|----|----|----|----|----|----|----|----|
| Put shoe on (LS) | Create overhand knot (LS) | Finish basic shoe knot (LS) | Create double knot (LS) | Put shoe on (RS) | Create overhand knot (RS) | Finish basic shoe knot (RS) | Create double knot (RS) |

However, there are many other valid ways to go about this process.
Not only does changing the order in which I tie the shoes
(left then right or right then left) not change the outcome of the
overall process, but I can also imagine doing the following:

| t1 | t2 | t3 | t4 | t5 | t6 | t7 | t8 |
|----|----|----|----|----|----|----|----|
| Put right shoe on (RS) | Put left shoe on (LS) | Create overhand knot (RS) | Finish basic shoe knot (RS) | Create double knot (RS) | Create overhand knot (LS) | Finish basic shoe knot (LS) | Create double knot (LS) |

In fact, since the composing sequential processes (tying a single shoe) are
themselves composed of subtasks, any permutation of these that maintains the
relative order for each shoe results in a valid execution.
This is because the tying of two shoes is not a sequential process,
but a concurrent one.


<!--
Now that we have a running example for concurrency let’s be clear that there
is still an order to how things are happening, however this is not guaranteed
to be the whole of process A first and then the whole of process B.

A key concept at this point is that of time-slicing
-->

It is important to notice at this point that the total time of execution does
not change with different execution orders. Concurrency only refers to the
ability to have multiple correct orders of execution, but does not lead to any
performance improvements in principle. This changes with parallelism

## Parallel execution

It is by now renown that parallel execution allows to leverage multi-core
hardware to execute programs faster.
But how does this work? The jist is that in concurrent programs, some steps are
independent from each other (these are the one that can be executed in either
order) and can therefore be executed independently on different cores.

In order to understand this, it's important to separate the concept of a task
to be executed, and the actual executor.
When we describe the shoe tying example we are describing the task, while our
hands would be the executor. If we had two pairs of hands we could actually tie
both of our shoes at the same time, or in _parallel_. In this case a possible
parallel execution trace is:

|    | t1 | t2 | t3 | t4 |
|----|----|----|----|----|
| **Hands1** | Put shoe on (LS) | Create overhand knot (LS) | Finish basic shoe knot (LS) | Create double knot (LS) |
| **Hands2** | Put shoe on (RS) | Create overhand knot (RS) | Finish basic shoe knot (RS) | Create double knot (RS) |

<!--
Different traces mixing shoes between executors would also be valid
-->

As we can see this is perfectly parallelisable, and using two executors leads to
a 2x speed up.

So to reiterate, parallelism leverages causal independence between substeps of
a concurrent task to execute them at the same time on multiple cores thus
achieving performance improvements.

## Asynchronous execution

The difference between concurrent and asynchronous is slightly more subtle.
To understand this let's clarify the meaning of scheduling and execution as
separate concepts when running a concurrent program.
Assuming we have one executor (thread, or core), this has the
responsibility of actually performing tasks or subtasks. However it does not
decide what to run next: that is the responsibility of the scheduler.

Let's now go back to our shoes example. Imagine that for some reason, you don't
know how to finish the basic shoe knot (probably the case at some point in your
childhood). In this case you might ask someone else to do it (your parents).
However while they are finishing the knot, you might as well start tying the
other shoe, as otherwise you'd be waiting idle! This is asynchronous execution
in a nutshell: the scheduler yields control of your local executor (your hands)
to carry on with other tasks while the one you were considering is being handled
by an external executor.


when you are little, you put your shoes on, you know how to set up the simple
knot but not the main one. So you ask your mum. but while she does that, your
hands are free, so you might as well start setting up the other shoe.

<!--
This is asynchronous execution: you delegate part of the computation to an
external agent that you have no control over. Since it might take some time for
that computation to give a result, you yield control of that thread (your hands)
so they can carry on with other tasks not dependent on that result
(the other shoe)
-->

In practice this is really useful when it is important to be able to carry on
and be responsive while lengthy computations are being executed (e.g. servers,
GUI, etc).

Here are two diagrams of the shoe example where someone else is finishing the
basic shoe knot, assuming it takes two time slots for the external executor to
finish the knot, and that external execution is represented by `...`:

**No yielding**:

| t1 | t2 | t3 | t4 | t5 | t6 | t7 | t8 | t9 | t10 |
|----|----|----|----|----|----|----|----|----|-----|
| Put shoe on (LS) | Create overhand knot (LS) | ... | ... | Create double knot (LS) | Put shoe on (RS) | Create overhand knot (RS) | ... | ... | Create double knot (RS) |

**With yielding**:

| t1 | t2 | t3 | t4 | t5 | t6 | t7 |
|----|----|----|----|----|----|----|
| Put shoe on (LS) | Create overhand knot (LS) | Put shoe on (RS) | Create overhand knot (RS) | Create double knot (LS) | ... | Create double knot (RS) |

It is worth noting that while not the primary goal, yielding control actually
led to shorter execution time. This is because when yielding control we are
_de facto_ performing parallel execution. In
the above example, at time t3 progress is being made on two fronts, as the local
executor makes progress with the RS while the external executor is progressing
with the LS.


## To conclude…

In practice your systems may well do a bit of everything, i.e. be parallel and
asynchronous (both of which have concurrent as a prerequisite) however from a
conceptual perspective there are no extra complications, they just happen to
have multiple cores available, and to depend on an external execution as
described in the sections above.


<!--
How to do justified text?
-->

---
layout: post
title:  "An easy to remember disambiguation between concurrent, parallel and asynchronous"
date:   2019-02-24 18:26:00 +0000
categories: jekyll update
---

Concurrent programming is confusing as it is, but it can get even worse without a clear idea of what the terms concurrent, parallel and asynchronous mean. While these are all somewhat related concepts, and definitely all important, they mean different things, and here I will share how I visualise their meaning in an informal way that can be helpful in your daily dealings with concurrency.

## Concurrent (vs sequential)

An example of a sequential process is tying a shoe, illustrated below

| t1 | t2 | t3 | t4 |
|----|----|----|----|
| Put shoe on | Create overhand knot | Finish basic shoe knot | Create double knot (for safety!) |

The process is composed of five subtasks (we assume throughout the post that
time is subdivised into equal time slots and that subtasks take 1 or multiple
time slots to execute) which have to be executed strictly in
this specific order. Scrambling steps wouldn’t make much sense.

However what about if you consider tying both of your shoes? The straight forward way would be

| t1 | t2 | t3 | t4 | t5 | t6 | t7 | t8 |
|----|----|----|----|----|----|----|----|
| Put shoe on (LS) | Create overhand knot (LS) | Finish basic shoe knot (LS) | Create double knot (LS) | Put shoe on (RS) | Create overhand knot (RS) | Finish basic shoe knot (RS) | Create double knot (RS) |

However tying two shoes not a sequential process, but a concurrent one.
This not only means that changing the order in which I tie the shoes
(left then right or right then left) does not change the outcome of the
overall process, but I can also imagine doing the following:

| t1 | t2 | t3 | t4 | t5 | t6 | t7 | t8 |
|----|----|----|----|----|----|----|----|
| Put right shoe on (RS) | Put left shoe on (LS) | Create overhand knot (RS) | Finish basic shoe knot (RS) | Create double knot (RS) | Create overhand knot (LS) | Finish basic shoe knot (LS) | Create double knot (LS) |

Given that the composing sequential processes (tying a single shoe) are
themselves composed by subtasks, mixing these subtasks around still results in
a valid execution as long as relative order is maintained for each shoe.

<!-- Now that we have a running example for concurrency let’s be clear that there
is still an order to how things are happening, however this is not guaranteed
to be the whole of process A first and then the whole of process B.

A key concept at this point is that of time-slicing -->

## Parallel - things actually happening at the same time

Any concurrent program has the theoretical requirements to be executed in parallel.
The main difference here is how many threads of execution are available. It's
important to separate the concept of a task to be execute, and the actual executor.
When we describe the shoe tying example we are describing the task, while our hands
would be the executor. If we had two pairs of hands we could actually tie both of
our shoes at the same time, or in _parallel_.

|    | t1 | t2 | t3 | t4 |
|----|----|----|----|----|
| **Hands1** | Put shoe on (LS) | Create overhand knot (LS) | Finish basic shoe knot (LS) | Create double knot (LS) |
| **Hands2** | Put shoe on (RS) | Create overhand knot (RS) | Finish basic shoe knot (RS) | Create double knot (RS) |

Since this essentially cuts the overall time of execution by a half, this is
actually the most important concept for anyone looking for performance gains,
especially from a computational perspective.

## Asynchronous - yield control as you wait on an external dependency

The difference between concurrent and asynchronous is slightly more subtle.

when you are little, you put your shoes on, you know how to set up the simple
knot but not the main one. So you ask your mum. but while she does that, your
hands are free, so you might as well start setting up the other shoe.

This is asynchronous execution: you delegate part of the computation to an
external agent that you have no control over. Since it might take some time for
that computation to give a result, you yield control of that thread (your hands)
so they can carry on with other tasks not dependent on that result
(the other shoe)
The main objective is to be able to carry on and be responsive with lengthy
computations

Assuming it takes two time slots for the external executor to
finish a basic shoe knot, and that external execution is represented by `...`

**No yielding**:

| t1 | t2 | t3 | t4 | t5 | t6 | t7 | t8 | t9 | t10 |
|----|----|----|----|----|----|----|----|----|-----|
| Put shoe on (LS) | Create overhand knot (LS) | ... | ... | Create double knot (LS) | Put shoe on (RS) | Create overhand knot (RS) | ... | ... | Create double knot (RS) |

**With yielding**:

| t1 | t2 | t3 | t4 | t5 | t6 | t7 |
|----|----|----|----|----|----|----|
| Put shoe on (LS) | Create overhand knot (LS) | Put shoe on (RS) | Create overhand knot (RS) | Create double knot (LS) | ... | Create double knot (RS) |

NB: while in principle this is different from parallel execution, asyncronicity
can result in performance benefits thanks to the yielding of thread control. In
the above example, at time t3 progress is being made on two fronts, as the local
executor makes progress with the RS while the external executor is progressing
with the LS


## To conclude…

In practice your systems may well do a bit of everything, i.e. be parallel and asynchronous (both of which have concurrent as a prerequisite) however from a conceptual perspective there are no extra complications, they just happen to have multiple cores available, and to depend on an external execution as described in the sections above.

---
layout: post
title:  "An easy to remember disambiguation between concurrent, parallel and asynchronous"
date:   2019-02-24 18:26:00 +0000
categories: jekyll update
---

Concurrent programming is confusing as it is, but it can get even worse without a clear idea of what the terms concurrent, parallel and asynchronous mean. While these are all somewhat related concepts, and definitely all important, they mean different things, and here I will share how I visualise their meaning in an informal way that can be helpful in your daily dealings with concurrency.

## Concurrent (vs sequential)

Take a sequential example: tying your shoe
put shoe on
create overhand knot
finish basic shoe knot
create double knot (for safety!)

The execution of this process is strictly sequential, meaning it has to happen in this order. scrambling steps wouldn’t make much sense.

However what about if you consider tying both of your shoes? The straight forward way would be
put right shoe (RS) on
create overhand knot
finish basic shoe knot
create double knot
put left shoe (LS) on
create overhand knot
finish basic shoe knot
create double knot

However I can easily imagine doing the following:
put right shoe (RS) on
put left shoe (LS) on
create overhand knot (RS)
finish basic shoe knot (RS)
create double knot (RS)
create overhand knot (LS)
finish basic shoe knot (LS)
create double knot (LS)

In fact even odder COMBINATIONS would still make sense — as long as relative order is maintained for each shoe. E.g.

put right shoe (RS) on
create overhand knot (RS)
put left shoe (LS) on
finish basic shoe knot (RS)
create overhand knot (LS)
create double knot (RS)
finish basic shoe knot (LS)
create double knot (LS)

Now that we have a running example for concurrency let’s be clear that there is still an order to how things are happening, however this is not guaranteed to be the whole of process A first and then the whole of process B.

A key concept at this point is that of time-slicing

## Parallel - things actually happening at the same time

any concurrent program has the theoretical requirements to be executed in parallel.

baking a cake

This is actually the most important concept for anyone looking for performance gains, especially from a computational perspective.

## Asynchronous - yield control as you wait on an external dependency

The difference between concurrent and asynchronous is slightly more subtle.

when you are little, you put your shoes on, you know how to set up the simple knot but not the main one. So you ask your mum. but while she does that, your hands are free, so you might as well start setting up the other shoe.

This is asynchronous execution: you delegate part of the computation to an external agent that you have no control over. Since it might take some time for that computation to give a result, you yield control of that thread (your hands) so they can carry on with other tasks not dependent on that result (the other shoe)

## To conclude…

In practice your systems may well do a bit of everything, i.e. be parallel and asynchronous (both of which have concurrent as a prerequisite) however from a conceptual perspective there are no extra complications, they just happen to have multiple cores available, and to depend on an external execution as described in the sections above.

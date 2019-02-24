---
layout: post
title:  "Threads, actors and message passing - different paradigms for concurrent programming"
date:   2019-02-24 18:26:00 +0000
categories: jekyll update
---

Concurrent programs are a tricky business. Even for experienced programmers
complex distributed applications with many independent parts are extremely hard
to get right. Whether we consider a system comprising several microservices or
a biological simulation with hundreds of thousands of independent agents
interacting with each other the risk of race conditions and deadlock is always
looming over us.

What makes things worse is that these errors are often really hard to debug.
Not many bugs are harder to identify and correct than a heisenbug. This is in
part because thinking about the possible interleaving of our program's execution
is a mammoth task for our brain, and it gets exponentially worse as the
number of concurrent agents and the complexity of the program increase.

Arguably the single most troublesome task in concurrent programming is dealing
with shared memory -- that is memory (e.g. variables) that is accessible by
multiple threads.

However the most widely used concurrency paradigm requires the programmer to do
exactly that: manage a number of threads and their access of common memory,
possibly using locks and synchronisation mechanism to avoid race conditions and
deadlocks.

As I work surrounded by data scientists and data engineers, I got accustomed to
people having Python as a primary language. I am not exactly an expert in Python,
but I have had the opportunity to use it in a concurrent scenario, and when I
did I relied on the [Asyncio][ASYNCIO] library. This library is useful because
Python

[ASYNCIO]: https://docs.python.org/3/library/asyncio.html




What has always been hard in concurrent programming is how to deal with memory sharing across concurrent processes

Most people (using python) still mostly thinks threads and shared memory when thinking concurrency

However the share memory by comunicating over communicate by sharing memory mantra (although fairly old news) has been picking up in recent years

The actor model has become trendier recently with more people using tools like akka

A few people are also aware of a slightly different model that uses concurrent processes communicating over channels. This is the kind of model followed by Erlang and Go

First of all, how does this even work? <give example in the three flavours>

What’s so good about it?
<show how it encourages safer code>

This is awesome, no more deadlock, no more race conditions! Or is it?
<show deadlock/race condition with actors and pi>

Back to square one? Maybe not
<contend that it encourages better style, plus you can augment with types... to follow in future blogs>

IN ALL THIS USE: python asyncio, erlang, go. Maybe mention python MPI

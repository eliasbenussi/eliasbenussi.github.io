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

## Concurrency in Python - threads, shared memory and locking

As I work surrounded by data scientists and data engineers, I got accustomed to
people having Python as a primary language. I am not exactly an expert in Python,
but I have had the opportunity to use it in a concurrent scenario, and when I
did I relied on the [Asyncio][ASYNCIO] library. This library is useful because
Python does not have much native support for multi-threaded programming. Here
is an example of a ping-pong system:

{% highlight python %}
def ping():
    println("ping")
print_hi('Tom')
#=> prints 'Hi, Tom' to STDOUT.
{% endhighlight %}

The model here is that there are multiple threads, which access common memory
and locking infrastructure is in place to prevent dangerous access.

[ASYNCIO]: https://docs.python.org/3/library/asyncio.html

So how do message passing and actors work?

## Actors & message passing

In actors the idea is that you have agents, called actors, whose internal
execution is strictly sequential, and therefore safe. However actors can send
each other asynchronous messages, and execution across actors is concurrent.
Actors generally have rules for sharing memory by sending messages to each other
that - if they don't guarantee safety by design - I contend they at least
encourage thinking about concurrency in a way that is less conducive of errors,
because memory is shared _explicitly_.

In order to send a message to an actor, its reference must be known. Furthemore
and actor receives messages in its Mailbox. While this is not strictly ubiquitous
and there are exceptions (e.g. selectors from rice university) in general there
is a one-to-one relationship between actor and mailbox.

Message passing bears some similarities with the actor model, in the sense that
memory is shared _explicitly_ via messages, however there is a key difference.
There are two first class entities in message passing: processes and channels.
Processes can communicate with each other sending messages over shared channels.
Just like an actor, process's internal execution is sequential, while its
communication is concurrent. However communication between process A and B does
not revolve always around the same mailboxes. Channels can be created and
shared, and two processes can communicate using several channels.

This is the minimal intuition behind actors and message passing for now, although
I plan to explore more the details in future posts.

## Actors with Akka (mention Pony)

## Message passing with Erlang/Go

## Time for demistification
TODO: Deadlock and race condition with actors and message passing

## Conclusion

Communicating to share memory is not the silver bullet for correctness in
concurrent programs, but I believe exploring it has two advantages:
- paradigm shift in thinking about concurrency. It has been for me an
  interesting learning experience
- In practice it encourages better practices. Having to explicitly think about
  sharing memory implies forcing the developer to think about correctness when
  performing a potentially dangerous action



==============================================================================


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

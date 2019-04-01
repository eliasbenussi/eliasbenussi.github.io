---
layout: post
title:  "Concurrent programming with message passing vs shared memory"
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

I would not call Python my primary language, however since it is so predominant
in the data science world, I have been using it at work, and more importantly I
have had the opportunity to see its use in concurrent scenarios.

Support for concurrent programming in Python is relatively new, however the
ecosystem is fast expanding. Currently there seem to be three primary
concurrency modules: `asyncio`, `threading` and `multiprocessing`.
I intend to explore their purposes and differences in the future, but for this
post I will use them to present the two topical concepts: concurrency though
shared memory vs message passing.


The model here is that there are multiple threads, which access common memory
and locking infrastructure is in place to prevent dangerous access.

[ASYNCIO]: https://docs.python.org/3/library/asyncio.html

{% highlight python %}
from multiprocessing import Process, Pipe
import os

def chef_f(chef_restaurant_conn, chef_waiter_conn):
    food_state = chef_restaurant_conn.recv()
    print("chef preparing food...")
    food_state.append("PREPARED")
    chef_waiter_conn.send(food_state)

def waiter_f(waiter_chef_conn, waiter_restaurant_conn):
    food_state = waiter_chef_conn.recv()
    print("waiter about to serve")
    food_state.append("PREPARED")
    waiter_restaurant_conn.send(food_state)

def restaurant():
    print('restaurant processing order')
    food_state = ["ORDERED"]

    restaurant_chef_conn, chef_restaurant_conn = Pipe()
    chef_waiter_conn, waiter_chef_conn = Pipe()
    restaurant_waiter_conn, waiter_restaurant_conn = Pipe()
    print('create connections')

    waiter = Process(
        target=waiter_f,
        args=(waiter_chef_conn, waiter_restaurant_conn))
    waiter.start()
    print('generated waiter process')

    chef = Process(
        target=chef_f,
        args=(chef_restaurant_conn, chef_waiter_conn))
    chef.start()
    print('generated chef process')

    restaurant_chef_conn.send(food_state)
    print(restaurant_waiter_conn.recv())

    chef.join()
    waiter.join()

def main():
    restaurant()

if __name__ == '__main__':
    main()
#=> prints:
# restaurant processing order
# create connections
# generated waiter process
# generated chef process
# chef preparing food...
# waiter about to serve
# ['ORDERED', 'PREPARED', 'PREPARED']
{% endhighlight %}

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
- Since it is a paradigm shift in thinking about concurrency, it provides a
  different perspective when thinking about correctness. As previously mentioned
  concurrency is hard and distributed systems are complex and we can benefit
  from any mental model that helps us think about these things systematically.
  In this sense it is useful even just as a thought experiment.
- I actually believe there is a practical benefit in using this paradigms.
  I believe that the fact that communication forces you to be _explicit_  about
  sharing memory, it encourages thoughtfullness around dangerous actions, and it
  leads to better practices.
It is also worth noting that this is a minimal summary of actors and message
passings and what they entail. I am hoping to continue writing about this
topics, with the hope to eventually get onto more niche -- yet intriguing --
topics such as _reference capabilities_ and _session types_.



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

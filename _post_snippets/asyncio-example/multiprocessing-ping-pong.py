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

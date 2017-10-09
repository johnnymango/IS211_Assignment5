#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""IS 211 Assignment 5 - Simulation"""

import csv
import urllib2
import argparse

#Implement Queue Class (from book).
class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

#Implement Server Class (similar to Printer class from book)
class Server:
    def __init__(self):
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self,new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_processing_time()


#Implement Request Class (similar to Task class from book)
class Request:
    def __init__(self, timestamp, processing_time):
        self.timestamp = int(timestamp)
        self.processing_time = int(processing_time)

    def get_stamp(self):
        return self.timestamp

    def get_processing_time(self):
        return self.processing_time

    def wait_time(self, timestamp):
        return self.timestamp - self.processing_time

#Function to process 1 server.
def simulateOneServer(url):

    #Read CSV
    response = urllib2.urlopen(url)
    reader = csv.reader(response)

    #Instantiate
    server = Server()
    queue = Queue()
    waiting_times = []

    #Pass each row to calculate the
    for row in reader:
        timestamp = row[0]
        processing_time = row[2]
        request = Request(timestamp, processing_time)
        queue.enqueue(request)

        if (not server.busy()) and (not queue.is_empty()):
            new_request = queue.dequeue()
            waiting_times.append(new_request.wait_time(timestamp))
            server.start_next(request)

        server.tick()

    average_wait = (sum(waiting_times)) / (len(waiting_times))
    print("For 1 Server, average Wait %6.2f secs %3d tasks remaining." % (average_wait, queue.size()))

#Function to simulate many servers
def simulateManyServers(url, manyservers):

    #Read CSV
    response = urllib2.urlopen(url)
    reader = csv.reader(response)

    #Instantiate
    server = Server()
    queue = Queue()
    waiting_times = []
    server_list = []

    #Create a listing of multiple servers
    for i in xrange(manyservers):
        server_list.append(server)

    #Iterate for each server in server list
        for j in server_list:
            for row in reader:
                timestamp = row[0]
                processing_time = row[2]
                request = Request(timestamp, processing_time)
                queue.enqueue(request)

                if (not server.busy()) and (not queue.is_empty()):
                    new_request = queue.dequeue()
                    waiting_times.append(new_request.wait_time(timestamp))
                    server.start_next(request)

                server.tick()

    average_wait = (sum(waiting_times)) / (len(waiting_times))
    print("For %3d Servers, average Wait %6.2f secs %3d tasks remaining." % (len(server_list), average_wait,
                                                                               queue.size()))

#Main function using argparse to intake the url and server input.  Calls the single or multiserver functions.
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True)
    parser.add_argument("--servers", type=int, default=1)
    args = parser.parse_args()
    url = args.url
    servers = args.servers

    if servers == 1:
        simulateOneServer(url)
    else:
        simulateManyServers(url, servers)


if __name__ == '__main__':
    main()

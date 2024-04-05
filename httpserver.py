from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import sys 

# origin server to for cdn 
# http://cs5700cdnorigin.ccs.neu.edu:8080/. 

# Size limit for the cache is 20MB (20 * 1024 * 1024 bytes)
CACHE_SIZE = 20 * 1024 * 1024 

hostname = "localhost"
port = 8080

class cacheNode:
    def __init__(self, key, content):
        self.key = key
        self.content = content
        self.freq = 1
        self.prev = None
        self.next = None
        self.size = calculate_size(content)
        
    def calculate_size(self, content):
        return sys.getsizeof(self.key.encode('utf-8')) + sys.getsizeof(self.content.encode('utf-8'))

class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {} # map key to cache node 
        self.frequencyMap = {} # map frequency to the head of each frequency list
        self.min_freq = None
        self.current_size = 0
        
    def get(self, key):
        if key not in self.cache:
            return -1 
        
        node = self.cache[key]
        self.updateFrequency_list(node)
        return node.content

    def put(self, key, value):
        if key in self.cache:
            raise ValueError("Key already exists in cache")
        
        node = cacheNode(key, value)
        while self.current_size + node.size > self.capacity:
            self.evict()
        
        self.cache[key] = node
        if not self.frequencyMap[1]:
            self.frequencyMap[1] = node 
        else:
            node.next = frequencyMap[1]
            self.frequencyMap[1].prev = node
            self.frequencyMap[1] = node
        
        self.min_freq = 1
        
    def updateFrequency_list(self, node):
     
         # remove the node from the previous frequency list
        if node.prev:
            node.prev.next = node.next
            if node.next:
                node.next.prev = node.prev
        else:
            if node.next:
                self.frequencyMap[node.freq] = node.next
                node.next.prev = None
            else:
                self.frequencyMap[node.freq] = None
            
         # update the min_freq
        if node.freq == self.min_freq and not self.frequencyMap[self.min_freq]:
            self.min_freq += 1
        
        # update the frequency of the node
        node.freq += 1
        if not self.frequencyMap[node.freq]:
            self.frequencyMap[node.freq] = node
            node.prev = None
            node.next = None
        else:
            self.frequencyMap[node.freq].prev = node
            node.next = self.frequencyMap[node.freq]
            self.frequencyMap[node.freq] = node
        
        
    def evict(self):
        # remove the least recently used item from the frequency list
        
        if not self.frequencyMap[self.min_freq]:
            raise ValueError("No item in the min_freq list, something is wrong")

        node = self.frequencyMap[self.min_freq]
        
        if not node.next:
            del self.frequencyMap[self.min_freq]
        
         # remove the least frequently used item from cache
        del self.cache[node.key]
            
        # update the size of the cache
        self.current_size -= node.size
        
        # update the min_freq to the next frequency
        # O(n) operation
        
        self.min_freq = min(self.frequencyMap.keys())
        
        
    
class MyServer(BaseHTTPRequestHandler):

    def __init__(self):
        # A hash map to store the cache items and their metadata 
        # key: path, value: (content, size, frequency)
        self.LFUcache = LFUCache(CACHE_SIZE)

    def do_GET(self):
        
        if self.path in self.LFUcache.cache:
            response_content = cache[self.path]
        else:
            # fetch from origin server
            response_content = fetch_from_origin_server(self.path)
            cache[self.path] = response_content
        
        
        print("GET request received")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello World")
    
    
    def fetch_from_origin_server(self, path):
        print("Fetching from origin server")
        return "Hello World"
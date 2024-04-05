from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import sys 
import requests
import gzip
import argparse


# origin server to for cdn 
# http://cs5700cdnorigin.ccs.neu.edu:8080/. 

# Size limit for the cache is 20MB (20 * 1024 * 1024 bytes)
CACHE_SIZE = 20 * 1024 * 1024 

hostname = "localhost"
port = 8080

LFUcache = LFUCache(CACHE_SIZE)

class cacheNode:
    def __init__(self, key, content):
        self.key = key
        self.content = self.compress_content(content)
        self.freq = 1
        self.prev = None
        self.next = None
        self.size = self.calculate_size(content)
    
    def compress_content(self):
        return gzip.compress(self.content.encode('utf-8'))
        
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

class MyHTTPServer(HTTPServer):
    def __init__(self, server_address, handler_class, origin):
        self.origin = origin
        super().__init__(server_address, handler_class)
       
class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):  
        global LFUcache
        if self.path in LFUcache.cache:
            response_content = LFUcache.get(self.path).content
            decompress_content = gzip.decompress(response_content).decode('utf-8')
        else:
            # fetch from origin server
            response_content = self.fetch_from_origin_server(self.path)
            if not response_content:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"404 Not Found")
                return
            else:
                LFUcache.put(self.path, response_content)
        
        print("GET request received")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        # self.send_header("Content-Encoding", "gzip")
        self.end_headers()
        self.wfile.write(decompress_content.encode('utf-8'))
    
    
    def fetch_from_origin_server(self, path):
        origin_url = f"{self.server.origin}{path}"
    
        print("Fetching from origin server")
        try: 
            response = requests.get(origin_url)
            response.raise_for_status()
            content = response.content.decode('utf-8')
            return content
        except requests.exceptions.HTTPError as err:
            print(f"Error: {err}")
            return None 
        
def run(server_class=MyHTTPServer, handler_class=MyHandler, port=8080, origin =""):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class, origin)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP CDN Server")
    parser.add_argument('-p', '--port', type=int, help='Port number the HTTP server binds to', required=True)
    parser.add_argument('-o', '--origin', type=str, help='Origin server URL for the CDN', required=True)

    args = parser.parse_args()

    run(port=args.port, origin=args.origin)
                                    
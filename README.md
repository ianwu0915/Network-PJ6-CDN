## Content Delivery Network (CDN) Implementation

This document outlines the implementation of a simple Content Delivery Network (CDN) using custom DNS and HTTP servers written in Python. The CDN is designed to optimize the delivery of web content by reducing latency, improving security, and increasing redundancy.

### High-Level Approach

The CDN system consists of two main components:

1. **DNS Server**: Directs users to the closest CDN edge server based on their geographic location to reduce latency.
2. **HTTP Server**: Hosts the content and implements caching strategies to improve load times and reduce requests to the origin server.

### DNS Server Implementation

The DNS server is implemented using Python's `socket` and `dnslib` libraries. It handles DNS queries and directs them to the closest edge server using a simple geolocation-based algorithm. The server locations are predefined, and their latitude and longitude are used to calculate the distance to the client's IP address.

**Key Features:**

- **Geolocation Lookup**: For each DNS query, the server calculates the client's location using the IP2Location API and determines the closest server by geographic proximity.
- **Load Balancing**: Distributes client requests based on server load and proximity, aiming to use servers with less than 80% load preferentially.
- **DNS Caching**: Improves response time and reduces API calls by caching IP-to-location lookups.

**Challenges Faced:**

- **API Rate Limits**: The free tier of IP2Location API has rate limits that required handling of exceptions and implementing caching to minimize lookups.
- **Error Handling**: Various network errors and API response issues needed robust exception handling to ensure server stability.

```python
# Simplified DNS Server Example
class Dns_server:
    def get_closest_location(self, client_ip):
        # This method finds the closest server by calculating geographic distance
        pass
```

### HTTP Server Implementation

The HTTP server is implemented using Python's `http.server` and `socketserver` modules. It serves content from the CDN's edge servers, implementing an LFU (Least Frequently Used) cache to optimize content delivery.

**Key Features:**

- **LFU Caching**: Stores frequently requested files to reduce latency and server load on the origin.
- **Content Compression**: Uses gzip compression to reduce data transfer size.
- **Dynamic Origin Change Handling**: Can dynamically handle changes in the origin server without downtime or manual configuration changes.

**Challenges Faced:**

- **Cache Eviction Strategy**: Implementing and testing the LFU cache eviction strategy to ensure it efficiently utilizes the limited cache space.
- **Concurrency**: Managing concurrent requests using threading to ensure high availability and responsiveness.

```python
# Simplified HTTP Server Example
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handles GET requests by fetching cached content or retrieving from the origin server
        pass
```

### Setup and Running

#### Deployment

To deploy the CDN, use the `deployCDN` script which will configure both DNS and HTTP servers on specified machines:

```bash
./deployCDN [-p port] [-o origin] [-n name] [-u username] [-i keyfile]
```

#### Running the Servers

After deployment, use the `runCDN` script to start the servers:

```bash
./runCDN [-p port] [-o origin] [-n name] [-u username] [-i keyfile]
```

#### Stopping the Servers

To stop all components of the CDN, use the `stopCDN` script:

```bash
./stopCDN [-p port][-u username] [-i keyfile]
```

### Conclusion

This CDN implementation leverages basic DNS redirection and HTTP caching techniques to demonstrate the core functionalities of a CDN. The project faced challenges mainly related to network programming and caching strategies, which were addressed using Python's robust libraries and careful exception handling.

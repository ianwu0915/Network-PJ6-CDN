import argparse
import socket
import sys
from dnslib import DNSRecord, DNSHeader, RR, A
import ip2geotools.databases.noncommercial as ip


class Dns_server:
    def __init__(self, port, name):
        self.index = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", port))
        if not name.endswith("."):
            name += "."
        self.name = name
        self.location = [
            "45.33.55.171",
            "170.187.142.220",
            "213.168.249.157",
            "139.162.82.207",
            "45.79.124.209",
            "192.53.123.145",
            "192.46.221.203",
        ]
        self.city = []
        for each in self.location:
            x = ip.DbIpCity.get(each)
            self.city.append(x)

    def get_closest_location(self, client_ip):
        try:
            client_location = ip.DbIpCity.get(client_ip)
        except Exception as e:
            print(f"An error occured {e}", file=sys.stderr)
            return None

        min_distance = float("inf")
        closest_location = None
        for i in range(len(self.city)):
            server_location = self.city[i]
            distance_lat = abs(client_location.latitude - server_location.latitude)
            distance_lon = abs(client_location.longitude - server_location.longitude)
            distance = distance_lat + distance_lon  # Sum of absolute differences
            if distance < min_distance:
                min_distance = distance
                closest_location = server_location
        return closest_location

    def check_index_range(self):
        if self.index >= len(self.city):
            self.index = 0
        if self.index < 0:
            self.index = 0

    def run(self):
        print("DNS Server is running...")
        print(f"The self.name is {self.name}")
        print("This is the stderr output", file=sys.stderr)
        while True:
            data, addr = self.socket.recvfrom(1024)
            request = DNSRecord.parse(data)
            qname = str(request.q.qname)
            qtype = request.q.qtype
            print(f"Qname: {qname}\nGet request: {request}")
            if (
                qname == self.name and qtype == 1
            ):  # Check if it's an A query for the specified name
                print("Trying to get the closet location!")
                closest = self.get_closest_location(addr)
                if not closest:
                    self.check_index_range()
                    closest = self.city[self.index]
                    self.index += 1
                response = DNSRecord(
                    DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q
                )
                response.add_answer(RR(qname, rdata=A(closest.ip_address)))
                self.socket.sendto(response.pack(), addr)


def main():
    parser = argparse.ArgumentParser(description="DNS Server")
    parser.add_argument(
        "-n",
        dest="name",
        default="cs5700cdn.example.com.",
        type=str,
        help="CDN-specific name",
    )
    parser.add_argument(
        "-p",
        dest="port",
        type=int,
        default=20210,
        help="Port number for the DNS server",
    )
    args = parser.parse_args()

    dns_server = Dns_server(args.port, args.name)
    dns_server.run()


if __name__ == "__main__":
    main()

import heapq
from typing import Dict, List, Tuple, Optional

# --- estructuras de datos ---
class Key:
    def __init__(self, key_id: str, max_usages: int):
        self.key_id = key_id
        self.usages = 0
        self.max_usages = max_usages
        self.expired = False

    def available(self) -> bool:
        return (not self.expired) and (self.usages < self.max_usages)

    def use(self):
        self.usages += 1
        if self.usages >= self.max_usages:
            self.expired = True

class Server:
    def __init__(self, name: str):
        self.name = name
        self.keys: List[Key] = []

    def add_key(self, key: Key):
        self.keys.append(key)

    def has_available_key(self) -> bool:
        return any(k.available() for k in self.keys)

    def select_key(self) -> Optional[Key]:
        avail = [k for k in self.keys if k.available()]
        if not avail:
            return None
        return min(avail, key=lambda k: k.usages)

# --- grafo: adjacency list con pesos no negativos ---
def dijkstra_find_server_with_key(graph: Dict[str, List[Tuple[str, float]]],
                                  servers: Dict[str, Server],
                                  origin: str) -> Optional[str]:
    dist = {node: float('inf') for node in graph}
    dist[origin] = 0.0
    heap = [(0.0, origin)]
    visited = set()

    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        if servers[u].has_available_key():
            return u
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return None

# --- asignación de llave a transacción ---
audit_log = []

def assign_key(transaction_id: str, origin: str,
               graph: Dict[str, List[Tuple[str, float]]],
               servers: Dict[str, Server]) -> Optional[Tuple[str, str]]:
    server_name = dijkstra_find_server_with_key(graph, servers, origin)
    if server_name is None:
        print(f"[TX {transaction_id}] No available key reachable from {origin}")
        return None
    server = servers[server_name]
    key = server.select_key()
    if key is None:
        print(f"[TX {transaction_id}] Race: server {server_name} no key on second check")
        return None
    key.use()
    audit_log.append((transaction_id, server_name, key.key_id))
    print(f"[TX {transaction_id}] Assigned key {key.key_id} from server {server_name} (usages={key.usages}/{key.max_usages})")
    return (server_name, key.key_id)

# --- ejemplo de uso ---
if __name__ == "__main__":
    graph = {
        'A': [('B', 10), ('C', 5)],
        'B': [('A', 10), ('C', 2), ('D', 1)],
        'C': [('A', 5), ('B', 2), ('D', 9)],
        'D': [('B', 1), ('C', 9)]
    }

    servers = {name: Server(name) for name in graph.keys()}
    servers['B'].add_key(Key("kB1", max_usages=3))
    servers['C'].add_key(Key("kC1", max_usages=2))
    servers['D'].add_key(Key("kD1", max_usages=1))

    txs = [("T1","A"), ("T2","A"), ("T3","A"), ("T4","A"), ("T5","A")]

    for txid, origin in txs:
        assign_key(txid, origin, graph, servers)

    print("\nAudit log:")
    for entry in audit_log:
        print(entry)

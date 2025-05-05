import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import networkx as nx
import random

# Generate random coordinates within UK map bounds
random_lat = random.uniform(49.5, 59.0)
random_lon = random.uniform(-8.0, 2.0)

# Sample UK locations (city: (latitude, longitude))
locations = {
    "London": (51.5074, -0.1278),
    "Manchester": (53.4808, -2.2426),
    "Edinburgh": (55.9533, -3.1883),
    "Bristol": (51.4545, -2.5879),
    "Birmingham": (52.4862, -1.8904),
    "Secret Treasure": (random_lat, random_lon),
}

# Sample network edges between cities
edges = [
    ("London", "Birmingham"),
    ("Birmingham", "Manchester"),
    ("Manchester", "Edinburgh"),
    ("London", "Bristol"),
    ("Bristol", "Manchester"),
]

# Create graph
G = nx.Graph()
for city, coords in locations.items():
    G.add_node(city, pos=coords)
G.add_edges_from(edges)

# Plot map and network
plt.figure(figsize=(10, 12))
m = Basemap(
    projection='merc',
    llcrnrlat=49.5,
    urcrnrlat=59,
    llcrnrlon=-8,
    urcrnrlon=2,
    resolution='i'
)
m.drawmapboundary(fill_color='lightblue')
m.fillcontinents(color='lightgray', lake_color='lightblue')
m.drawcoastlines()
m.drawcountries()

# Draw nodes
for city, (lat, lon) in locations.items():
    x, y = m(lon, lat)
    if city == "Secret Treasure":
        plt.plot(x, y, marker='x', color='red', markersize=12, markeredgewidth=3)
    else:
        plt.plot(x, y, 'ro', markersize=8)
    plt.text(x + 10000, y + 10000, city, fontsize=10)

# Draw edges
for u, v in G.edges():
    lat1, lon1 = locations[u]
    lat2, lon2 = locations[v]
    x1, y1 = m(lon1, lat1)
    x2, y2 = m(lon2, lat2)
    plt.plot([x1, x2], [y1, y2], 'b-', linewidth=2)

plt.title("Network Overlay on UK Map with Secret Treasure", fontsize=14)
plt.show()

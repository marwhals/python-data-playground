import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Use a reliable online GeoJSON of world countries from GitHub
url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
gdf = gpd.read_file(url)

# Print basic info
print("CRS:", gdf.crs)
print("Columns:", gdf.columns)
print("Number of features:", len(gdf))

# Create a point and buffer it
point = Point(-0.1278, 51.5074)  # London
buffer = point.buffer(1.0)  # Buffer in degrees (CRS is EPSG:4326)

# Create GeoDataFrame for buffer
buffer_gdf = gpd.GeoDataFrame(geometry=[buffer], crs=gdf.crs)

# Find features that intersect with the buffer
intersecting = gdf[gdf.geometry.intersects(buffer)]

# Plot and save
fig, ax = plt.subplots(figsize=(10, 8))
gdf.plot(ax=ax, color='lightgrey', edgecolor='black')
buffer_gdf.plot(ax=ax, color='blue', alpha=0.3)
intersecting.plot(ax=ax, color='red')

plt.title("Features Intersecting with Buffer Zone")

# Save the figure as a PNG
output_path = "buffer_intersections.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Plot saved to {output_path}")

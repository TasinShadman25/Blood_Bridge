import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Load donors CSV
df = pd.read_csv("data/donors.csv")

# Initialize geocoder
geolocator = Nominatim(user_agent="blood_donation_app", timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Only fill missing lat/lon
if 'latitude' not in df.columns or 'longitude' not in df.columns:
    df['full_location'] = df['location'] + ', Bangladesh'
    df[['latitude','longitude']] = df['full_location'].apply(
        lambda x: pd.Series((geocode(x).latitude, geocode(x).longitude) if geocode(x) else (None, None))
    )

# Save back to CSV
df.to_csv("data/donors.csv", index=False)
print("Lat/Lon added to donors.csv successfully!")

import pandas as pd
from geopy.distance import geodesic

def load_hospital_data():
    """Load the hospital CSV file."""
    try:
        df = pd.read_csv("healthcare_facilities.csv")
        df.fillna("Unknown", inplace=True)  # Clean missing data
        return df
    except FileNotFoundError:
        print("Error: CSV file not found. Place 'healthcare_facilities.csv' in the project folder.")
        return None

def get_user_location():
    """Ask user for their GPS coordinates."""
    print("\n=== Hospital Finder ===")
    print("Enter your current coordinates:")
    while True:
        try:
            lat = float(input("Latitude (e.g., -1.2864 for Nairobi): "))
            lon = float(input("Longitude (e.g., 36.8172 for Nairobi): "))
            return (lat, lon)
        except ValueError:
            print("Invalid input! Enter numbers only.")

def find_nearest_hospital(hospitals_df, user_coords):
    """Calculate distances and return the closest hospital."""
    hospitals_df["Distance_km"] = hospitals_df.apply(
        lambda row: geodesic(user_coords, (row["Latitude"], row["Longitude"])).km,
        axis=1
    )
    nearest_hospital = hospitals_df.sort_values("Distance_km").iloc[0]
    return nearest_hospital

def main():
    hospitals_df = load_hospital_data()
    if hospitals_df is None:
        return
    
    user_coords = get_user_location()
    nearest = find_nearest_hospital(hospitals_df, user_coords)
    
    print("\n🚑 Nearest Hospital Found!")
    print("------------------------")
    print(f"Name: {nearest['Facility_N']}")
    print(f"Type: {nearest['Type']}")
    print(f"County: {nearest['County']}")
    print(f"Distance: {nearest['Distance_km']:.2f} km")
    print(f"Contact: {nearest['Contact']}")

if __name__ == "__main__":
    main()
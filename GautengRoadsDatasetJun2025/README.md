# Gauteng Road Traffic Dataset

This dataset provides detailed information on the road network, traffic conditions, incidents, weather, and delivery logistics within the Gauteng province of South Africa.  
It is structured for exploratory analysis, visualization, and research into traffic, mobility, and logistics.

---

## 📂 Files

### 1. `roads.csv`
- Road segments across Gauteng.  
- Fields:  
  - `road_id` – Road identifier (N = National, R = Regional/Provincial, M = Metropolitan).  
  - `segment_id` – Unique segment code.  
  - `from_lat`, `from_lon`, `to_lat`, `to_lon` – Segment endpoints.  
  - `length_m` – Segment length in meters.  
  - `road_type` – {national, provincial, regional, metropolitan}.  
  - `lanes` – Number of lanes.  
  - `speed_limit_kph` – Speed limit.  
  - `oneway` – Whether the road is one-way (1 = yes, 0 = no).  
  - `municipality` – Johannesburg, Tshwane, or Ekurhuleni.

---

### 2. `historical_speeds.csv`
- Historical speed and volume measurements.  
- Collected in **5-minute intervals**.  
- Fields:  
  - `segment_id` – Road segment.  
  - `timestamp` – Date/time (SAST).  
  - `avg_speed_kph` – Average speed.  
  - `pct_freeflow` – Speed as a fraction of typical freeflow speed.  
  - `vehicle_count` – Estimated number of vehicles observed in the interval.  
  - `interval_minutes` – Interval length (5).  
  - `source` – Data origin tag.

**Traffic volumes are scaled realistically:**  
- National roads (N): 200–1500 vehicles / 5 min during peak.  
- Regional roads (R): 50–400 vehicles / 5 min during peak.  
- Metropolitan roads (M): 20–200 vehicles / 5 min during peak.  

---

### 3. `incidents.csv`
- Road and traffic-related incidents.  
- Fields:  
  - `incident_id` – Unique incident code.  
  - `timestamp` – Time of report.  
  - `type` – {accident, roadwork, closure, hazard}.  
  - `severity` – Scale 1–5.  
  - `lat`, `lon` – Location.  
  - `affected_segment_id` – Road segment (if applicable).  
  - `description` – Incident description.  
  - `source` – Origin tag.

---

### 4. `weather.csv`
- Weather conditions linked to road segments.  
- Fields:  
  - `station_id` – Weather station ID.  
  - `timestamp` – Time of record.  
  - `lat`, `lon` – Station coordinates.  
  - `temperature_c` – Temperature in Celsius.  
  - `precip_mm_h` – Precipitation rate.  
  - `wind_kph` – Wind speed.  
  - `visibility_km` – Visibility.  
  - `wx_condition` – {clear, partly_cloudy, rain, thunderstorm, fog}.  
  - `nearest_segment_id` – Closest road segment.

---

### 5. `deliveries.csv`
- Example delivery schedule records.  
- Fields:  
  - `delivery_id` – Delivery identifier.  
  - `truck_id` – Assigned truck.  
  - `scheduled_departure_utc`, `scheduled_arrival_utc` – Planned times.  
  - `origin_name`, `origin_lat`, `origin_lon` – Origin details.  
  - `destination_name`, `destination_lat`, `destination_lon` – Destination details.  
  - `priority` – {low, normal, high, urgent}.  
  - `commodity` – Goods transported.  
  - `per_km_cost_rand` – Cost per kilometer.  
  - `per_hour_cost_rand` – Cost per hour.

---

### 6. `truck_profiles.csv`
- Truck specifications.  
- Fields:  
  - `truck_id` – Unique truck ID.  
  - `max_weight_tons` – Maximum load.  
  - `height_m`, `width_m` – Dimensions.  
  - `hazmat` – Hazardous materials flag (0 = no, 1 = yes).

---

### 7. `assignments.csv`
- Delivery assignments with planned routes and outcomes.  
- Fields:  
  - `assignment_id` – Unique ID.  
  - `delivery_id` – Links to deliveries.  
  - `planned_departure_utc`, `planned_arrival_utc` – Planned times.  
  - `planned_distance_km` – Distance in kilometers.  
  - `planned_duration_min` – Duration in minutes.  
  - `route_segments` – JSON list of segment IDs.  
  - `status` – {planned, in_progress, delayed, rescheduled, completed}.  
  - `reason` – Cause of delay/rescheduling (if applicable).

---

## 🌍 Geographic Coverage
- Province: **Gauteng, South Africa**  
- Municipalities: Johannesburg, Tshwane (Pretoria), Ekurhuleni.  
- Roads: National freeways (N1, N3, N12, N14), regional roads (R21, R24, R55, R511), and metropolitan roads (M1, M2).  

---

## 📜 Notes
- The dataset includes both road infrastructure and temporal measurements (traffic speeds, volumes, weather, incidents).  
- Time-based data is structured in **5-minute intervals** for one week of history.  
- Vehicle counts are scaled to reflect realistic conditions on Gauteng’s roads.  

---

## 🏷️ License
- Synthetic records are freely shareable.  
- If merged with external sources (e.g., OSM, SANRAL, SAWS), follow their license requirements.  
- Cite: “© OpenStreetMap contributors” when including OSM-derived data.

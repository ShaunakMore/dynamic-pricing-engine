# Dataset Design

Dynamic Pricing system for vacation rentals.

## Features

### Temporal Features

```
date
day_of_week
month
weekend
season
holiday
```

### Property Features

```
room_type
rating
amenities_score
location_score
```

### Market Features

```
competitor_price
nearby_event
demand_index
```

### Pricing Features

```
price
occupancy_rate
```

## Feature Relations

- Higher prices reduces occupancy
- Weekends increase occupancy
- Holidays increase demand
- Competitior prices influence our prices
- Nearby events increase demand
- Good aminities increases demand
- Amicable seasons increases demand


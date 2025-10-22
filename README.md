# Shipment Tracking API

A Django REST Framework API for tracking shipments using the Shippo API.

## Setup

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install django djangorestframework requests
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

## API Endpoints

### List All Shipments

Get a list of all tracked shipments stored in the database.

**Endpoint:** `GET /shipments/`

**Example:**
```bash
curl -X GET http://127.0.0.1:8000/shipments/
```

### Track a Shipment

Track a shipment using carrier and tracking number. This endpoint fetches tracking information from the Shippo API and stores it in the database.

**Endpoint:** `GET /shipments/shipment/`

**Headers:**
- `Authorization` (required): Your Shippo API token (format: `ShippoToken <your_token>`)
- `X-Tracking-Number` (required): The tracking number to look up
- `X-Carrier` (optional): The carrier name (defaults to "shippo")
- `X-Metadata` (optional): Additional metadata to associate with the shipment

**Example:**
```bash
curl -X GET http://127.0.0.1:8000/shipments/shipment/ \
  -H "Content-Type: application/json" \
  -H "Authorization: ShippoToken YOUR_SHIPPO_TOKEN_HERE" \
  -H "X-Carrier: shippo" \
  -H "X-Tracking-Number: SHIPPO_DELIVERED" \
  -H "X-Metadata: Order 0001234"
```

**Response:**
```json
{
  "tracking_number": "SHIPPO_DELIVERED",
  "events": [
    {
      "status": "DELIVERED",
      "status_date": "2025-01-15T10:30:00Z",
      "status_details": "Package delivered successfully"
    }
  ]
}
```

## Testing with Shippo Test Tracking Numbers

Shippo provides test tracking numbers for development:
- `SHIPPO_DELIVERED` - Simulates a delivered package
- `SHIPPO_TRANSIT` - Simulates a package in transit
- `SHIPPO_PRE_TRANSIT` - Simulates a package awaiting pickup

## Database Models

### Shipment
- `tracking_number`: Unique tracking identifier
- `carrier`: Shipping carrier name
- `tracking_status`: Current status of the shipment
- `eta`: Estimated time of arrival
- `metadata`: Additional custom metadata

### TrackingEvent
- `shipment`: Foreign key to Shipment
- `status`: Event status
- `status_date`: When the status occurred
- `status_details`: Additional details about the status

## Notes

- Make sure to get a Shippo API token from [goshippo.com](https://goshippo.com)
- The API uses custom headers (prefixed with `X-`) to pass tracking parameters
- All tracking data is stored locally in the SQLite database

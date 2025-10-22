from rest_framework.decorators import api_view
from tracking.serializers import ShipmentSerializer
from rest_framework.response import Response
from rest_framework import status
import requests

from .models import Shipment


@api_view(["GET"])
def shipments_list(request):
    shipments = Shipment.objects.all()
    serializer = ShipmentSerializer(shipments, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def shipment(request):
    carrier = request.data.get("carrier", "shippo")
    tracking_number = request.data.get("tracking_number")
    metadata = request.data.get("metadata", "")

    # TODO: Include error checking for when required field not provided (eg tracking number)
    url = "https://api.goshippo.com/tracks/"
    # TODO: Remove hardcode authoriation token and get from request
    headers = {
        "Authorization": "ShippoToken REDACTED_TOKEN"
    }
    data = {
        "carrier": carrier,
        "tracking_number": tracking_number,
        "metadata": metadata,
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        print(response.json())
        response.raise_for_status()  # Raise exception for 4xx/5xx status codes

        serializer = ShipmentSerializer(data=response.json())
        serializer.is_valid(raise_exception=True)
        shipment = serializer.save()

        response_data = {
            "tracking_number": shipment.tracking_number,
            "events": [
                {
                    "status": event.status,
                    "status_date": event.status_date,
                    "status_details": event.status_details,
                }
                for event in shipment.tracking_events.all()
            ],
        }

        return Response(response_data, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

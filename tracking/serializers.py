from rest_framework import serializers
from .models import Shipment, TrackingEvent
from drf_writable_nested.serializers import WritableNestedModelSerializer


class TrackingEventSerializer(WritableNestedModelSerializer):

    class Meta:
        model = TrackingEvent
        fields = [
            "status",
            "status_date",
            "status_details",
            "object_id",
            "object_created",
            "object_updated",
        ]


class ShipmentSerializer(WritableNestedModelSerializer):
    tracking_history = TrackingEventSerializer(many=True, source="tracking_events")

    class Meta:
        model = Shipment
        fields = ["tracking_number", "tracking_history"]

    def create(self, validated_data):
        tracking_number = validated_data.get("tracking_number")

        try:
            shipment = Shipment.objects.get(tracking_number=tracking_number)
            return shipment
        except Shipment.DoesNotExist:
            return super().create(validated_data)

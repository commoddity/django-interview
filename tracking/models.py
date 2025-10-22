from django.db import models


class Shipment(models.Model):
    """Simplified shipment tracking model"""

    tracking_number = models.CharField(max_length=100, db_index=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.tracking_number

    @property
    def current_status(self):
        """Returns the most recent tracking event"""
        return self.tracking_events.order_by("-status_date").first()


class TrackingEvent(models.Model):
    """Represents a tracking event/history entry from tracking_history"""

    STATUS_CHOICES = [
        ("UNKNOWN", "Unknown"),
        ("PRE_TRANSIT", "Pre-Transit"),
        ("TRANSIT", "In Transit"),
        ("DELIVERED", "Delivered"),
        ("RETURNED", "Returned"),
        ("FAILURE", "Failure"),
    ]

    shipment = models.ForeignKey(
        Shipment, on_delete=models.CASCADE, related_name="tracking_events"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    status_date = models.DateTimeField()
    status_details = models.TextField()

    object_id = models.CharField(max_length=100)
    object_created = models.DateTimeField()
    object_updated = models.DateTimeField()

    class Meta:
        ordering = ["-status_date"]
        indexes = [
            models.Index(fields=["shipment", "-status_date"]),
        ]

    def __str__(self):
        return f"{self.shipment.tracking_number} - {self.status} - {self.status_date}"

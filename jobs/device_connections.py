from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device, ConsolePort, PowerPort
from nautobot.extras.models import Status


name = "Device Connections Validation"


class DeviceConnectionsReport(Job):
    """Validate the minimum physical connections for each device."""

    class Meta:
        """Meta class for DeviceConnectionsReport"""

        name = "Verify console connections and power supplies"
        description = "Validate that each device has a console connection and a minimum number of power supplies"
        read_only = True

    def test_console_connection(self):
        """Test console connections."""
        # Check that every console port for every active device has a connection defined.
        active_status = Status.objects.get_for_model(Device).get(slug="active")
        for console_port in ConsolePort.objects.prefetch_related("device").filter(
            device__status=active_status
        ):
            if console_port.connected_endpoint is None:
                self.log_failure(
                    obj=console_port.device,
                    message="No console connection defined for {}".format(
                        console_port.name
                    ),
                )
            elif not console_port.connection_status:
                self.log_warning(
                    obj=console_port.device,
                    message="Console connection for {} marked as planned".format(
                        console_port.name
                    ),
                )
            else:
                self.log_success(obj=console_port.device)

    def test_power_connections(self):
        """Test power connections."""
        # Check that every active device has at least two connected power supplies.
        active_status = Status.objects.get_for_model(Device).get(slug="active")
        for device in Device.objects.filter(status=active_status):
            connected_ports = 0
            for power_port in PowerPort.objects.filter(device=device):
                if power_port.connected_endpoint is not None:
                    connected_ports += 1
                    if not power_port.connection_status:
                        self.log_warning(
                            obj=device,
                            message="Power connection for {} marked as planned".format(
                                power_port.name
                            ),
                        )
            if connected_ports < 2:
                self.log_failure(
                    obj=device,
                    message="{} connected power supplies found (2 needed)".format(
                        connected_ports
                    ),
                )
            else:
                self.log_success(obj=device)

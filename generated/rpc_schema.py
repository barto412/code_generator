from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict

SERVICE_NAME = 'DeviceManagement'

@dataclass
class SendTelemetryRequest: 
    device_id: str
    timestamp: str
    temperature: float
    humidity: float
    vibration: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "device_id": self.device_id,
            "timestamp": self.timestamp,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "vibration": self.vibration,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'SendTelemetryRequest':
        return SendTelemetryRequest(**{
            "device_id": data.get("device_id"),
            "timestamp": data.get("timestamp"),
            "temperature": data.get("temperature"),
            "humidity": data.get("humidity"),
            "vibration": data.get("vibration"),
        })

@dataclass
class SendTelemetryResponse: 
    status: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "message": self.message,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'SendTelemetryResponse':
        return SendTelemetryResponse(**{
            "status": data.get("status"),
            "message": data.get("message"),
        })

@dataclass
class UpdateConfigurationRequest: 
    device_id: str
    sampling_rate: int
    operational_mode: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "device_id": self.device_id,
            "sampling_rate": self.sampling_rate,
            "operational_mode": self.operational_mode,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'UpdateConfigurationRequest':
        return UpdateConfigurationRequest(**{
            "device_id": data.get("device_id"),
            "sampling_rate": data.get("sampling_rate"),
            "operational_mode": data.get("operational_mode"),
        })

@dataclass
class UpdateConfigurationResponse: 
    accepted: bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "accepted": self.accepted,
            "message": self.message,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'UpdateConfigurationResponse':
        return UpdateConfigurationResponse(**{
            "accepted": data.get("accepted"),
            "message": data.get("message"),
        })

@dataclass
class ValidateFirmwareRequest: 
    device_id: str
    firmware_checksum: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "device_id": self.device_id,
            "firmware_checksum": self.firmware_checksum,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'ValidateFirmwareRequest':
        return ValidateFirmwareRequest(**{
            "device_id": data.get("device_id"),
            "firmware_checksum": data.get("firmware_checksum"),
        })

@dataclass
class ValidateFirmwareResponse: 
    valid: bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "message": self.message,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'ValidateFirmwareResponse':
        return ValidateFirmwareResponse(**{
            "valid": data.get("valid"),
            "message": data.get("message"),
        })

@dataclass
class RunDiagnosticsRequest: 
    device_id: str
    test_suite: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "device_id": self.device_id,
            "test_suite": self.test_suite,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'RunDiagnosticsRequest':
        return RunDiagnosticsRequest(**{
            "device_id": data.get("device_id"),
            "test_suite": data.get("test_suite"),
        })

@dataclass
class RunDiagnosticsResponse: 
    result: str
    passed: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "result": self.result,
            "passed": self.passed,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'RunDiagnosticsResponse':
        return RunDiagnosticsResponse(**{
            "result": data.get("result"),
            "passed": data.get("passed"),
        })

class ClientStub:
    def __init__(self, transport):
        self.transport = transport

    def send_telemetry(self, request: SendTelemetryRequest) -> SendTelemetryResponse:
        payload = {'method': 'send_telemetry', 'params': request.to_dict()}
        response = self.transport.call(payload)
        return SendTelemetryResponse.from_dict(response['result'])

    def update_configuration(self, request: UpdateConfigurationRequest) -> UpdateConfigurationResponse:
        payload = {'method': 'update_configuration', 'params': request.to_dict()}
        response = self.transport.call(payload)
        return UpdateConfigurationResponse.from_dict(response['result'])

    def validate_firmware(self, request: ValidateFirmwareRequest) -> ValidateFirmwareResponse:
        payload = {'method': 'validate_firmware', 'params': request.to_dict()}
        response = self.transport.call(payload)
        return ValidateFirmwareResponse.from_dict(response['result'])

    def run_diagnostics(self, request: RunDiagnosticsRequest) -> RunDiagnosticsResponse:
        payload = {'method': 'run_diagnostics', 'params': request.to_dict()}
        response = self.transport.call(payload)
        return RunDiagnosticsResponse.from_dict(response['result'])


class ServerSkeleton:
    def dispatch(self, payload: dict[str, Any]) -> dict[str, Any]:
        method = payload.get('method')
        params = payload.get('params', {})

        if method is None:
            raise ValueError('Missing RPC method name')

        if method == 'send_telemetry':
            request = SendTelemetryRequest.from_dict(params)
            result = self.on_send_telemetry(request)
            return {'result': result.to_dict()}
        if method == 'update_configuration':
            request = UpdateConfigurationRequest.from_dict(params)
            result = self.on_update_configuration(request)
            return {'result': result.to_dict()}
        if method == 'validate_firmware':
            request = ValidateFirmwareRequest.from_dict(params)
            result = self.on_validate_firmware(request)
            return {'result': result.to_dict()}
        if method == 'run_diagnostics':
            request = RunDiagnosticsRequest.from_dict(params)
            result = self.on_run_diagnostics(request)
            return {'result': result.to_dict()}

        raise ValueError(f'Unknown method: {method}')

    def on_send_telemetry(self, request: SendTelemetryRequest) -> SendTelemetryResponse:
        raise NotImplementedError('Override send_telemetry in a concrete service implementation')

    def on_update_configuration(self, request: UpdateConfigurationRequest) -> UpdateConfigurationResponse:
        raise NotImplementedError('Override update_configuration in a concrete service implementation')

    def on_validate_firmware(self, request: ValidateFirmwareRequest) -> ValidateFirmwareResponse:
        raise NotImplementedError('Override validate_firmware in a concrete service implementation')

    def on_run_diagnostics(self, request: RunDiagnosticsRequest) -> RunDiagnosticsResponse:
        raise NotImplementedError('Override run_diagnostics in a concrete service implementation')


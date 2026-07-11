Description
This is an example program demonstrating the design and implementation of automated code generators.

The topic of this example is an IoT Device Management and Telemetry Service that provides remote operations for smart hardware:

Telemetry Streaming: Ingestion of sensor payloads (temperature, humidity, vibration).

Device Configuration: Remote updating of device sampling rates and operational modes.

Firmware Validation: Initiating and verifying cryptographic checksums of device firmware.

Diagnostics Execution: Triggering remote self-tests on connected hardware.

The program is modularly structured, with each component isolated in its own directory, utilizing automated code generation to bridge the interface gap between client and server.

Program Components
1. Interface Specification
File: interface/schema.json

Role: A single source of truth defined in JSON format. It strictly defines the RPC methods, arguments, data types, and structural payloads for both telemetry data and configuration schemas.

2. Code Generator for RPC Framework
Directory: generator/

Role: A Python script that parses interface/schema.json and automatically outputs native Python source files. It handles the generation of:

Serialization/Deserialization: Converting Python dictionaries/dataclasses into byte streams (or JSON strings) for network transmission and vice versa.

Stub & Skeleton Classes: Boilerplate networking code so developers only need to implement the core logic.

3. RPC Framework
Directory: rpc_core/

Role: The underlying transport layer (built using standard Python sockets or asyncio) responsible for moving raw serialized buffers between the network endpoints. It has no knowledge of specific IoT methods—only how to route data.

4. IoT Telemetry Service (Server)
Directory: server/

Role: The concrete implementation of the generated RPC skeleton. It acts as the cloud/gateway endpoint that stores incoming telemetry, validates configurations, and processes device diagnostic requests.

5. IoT Device Client
Directory: client/

Role: The hardware-facing edge application utilizing the generated RPC stubs to effortlessly push sensor data to the server and listen for incoming remote commands.

6. Developer Guide
File: DEV_GUIDE.md

Role: Complete instructions for setting up the environment, compiling a new schema change via the generator, and running the client-server ecosystem.

Tooling & Environment Requirements
Language & Isolation: Developed entirely in Python. The project mandates a Python Virtual Environment (venv) for local dependency isolation.

Package Management: pip handles all external library management (e.g., parsing utilities or networking aids).

Code Quality & Formatting: Strict enforcement of clean code practices:

black for deterministic code formatting.

pylint for static code analysis and linting.

Testing: pytest handles unit and integration tests, ensuring both the code generator itself and the generated RPC endpoints perform flawlessly.
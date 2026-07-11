import argparse
import json
import re
from pathlib import Path
from typing import Any

TYPE_MAP = {
    "string": "str",
    "int": "int",
    "float": "float",
    "bool": "bool",
    "object": "dict[str, Any]",
    "any": "Any",
}

INDENT = " " * 4


def python_type(schema_type: Any) -> str:
    if isinstance(schema_type, str):
        if schema_type.startswith("list[") and schema_type.endswith("]"):
            item_type = schema_type[5:-1]
            return f"list[{python_type(item_type)}]"
        return TYPE_MAP.get(schema_type, "Any")
    return "dict[str, Any]"


def class_name_from_method(method_name: str, suffix: str) -> str:
    parts = re.split(r"[_\- ]+", method_name)
    return "".join(word.capitalize() for word in parts) + suffix


def render_dataclass(name: str, fields: dict[str, Any]) -> str:
    lines = [f"@dataclass", f"class {name}: "]
    if not fields:
        lines.append(INDENT + "pass")
        return "\n".join(lines)

    for field_name, field_type in fields.items():
        lines.append(f"{INDENT}{field_name}: {python_type(field_type)}")

    lines.append("")
    lines.append(f"{INDENT}def to_dict(self) -> dict[str, Any]:")
    lines.append(f"{INDENT*2}return {{")
    for field_name in fields:
        lines.append(f"{INDENT*3}\"{field_name}\": self.{field_name},")
    lines.append(f"{INDENT*2}}}")
    lines.append("")
    lines.append(f"{INDENT}@staticmethod")
    lines.append(f"{INDENT}def from_dict(data: dict[str, Any]) -> '{name}':")
    lines.append(f"{INDENT*2}return {name}(**{{")
    for field_name, field_type in fields.items():
        cast = "data.get(\"{0}\")".format(field_name)
        lines.append(f"{INDENT*3}\"{field_name}\": {cast},")
    lines.append(f"{INDENT*2}}})")

    return "\n".join(lines)


def render_client_methods(methods: list[dict[str, Any]]) -> str:
    lines = ["class ClientStub:", f"{INDENT}def __init__(self, transport):", f"{INDENT*2}self.transport = transport", ""]
    for method in methods:
        request_class = class_name_from_method(method["name"], "Request")
        response_class = class_name_from_method(method["name"], "Response")
        lines.append(f"{INDENT}def {method['name']}(self, request: {request_class}) -> {response_class}:")
        lines.append(f"{INDENT*2}payload = {{'method': '{method['name']}', 'params': request.to_dict()}}")
        lines.append(f"{INDENT*2}response = self.transport.call(payload)")
        lines.append(f"{INDENT*2}return {response_class}.from_dict(response['result'])")
        lines.append("")
    return "\n".join(lines)


def render_server_skeleton(methods: list[dict[str, Any]]) -> str:
    lines = ["class ServerSkeleton:", f"{INDENT}def dispatch(self, payload: dict[str, Any]) -> dict[str, Any]:", f"{INDENT*2}method = payload.get('method')", f"{INDENT*2}params = payload.get('params', {{}})", ""]
    lines.append(f"{INDENT*2}if method is None:")
    lines.append(f"{INDENT*3}raise ValueError('Missing RPC method name')")
    lines.append("")
    for method in methods:
        request_class = class_name_from_method(method["name"], "Request")
        response_class = class_name_from_method(method["name"], "Response")
        lines.append(f"{INDENT*2}if method == '{method['name']}':")
        lines.append(f"{INDENT*3}request = {request_class}.from_dict(params)")
        lines.append(f"{INDENT*3}result = self.on_{method['name']}(request)")
        lines.append(f"{INDENT*3}return {{'result': result.to_dict()}}")
    lines.append("")
    lines.append(f"{INDENT*2}raise ValueError(f'Unknown method: {{method}}')")
    lines.append("")

    for method in methods:
        request_class = class_name_from_method(method["name"], "Request")
        response_class = class_name_from_method(method["name"], "Response")
        lines.append(f"{INDENT}def on_{method['name']}(self, request: {request_class}) -> {response_class}:")
        lines.append(f"{INDENT*2}raise NotImplementedError('Override {method['name']} in a concrete service implementation')")
        lines.append("")

    return "\n".join(lines)


def generate_module(schema: dict[str, Any]) -> str:
    service_name = schema.get("service_name", "RpcService")
    methods = schema.get("methods", [])
    lines = [
        "from __future__ import annotations",
        "from dataclasses import dataclass",
        "from typing import Any, Dict",
        "",
        f"SERVICE_NAME = '{service_name}'",
        "",
    ]

    for method in methods:
        request_class = class_name_from_method(method["name"], "Request")
        response_class = class_name_from_method(method["name"], "Response")
        lines.append(render_dataclass(request_class, method.get("request", {})))
        lines.append("")
        lines.append(render_dataclass(response_class, method.get("response", {})))
        lines.append("")

    lines.append(render_client_methods(methods))
    lines.append("")
    lines.append(render_server_skeleton(methods))
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Python RPC bindings from schema.json")
    parser.add_argument("schema", help="Path to interface/schema.json")
    parser.add_argument("--output", default="generated/rpc_schema.py", help="Output Python file")
    args = parser.parse_args()

    schema_path = Path(args.schema)
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    module_code = generate_module(schema)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(module_code, encoding="utf-8")
    print(f"Generated {output_path}")


if __name__ == "__main__":
    main()

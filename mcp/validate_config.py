"""
Validate MCP configuration file (mcp/config.yaml)
"""
import sys
import yaml
from pathlib import Path


def validate(path: Path) -> int:
    if not path.exists():
        print(f"✗ MCP config not found at {path}")
        return 1

    try:
        data = yaml.safe_load(path.read_text())
    except Exception as e:
        print(f"✗ Failed to parse YAML: {e}")
        return 1

    if 'mcp_servers' not in data:
        print("✗ 'mcp_servers' key missing")
        return 1

    for server in data['mcp_servers']:
        if 'name' not in server or 'host' not in server or 'tools' not in server:
            print(f"✗ MCP server entry invalid: {server}")
            return 1
        for tool in server['tools']:
            if 'name' not in tool or 'endpoint' not in tool:
                print(f"✗ Tool definition invalid in server {server.get('name')}: {tool}")
                return 1

    print(f"✓ MCP config at {path} is valid ({len(data['mcp_servers'])} servers)")
    return 0


if __name__ == '__main__':
    p = Path(__file__).parent / 'config.yaml'
    raise SystemExit(validate(p))

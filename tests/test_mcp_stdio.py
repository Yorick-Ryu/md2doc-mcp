#!/usr/bin/env python3
"""Test script to simulate MCP client-server communication via stdio."""

import asyncio
import json
import os


async def test_mcp_stdio():
    """Test MCP server communication via stdio."""
    print("🔍 Testing MCP Server via stdio communication...")
    print("=" * 60)
    
    # Set environment variables
    env = os.environ.copy()
    env["DEEP_SHARE_API_KEY"] = "your-api-key-here"
    
    # Start the MCP server process
    cmd = [
        "uv", "--directory", "/Users/yorick/WebProjects/md2docx-mcp", 
        "run", "python", "-m", "md2doc.server"
    ]
    
    print(f"Starting MCP server with command: {' '.join(cmd)}")
    
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env
    )
    
    # Send initialization message
    init_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    print("\n📤 Sending initialization message...")
    message_str = json.dumps(init_message) + "\n"
    process.stdin.write(message_str.encode())
    await process.stdin.drain()
    
    # Read response
    try:
        response_line = await asyncio.wait_for(process.stdout.readline(), timeout=10.0)
        if response_line:
            response = json.loads(response_line.decode().strip())
            print(f"📥 Received init response: {json.dumps(response, indent=2)}")
        else:
            print("❌ No response received to initialization")
    except asyncio.TimeoutError:
        print("❌ Timeout waiting for initialization response")
    except Exception as e:
        print(f"❌ Error reading init response: {e}")
    
    # Send initialized notification
    initialized_message = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }
    
    print("\n📤 Sending initialized notification...")
    message_str = json.dumps(initialized_message) + "\n"
    process.stdin.write(message_str.encode())
    await process.stdin.drain()
    
    # Send tools/list request
    list_tools_message = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    print("\n📤 Sending tools/list request...")
    message_str = json.dumps(list_tools_message) + "\n"
    process.stdin.write(message_str.encode())
    await process.stdin.drain()
    
    # Read tools response
    try:
        response_line = await asyncio.wait_for(process.stdout.readline(), timeout=10.0)
        if response_line:
            response = json.loads(response_line.decode().strip())
            print(f"📥 Received tools response: {json.dumps(response, indent=2)}")
            
            # Check if tools are present
            if "result" in response and "tools" in response["result"]:
                tools = response["result"]["tools"]
                print(f"\n✅ Found {len(tools)} tools:")
                for tool in tools:
                    print(f"  - {tool['name']}: {tool['description']}")
            else:
                print("❌ No tools found in response")
        else:
            print("❌ No response received to tools/list")
    except asyncio.TimeoutError:
        print("❌ Timeout waiting for tools/list response")
    except Exception as e:
        print(f"❌ Error reading tools response: {e}")
    
    # Check for any stderr output
    try:
        stderr_data = await asyncio.wait_for(process.stderr.read(), timeout=1.0)
        if stderr_data:
            print(f"\n⚠️ Server stderr output:\n{stderr_data.decode()}")
    except asyncio.TimeoutError:
        pass  # No stderr output
    
    # Cleanup
    try:
        process.stdin.close()
        await process.wait()
    except:
        process.kill()
        await process.wait()
    
    print("\n" + "=" * 60)
    print("MCP stdio communication test completed!")


if __name__ == "__main__":
    asyncio.run(test_mcp_stdio()) 
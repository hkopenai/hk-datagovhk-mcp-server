import asyncio
import json
import argparse
import sys
import logging
import os
import subprocess
import time
import socket
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

# Configure logging
log_level = os.environ.get("LOG_LEVEL", "DEBUG").upper()
logging.basicConfig(level=getattr(logging, log_level),
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Force DEBUG level for this script
logger.debug("Logging initialized with DEBUG level")

async def call_mcp_tool(server_url, tool_name, params, use_stdio=False, server_module=None):
    """
    Call an MCP tool with the given parameters and return the response.
    
    Args:
        server_url (str): The URL of the MCP server (used if not using stdio).
        tool_name (str): The name of the tool to call.
        params (dict): The parameters to pass to the tool.
        use_stdio (bool): If True, start the server as a subprocess and connect via HTTP.
        server_module (str): The module name to run as the MCP server (used with stdio mode).
    
    Returns:
        dict: The response from the tool call.
    """
    if use_stdio:
        if not server_module:
            raise ValueError("Server module must be provided when using stdio mode")
        logger.info(f"Starting MCP server as a subprocess with module: {server_module}")
        
        # Start the server as a subprocess
        server_process = subprocess.Popen(
            [sys.executable, "-m", server_module],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        logger.debug("MCP server subprocess started. Waiting for it to initialize...")
        
        # Wait for the server to start (look for a log message indicating it's ready)
        initialization_timeout = 20  # seconds
        start_time = time.time()
        server_ready = False
        while time.time() - start_time < initialization_timeout:
            if server_process.stderr:
                stderr_line = server_process.stderr.readline().strip()
                if stderr_line:
                    logger.debug(f"Server stderr: {stderr_line}")
                    if "stdio" in stderr_line.lower():
                        logger.info("Server initialization detected as ready via stderr (stdio mode detected).")
                        server_ready = True
                        break            
            # if server_process.stdout:
            #     stdout_line = server_process.stdout.readline().strip()
            #     if stdout_line:
            #         logger.debug(f"Server stdout: {stdout_line}")
            #         if "HK Data.gov.hk MCP Server running" in stdout_line:
            #             logger.info("Server initialization detected as ready via stdout.")
            #             server_ready = True
            #             break
            time.sleep(0.5)
        
        if not server_ready:
            logger.warning("Server did not indicate readiness within the extended timeout of 20 seconds. Proceeding to connect anyway, but connection may fail.")
        
        # Check stderr for any errors during initialization
        stderr_output = ""
        if server_process.stderr:
            while True:
                line = server_process.stderr.readline().strip()
                if line:
                    stderr_output += line + "\n"
                    logger.debug(f"Server stderr: {line}")
                else:
                    break
        if stderr_output:
            logger.warning(f"Server stderr during initialization: {stderr_output[:500]}...")
        
        # Connect to the server via HTTP (assuming default port 8000)
        local_server_url = "http://127.0.0.1:8000/mcp/"
        logger.info(f"Connecting to local MCP server at {local_server_url}")
        try:
            async with streamablehttp_client(local_server_url) as (read_stream, write_stream, _):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    logger.debug(f"Calling tool '{tool_name}' with parameters: {json.dumps(params, ensure_ascii=False)}")
                    response = await session.call_tool(tool_name, params)
                    logger.debug(f"Full response received from '{tool_name}': {response}")
                    logger.info(f"Response summary from '{tool_name}': {str(response)[:500]}...")
                    
                    json_text = "{}"
                    if response.content:
                        for content in response.content:
                            try:
                                # type: ignore - Pylance warning suppression for attribute access
                                if hasattr(content, 'text') and content.text:
                                    json_text = content.text
                                    logger.debug(f"Extracted text content from response: {json_text[:500]}...")
                                    break
                            except AttributeError:
                                logger.debug(f"Content item lacks 'text' attribute: {content}")
                                continue
                    try:
                        data = json.loads(json_text)
                        logger.debug(f"Parsed JSON data from response: {json.dumps(data, ensure_ascii=False)[:500]}...")
                    except json.JSONDecodeError:
                        logger.error(f"Invalid JSON response: {json_text}")
                        raise ValueError(f"Invalid JSON response received from tool")
                    if "error" in data:
                        logger.error(f"Error in response: {data['error']}")
                        raise ValueError(f"Tool call failed: {data['error']}")
                    logger.info(f"Tool call successful, returning data")
                    return data
        finally:
            # Terminate the server process
            server_process.terminate()
            try:
                server_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                server_process.kill()
            logger.info("Local MCP server subprocess terminated.")
    else:
        logger.info(f"Connecting to MCP server at {server_url}")
        async with streamablehttp_client(server_url) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                logger.debug(f"Calling tool '{tool_name}' with parameters: {json.dumps(params, ensure_ascii=False)}")
                response = await session.call_tool(tool_name, params)
                logger.debug(f"Full response received from '{tool_name}': {response}")
                logger.info(f"Response summary from '{tool_name}': {str(response)[:500]}...")
                
                json_text = "{}"
                if response.content:
                    for content in response.content:
                        try:
                            # type: ignore - Pylance warning suppression for attribute access
                            if hasattr(content, 'text') and content.text:
                                json_text = content.text
                                logger.debug(f"Extracted text content from response: {json_text[:500]}...")
                                break
                        except AttributeError:
                            logger.debug(f"Content item lacks 'text' attribute: {content}")
                            continue
                try:
                    data = json.loads(json_text)
                    logger.debug(f"Parsed JSON data from response: {json.dumps(data, ensure_ascii=False)[:500]}...")
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON response: {json_text}")
                    raise ValueError(f"Invalid JSON response received from tool")
                if "error" in data:
                    logger.error(f"Error in response: {data['error']}")
                    raise ValueError(f"Tool call failed: {data['error']}")
                logger.info(f"Tool call successful, returning data")
                return data

def main():
    parser = argparse.ArgumentParser(description="MCP Client to call tools on an MCP server.")
    parser.add_argument("--server-url", default="http://127.0.0.1:8000/mcp/",
                        help="URL of the MCP server (default: http://127.0.0.1:8000/mcp/)")
    parser.add_argument("--tool", required=True, help="Name of the tool to call")
    parser.add_argument("--params", type=str, default="{}",
                        help="JSON string of parameters for the tool (default: {}). Use double quotes around the JSON string.")
    parser.add_argument("--stdio", action="store_true",
                        help="Start the MCP server as a subprocess and use stdio for communication")
    parser.add_argument("--server-module", default="hkopenai.hk_datagovhk_mcp_server",
                        help="Python module to run as the MCP server in stdio mode (default: hkopenai.hk_datagovhk_mcp_server)")
    
    # Manually parse arguments to handle JSON string properly
    args_list = sys.argv[1:]
    processed_args = []
    i = 0
    params_value = "{}"
    while i < len(args_list):
        arg = args_list[i]
        if arg == "--params" and i + 1 < len(args_list):
            # Collect everything after --params as a single argument until the next flag
            params_parts = []
            i += 1
            while i < len(args_list) and not args_list[i].startswith("--"):
                params_parts.append(args_list[i])
                i += 1
            params_value = " ".join(params_parts)
            processed_args.extend(["--params", params_value])
        else:
            processed_args.append(arg)
            i += 1
    
    args = parser.parse_args(processed_args)
    
    # Parse the params string as JSON, handling escaped quotes and extra quotes
    try:
        logger.debug(f"Raw params input: {args.params}")
        # Check if params points to a file
        if os.path.isfile(args.params):
            logger.info(f"Reading params from file: {args.params}")
            with open(args.params, 'r') as f:
                params = json.load(f)
        else:
            # Remove leading/trailing quotes if they exist (shell might add them)
            cleaned_params = args.params.strip('"\'')
            # Replace escaped quotes if they exist
            cleaned_params = cleaned_params.replace('\\"', '"')
            logger.debug(f"Cleaned params input: {cleaned_params}")
            params = json.loads(cleaned_params)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON for --params: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        logger.error(f"File not found for --params: {e}")
        sys.exit(1)
    
    # Check if stdin has data and use it as params if --params is empty
    if args.params == "{}" and not sys.stdin.isatty():
        try:
            stdin_input = sys.stdin.read().strip()
            if stdin_input:
                params = json.loads(stdin_input)
                logger.info("Using parameters from stdin")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON input from stdin: {e}")
            sys.exit(1)
    
    try:
        logger.debug("Starting asyncio run for tool call")
        if args.stdio:
            result = asyncio.run(call_mcp_tool(args.server_url, args.tool, params, use_stdio=True, server_module=args.server_module))
        else:
            result = asyncio.run(call_mcp_tool(args.server_url, args.tool, params))
        logger.debug("Tool call completed, printing result")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        logger.debug("Result printed, exiting normally")
        sys.exit(0)  # Explicitly exit with success code
    except Exception as e:
        logger.error(f"Failed to call tool: {e}")
        sys.exit(1)
    finally:
        logger.debug("Main execution completed, ensuring exit")
        sys.exit(0)  # Force exit in case of any lingering tasks

if __name__ == "__main__":
    main()

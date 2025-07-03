import unittest
import subprocess
import json
import sys
import os
import time
import asyncio
import socket
import logging

# Configure logging
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level),
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import necessary components from mcp.client
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession


@unittest.skipUnless(os.environ.get('RUN_LIVE_TESTS') == 'true', "Set RUN_LIVE_TESTS=true to run live tests")
class TestMCPClientSimulation(unittest.TestCase):
    server_process = None
    SERVER_URL = "http://127.0.0.1:8000/mcp/"

    def setUp(self):
        logger.debug("Starting MCP server subprocess for HTTP communication...")
        # Start the hk-datagovhk-mcp-server as a subprocess
        self.server_process = subprocess.Popen(
            [sys.executable, "-m", "hkopenai.hk_datagovhk_mcp_server", "--sse"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        logger.debug("MCP server subprocess started. Giving it a moment to start up and listen on HTTP...")
        time.sleep(5)

        # Check if the server is actually listening on the port
        for _ in range(10):
            try:
                with socket.create_connection(("127.0.0.1", 8000), timeout=1):
                    logger.debug("Server is listening on port 8000.")
                    break
            except OSError as e:
                logger.debug(f"Waiting for server to start: {e}")
                time.sleep(1)
        else:
            self.server_process.terminate()
            self.server_process.wait(timeout=5)
            if self.server_process.poll() is None:
                self.server_process.kill()
            raise Exception("Server did not start listening on port 8000 in time.")

        logger.debug(f"Server setup complete.")

    def tearDown(self):
        # Terminate the server process
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait(timeout=5)
            if self.server_process.poll() is None:
                logger.debug("Tear down complete.")
                self.server_process.kill()
            
            # Print any remaining stderr output from the server process
            if self.server_process.stdout:
                self.server_process.stdout.close()
            if self.server_process.stderr:
                stderr_output = self.server_process.stderr.read()
                if stderr_output:
                    logger.debug(f"Server stderr (remaining):\n{stderr_output}")
                else:
                    logger.debug("Server stderr (remaining): (empty)")
                self.server_process.stderr.close()
            logger.info("Tear down complete.")

    async def _call_tool_and_assert(self, tool_name, params):
        async with streamablehttp_client(self.SERVER_URL) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                response = await session.call_tool(tool_name, params)
                logger.info(f"'{tool_name}' tool response: {str(response)[:500]}...")

                json_text = response.content[0].text if response.content else "{}"
                data = json.loads(json_text)
                self.assertIsInstance(data, dict, f"Result should be a dictionary")
                self.assertNotIn("error", data, f"Result should not contain an error: {data}")
                return data

    def test_crawl_datasets_tool(self):
        logger.debug("Testing 'crawl_datasets' tool...")
        asyncio.run(self._call_tool_and_assert("crawl_datasets", {"category": "finance", "page": 1}))

if __name__ == "__main__":
    unittest.main()

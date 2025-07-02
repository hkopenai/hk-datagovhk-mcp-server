# HK Data.gov.hk MCP Server

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/hkopenai/hk-datagovhk-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This is an MCP server that provides access to data from data.gov.hk through a FastMCP interface.

## Data Source

* data.gov.hk

## Features

- Data.gov.hk Crawler: Crawl datasets from data.gov.hk based on category and page number.

## API Reference

### Data.gov.hk Crawler
`crawl_datasets(category: str, page: int = 1) -> Dict`
- Crawl datasets from data.gov.hk based on category and page number.
- Parameters:
  - category: The category of datasets to crawl (e.g., 'finance', 'education').
  - page: The page number to crawl (default: 1).
- Returns:
  - Dict containing a list of datasets with their titles and links.

## Setup

1. Clone this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python server.py
   ```

### Running Options

- Default stdio mode: `python server.py`
- SSE mode (port 8000): `python server.py --sse`

## Cline Integration

To connect this MCP server to Cline using stdio:

1. Add this configuration to your Cline MCP settings (cline_mcp_settings.json):
```json
{
  "datagovhk-server": {
    "disabled": false,
    "timeout": 3,
    "type": "stdio",
    "command": "python",
    "args": [
      "-m",
      "hkopenai.hk_datagovhk_mcp_server"
    ]
  }
}
```

## Testing

Tests are available in `tests`. Run with:
```bash
pytest

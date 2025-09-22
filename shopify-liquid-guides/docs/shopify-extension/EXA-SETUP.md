# EXA API Key Setup (MCP Server)

The EXA MCP server requires an EXA_API_KEY provided via your local environment. We removed any hardcoded keys from the repo.

## Set EXA_API_KEY locally

- macOS/Linux (bash/zsh):
  export EXA_API_KEY="your_key_here"

- Fish shell:
  set -x EXA_API_KEY "your_key_here"

- VS Code workspace:
  Use your terminal integrated in VS Code so the environment propagates to the MCP servers.

## How it is used

- .mcp.json defines the exa MCP server without embedding credentials: env is empty
- The server reads EXA_API_KEY from your process environment

## Verifying

- Restart your editor/terminal after exporting
- Run any tools that rely on EXA MCP (web_search_exa, crawling, github_search)
- If authentication fails, confirm the variable is available: echo $EXA_API_KEY


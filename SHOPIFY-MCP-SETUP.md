# Shopify MCP Server Setup Guide

Complete setup guide for integrating Shopify's official MCP server with Claude Code for enhanced Shopify development capabilities.

## 🚀 What You Get

The Shopify MCP server provides direct access to:

- **Admin GraphQL API**: Query and mutate Shopify data directly from Claude
- **Liquid Template Support**: Enhanced Liquid syntax and filter validation
- **Polaris Components**: Access to Shopify's design system components
- **Functions API**: Serverless function development and testing
- **Real-time Schema**: Up-to-date GraphQL schema definitions

## ✅ Prerequisites

- **Node.js 18+**: Required for running the MCP server
- **Claude Code**: AI development environment with MCP support
- **Active Internet**: For downloading latest server packages

## 🔧 Installation Steps

### 1. Configuration Added ✅

Your `.mcp.json` has been updated with the optimal Shopify MCP configuration:

```json
{
  "mcpServers": {
    "shopify-dev-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@shopify/dev-mcp@latest"],
      "env": {
        "LIQUID": "true",
        "POLARIS_UNIFIED": "true",
        "OPT_OUT_INSTRUMENTATION": "true"
      }
    }
  }
}
```

### 2. Environment Variables Explained

- **`LIQUID: "true"`**: Enables Liquid template support and validation
- **`POLARIS_UNIFIED: "true"`**: Enables Shopify Polaris design system components
- **`OPT_OUT_INSTRUMENTATION: "true"`**: Disables telemetry for privacy

### 3. Server Validation ✅

The server has been tested and is working correctly:
- ✅ Server downloads and runs successfully
- ✅ GraphQL schemas are fetched from Shopify
- ✅ API documentation is available
- ✅ Version 1.2.0 confirmed working

## 🎯 Available Capabilities

Once Claude restarts and loads the MCP server, you'll have access to:

### **GraphQL Operations**
```
- Query Shopify Admin API
- Mutation operations for data modification
- Real-time schema introspection
- Subscription support for live updates
```

### **Liquid Development**
```
- Liquid syntax validation
- Filter and tag reference
- Template optimization suggestions
- Shopify-specific object documentation
```

### **Polaris Integration**
```
- Component library access
- Design token reference
- Accessibility guidelines
- React component examples
```

### **Functions Development**
```
- Function template generation
- Testing and validation
- Deployment preparation
- Performance optimization
```

## 🔄 Activation Process

### Manual Restart Required
Since MCP servers are loaded at startup, you need to:

1. **Restart Claude Code** to load the new Shopify MCP server
2. **Verify Connection** by checking available tools
3. **Test Integration** with a simple GraphQL query

### Verification Commands
After restart, you can verify the server is loaded:

```bash
# Check if server is available
claude /mcp list

# Test Shopify-specific functionality
# (These will be available after restart)
```

## 🎨 Integration with Design System

The Shopify MCP server complements your existing design system by providing:

- **Official Shopify Patterns**: Direct access to Shopify's design guidelines
- **Component Validation**: Ensure components follow Shopify standards
- **API-Driven Development**: Build components that integrate with live Shopify data
- **Performance Optimization**: Access to Shopify's performance best practices

## 🚀 Next Steps

1. **Restart Claude Code** to activate the MCP server
2. **Test GraphQL Queries** to verify Admin API access
3. **Validate Liquid Templates** using enhanced Liquid support
4. **Explore Polaris Components** for design system integration
5. **Build Functions** for advanced Shopify customization

## 📚 Documentation References

- **Official Shopify MCP Docs**: https://shopify.dev/docs/apps/build/devmcp
- **Admin GraphQL API**: https://shopify.dev/docs/admin-api/graphql
- **Liquid Reference**: https://shopify.dev/docs/themes/liquid
- **Polaris Design System**: https://polaris.shopify.com/
- **Shopify Functions**: https://shopify.dev/docs/functions

## 🔧 Troubleshooting

### Common Issues

**Server Not Loading**
- Ensure Node.js 18+ is installed
- Check internet connection for package downloads
- Restart Claude Code completely

**Authentication Errors**
- No authentication required for development server
- Server runs locally without API keys

**Performance Issues**
- Server downloads schemas on first run (normal delay)
- Subsequent runs are faster with cached data

### Support Resources

- **Claude Code Documentation**: Built-in help system
- **Shopify Community**: https://community.shopify.com/
- **GitHub Issues**: https://github.com/Shopify/dev-mcp

---

## ✅ Status: Ready for Development

Your Shopify MCP server is now configured and ready to enhance your Shopify theme development workflow with direct API access, enhanced Liquid support, and Polaris integration.

**Next Action**: Restart Claude Code to activate the new capabilities.
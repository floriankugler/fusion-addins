# Graph.getNodeOutputPinConnectors Method

Parent Object: [Graph](Graph.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Get an array of downstream connections from the node's output pin.

## Syntax

"graph_var" is a variable referencing a [Graph](Graph.md) object.

```python
returnValue = graph_var.getNodeOutputPinConnectors(node, outputPinIndex)
```

## Return Value

| Type | Description |
|----|----|
| [GraphConnector](GraphConnector.md)\[\] | An array of GraphConnector objects, one for each connection to another node. |

## Parameters

| Name | Type | Description |
|----|----|----|
| node | [GraphNode](GraphNode.md) | The node in question. |
| outputPinIndex | uinteger | The index of the output pin of the node. |

## Version

Introduced in version May 2025  


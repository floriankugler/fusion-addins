# Graph.allPossibleNodeTypes Property

Parent Object: [Graph](Graph.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Get all the possible node types that can be used as the nodeType parameter for addNode.

## Syntax

"graph_var" is a variable referencing a Graph object.  

```python
# Get the value of the property.
propertyValue = graph_var.allPossibleNodeTypes
```

## Property Value

This is a read only property whose value is an array of type string.

## Version

Introduced in version May 2025  


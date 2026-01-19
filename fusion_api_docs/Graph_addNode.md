# Graph.addNode Method

Parent Object: [Graph](Graph.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Add a new node to the graph. Node names are unique, attempting to add two nodes with the same name produces an error.

## Syntax

"graph_var" is a variable referencing a [Graph](Graph.md) object.

```python
returnValue = graph_var.addNode(name, nodeType)
```

## Return Value

| Type | Description |
|----|----|
| [GraphNode](GraphNode.md) | The new node if it could be added, null otherwise. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | Name of the new node. |
| nodeType | string | The node type string, one of the types listed in the documentation. |

## Samples

| Name | Description |
| --- | --- |
| [Volumetric Custom Feature API Sample](VolumetricCustomFeatureSample_Sample.md) | Demonstrates how to create a Volumetric Custom Feature using the API for graph creation. To run the sample script, have a document open in Fusion’s DESIGN workspace. This script will create a component with a box by sketching then extruding that sketch. It will then use that box as a boundary body and create a Volumetric Custom Feature. The script will the create a gyroid lattice using the Volumetric Model API with the appropriate Graphs, Nodes and Connections for a minimal example. Finally, the script will convert that Volumetric Model to Mesh using the API and the VolumetricModelToMeshFeature. |

## Version

Introduced in version May 2025  


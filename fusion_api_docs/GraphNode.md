
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

An individual node within a graph.

## Methods

| Name | Description |
|----|----|
| [classType](GraphNode_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](GraphNode_deleteMe.md) | Deletes the graphNode and all of its connections. |
| [getInputPinCount](GraphNode_getInputPinCount.md) | How many input pins does this node have. |
| [getInputPinName](GraphNode_getInputPinName.md) | The name of this graph node input pin describing its function. |
| [getInputPinType](GraphNode_getInputPinType.md) | Get the type of the node input pin. |
| [getOutputPinCount](GraphNode_getOutputPinCount.md) | How many output pins does this node have. |
| [getOutputPinName](GraphNode_getOutputPinName.md) | The name of this graph node input pin describing its function. |
| [getOutputPinType](GraphNode_getOutputPinType.md) | Get the type of the node output pin. |
| [hasValidProperties](GraphNode_hasValidProperties.md) | Check if the graph node properties are valid. |
| [isInputPinOptional](GraphNode_isInputPinOptional.md) | Some input pins can be optional, so they do not need to be connected for the node to work. |

## Properties

| Name | Description |
| --- | --- |
| [description](GraphNode_description.md) | A user readable description that explains the function of this node type. |
| [isValid](GraphNode_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](GraphNode_name.md) | The name of this graph node as give on creation. Node names for each graph should be unique. |
| [nodeType](GraphNode_nodeType.md) | Get the string node type that is was created with. |
| [objectType](GraphNode_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [properties](GraphNode_properties.md) | Get a collection of all node properties supported by this node. |

## Accessed From

[Graph.addNode](Graph_addNode.md), [Graph.allNodes](Graph_allNodes.md), [Graph.getNode](Graph_getNode.md), [Graph.getOutputNode](Graph_getOutputNode.md), [GraphConnector.sourceGraphNode](GraphConnector_sourceGraphNode.md), [GraphConnector.targetGraphNode](GraphConnector_targetGraphNode.md)

## Samples

| Name | Description |
| --- | --- |
| [Volumetric Custom Feature API Sample](VolumetricCustomFeatureSample_Sample.md) | Demonstrates how to create a Volumetric Custom Feature using the API for graph creation. To run the sample script, have a document open in Fusion’s DESIGN workspace. This script will create a component with a box by sketching then extruding that sketch. It will then use that box as a boundary body and create a Volumetric Custom Feature. The script will the create a gyroid lattice using the Volumetric Model API with the appropriate Graphs, Nodes and Connections for a minimal example. Finally, the script will convert that Volumetric Model to Mesh using the API and the VolumetricModelToMeshFeature. |

## Version

Introduced in version May 2025  


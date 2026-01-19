
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

The graph that describes the volumetric model. Possible node types: "BoxSDF", "CylinderSDF", "SphereSDF", "TorusSDF", "PlaneSDF", "ReferencedGeometrySDF", "ReferencedCurveLength", "ReferencedCurveCoords", "ReferencedFaceCoords", "GradientVector", "InvertDensity", "PerlinNoiseScalar", "VoronoiNoiseScalar", "Shell", "ConstantScalar", "ConstantColor", "ImageSamplerScalar", "ImageSamplerVector", "ImageSamplerColor", "3DImageSamplerScalar", "SphereCoords", "TorusCoords", "CylinderCoords", "HomogenousTransformCoords", "TransformCoords", "AxisBasedDeformCoords ", "TwistCoords", "ControlPointMapScalarToScalar", "ControlPointMapScalarToColor", "FalloffMapping", "VectorToColor", "CombineScalarsToVector", "CombineScalarsToColor", "SplitVectorToScalars", "SplitColorToScalars", "LengthOfVector", "NormalizeVector", "ExternalColor", "FunctionScalarToScalar", "FunctionVectorToColor", "FunctionVectorToVector", "FunctionVectorToScalar", "BinaryOperatorColor", "BinaryOperatorVector", "BinaryOperatorScalar", "MultiplyColor", "MultiplyVector", "MultiplyScalar"

## Methods

| Name | Description |
|----|----|
| [addNode](Graph_addNode.md) | Add a new node to the graph. Node names are unique, attempting to add two nodes with the same name produces an error. |
| [canEvaluateGraph](Graph_canEvaluateGraph.md) | Check if all the channels in the graph can be evaluated and in a good state. |
| [classType](Graph_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [connect](Graph_connect.md) | Create a connection between nodes. |
| [disconnect](Graph_disconnect.md) | Delete a connection between nodes. |
| [getNode](Graph_getNode.md) | Get node with the given name. |
| [getNodeInputPinConnector](Graph_getNodeInputPinConnector.md) | Get an upstream connection to the node's input pin. |
| [getNodeOutputPinConnectors](Graph_getNodeOutputPinConnectors.md) | Get an array of downstream connections from the node's output pin. |
| [getOutputNode](Graph_getOutputNode.md) | Get one of the special graph output nodes. Every graph has one or more, the cannot be created or added. The final output pins of the graph nodes should be connected to these to make a useful graph. |

## Properties

| Name | Description |
| --- | --- |
| [allGraphConnectors](Graph_allGraphConnectors.md) | Get all the connectors in the graph. |
| [allNodes](Graph_allNodes.md) | Get all the nodes in the graph, including the output nodes. |
| [allPossibleNodeTypes](Graph_allPossibleNodeTypes.md) | Get all the possible node types that can be used as the nodeType parameter for addNode. |
| [isValid](Graph_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Graph_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[VolumetricModel.getGraph](VolumetricModel_getGraph.md)

## Samples

| Name | Description |
| --- | --- |
| [Volumetric Custom Feature API Sample](VolumetricCustomFeatureSample_Sample.md) | Demonstrates how to create a Volumetric Custom Feature using the API for graph creation. To run the sample script, have a document open in Fusion’s DESIGN workspace. This script will create a component with a box by sketching then extruding that sketch. It will then use that box as a boundary body and create a Volumetric Custom Feature. The script will the create a gyroid lattice using the Volumetric Model API with the appropriate Graphs, Nodes and Connections for a minimal example. Finally, the script will convert that Volumetric Model to Mesh using the API and the VolumetricModelToMeshFeature. |

## Version

Introduced in version May 2025  


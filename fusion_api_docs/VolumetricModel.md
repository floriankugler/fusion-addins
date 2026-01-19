
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

The main volumetric graph object. It has a parent component and is defined in this parent component's space. It also contains the primary and cell graphs.

## Methods

| Name | Description |
| --- | --- |
| [classType](VolumetricModel_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createSampler](VolumetricModel_createSampler.md) | Creates a VolumetricSampler object that can be used to sample the volumetric model. |
| [getGraph](VolumetricModel_getGraph.md) | Returns a graph from the volumetric model. |
| [registerCustomSDFCallback](VolumetricModel_registerCustomSDFCallback.md) | Handling for custom Signed Distance Field callback events. These can be registered by the API client, they will provide a string ID and a handler object that implements the abstract methods. To use the callback, a GeometryGraphNodeProperty's customSDFCallbackID should be set to the same string ID. Register a custom Signed Distance Field callback handler with a given ID. |
| [removeCustomSDFCallback](VolumetricModel_removeCustomSDFCallback.md) | De-register the Signed Distance Field callback handler with the given ID. |

## Properties

| Name | Description |
| --- | --- |
| [boundaryBody](VolumetricModel_boundaryBody.md) | Get or set the main boundary body for this volumetric model. The volumetric model is bound by the axis aligned bounding box and will only be rendered within this body. |
| [isLightBulbOn](VolumetricModel_isLightBulbOn.md) | Is the light bulb / eye (as displayed in the browser) controlling the model's visibility on. |
| [isValid](VolumetricModel_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](VolumetricModel_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentComponent](VolumetricModel_parentComponent.md) | Returns the parent Component. |

## Samples

| Name | Description |
| --- | --- |
| [Volumetric Custom Feature API Sample](VolumetricCustomFeatureSample_Sample.md) | Demonstrates how to create a Volumetric Custom Feature using the API for graph creation. To run the sample script, have a document open in Fusion’s DESIGN workspace. This script will create a component with a box by sketching then extruding that sketch. It will then use that box as a boundary body and create a Volumetric Custom Feature. The script will the create a gyroid lattice using the Volumetric Model API with the appropriate Graphs, Nodes and Connections for a minimal example. Finally, the script will convert that Volumetric Model to Mesh using the API and the VolumetricModelToMeshFeature. |

## Version

Introduced in version May 2025  


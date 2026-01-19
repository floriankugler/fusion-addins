# Operations Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to the individual operations within an existing setup, folder or pattern.

## Methods

| Name | Description |
|----|----|
| [add](Operations_add.md) | Create a new Operation. |
| [classType](Operations_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](Operations_createInput.md) | Creates a new OperationInput object, which is used to define the operation you want to create. Use properties and methods on the returned OperationInput object to define the desired operation and then pass it into the add method to create the operation. |
| [item](Operations_item.md) | Function that returns the specified operation using an index into the collection. |
| [itemByName](Operations_itemByName.md) | Returns the operation with the specified name (as appears in the browser). |
| [itemByOperationId](Operations_itemByOperationId.md) | Returns the operation with the specified operation id. |

## Properties

| Name | Description |
| --- | --- |
| [compatibleStrategies](Operations_compatibleStrategies.md) | Gets a list of the strategies that are compatible with the parent setup. This only returns strategies that are allowed to be added based on the active Setup or CAMFolder. Note: There may be cases where a compatible strategy might not be allowed to be created due to licensing or other issues like disabled preview features. |
| [count](Operations_count.md) | The number of items in the collection. |
| [isValid](Operations_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Operations_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CAMFolder.operations](CAMFolder_operations.md), [CAMHoleRecognition.operations](CAMHoleRecognition_operations.md), [CAMPattern.operations](CAMPattern_operations.md), [GenerateToolpathFuture.operations](GenerateToolpathFuture_operations.md), [Setup.operations](Setup_operations.md)

## Samples

| Name | Description |
| --- | --- |
| [Create Setups From Hole Recognition API Sample](CreateSetupsFromHoleRecognition_Sample.md) | This sample script demonstrates how to create a correctly oriented setup using Hole Recognition functionality. The Fusion Manufacturing Extension is required for Hole Recognition. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a 3 way coupling containing holes in various orientations and mounted on a fixture. A reference setup is created for the model using a simple stock mode and offsets. The Hole Recognition feature of the Fusion Manufacturing Extension creates 5 hole groups containing 11 holes between them. For each unique hole group vector captured, a new setup is created and its orientation transformed to match the vector. |
| [Generate Setup Sheets API Sample](GenerateSetupSheets_Sample_Sample.md) | Demonstrates generating the setup sheets for an existing toolpath.. |
| [Generate Toolpaths API Sample](GenerateToolpaths_Sample_Sample.md) | Demonstrates generating the toolpaths in the active document. |
| [Hole and Pocket Recognition API Sample](HoleAndPocketRecognition_Sample.md) | This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets. The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature. RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations. The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets. This script works only if the Manufacturing Extension is active. |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |
| [Post Toolpaths API Sample](PostToolpaths_Sample_Sample.md) | Demonstrates posting toolpaths in the active document. |
| [Turning Workflow API Sample](Turning_Workflow_API_Sample_Sample.md) | Turning Workflow API Sample This sample script starts by opening a simple component which is then used to describe a basic turning workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version January 2016  


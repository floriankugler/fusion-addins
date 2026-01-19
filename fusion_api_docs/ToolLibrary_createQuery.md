# ToolLibrary.createQuery Method

Parent Object: [ToolLibrary](ToolLibrary.md)  

## Description

Creates a new ToolQuery that is used to query the library for tools matching the query.

## Syntax

"toolLibrary_var" is a variable referencing a [ToolLibrary](ToolLibrary.md) object.

```python
returnValue = toolLibrary_var.createQuery()
```

## Return Value

| Type | Description |
|----|----|
| [ToolQuery](ToolQuery.md) | Returns a new ToolQuery. The query is predefined by given parameter. |

## Samples

| Name | Description |
| --- | --- |
| [Hole and Pocket Recognition API Sample](HoleAndPocketRecognition_Sample.md) | This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets. The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature. RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations. The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets. This script works only if the Manufacturing Extension is active. |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  


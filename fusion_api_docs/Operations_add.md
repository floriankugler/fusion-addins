# Operations.add Method

Parent Object: [Operations](Operations.md)  

## Description

Create a new Operation.

## Syntax

"operations_var" is a variable referencing an [Operations](Operations.md) object.

```python
returnValue = operations_var.add(input)
```

## Return Value

| Type                               | Description                          |
|------------------------------------|--------------------------------------|
| [OperationBase](OperationBase.md) | Returns the newly created Operation. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [OperationInput](OperationInput.md) | The OperationInput object defines the desired Operation. Use the createInput method to create a new OperationInput object and then use methods on it to define the Operation. The new Operation will be appended at the end of the current list of Operations. Throws an error if the strategy type is incompatible with the setup. |

## Samples

| Name | Description |
| --- | --- |
| [Additive Manufacturing MJF API Sample](AdditiveMJFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive MJF manufacturing setup and arrange components within the build volume of a 3D printer. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive Arrange using that manufacturing model as an input. The setup will select an MJF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically arranged within the build volume of the selected MJF machine. |
| [Basic Milling Workflow Sample](BasicMillingWorkflowSample_Sample.md) | Demonstrates the creation of a basic milling workflow from script Demonstrates creating a setup, searching tool library to retrieve a tool, create a couple of machining operations and a NC program, ready for post processing. Use the 2D Strategies model from the Fusion CAM Samples folder as your CAD model. |
| [Hole and Pocket Recognition API Sample](HoleAndPocketRecognition_Sample.md) | This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets. The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature. RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations. The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets. This script works only if the Manufacturing Extension is active. |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |
| [Turning Workflow API Sample](Turning_Workflow_API_Sample_Sample.md) | Turning Workflow API Sample This sample script starts by opening a simple component which is then used to describe a basic turning workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |
| [Wood Routing Workflow Sample](WoodRoutingSample_Sample.md) | This script demonstrates routing wood panels. When running the sample, it assumes you have an open design containing one or more "panels" oriented flat in the X-Y plane. The script creates a setup and a 2D contour operation with tabs to route the panels from a standard sheet. |

## Version

Introduced in version April 2023  


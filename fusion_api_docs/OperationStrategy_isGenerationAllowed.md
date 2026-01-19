# OperationStrategy.isGenerationAllowed Property

Parent Object: [OperationStrategy](OperationStrategy.md)  

## Description

Returns true if the strategy is allowed to be generated due to licensing and enabled preview features. Some strategies also require Active machining extension to be generated. Returns false otherwise.

## Syntax

"operationStrategy_var" is a variable referencing an OperationStrategy object.  

```python
# Get the value of the property.
propertyValue = operationStrategy_var.isGenerationAllowed
```

## Property Value

This is a read only property whose value is a boolean.

## Samples

| Name | Description |
| --- | --- |
| [Create Setups From Hole Recognition API Sample](CreateSetupsFromHoleRecognition_Sample.md) | This sample script demonstrates how to create a correctly oriented setup using Hole Recognition functionality. The Fusion Manufacturing Extension is required for Hole Recognition. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a 3 way coupling containing holes in various orientations and mounted on a fixture. A reference setup is created for the model using a simple stock mode and offsets. The Hole Recognition feature of the Fusion Manufacturing Extension creates 5 hole groups containing 11 holes between them. For each unique hole group vector captured, a new setup is created and its orientation transformed to match the vector. |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  


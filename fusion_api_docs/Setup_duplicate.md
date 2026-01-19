# Setup.duplicate Method

Parent Object: [Setup](Setup.md)  

## Description

Creates a duplicate of the operation in the tree after the itself.

## Syntax

"setup_var" is a variable referencing a [Setup](Setup.md) object.

```python
returnValue = setup_var.duplicate()
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns if duplicate command was successful. |

## Samples

| Name | Description |
| --- | --- |
| [Create Setups From Hole Recognition API Sample](CreateSetupsFromHoleRecognition_Sample.md) | This sample script demonstrates how to create a correctly oriented setup using Hole Recognition functionality. The Fusion Manufacturing Extension is required for Hole Recognition. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a 3 way coupling containing holes in various orientations and mounted on a fixture. A reference setup is created for the model using a simple stock mode and offsets. The Hole Recognition feature of the Fusion Manufacturing Extension creates 5 hole groups containing 11 holes between them. For each unique hole group vector captured, a new setup is created and its orientation transformed to match the vector. |

## Version

Introduced in version May 2024  


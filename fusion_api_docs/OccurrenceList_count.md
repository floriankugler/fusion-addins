# OccurrenceList.count Property

Parent Object: [OccurrenceList](OccurrenceList.md)  

## Description

Returns the number of occurrences in the collection.

## Syntax

"occurrenceList_var" is a variable referencing an OccurrenceList object.  

```python
# Get the value of the property.
propertyValue = occurrenceList_var.count
```

## Property Value

This is a read only property whose value is a uinteger.

## Samples

| Name | Description |
| --- | --- |
| [Assembly traversal using recursion API Sample](AssemblyTraversalUsingRecursion_Sample.md) | Traverses the entire structure of the currently open assemlby using a recursive function and displays the result in a message box. This will match the occurrence structure seen in the browser. |
| [Create Setups From Hole Recognition API Sample](CreateSetupsFromHoleRecognition_Sample.md) | This sample script demonstrates how to create a correctly oriented setup using Hole Recognition functionality. The Fusion Manufacturing Extension is required for Hole Recognition. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a 3 way coupling containing holes in various orientations and mounted on a fixture. A reference setup is created for the model using a simple stock mode and offsets. The Hole Recognition feature of the Fusion Manufacturing Extension creates 5 hole groups containing 11 holes between them. For each unique hole group vector captured, a new setup is created and its orientation transformed to match the vector. |
| [Get Volume of Active Design API Sample](GetsVolumeOfActiveDesign_Sample.md) | Traverses through the active design and totals the volume of every body within the design. |

## Version

Introduced in version August 2014  


# BRepBodyDefinition.outcomeInfo Property

Parent Object: [BRepBodyDefinition](BRepBodyDefinition.md)  

## Description

Returns an array of strings that contain information about the outcome of the previous call of the createBody method. This is especially useful when the createBody method fails, (returns null), because it provides information about why the failure occurred. It can also sometimes provide some information even when createBody succeeds.  

Each string that's returned represents a single set of information and is packaged as JSON such as '{"description":"vertex data is null or inconsistent with edge geometry","associativeID":"unknown","code":37}'  

The description is an English description of the error or warning. The associativeID maps back to the entity provided that is the cause of the problem. The ID is the associative ID you can optionally assign to the entity definition. The code is an internal code for the error or warning.  

An empty array is returned if createBody succeeded and there's no additional information.

## Syntax

"bRepBodyDefinition_var" is a variable referencing a BRepBodyDefinition object.  

```python
# Get the value of the property.
propertyValue = bRepBodyDefinition_var.outcomeInfo
```

## Property Value

This is a read only property whose value is an array of type string.

## Samples

| Name | Description |
|----|----|
| [BRep Body definition Sample](BRepBodyDefinition_Sample.md) | Demonstrates creating BRep bodies by BRepBodyDefinition. |

## Version

Introduced in version September 2020  


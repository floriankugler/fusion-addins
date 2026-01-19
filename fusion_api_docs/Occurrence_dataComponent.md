# Occurrence.dataComponent Property

Parent Object: [Occurrence](Occurrence.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets the DataComponent for the target component in the source component's document. This only applies for Occurrence's with an assembly context whose source component is a top level opened design.

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.dataComponent
```

## Property Value

This is a read only property whose value is a [DataComponent](DataComponent.md).

## Samples

| Name | Description |
|----|----|
| [Get part number using GraphQL](FetchPartNumberForComponents_Sample.md) | Fetches part number of root component and from occurrences via GQL query. |

## Version

Introduced in version July 2025  


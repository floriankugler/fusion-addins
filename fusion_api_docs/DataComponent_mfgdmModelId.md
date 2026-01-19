# DataComponent.mfgdmModelId Property

Parent Object: [DataComponent](DataComponent.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Get the MFGDM model Id.

## Syntax

"dataComponent_var" is a variable referencing a DataComponent object.  

```python
# Get the value of the property.
propertyValue = dataComponent_var.mfgdmModelId
```

## Property Value

This is a read only property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [Gets all properties using GraphQL](FetchBulkComponentProperties_Sample.md) | Fetches bulk component properties of the root component and from occurrences via single GraphQL query. |
| [Get part number using GraphQL](FetchPartNumberForComponents_Sample.md) | Fetches part number of root component and from occurrences via GQL query. |
| [Set part number using GraphQL](SetPartNumberUsingGraphQL_Sample.md) | Sets part number of root component and from occurrences via GQL query. |

## Version

Introduced in version July 2025  


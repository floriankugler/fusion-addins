# ClearanceHoleDataQuery.allStandards Property

Parent Object: [ClearanceHoleDataQuery](ClearanceHoleDataQuery.md)  

## Description

This method returns an array of all the available standards. The standards' names are always English. This English name should be used in the other methods that take the standard as an input argument. If you need to display the standard name to the user, you can use the standardCustomName method To get the localized name.

## Syntax

"clearanceHoleDataQuery_var" is a variable referencing a ClearanceHoleDataQuery object.  

```python
# Get the value of the property.
propertyValue = clearanceHoleDataQuery_var.allStandards
```

## Property Value

This is a read only property whose value is an array of type string.

## Version

Introduced in version September 2025  


# UntrimFeature.extensionDistance Property

Parent Object: [UntrimFeature](UntrimFeature.md)  

## Description

Gets the ModelParameter that defines the extension distance used to extend external boundaries. This can return null in the case where only internal boundaries have been removed. The value can be edited by using the properties of the returned ModelParameter object.

## Syntax

"untrimFeature_var" is a variable referencing a UntrimFeature object.  

```python
# Get the value of the property.
propertyValue = untrimFeature_var.extensionDistance
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version January 2021  


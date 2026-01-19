# DeriveFeatures.createInput Method

Parent Object: [DeriveFeatures](DeriveFeatures.md)  

## Description

Creates a DeriveFeatureInput object. Use properties and methods on this object to define the derive you want to create and then use the Add method, passing in the DeriveFeatureInput object.

## Syntax

"deriveFeatures_var" is a variable referencing a [DeriveFeatures](DeriveFeatures.md) object.

```python
returnValue = deriveFeatures_var.createInput(sourceDesign)
```

## Return Value

| Type | Description |
|----|----|
| [DeriveFeatureInput](DeriveFeatureInput.md) | Returns a DeriveFeatureInput or null if the creation failed. |

## Parameters

| Name         | Type                 | Description                      |
|--------------|----------------------|----------------------------------|
| sourceDesign | [Design](Design.md) | The Design that will be derived. |

## Version

Introduced in version January 2026  


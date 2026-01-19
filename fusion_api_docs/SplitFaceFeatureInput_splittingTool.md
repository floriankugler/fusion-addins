# SplitFaceFeatureInput.splittingTool Property

Parent Object: [SplitFaceFeatureInput](SplitFaceFeatureInput.md)  

## Description

Gets and sets the entity(s) that define the splitting tool(s). The splitting tool can be a single entity or an ObjectCollection containing solid and/or open bodies, construction planes, faces, or sketch curves that partially or fully intersect the faces that are being split.

## Syntax

"splitFaceFeatureInput_var" is a variable referencing a SplitFaceFeatureInput object.  

```python
# Get the value of the property.
propertyValue = splitFaceFeatureInput_var.splittingTool

# Set the value of the property.
splitFaceFeatureInput_var.splittingTool = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version June 2015  


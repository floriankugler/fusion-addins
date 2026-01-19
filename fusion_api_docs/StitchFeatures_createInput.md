# StitchFeatures.createInput Method

Parent Object: [StitchFeatures](StitchFeatures.md)  

## Description

Creates a StitchFeatureInput object. Use properties and methods on this object to define the stitch feature you want to create and then use the Add method, passing in the StitchFeatureInput object.

## Syntax

"stitchFeatures_var" is a variable referencing a [StitchFeatures](StitchFeatures.md) object.

```python
# Uses no optional arguments.
returnValue = stitchFeatures_var.createInput(stitchSurfaces, tolerance)

# Uses optional arguments.
returnValue = stitchFeatures_var.createInput(stitchSurfaces, tolerance, operation)
```

## Return Value

| Type | Description |
|----|----|
| [StitchFeatureInput](StitchFeatureInput.md) | Returns the newly created StitchFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| stitchSurfaces | [ObjectCollection](ObjectCollection.md) | The surfaces (open BRepBodies) to stitch together. Stitching surfaces can form multiple closed volumes resulting in multiple solids. Stitch Surfaces can form multiple BRepShells (entirely connected set of entities) that would result in a single non-solid BRepBody. |
| tolerance | [ValueInput](ValueInput.md) | ValueInput object that defines the stitching tolerance. It must define a distance value. |
| operation | [FeatureOperations](FeatureOperations.md) | Specifies the operation type for the result when the final result is a closed solid. Otherwise this argument is ignored. This is an optional argument whose default value is FeatureOperations.NewBodyFeatureOperation. |

## Samples

| Name | Description |
|----|----|
| [stitchFeatures.add](stitchFeatures_add_Sample.md) | Demonstrates the stitchFeatures.add method. |
| [Stitch Feature API Sample](StitchFeatureSample_Sample.md) | Demonstrates creating a new stitch feature. |

## Version

Introduced in version June 2015  


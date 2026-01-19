# ExtrudeFeature.symmetricExtent Property

Parent Object: [ExtrudeFeature](ExtrudeFeature.md)  

## Description

If the current extent of the feature is defined as a symmetric extent, this property returns the SymmericExtentDefinition object that provides access to the information defining the symmetric extent. If the current extent is not symmetric, this property returns null. You can determine the type of extent by using the extentType property.  

To change the extent of a feature to symmetric extent you can use the setSymmetricExtent method.

## Syntax

"extrudeFeature_var" is a variable referencing an ExtrudeFeature object.  

```python
# Get the value of the property.
propertyValue = extrudeFeature_var.symmetricExtent
```

## Property Value

This is a read only property whose value is a [SymmetricExtentDefinition](SymmetricExtentDefinition.md).

## Samples

| Name | Description |
|----|----|
| [Extrude Feature API Sample](ExtrudeFeatureSample_Sample.md) | Demonstrates creating a new extrude feature. |

## Version

Introduced in version March 2017  


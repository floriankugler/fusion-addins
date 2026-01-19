# ExtendFeature.extendType Property

Parent Object: [ExtendFeature](ExtendFeature.md)  

## Description

Gets and sets surface extend type to use.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"extendFeature_var" is a variable referencing an ExtendFeature object.  

```python
# Get the value of the property.
propertyValue = extendFeature_var.extendType

# Set the value of the property.
extendFeature_var.extendType = propertyValue
```

## Property Value

This is a read/write property whose value is a [SurfaceExtendTypes](SurfaceExtendTypes.md).

## Version

Introduced in version June 2015  


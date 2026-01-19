# ExtendFeature.extendAlignment Property

Parent Object: [ExtendFeature](ExtendFeature.md)  

## Description

Gets and sets surface extend alignment to use.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"extendFeature_var" is a variable referencing an ExtendFeature object.  

```python
# Get the value of the property.
propertyValue = extendFeature_var.extendAlignment

# Set the value of the property.
extendFeature_var.extendAlignment = propertyValue
```

## Property Value

This is a read/write property whose value is a [SurfaceExtendAlignment](SurfaceExtendAlignment.md).

## Version

Introduced in version September 2020  


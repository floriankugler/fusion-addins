# SceneSettings.centerOfFocus Property

Parent Object: [SceneSettings](SceneSettings.md)  

## Description

When the isDepthofFieldEnabled property is true, this point is used as the center of focus. All objects that are the same distance from the camera as this point will be in focus. Any geometry that is closer or further away from the camera than this point will appear more out of focus.  

Setting this property has the side effect of setting the isDepthOfField property to true. If the isDepthOfFieldEnabled property is false, the value of this property is ignored.

## Syntax

"sceneSettings_var" is a variable referencing a SceneSettings object.  

```python
# Get the value of the property.
propertyValue = sceneSettings_var.centerOfFocus

# Set the value of the property.
sceneSettings_var.centerOfFocus = propertyValue
```

## Property Value

This is a read/write property whose value is a [Point3D](Point3D.md).

## Version

Introduced in version May 2023  


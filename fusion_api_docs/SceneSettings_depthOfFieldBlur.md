# SceneSettings.depthOfFieldBlur Property

Parent Object: [SceneSettings](SceneSettings.md)  

## Description

Specify the amount of blur to apply to objects outside the center of focus. This must be a value between 0.001 and 2.000 inclusive. The depth of field is defined by using the centerOfFocus property to set the depth where the model is in focus.  

Setting this property has the side effect of setting the isDepthOfField property to true. If the isDepthOfFieldEnabled property is false, the value of this property is ignored.

## Syntax

"sceneSettings_var" is a variable referencing a SceneSettings object.  

```python
# Get the value of the property.
propertyValue = sceneSettings_var.depthOfFieldBlur

# Set the value of the property.
sceneSettings_var.depthOfFieldBlur = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version May 2023  


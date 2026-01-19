# SceneSettings.backgroundSolidColor Property

Parent Object: [SceneSettings](SceneSettings.md)  

## Description

Gets and sets the background color. When this property is set, it defines the background to be a solid color. The opacity component of the color is ignored.  

Getting this property is only valid when the backgroundType property returns SolidColorRenderSceneBackgroundType. Setting this property will automatically set the background type to SolidColorRenderSceneBackgroundType.

## Syntax

"sceneSettings_var" is a variable referencing a SceneSettings object.  

```python
# Get the value of the property.
propertyValue = sceneSettings_var.backgroundSolidColor

# Set the value of the property.
sceneSettings_var.backgroundSolidColor = propertyValue
```

## Property Value

This is a read/write property whose value is a [Color](Color.md).

## Version

Introduced in version May 2023  


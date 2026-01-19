# SceneSettings.backgroundEnvironment Property

Parent Object: [SceneSettings](SceneSettings.md)  

## Description

Gets and sets the environment to use for the background. The available environments can be accessed through the RenderManager.renderEnvironments property.  

Getting this property is only valid when the backgroundType property returns EnvironmentRenderSceneBackgroundType. Setting this property will automatically set the background type to EnvironmentRenderSceneBackgroundType.

## Syntax

"sceneSettings_var" is a variable referencing a SceneSettings object.  

```python
# Get the value of the property.
propertyValue = sceneSettings_var.backgroundEnvironment

# Set the value of the property.
sceneSettings_var.backgroundEnvironment = propertyValue
```

## Property Value

This is a read/write property whose value is a [RenderEnvironment](RenderEnvironment.md).

## Version

Introduced in version May 2023  


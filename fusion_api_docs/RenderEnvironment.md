# RenderEnvironment Object

Derived from: [Base](Base.md) Object  

## Description

A render environment that is used when defining the scene for rendering. You see these in the user interface in the "Environment Library" tab of the "Scene Settings" dialog. Use this with the backgroundEnvironment property of the SceneSettings object to set a render environment. For a custom render environment, use the loadCustomEnvironment method to statically create a custom environment and assign it to the backgroundEnvironment property.

## Methods

| Name | Description |
|----|----|
| [classType](RenderEnvironment_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [loadCustomEnvironment](RenderEnvironment_loadCustomEnvironment.md) | Statically creates a RenderEnvironment which can be used to set the environment for a scene using the SceneSettings.backgroundEnvironment property. |

## Properties

| Name | Description |
| --- | --- |
| [id](RenderEnvironment_id.md) | The internal ID of the environment. |
| [isCustomEnvironment](RenderEnvironment_isCustomEnvironment.md) | Returns true if this environment is a custom environment. |
| [isValid](RenderEnvironment_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](RenderEnvironment_name.md) | The name of the environment. |
| [objectType](RenderEnvironment_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[RenderEnvironment.loadCustomEnvironment](RenderEnvironment_loadCustomEnvironment.md), [RenderEnvironments.item](RenderEnvironments_item.md), [RenderEnvironments.itemById](RenderEnvironments_itemById.md), [RenderEnvironments.itemByName](RenderEnvironments_itemByName.md), [SceneSettings.backgroundEnvironment](SceneSettings_backgroundEnvironment.md)

## Version

Introduced in version May 2023  


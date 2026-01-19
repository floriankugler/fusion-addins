
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

The CustomFeatureDefinition object defines a specific type of custom feature. It contains the settings that apply to all custom features of that type and is used when creating new custom features of that type. It also supports the events used to handle changes to custom features of that type.

## Methods

| Name | Description |
| --- | --- |
| [classType](CustomFeatureDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](CustomFeatureDefinition_create.md) | A static function that creates a new CustomFeatureDefinition object. The creation of a CustomFeatureDefinition object is required to be able to create new custom features and for existing custom features to behave correctly. The CustomFeatureDefinition object defines all of the information that is common for all custom features of a particular type. For example, it defines the icon and the default name. The CustomFeatureDefinition object also supports the events that used to react to an existing feature being edited or re-computed. The custom feature definition should be created when your add-in is initially loaded to notify Fusion that the add-in that supports that custom feature type is available. |

## Properties

| Name | Description |
| --- | --- |
| [defaultName](CustomFeatureDefinition_defaultName.md) | Gets and sets the default name of the feature. Fusion will use this name and append a number to each feature instance as it's created. For example, if this is "Dovetail" the first custom feature created will be named "Dovetail1" and the second will be "Dovetail2". If you want to localize this name you can use the Application.Preferences.generalPreferences.userLanguage property to determine what language the user has chosen and use the corresponding name for that language. |
| [editCommandId](CustomFeatureDefinition_editCommandId.md) | Gets and sets which command will be invoked when the feature is edited. This is the id of the CommandDefinition object that you have created to do the edit of the feature. |
| [iconFolder](CustomFeatureDefinition_iconFolder.md) | Gets and sets the folder that contains the images that are used for the icon in the timeline for this custom feature. The folder should contain the image files named 16x16.png and 32x32.png which should be images that are 16 and 32 pixels square. |
| [id](CustomFeatureDefinition_id.md) | Gets the unique ID used for this type of custom feature. |
| [isValid](CustomFeatureDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CustomFeatureDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Events

| Name | Description |
|----|----|
| [customFeatureCompute](CustomFeatureDefinition_customFeatureCompute.md) | The customFeatureCompute event fires when Fusion is computing the timeline and reaches the custom feature. The event is fired if any of the dependencies of the custom feature have changed. You can modify the results of your custom feature based on the dependencies. |

## Accessed From

[CustomFeature.definition](CustomFeature_definition.md), [CustomFeatureDefinition.create](CustomFeatureDefinition_create.md)

## Version

Introduced in version January 2021  


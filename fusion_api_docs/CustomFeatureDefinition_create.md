# CustomFeatureDefinition.create Method

Parent Object: [CustomFeatureDefinition](CustomFeatureDefinition.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

A static function that creates a new CustomFeatureDefinition object. The creation of a CustomFeatureDefinition object is required to be able to create new custom features and for existing custom features to behave correctly. The CustomFeatureDefinition object defines all of the information that is common for all custom features of a particular type. For example, it defines the icon and the default name. The CustomFeatureDefinition object also supports the events that used to react to an existing feature being edited or re-computed.  

The custom feature definition should be created when your add-in is initially loaded to notify Fusion that the add-in that supports that custom feature type is available.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.CustomFeatureDefinition.create(id, defaultName, iconFolder)
```

## Return Value

| Type | Description |
|----|----|
| [CustomFeatureDefinition](CustomFeatureDefinition.md) | Returns the newly created CustomFeatureDefinition or null in the case of failure. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique ID for custom features of a particular type. Care must be taken to ensure that this is unique and you must be consistent in its use once you've chosen an ID. A good practice to help ensure unique naming is to use the name of your company in combination with the name of the feature, such as "CompanyName.FeatureName". For example, "WoodTools4U.Dovetail". |
| defaultName | string | The default name of the feature. Fusion will use this name and append a number to each feature instance as it's created. For example, if this is "Dovetail" the first custom feature created will be named "Dovetail1" and the second will be "Dovetail2". If you want to localize this name you can use the Application.Preferences.generalPreferences.userLanguage property to determine what language the user has chosen and use the corresponding name for that language. |
| iconFolder | string | The folder that contains the image files that will be used for the icon for this feature in the timeline. This can be a full path or a relative path where it will be relative to the add-in file. The folder should contain the image files named 16x16.png and 32x32.png which should be images that are 16 and 32 pixels square. |

## Version

Introduced in version January 2021  


# ApplicationFolders Object

Derived from: [Base](Base.md) Object  

## Description

The ApplicationFolders object provides access to the paths of various folders associated with Fusion.

## Methods

| Name | Description |
|----|----|
| [classType](ApplicationFolders_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [appLogFilePath](ApplicationFolders_appLogFilePath.md) | Returns the full filename for the current application log file. |
| [appStoreInstallPath](ApplicationFolders_appStoreInstallPath.md) | Returns the path where apps from the Autodesk App Store are installed. |
| [defaultPathForScriptsAndAddIns](ApplicationFolders_defaultPathForScriptsAndAddIns.md) | Gets and sets the default path for scripts and add-ins. This is the same as the defaultPathForScriptsAndAddIns property on the APIPreferences object. |
| [isValid](ApplicationFolders_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [materialsPath](ApplicationFolders_materialsPath.md) | Returns the path where user-created material and appearance libraries are saved. |
| [objectType](ApplicationFolders_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [optionsPath](ApplicationFolders_optionsPath.md) | Returns the path to the user-specific folder where Fusion saves various options. |
| [rootPath](ApplicationFolders_rootPath.md) | Returns the path to the version-specific folder where Fusion is installed. |
| [userDataPath](ApplicationFolders_userDataPath.md) | Returns the path where some user-specific data is stored. |

## Accessed From

[Application.applicationFolders](Application_applicationFolders.md)

## Version

Introduced in version September 2024  


# Script Object

Derived from: [Base](Base.md) Object  

## Description

Object that represents a script or add-in.

## Methods

| Name | Description |
| --- | --- |
| [classType](Script_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [edit](Script_edit.md) | Invokes the default edit behavior for this script or add-in. |
| [run](Script_run.md) | Runs this script or add-in, if it's not already running. |
| [stop](Script_stop.md) | If this script or add-in is running, this method will stop it. The isRunning property can be used to determine if it is running. If the script or add-in is not running and this method is called, there is no effect. |
| [unlink](Script_unlink.md) | Unlinks this script or add-in. This removes it from Fusion's list of linked scripts and add-ins, so it is no longer displayed in the dialog, and if it's an add-in, it will no longer run on startup. This is only valid for a script or add-in that is linked; the sourceLocation property returns LinkedScriptSourceLocation. |

## Properties

| Name | Description |
| --- | --- |
| [appStoreURL](Script_appStoreURL.md) | For an add-in installed from the Autodesk App Store, this property returns the URL on the store for the page of this app. This property returns an empty string for all scripts and add-ins not installed from the App Store and if there is a problem determining the URL for an App Store app. |
| [author](Script_author.md) | Returns the author information associated with this script or add-in. |
| [description](Script_description.md) | Gets the description of this script or add-in. |
| [folder](Script_folder.md) | Gets the full path of the folder that contains this script or add-in. |
| [helpFilename](Script_helpFilename.md) | Returns the filename of a local html file that serves as the help file for this script or add-in. This filename is defined in the manifest of the script or add-in using the "helpFilename" setting. |
| [iconFilename](Script_iconFilename.md) | Returns the filename of the image file that can be used as the icon for this script or add-in. This filename is defined in the manifest of the script or add-in using the "iconFilename" setting. |
| [id](Script_id.md) | Gets the ID of this script or add-in. This is typically a GUID and is assumed to be unique with respect to all other add-ins. |
| [isAddIn](Script_isAddIn.md) | Gets if this Script object represents a script or an add-in. Returns true if it is an add-in. |
| [isEditable](Script_isEditable.md) | Indicates if this script or add-in is blocked from being edited by the user in the "Scripts and Add-Ins" dialog. |
| [isFavorite](Script_isFavorite.md) | Gets and sets whether this script or add-in is a favorite of the user. |
| [isInternal](Script_isInternal.md) | Indicates if this is an internal script or add-in that is delivered with Fusion. Returns true if it is an internal script or add-in. |
| [isRunning](Script_isRunning.md) | Gets if this script or add-in is currently running. |
| [isRunOnStartup](Script_isRunOnStartup.md) | Gets and sets whether this add-in will automatically run when Fusion is started. This property is only valid when the isAddIn property returns true. |
| [isValid](Script_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](Script_isVisible.md) | Gets and sets whether the script or add-in is visible within the “Scripts and Add-Ins” dialog. By default, all scripts and add-ins are visible. Setting this to false will cause it to be hidden and unloaded if it is already running. Also, if it’s an add-in set to load on startup, it will no longer be loaded. |
| [location](Script_location.md) | Gets which standard location this script is located. |
| [manifestContent](Script_manifestContent.md) | Gets the full contents of the manifest file associated with this script or add-in. This is particularly useful if you have any custom information defined in the manifest. The manifest file uses JSON to format its content. |
| [name](Script_name.md) | Gets the name of this script or add-in. |
| [objectType](Script_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [programmingLanguage](Script_programmingLanguage.md) | Returns the programming language this script or add-in is written in. |
| [targetOperatingSystem](Script_targetOperatingSystem.md) | Returns the operating systems this script or add-in is available for. |
| [version](Script_version.md) | Returns the version information associated with this script or add-in. |

## Accessed From

[Scripts.addExisting](Scripts_addExisting.md), [Scripts.addNew](Scripts_addNew.md), [Scripts.item](Scripts_item.md), [Scripts.itemByPath](Scripts_itemByPath.md), [Scripts.itemsByName](Scripts_itemsByName.md)

## Version

Introduced in version October 2023  


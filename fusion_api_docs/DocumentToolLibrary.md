# DocumentToolLibrary Object

Derived from: [ToolLibrary](ToolLibrary.md) Object  

## Description

DocumentToolLibrary provides access to tools used by the document. It supports adding, updating and deleting tools in the document tool library.

## Methods

| Name | Description |
|----|----|
| [add](DocumentToolLibrary_add.md) | Inserts a Tool at the end of the ToolLibrary. |
| [classType](DocumentToolLibrary_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createEmpty](DocumentToolLibrary_createEmpty.md) | Creates an empty ToolLibrary. |
| [createFromJson](DocumentToolLibrary_createFromJson.md) | Creates a ToolLibrary by given JSON-string. Raises an error if the given JSON is invalid. |
| [createQuery](DocumentToolLibrary_createQuery.md) | Creates a new ToolQuery that is used to query the library for tools matching the query. |
| [item](DocumentToolLibrary_item.md) | Get Tool by index in ToolLibrary. |
| [operationsByTool](DocumentToolLibrary_operationsByTool.md) | Returns all operations that use the given tool. The tool must exist in the document tool library. Raises an error if the tool is not in the document. |
| [remove](DocumentToolLibrary_remove.md) | Remove Tool by index from ToolLibrary. |
| [toJson](DocumentToolLibrary_toJson.md) | Generate and return JSON string that contains all tools of that list. |
| [toolsBySetupOrFolder](DocumentToolLibrary_toolsBySetupOrFolder.md) | Returns all tools used in a given setup or folder. Given setup or folder must belong to the document of the DocumentToolLibrary. Raises an error if given operation is not in the document. |
| [update](DocumentToolLibrary_update.md) | Update the given tool in the document tool library. The update applies all changes to the tool in the document tool library and therefore on all operations that use the tool. Will error if the tool does not exist in the document tool library. |

## Properties

| Name | Description |
| --- | --- |
| [count](DocumentToolLibrary_count.md) | The number of tools in the ToolLibrary. |
| [isValid](DocumentToolLibrary_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DocumentToolLibrary_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CAM.documentToolLibrary](CAM_documentToolLibrary.md)

## Version

Introduced in version April 2023  


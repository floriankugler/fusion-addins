# CAMTemplate Object

Derived from: [Base](Base.md) Object  

## Description

Object that represents a template for a set of operations. These can be created from operations, optionally stored to files or in a library. The template can be used to re-create those operations in another document.

## Methods

| Name | Description |
|----|----|
| [classType](CAMTemplate_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createEmpty](CAMTemplate_createEmpty.md) | Create an empty CAMTemplate |
| [createFromFile](CAMTemplate_createFromFile.md) | Create a CAMTemplate from a file on disk, i.e. Import the template file. Invalid files will produce errors |
| [createFromOperations](CAMTemplate_createFromOperations.md) | Create a CAMTemplate from a list of Operations |
| [createFromXML](CAMTemplate_createFromXML.md) | Creates a CAMTemplate from an XML string. Invalid template XML will produce errors |
| [createHoleTemplateFromOperations](CAMTemplate_createHoleTemplateFromOperations.md) | Create a hole CAMTemplate from a list of hole operations. Hole templates may be used in Hole Recognition |
| [getHoleSignatureXML](CAMTemplate_getHoleSignatureXML.md) | Convert hole signature to XML. This will be empty if this is not a hole template, or if there is no signature. |
| [save](CAMTemplate_save.md) | Save the CAMTemplate to a file |
| [setHoleSignatureXML](CAMTemplate_setHoleSignatureXML.md) | Provide an XML snippet to specify a hole signature. This will have no effect if this is not a hole template. This will fail if the provided snippet is not valid. |

## Properties

| Name | Description |
| --- | --- |
| [attributes](CAMTemplate_attributes.md) | Returns the collection of attributes associated with this template. |
| [description](CAMTemplate_description.md) | Gets and sets the description of the template. |
| [isHoleTemplate](CAMTemplate_isHoleTemplate.md) | Whether or not this is a hole template |
| [isValid](CAMTemplate_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](CAMTemplate_name.md) | Gets and sets the name of the template. |
| [objectType](CAMTemplate_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [operations](CAMTemplate_operations.md) | Expose operations. |

## Accessed From

[CAMTemplate.createEmpty](CAMTemplate_createEmpty.md), [CAMTemplate.createFromFile](CAMTemplate_createFromFile.md), [CAMTemplate.createFromOperations](CAMTemplate_createFromOperations.md), [CAMTemplate.createFromXML](CAMTemplate_createFromXML.md), [CAMTemplate.createHoleTemplateFromOperations](CAMTemplate_createHoleTemplateFromOperations.md), [CAMTemplateLibrary.childTemplates](CAMTemplateLibrary_childTemplates.md), [CAMTemplateLibrary.templateAtURL](CAMTemplateLibrary_templateAtURL.md), [CreateFromCAMTemplateInput.camTemplate](CreateFromCAMTemplateInput_camTemplate.md)

## Version

Introduced in version April 2023  


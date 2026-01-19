# PostProcessingMachineElement Object

Derived from: [MachineElement](MachineElement.md) Object  

## Description

Machine element representing the post processor and post properties.

## Methods

| Name | Description |
|----|----|
| [classType](PostProcessingMachineElement_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [staticTypeId](PostProcessingMachineElement_staticTypeId.md) | Identifying name for all elements of this type. Pass this to the itemByType or itemById methods of MachineElements to filter to elements of this type. |
| [updatePostParameters](PostProcessingMachineElement_updatePostParameters.md) | Overrides the default post parameters with the given user's input. |

## Properties

| Name | Description |
| --- | --- |
| [elementId](PostProcessingMachineElement_elementId.md) | Identifier for this element. Unique within an element type. |
| [isValid](PostProcessingMachineElement_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](PostProcessingMachineElement_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [outputFolder](PostProcessingMachineElement_outputFolder.md) | Gets and sets the path for the output folder where the .nc files will be located. |
| [postParameters](PostProcessingMachineElement_postParameters.md) | Gets the machine scope post properties as parameters. |
| [postURL](PostProcessingMachineElement_postURL.md) | Gets or sets the URL of the post assigned to the machine. |
| [typeId](PostProcessingMachineElement_typeId.md) | Identifier for this type of machine element. |

## Version

Introduced in version July 2025  


# MultiLineTextDefinition Object

Derived from: [SketchTextDefinition](SketchTextDefinition.md) Object  

## Description

Defines the information for multi-line text.

## Methods

| Name | Description |
|----|----|
| [classType](MultiLineTextDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [rotate](MultiLineTextDefinition_rotate.md) | Rotates the text box. |

## Properties

| Name | Description |
| --- | --- |
| [characterSpacing](MultiLineTextDefinition_characterSpacing.md) | Gets and sets the spacing between the characters. This is an additional spacing to apply that is defined as a percentage of the default spacing. A spacing of 0 indicates no additional spacing. A spacing of 50 indicates to use the default plus 50% of the default. |
| [horizontalAlignment](MultiLineTextDefinition_horizontalAlignment.md) | Gets and sets the horizontal alignment of the text with respect to the text rectangle. |
| [isValid](MultiLineTextDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MultiLineTextDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentSketchText](MultiLineTextDefinition_parentSketchText.md) | Returns the SketchText object this definition is associated with. This property will return null in the case the definition object was obtained from a SketchTextInput object because the SketchText object does not yet exist. |
| [rectangleLines](MultiLineTextDefinition_rectangleLines.md) | Returns the four sketch lines that define the boundary of the sketch text. By adding constraints to these lines you can associatively control the size, position and angle of the sketch text. If the MultiLineTextDefinition object is obtained from a SketchTextInput object, this property will return null because the text and it's associated lines have not been created yet. |
| [verticalAlignment](MultiLineTextDefinition_verticalAlignment.md) | Gets and sets the vertical alignment of the text with respect to the text rectangle. |

## Version

Introduced in version December 2020  


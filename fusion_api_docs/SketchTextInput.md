# SketchTextInput Object

Derived from: [Base](Base.md) Object  

## Description

The SketchTextInput object is equivalent to the Sketch Text dialog in that it collects all of the input required to create sketch text. Once the properties of the SketchTextInput object have been defined, use the add method to create the sketch text. A SketchTextInput object is created by using the createInput of the SketchTexts object.

## Methods

| Name | Description |
|----|----|
| [classType](SketchTextInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [setAsAlongPath](SketchTextInput_setAsAlongPath.md) | Sets this SketchTextInput to define text that follows along a specified path. |
| [setAsFitOnPath](SketchTextInput_setAsFitOnPath.md) | Sets this SketchTextInput to define text that fits along a specified path. Fitting on a path will space the characters so the text fits along the entire length of the path entity. |
| [setAsMultiLine](SketchTextInput_setAsMultiLine.md) | Defines the first corner point of the rectangle that will contain the text. |

## Properties

| Name | Description |
| --- | --- |
| [angle](SketchTextInput_angle.md) | **RETIRED** Gets and sets the angle of the text relative to the x-axis of the x-y plane of the sketch. |
| [definition](SketchTextInput_definition.md) | Returns the SketchTextDefinition object associated with this input. When the SketchTextInput is first created this property will return null. Once one of the "set" methods have been called, this will return the SketchTextDefinition of the appropriate type and can be used to make any additional changes to the text. |
| [expression](SketchTextInput_expression.md) | Gets and sets the expression of the parameter that will be created when this SketchText is created. It can be a simple string or it can be an expression that combines text with parameter values. Simple text must be enclosed within single quotes, the same as it is required in the TEXT command dialog. An example of a valid expression is: "'Length: ' + lengthParam" and will result in "Length: 3.0 mm". The expression result can be obtained by using the text property on the created SketchTextInput object. |
| [fontName](SketchTextInput_fontName.md) | Gets and sets the name of the font to use. |
| [height](SketchTextInput_height.md) | **RETIRED** This property has been retired and replaced by the height2 property. |
| [height2](SketchTextInput_height2.md) | Gets and sets the ValueInput that defines the height of the text. This value is used to create a parameter that will control the height of the text. It can be a value where it defines the height of the text in centimeters, or it can be a string where it defines the equation of the parameter and must evaluate to a valid length. |
| [isHorizontalFlip](SketchTextInput_isHorizontalFlip.md) | Gets and sets if the text is flipped horizontally. |
| [isValid](SketchTextInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVerticalFlip](SketchTextInput_isVerticalFlip.md) | Gets and sets if the text is flipped vertically. |
| [objectType](SketchTextInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [position](SketchTextInput_position.md) | **RETIRED** Gets and sets the position of the text on the x-y plane of the sketch. The text must lie on the x-y plane so the Z component of the point is ignored and always treated as zero. |
| [text](SketchTextInput_text.md) | Gets and sets the displayed text. This represents the text that results from evaluating the input formatted text. For example, if the formatted text is "'Length: ' + lengthParam", this property will return "Length: 3.0 in". Setting this property will overwrite any equation defined by the expression and replace it with simple text. Use the expression property to be able to define a full expression. |
| [textStyle](SketchTextInput_textStyle.md) | Gets and sets the text style to apply to the entire text. This is a bitwise enum so styles can be combined to apply multiple styles. For example you can apply bold and italic. |

## Accessed From

[SketchTexts.createInput](SketchTexts_createInput.md), [SketchTexts.createInput2](SketchTexts_createInput2.md), [SketchTexts.createInput3](SketchTexts_createInput3.md)

## Samples

| Name | Description |
|----|----|
| [Sketch Text API Sample](SketchTextSample_Sample.md) | Demonstrates creating sketch text by creating both mult-line text and text along a curve. |

## Version

Introduced in version March 2015  


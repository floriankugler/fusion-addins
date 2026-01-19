# SketchTexts Object

Derived from: [Base](Base.md) Object  

## Description

The collection of text blocks in a sketch. This provides access to the existing text blocks and supports creating new text blocks.

## Methods

| Name | Description |
|----|----|
| [add](SketchTexts_add.md) | Creates a sketch text. |
| [classType](SketchTexts_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](SketchTexts_createInput.md) | \*\*RETIRED\*\* Creates a SketchTextInput object that can be used to define additional settings when creating sketch text. The SketchTextInput object is equivalent to the Sketch Text dialog in that it collects all of the input required to create sketch text. Once the properties of the SketchTextInput object have been defined, use the add method to create the sketch text. |
| [createInput2](SketchTexts_createInput2.md) | \*\*RETIRED\*\* This method has been retired and replaced by createInput3. Use the new method to define text using an expression that can combine literal text with parameter values. |
| [createInput3](SketchTexts_createInput3.md) | Creates a SketchTextInput object that is used to define the additional input to create text. The SketchTextInput object is equivalent to the Sketch Text dialog in that it collects all of the input required to create sketch text. You must call setAsFitOnPath, setAsAlongPath, or setAsMultiLine methods to define one of the three types of text. Once the properties of the SketchTextInput object have been defined, pass the SketchTextInput to the add method to create the sketch text. |
| [item](SketchTexts_item.md) | Function that returns the specified sketch text using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](SketchTexts_count.md) | Returns the number of texts in the sketch. |
| [isValid](SketchTexts_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SketchTexts_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Sketch.sketchTexts](Sketch_sketchTexts.md)

## Samples

| Name | Description |
|----|----|
| [SketchTextInput.setAsAlongPath](SketchTextinput_setAsAlongPath_Sample.md) | Demonstrates the SketchTextInput.setAsAlongPath method. |
| [SketchTextInput.setAsFitOnPath](SketchTextInput_setAsFitOnPath_Sample.md) | Demoonstrates the SketchTextInput.setAsFitOnPath method. |
| [SketchTextInput.setAsMultiLine](SketchTextInput_setAsMultiLine_Sample.md) | Demonstrates the SketchTextInput.setAsMultiLine method. |
| [Sketch Text API Sample](SketchTextSample_Sample.md) | Demonstrates creating sketch text by creating both mult-line text and text along a curve. |

## Version

Introduced in version March 2015  


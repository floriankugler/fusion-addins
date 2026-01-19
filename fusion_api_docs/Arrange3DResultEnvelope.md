# Arrange3DResultEnvelope Object

Derived from: [ArrangeResultEnvelope](ArrangeResultEnvelope.md) Object  

## Description

Represents the arrange envelope result of a 3D arrange feature.

## Methods

| Name | Description |
|----|----|
| [classType](Arrange3DResultEnvelope_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [boundingBox](Arrange3DResultEnvelope_boundingBox.md) | The bounding box of this result. The coordinates are defined with respect to the root component base coordinate system. |
| [envelopeDefinition](Arrange3DResultEnvelope_envelopeDefinition.md) | Returns the envelope definition that provides the settings for this envelope. To use this property, you need to position the timeline marker immediately before the Arrange feature. This can be accomplished using the following code: arrangeFeature.timelineObject.rollTo(True) |
| [isValid](Arrange3DResultEnvelope_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](Arrange3DResultEnvelope_name.md) | Gets and sets the name of the envelope as seen in the browser. |
| [objectType](Arrange3DResultEnvelope_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [occurrences](Arrange3DResultEnvelope_occurrences.md) | Returns a collection object of the occurrences in this envelope. |
| [parentFeature](Arrange3DResultEnvelope_parentFeature.md) | Returns the ArrangeFeature object this result is for. |

## Version

Introduced in version January 2025  


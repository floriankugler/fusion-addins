# ArrangePlaneResultEnvelope Object

Derived from: [ArrangeResultEnvelope](ArrangeResultEnvelope.md) Object  

## Description

Represents the arrange result of a single envelope that is defined on a plane.

## Methods

| Name | Description |
|----|----|
| [classType](ArrangePlaneResultEnvelope_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [boundingBox](ArrangePlaneResultEnvelope_boundingBox.md) | The bounding box of the this result. The coordinates are defined using the coordinate system of the construction plane used to define the envelope. |
| [envelopeDefinition](ArrangePlaneResultEnvelope_envelopeDefinition.md) | Returns the envelope definition that provides the settings for this envelope. To use this property, you need to position the timeline marker immediately before the Arrange feature. This can be accomplished using the following code: arrangeFeature.timelineObject.rollTo(True) |
| [isValid](ArrangePlaneResultEnvelope_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](ArrangePlaneResultEnvelope_name.md) | Gets and sets the name of the envelope as seen in the browser. |
| [objectType](ArrangePlaneResultEnvelope_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [occurrences](ArrangePlaneResultEnvelope_occurrences.md) | Returns a collection object of the occurrences in this envelope. |
| [parentFeature](ArrangePlaneResultEnvelope_parentFeature.md) | Returns the ArrangeFeature object this result is for. |

## Version

Introduced in version January 2025  


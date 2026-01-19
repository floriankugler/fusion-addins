# ArrangePlaneEnvelopeDefinition Object

Derived from: [ArrangeEnvelopeDefinition](ArrangeEnvelopeDefinition.md) Object  

## Description

The ArrangePlaneEnvelope object represents an arrange envelope defined by a construction plane. This defines the settings of the envelope and the EnvelopeResult provides access to the resulting envelope and its contents.

## Methods

| Name | Description |
|----|----|
| [classType](ArrangePlaneEnvelopeDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [envelopeSpacing](ArrangePlaneEnvelopeDefinition_envelopeSpacing.md) | Returns the parameter that controls the offset distance between envelopes when there is more than one. You can modify the value by using the properties on the returned ModelParameter object. |
| [frameWidth](ArrangePlaneEnvelopeDefinition_frameWidth.md) | Returns the parameter that controls the width of the envelope frame. This defines the offset distance of the objects from the edge of the frame. You can modify the value by using the properties on the returned ModelParameter object. |
| [isPartialArrangeAllowed](ArrangePlaneEnvelopeDefinition_isPartialArrangeAllowed.md) | Gets and sets if a partial arrange is allowed for this envelope. |
| [isValid](ArrangePlaneEnvelopeDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [length](ArrangePlaneEnvelopeDefinition_length.md) | Returns the parameter that controls the length of the envelope frame. This defines the You can modify the value by using the properties on the returned ModelParameter object. |
| [objectSpacing](ArrangePlaneEnvelopeDefinition_objectSpacing.md) | Returns the parameter that controls the space between objects in the arrangement. You can modify the value by using the properties on the returned ModelParameter object. |
| [objectType](ArrangePlaneEnvelopeDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [originXOffset](ArrangePlaneEnvelopeDefinition_originXOffset.md) | Returns the parameter that controls the X offset of the frame from the origin of the construction plane. You can modify the value by using the properties on the returned ModelParameter object. |
| [originYOffset](ArrangePlaneEnvelopeDefinition_originYOffset.md) | Returns the parameter that controls the Y offset of the frame from the origin of the construction plane. You can modify the value by using the properties on the returned ModelParameter object. |
| [parentArrange](ArrangePlaneEnvelopeDefinition_parentArrange.md) | Returns the parent ArrangeFeature this envelope is associated with. |
| [placementClearance](ArrangePlaneEnvelopeDefinition_placementClearance.md) | Returns the parameter that controls the offset of the objects from the base plane of the arrangement (the "up" direction). You can modify the value by using the properties on the returned ModelParameter object. |
| [plane](ArrangePlaneEnvelopeDefinition_plane.md) | Gets and sets the ConstructionPlane the envelope is defined on. |
| [quantity](ArrangePlaneEnvelopeDefinition_quantity.md) | Returns the parameter that defines the number of envelopes that can be created. A value of -1 indicates that there is no limit. |
| [width](ArrangePlaneEnvelopeDefinition_width.md) | Returns the parameter that controls the width of the envelope frame. This defines the You can modify the value by using the properties on the returned ModelParameter object. |

## Version

Introduced in version January 2025  


# ArrangeComponent Object

Derived from: [Base](Base.md) Object  

## Description

Defines a component within an arrangement. This specifies an occurrence along with additional arrangement information. This object is the API equivalent of a single line within the component list shown in the Arrange dialog. This object is used for both the creation of a new Arrange feature and querying and modifying an existing Arrange feature.

## Methods

| Name | Description |
| --- | --- |
| [classType](ArrangeComponent_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](ArrangeComponent_deleteMe.md) | Deletes this ArrangeComponent from the arrangement. |
| [setRotationUsingEdge](ArrangeComponent_setRotationUsingEdge.md) | Sets the rotation angle using the specified edge such that the edge is pointing in the zero rotation angle. This is a convenience method to set the rotation angle. The rotation property can be used to accomplish the same result. This is only valid for 2D True Shape arrangements and will fail for 2D rectangular and 3D arrangements. |

## Properties

| Name | Description |
| --- | --- |
| [isDirectionFlipped](ArrangeComponent_isDirectionFlipped.md) | Specifies if the direction is flipped from it's default direction. For a component defined by a face the default direction is defined by the selected face and the isGlobalDirectionFaceUp property of the Arrange2DDefinition associated with the parent ArrangeFeature object. For a component defined by an occurrence, the default direction orients the occurrence such that the largest face points downward. For a 3D arrange, this property is ignored and the orientation of the part is the same as it exists in the original assembly. |
| [isFiller](ArrangeComponent_isFiller.md) | Specifies if this component will be used to fill any left over empty space in the available envelopes. This is only valid for 2D True Shape arrangements and is ignored for 2D rectangular and 3D arrangements. |
| [isValid](ArrangeComponent_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ArrangeComponent_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [occurrence](ArrangeComponent_occurrence.md) | Returns the Occurrence associated with this ArrangeComponent. If an Occurrence was used to define this ArrangeComponent, this will return the same thing as the occurrenceOrFace. If a BRepFace was used to define this ArrangeComponent, this will return the Occurrence the face is in. This is a convenience property to make accessing the occurrence simpler. |
| [occurrenceOrFace](ArrangeComponent_occurrenceOrFace.md) | The BRepFace or Occurrence that was used to identify this ArrangeComponent. |
| [parentArrangeFeature](ArrangeComponent_parentArrangeFeature.md) | Returns the ArrangeFeature this ArrangeComponent is associated with. This property returns null in the case where a feature hasn't been created yet and there is only an ArrangeFeatureInput. |
| [priority](ArrangeComponent_priority.md) | Specifies the nesting priority for this component. For a 3D arrange, this property is ignored and setting it will fail. |
| [quantity](ArrangeComponent_quantity.md) | Specifies the quantity of this component to use in the arrange. This defaults to -1, which indicates that the global quantity is to be used. For a 3D arrange, this property is ignored and the quantity is always one. |
| [rotation](ArrangeComponent_rotation.md) | Gets and sets the rotation angle of this ArrangeComponent. The value is defined in Radians, is relative to the zero direction vector returned by the zeroDirectionVector property, and is in a counterclockwise direction. This is only valid for 2D True Shape arrangements and is ignored for 2D rectangular and 3D arrangements. |
| [rotationType](ArrangeComponent_rotationType.md) | Gets and sets the rotation type for this ArrangeComponent. This defaults to use the global rotation type defined for the arrangement. For a 3D arrange, this property is ignored. |
| [upDirection](ArrangeComponent_upDirection.md) | Returns a vector that is the up direction of this ArrangeComponent. |
| [zeroDirection](ArrangeComponent_zeroDirection.md) | Returns a vector that is the zero degree direction of this ArrangeComponent. |

## Accessed From

[ArrangeComponents.add](ArrangeComponents_add.md), [ArrangeComponents.item](ArrangeComponents_item.md), [ArrangeFeature.unusedComponents](ArrangeFeature_unusedComponents.md), [ArrangeOccurrenceResult.arrangeComponent](ArrangeOccurrenceResult_arrangeComponent.md)

## Version

Introduced in version January 2025  



Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Represent a connected region on a single geometric surface.

## Methods

| Name | Description |
|----|----|
| [classType](FaceGroup_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](FaceGroup_createForAssemblyContext.md) | Returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |

## Properties

| Name | Description |
| --- | --- |
| [area](FaceGroup_area.md) | Returns the area in cm ^ 2. |
| [assemblyContext](FaceGroup_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this face group object is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly. but is already the native object. |
| [attributes](FaceGroup_attributes.md) | Returns the collection of attributes associated with this face group. |
| [boundingBox](FaceGroup_boundingBox.md) | Returns the bounding box of this face |
| [centroid](FaceGroup_centroid.md) | Returns a point at the centroid (aka, geometric center) of the face. |
| [entityToken](FaceGroup_entityToken.md) | Returns a token for the face group object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same face. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. This is only valid for faces that exist in the design, (the isTemporary property is false). |
| [isPlanar](FaceGroup_isPlanar.md) | Returns if the face group is planar or not. |
| [isValid](FaceGroup_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [nativeObject](FaceGroup_nativeObject.md) | The NativeObject is the object outside the context of an assembly. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](FaceGroup_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentBody](FaceGroup_parentBody.md) | Returns the parent body of the face. |
| [tempId](FaceGroup_tempId.md) | Returns the temporary ID of this face group. This ID is only good while the document remains open and as long as the owning mesh body is not modified in any way. |

## Accessed From

[FaceGroup.createForAssemblyContext](FaceGroup_createForAssemblyContext.md), [FaceGroup.nativeObject](FaceGroup_nativeObject.md), [FaceGroups.item](FaceGroups_item.md), [MeshCombineFaceGroupsFeature.inputFaceGroups](MeshCombineFaceGroupsFeature_inputFaceGroups.md), [MeshCombineFaceGroupsFeatureInput.inputFaceGroups](MeshCombineFaceGroupsFeatureInput_inputFaceGroups.md)

## Version

Introduced in version September 2024  


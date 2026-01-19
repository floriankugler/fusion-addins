# MeshBody Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to a mesh body.

## Methods

| Name | Description |
|----|----|
| [classType](MeshBody_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](MeshBody_copy.md) | Copies the mesh body to the clipboard. |
| [copyToComponent](MeshBody_copyToComponent.md) | Creates a copy of this mesh body into the specified target. |
| [createComponent](MeshBody_createComponent.md) | Creates a new component and occurrence within the component that currently owns this body. This body is moved into the new component and returned. The newly created component can be obtained by using the parentComponent property of the MeshBody object. |
| [createForAssemblyContext](MeshBody_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. Fails if this object is not the NativeObject. |
| [cut](MeshBody_cut.md) | Cuts the mesh body to the clipboard. |
| [deleteMe](MeshBody_deleteMe.md) | Deletes the mesh body. |
| [findByTempId](MeshBody_findByTempId.md) | Returns the face group with the temporary id. |
| [moveToComponent](MeshBody_moveToComponent.md) | Moves this mesh body from it's current component into the root component or the component owned by the specified occurrence. |

## Properties

| Name | Description |
| --- | --- |
| [appearance](MeshBody_appearance.md) | Read-write property that gets and sets the current appearance of the body. Setting this property will result in applying an override appearance to the body and the AppearanceSourceType property will return OverrideAppearanceSource. Setting this property to null will remove any override. |
| [appearanceSourceType](MeshBody_appearanceSourceType.md) | Read-write property that gets the source of the appearance for the body. If this returns OverrideAppearanceSource, an override exists on this body. The override can be removed by setting the Appearance property to null. |
| [area](MeshBody_area.md) | Returns the area in cm ^ 2. |
| [assemblyContext](MeshBody_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](MeshBody_attributes.md) | Returns the collection of attributes associated with this mesh body. |
| [baseOrFormFeature](MeshBody_baseOrFormFeature.md) | This property returns the base or form feature that this mesh body is associated with. It returns null in a direct modeling design. |
| [boundingBox](MeshBody_boundingBox.md) | Returns the bounding box of this mesh body. |
| [displayMesh](MeshBody_displayMesh.md) | Returns the associated mesh that is used for the display. This will always be triangles and includes any textures. |
| [displayOverrides](MeshBody_displayOverrides.md) | Gets the object that allows manipulation of overrides that control how the mesh is displayed in the interactive 3D view. |
| [entityToken](MeshBody_entityToken.md) | Returns a token for the MeshBody object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same mesh body. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [faceGroups](MeshBody_faceGroups.md) | Returns a collection of all of the face groups in the body. |
| [isClosed](MeshBody_isClosed.md) | Check to see if the mesh is closed - i.e. contains no edges with only one triangle. Returns true if the mesh is closed, false if not. |
| [isLightBulbOn](MeshBody_isLightBulbOn.md) | Is the light bulb (as displayed in the browser) on. A mesh body will only be visible if the light bulb is switched on. However, the light bulb can be on and the mesh body is still invisible if the light bulb for all bodies or the owning component is off. |
| [isOriented](MeshBody_isOriented.md) | Check to see if the mesh is oriented - i.e. every edge has at most two triangles, and those triangles have consistent orientations. Returns true if the mesh is oriented, false if not. |
| [isSelectable](MeshBody_isSelectable.md) | Gets and sets if the mesh body is selectable in the graphics window. |
| [isValid](MeshBody_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](MeshBody_isVisible.md) | Gets if the mesh body point is visible. |
| [material](MeshBody_material.md) | Gets and sets the physical material assigned to this mesh body. |
| [mesh](MeshBody_mesh.md) | Returns the original mesh data that was imported. This can include triangles, quads, and polygons. |
| [name](MeshBody_name.md) | Gets and sets the name of the mesh body as displayed in the browser. |
| [nativeObject](MeshBody_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of it's parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](MeshBody_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [opacity](MeshBody_opacity.md) | Gets and sets the opacity override assigned to this body. A value of 1.0 specifies that is it completely opaque and a value of 0.0 specifies that is it completely transparent. This value is not necessarily related to what the user sees because the opacity is inherited. For example, if you this body is in a component and that component's opacity is set to something other than 1.0, the body will also be shown as slightly transparent even though the opacity property for the body will return 1.0. Because the component that contains the body can be referenced as an occurrence in other components and they can have different opacity settings, it's possible that different instances of the same body can display using different opacity levels. To get the opacity that it is being displayed with use the MeshBody.visibleOpacity property. This is the API equivalent of the "Opacity Control" command available for the body in the browser. |
| [orientedMinimumBoundingBox](MeshBody_orientedMinimumBoundingBox.md) | Returns an oriented bounding box of the body that is best oriented to tightly fit the body. |
| [parentComponent](MeshBody_parentComponent.md) | Returns the parent Component. |
| [textureMapControl](MeshBody_textureMapControl.md) | Returns the TextureMapControl object associated with this body when there is an appearance assigned to the body that has a texture associated with it. If there isn't a texture, this property will return null. If there is a texture, you can use the returned object to query and modify how the texture is applied to the body. |
| [visibleOpacity](MeshBody_visibleOpacity.md) | The user can set an override opacity for components and bodies these opacity overrides combine if children and parent components have overrides. This property returns the actual opacity that is being used to render the body. To set the opacity use the opacity property of the MeshBody object. |
| [volume](MeshBody_volume.md) | Returns the volume in cm ^ 3. Returns 0 in the case the mesh body is not closed. |

## Accessed From

[BaseFeature.meshBodies](BaseFeature_meshBodies.md), [FaceGroup.parentBody](FaceGroup_parentBody.md), [MeshBodies.addByTriangleMeshData](MeshBodies_addByTriangleMeshData.md), [MeshBodies.item](MeshBodies_item.md), [MeshBody.copyToComponent](MeshBody_copyToComponent.md), [MeshBody.createComponent](MeshBody_createComponent.md), [MeshBody.createForAssemblyContext](MeshBody_createForAssemblyContext.md), [MeshBody.moveToComponent](MeshBody_moveToComponent.md), [MeshBody.nativeObject](MeshBody_nativeObject.md), [MeshBodyList.item](MeshBodyList_item.md), [MeshCombineFeature.targetBody](MeshCombineFeature_targetBody.md), [MeshCombineFeature.toolBodies](MeshCombineFeature_toolBodies.md), [MeshCombineFeatureInput.targetBody](MeshCombineFeatureInput_targetBody.md), [MeshCombineFeatureInput.toolBodies](MeshCombineFeatureInput_toolBodies.md), [MeshConvertFeature.inputBodies](MeshConvertFeature_inputBodies.md), [MeshConvertFeatureInput.inputBodies](MeshConvertFeatureInput_inputBodies.md), [MeshRemoveFeature.inputBodies](MeshRemoveFeature_inputBodies.md), [MeshRemoveFeatureInput.inputBodies](MeshRemoveFeatureInput_inputBodies.md), [VolumetricModelToMeshFeature.meshBody](VolumetricModelToMeshFeature_meshBody.md)

## Version

Introduced in version August 2014  


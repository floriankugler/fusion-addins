# BRepBody Object

Derived from: [Base](Base.md) Object  

## Description

Represents a B-Rep (Boundary Representation) body.

## Methods

| Name | Description |
| --- | --- |
| [classType](BRepBody_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [convert](BRepBody_convert.md) | Creates a new body where the faces and edges are converted to different types of geometry based on the input options. This is particularly useful when you need a body made up entirely of NURBS surfaces. The tempId on the faces, edges, and vertices on the new body will match with the corresponding tempId on the original body. In cases where faces are split as a result of the conversion there can be more than one face or edge in the new body that matches to a single face or edge in the original body. The findByTempId method will find the entity with the matching id. |
| [copy](BRepBody_copy.md) | Copies the body to the clipboard. This property is only valid if the IsTransient property is false. |
| [copyToComponent](BRepBody_copyToComponent.md) | Creates a copy of this body into the specified target. |
| [createComponent](BRepBody_createComponent.md) | Creates a new component and occurrence within the component that currently owns this body. This body is moved into the new component and returned. The newly created component can be obtained by using the parentComponent property of the BRepBody object. This method is only valid if the IsTransient property is false. |
| [createForAssemblyContext](BRepBody_createForAssemblyContext.md) | Returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. This method is only valid if the IsTransient property is false. |
| [cut](BRepBody_cut.md) | Cuts the body to the clipboard. This property is only valid if the IsTransient property is false. |
| [deleteMe](BRepBody_deleteMe.md) | Deletes the body. This property is only valid if the IsTransient property is false. |
| [findByTempId](BRepBody_findByTempId.md) | Returns all of the faces, edges, or vertices that match the input ID. |
| [getPhysicalProperties](BRepBody_getPhysicalProperties.md) | Returns the PhysicalProperties object that has properties for getting the area, density, mass, volume, moments, etc of this body. |
| [moveToComponent](BRepBody_moveToComponent.md) | Moves this body from it's current component into the root component or the component owned by the specified occurrence. |
| [pointContainment](BRepBody_pointContainment.md) | Determines the relationship of the input point with respect to this body. |

## Properties

| Name | Description |
| --- | --- |
| [appearance](BRepBody_appearance.md) | Read-write property that gets and sets the current appearance of the body. Setting this property will result in applying an override appearance to the body and the AppearanceSourceType property will return OverrideAppearanceSource. Setting this property to null will remove any override. This property is only valid if the IsTransient property is false. |
| [appearanceSourceType](BRepBody_appearanceSourceType.md) | Read-write property that gets the source of the appearance for the body. If this returns OverrideAppearanceSource, an override exists on this body. The override can be removed by setting the Appearance property to null. This property is only valid if the IsTransient property is false. |
| [area](BRepBody_area.md) | Returns the area in cm ^ 2. |
| [assemblyContext](BRepBody_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this BRepBody object is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly. but is already the native object. Also returns null in the case where this body is transient. |
| [attributes](BRepBody_attributes.md) | Returns the collection of attributes associated with this face. |
| [baseFeature](BRepBody_baseFeature.md) | If this body is associated with a base feature, this property will return that base feature. If it's not associated with a base feature, this property will return null. |
| [boundingBox](BRepBody_boundingBox.md) | Returns the bounding box of this body. |
| [concaveEdges](BRepBody_concaveEdges.md) | Returns all of the edges that connect concave faces. |
| [convexEdges](BRepBody_convexEdges.md) | Returns all of the edges that connect convex faces. |
| [deriveFeature](BRepBody_deriveFeature.md) | Returns the DeriveFeature if this BRepBody is derived from another design. This property returns null if the BRepBody is not derived from another design (i.e. isDerived property returns false). |
| [edges](BRepBody_edges.md) | Returns a collection of all of the edges in the body. |
| [entityToken](BRepBody_entityToken.md) | Returns a token for the BRepBody object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same body. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. This is only valid for bodies that exist in the design, (the isTemporary property is false). |
| [faces](BRepBody_faces.md) | Returns a collection of all of the faces in the body. |
| [isDerived](BRepBody_isDerived.md) | Returns if this BRepBody is derived from another design. If true, this body cannot be deleted. |
| [isLightBulbOn](BRepBody_isLightBulbOn.md) | Gets and set if the light bulb beside the body node in the browser is on or not. Parent nodes in the browser can have their light bulb off which affects all of their children so this property does not indicate if the body is actually visible, just that it should be visible if all of it's parent nodes are also visible. Use the isVisible property to determine if it's actually visible. This property is only valid if the IsTransient property is false. |
| [isSelectable](BRepBody_isSelectable.md) | Gets and sets if this body is selectable. This property is only valid if the IsTransient property is false. |
| [isSheetMetal](BRepBody_isSheetMetal.md) | Indicates if this body represents a sheet metal folded part or not and if a flat pattern can be created. |
| [isSolid](BRepBody_isSolid.md) | Returns whether this body is closed (solid) or not. |
| [isTemporary](BRepBody_isTemporary.md) | Indicates if this body is represented in the model or is temporary. |
| [isTransient](BRepBody_isTransient.md) | Indicates if this body is represented in the model or is transient. |
| [isValid](BRepBody_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](BRepBody_isVisible.md) | Gets if this body is currently visible in the graphics window. Use the isLightBulbOn to change if the light bulb beside the body node in the browser is on or not. Parent nodes in the browser can have their light bulb off which affects all of their children. This property indicates the final result and whether this body is actually visible or not. This property is only valid if the IsTransient property is false. |
| [lumps](BRepBody_lumps.md) | Returns a collection of all of the lumps in the body. |
| [material](BRepBody_material.md) | Gets and sets the material assigned to this body. This property is only valid if the IsTransient property is false. |
| [meshManager](BRepBody_meshManager.md) | Returns the mesh manager object for this body. |
| [name](BRepBody_name.md) | Gets and sets the name of the body. This property is only valid if the IsTransient property is false. |
| [nativeObject](BRepBody_nativeObject.md) | The NativeObject is the object outside the context of an assembly. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](BRepBody_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [opacity](BRepBody_opacity.md) | Gets and sets the opacity override assigned to this body. A value of 1.0 specifies that is it completely opaque and a value of 0.0 specifies that is it completely transparent. This value is not necessarily related to what the user sees because the opacity is inherited. For example, if you this body is in a component and that component's opacity is set to something other than 1.0, the body will also be shown as slightly transparent even though the opacity property for the body will return 1.0. Because the component that contains the body can be referenced as an occurrence in other components and they can have different opacity settings, it's possible that different instances of the same body can display using different opacity levels. To get the opacity that it is being displayed with use the BrepBody.visibleOpacity property. This is the API equivalent of the "Opacity Control" command available for the body in the browser. |
| [orientedMinimumBoundingBox](BRepBody_orientedMinimumBoundingBox.md) | Returns an oriented bounding box of the body that is best oriented to tightly fit the body. |
| [parentComponent](BRepBody_parentComponent.md) | Returns the component this body is owned by. |
| [physicalProperties](BRepBody_physicalProperties.md) | Returns the PhysicalProperties object that has properties for getting the area, density, mass, volume, moments, etc of this body. Property values will be calculated using the 'LowCalculationAccuracy' setting when using this property to get the PhysicalProperties object. To specify a higher calculation tolerance, use the getPhysicalProperties method on the Design class instead. |
| [preciseBoundingBox](BRepBody_preciseBoundingBox.md) | Returns a bounding box that tightly fits this body. |
| [revisionId](BRepBody_revisionId.md) | Returns the current revision ID of the body. This ID changes any time the body is modified in any way. By getting and saving the ID when you create any data that is dependent on the body, you can then compare the saved ID with the current ID to determine if the body has changed to know if you should update your data. |
| [shells](BRepBody_shells.md) | Returns a collection of all of the shells in the body. |
| [textureMapControl](BRepBody_textureMapControl.md) | Returns the TextureMapControl object associated with this body when there is an appearance assigned to the body that has a texture associated with it. If there isn't a texture, this property will return null. If there is a texture, you can use the returned object to query and modify how the texture is applied to the body. |
| [vertices](BRepBody_vertices.md) | Returns a collection of all of the vertices in the body. |
| [visibleOpacity](BRepBody_visibleOpacity.md) | The user can set an override opacity for components and bodies these opacity overrides combine if children and parent components have overrides. This property returns the actual opacity that is being used to render the body. To set the opacity use the opacity property of the BRepBody object. |
| [volume](BRepBody_volume.md) | Returns the volume in cm ^ 3. Returns 0 in the case the body is not solid. |
| [wires](BRepBody_wires.md) | Returns any wire bodies that exist within this body. |

## Accessed From

[BaseFeature.sourceBodies](BaseFeature_sourceBodies.md), [BossFeatureInput.participantBodies](BossFeatureInput_participantBodies.md), [BRepBodies.add](BRepBodies_add.md), [BRepBodies.item](BRepBodies_item.md), [BRepBodies.itemByName](BRepBodies_itemByName.md), [BRepBody.convert](BRepBody_convert.md), [BRepBody.copyToComponent](BRepBody_copyToComponent.md), [BRepBody.createComponent](BRepBody_createComponent.md), [BRepBody.createForAssemblyContext](BRepBody_createForAssemblyContext.md), [BRepBody.moveToComponent](BRepBody_moveToComponent.md), [BRepBody.nativeObject](BRepBody_nativeObject.md), [BRepBodyDefinition.createBody](BRepBodyDefinition_createBody.md), [BRepCell.cellBody](BRepCell_cellBody.md), [BRepCoEdge.body](BRepCoEdge_body.md), [BRepEdge.body](BRepEdge_body.md), [BRepFace.body](BRepFace_body.md), [BRepFace.convert](BRepFace_convert.md), [BRepLoop.body](BRepLoop_body.md), [BRepLump.body](BRepLump_body.md), [BRepShell.body](BRepShell_body.md), [BRepVertex.body](BRepVertex_body.md), [BRepWire.offsetPlanarWire](BRepWire_offsetPlanarWire.md), [BRepWire.parent](BRepWire_parent.md), [CombineFeature.targetBody](CombineFeature_targetBody.md), [CombineFeatureInput.targetBody](CombineFeatureInput_targetBody.md), [CustomGraphicsBRepBody.bRepBody](CustomGraphicsBRepBody_bRepBody.md), [ExtrudeFeature.participantBodies](ExtrudeFeature_participantBodies.md), [ExtrudeFeatureInput.participantBodies](ExtrudeFeatureInput_participantBodies.md), [FlatPattern.bendLinesBody](FlatPattern_bendLinesBody.md), [FlatPattern.extentLinesBody](FlatPattern_extentLinesBody.md), [FlatPattern.flatBody](FlatPattern_flatBody.md), [FlatPattern.foldedBody](FlatPattern_foldedBody.md), [HoleFeature.participantBodies](HoleFeature_participantBodies.md), [HoleFeatureInput.participantBodies](HoleFeatureInput_participantBodies.md), [InterferenceResult.interferenceBody](InterferenceResult_interferenceBody.md), [LoftFeature.participantBodies](LoftFeature_participantBodies.md), [LoftFeatureInput.participantBodies](LoftFeatureInput_participantBodies.md), [PipeFeature.participantBodies](PipeFeature_participantBodies.md), [PipeFeatureInput.participantBodies](PipeFeatureInput_participantBodies.md), [RevolveFeature.participantBodies](RevolveFeature_participantBodies.md), [RevolveFeatureInput.participantBodies](RevolveFeatureInput_participantBodies.md), [SilhouetteSplitFeature.targetBody](SilhouetteSplitFeature_targetBody.md), [SilhouetteSplitFeatureInput.targetBody](SilhouetteSplitFeatureInput_targetBody.md), [SweepFeature.participantBodies](SweepFeature_participantBodies.md), [SweepFeature.solidBody](SweepFeature_solidBody.md), [SweepFeatureInput.participantBodies](SweepFeatureInput_participantBodies.md), [SweepFeatureInput.solidBody](SweepFeatureInput_solidBody.md), [TemporaryBRepManager.copy](TemporaryBRepManager_copy.md), [TemporaryBRepManager.createBox](TemporaryBRepManager_createBox.md), [TemporaryBRepManager.createCylinderOrCone](TemporaryBRepManager_createCylinderOrCone.md), [TemporaryBRepManager.createEllipticalCylinderOrCone](TemporaryBRepManager_createEllipticalCylinderOrCone.md), [TemporaryBRepManager.createFaceFromPlanarWires](TemporaryBRepManager_createFaceFromPlanarWires.md), [TemporaryBRepManager.createHelixWire](TemporaryBRepManager_createHelixWire.md), [TemporaryBRepManager.createProjectedBodyOutline](TemporaryBRepManager_createProjectedBodyOutline.md), [TemporaryBRepManager.createRuledSurface](TemporaryBRepManager_createRuledSurface.md), [TemporaryBRepManager.createSilhouetteCurves](TemporaryBRepManager_createSilhouetteCurves.md), [TemporaryBRepManager.createSphere](TemporaryBRepManager_createSphere.md), [TemporaryBRepManager.createTorus](TemporaryBRepManager_createTorus.md), [TemporaryBRepManager.createWireFromCurves](TemporaryBRepManager_createWireFromCurves.md), [TemporaryBRepManager.imprintOverlapBodies](TemporaryBRepManager_imprintOverlapBodies.md), [TemporaryBRepManager.planeIntersection](TemporaryBRepManager_planeIntersection.md), [TessellateFeature.inputBodies](TessellateFeature_inputBodies.md), [TessellateFeatureInput.inputBodies](TessellateFeatureInput_inputBodies.md)

## Samples

| Name | Description |
|----|----|
| [Get Volume of Active Design API Sample](GetsVolumeOfActiveDesign_Sample.md) | Traverses through the active design and totals the volume of every body within the design. |

## Version

Introduced in version August 2014  


# CustomGraphicsGroup Object

Derived from: [CustomGraphicsEntity](CustomGraphicsEntity.md) Object  

## Description

Represents of group of custom graphics entities. A group can also own other graphics groups.

## Methods

| Name | Description |
| --- | --- |
| [addBRepBody](CustomGraphicsGroup_addBRepBody.md) | Adds a new CustomGraphicsBRepBody object to this group. This displays a real or transient BRepBody object as custom graphics. No relationship exists back to the original input body so if it is changed, the custom graphics will not change. The body associated with the CustomGraphicsBRep body is a copy of the original input body. Equivalent Faces, Edges, and vertices can be found by using the indexes in the collection. For example if you have a face of the original body and find that it is at index 24 in the BRepFaces collection of that body, the equivalent face in the custom graphics body will also be at index 24. This works as long as the original body is not modified in any way. |
| [addCurve](CustomGraphicsGroup_addCurve.md) | Adds a new CustomGraphicsCurve entity to this group. A CustomGraphicsCurve is a wireframe graphic that is based on any object derived from Curve3D (except InfiniteLine3D). This is useful when drawing curved geometry where the alternative is to stroke the smooth curve and draw it as a series of lines. Using this you can directly use the curve and Fusion will automatically take care of creating the correct display for the current level of detail. |
| [addGroup](CustomGraphicsGroup_addGroup.md) | Creates a new, empty CustomGraphicsGroup that is owned by this CustomGraphicsGroup. |
| [addLines](CustomGraphicsGroup_addLines.md) | Adds a new CustomGraphicsLines entity to this group. |
| [addMesh](CustomGraphicsGroup_addMesh.md) | Adds a new CustomGraphicsMesh entity to this group. |
| [addPointSet](CustomGraphicsGroup_addPointSet.md) | Adds a new CustomGraphicsPointSet entity to this group. This will be displayed as one or more points where all of the points will display using the same image. |
| [addText](CustomGraphicsGroup_addText.md) | Adds a new CustomGraphicsText entity to this group. This will be displayed as a single line of text. It is placed so that the upper-left corner is at the point defined and the text will be parallel to the X-Y plane of the world coordinate system and in the X direction. To change it's position relative to the input point you can change the horizontal and vertical justification on the returned CustomGrahicsText object. You can also reorient the text by changing the transform of the returned CustomGraphicsText object. |
| [classType](CustomGraphicsGroup_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](CustomGraphicsGroup_deleteMe.md) | Deletes the entity from the custom graphics group. |
| [getOpacity](CustomGraphicsGroup_getOpacity.md) | Gets the opacity of the graphics entity. |
| [item](CustomGraphicsGroup_item.md) | Function that returns the specified custom graphics entity within this group. This also includes any child graphics groups. |
| [setOpacity](CustomGraphicsGroup_setOpacity.md) | Sets the opacity of the graphics entity. By default, when a new entity is it is completely opaque and does not override the opacity defined by the material. |

## Properties

| Name | Description |
| --- | --- |
| [billBoarding](CustomGraphicsGroup_billBoarding.md) | Gets and sets the billboarding behavior of this custom graphics entity. To define billboarding you can set this property using a CustomGraphicsBillBoard objects that you statically create using the create method of the CustomGraphicsBillBoard class. To remove billboarding from this entity you can set this property to null. Billboarding is used to specify that the orientation of custom graphics is defined relative to the screen instead of model space. This is commonly used for legends and symbols that you want to always face the user, even as the camera is rotated. |
| [boundingBox](CustomGraphicsGroup_boundingBox.md) | Returns a box oriented parallel to the world x-y-x axes that contains the graphics entity. Depending on whether the graphics are drawn in model space or screen space this will return the bounding box in either centimeters (model) or pixels (screen). In the case where it returns the bounding box in pixel space, the Z coordinates of the box will be 0 and can be ignored. |
| [color](CustomGraphicsGroup_color.md) | Gets and sets the current color definition for this entity. The color of custom graphics can be defined in many ways; solid color, simple material, and appearance. |
| [count](CustomGraphicsGroup_count.md) | Returns the number of graphics entities within the group. |
| [cullMode](CustomGraphicsGroup_cullMode.md) | Gets and sets the culling model to use when rendering the entity. Culling is used when the entity contains a mesh or B-Rep faces and defines which sides of the mesh or face are rendered. This is primarily used for a watertight mesh or solid B-Rep so that the "inside" of the faces is not rendered since it's never visible to the user. When a new graphics entity is created its default cull mode is CustomGraphicsCullBack which will optimize the rendering of "solid" meshes so the inside is not rendered. |
| [depthPriority](CustomGraphicsGroup_depthPriority.md) | Gets and sets the depth priority associated with the graphics entity. The depth priority defines how one graphics entity will be drawn with respect to another entity. This is useful when there are entities that lie in the same space so it's ambiguous which should be drawn on the other. For example, if you draw a curve on a planar mesh and want the curve to be completely visible. You can set the depth priority of the curve to be greater than the mesh so it will be drawn after the mesh and will remain visible. When a new graphics entity is created it's default depth priority is 0. |
| [id](CustomGraphicsGroup_id.md) | An id you can specify for the entity. By default, all new graphics entities do not have an id and this property will return an empty string. But in cases where entities will be selected, assigning an id can make understanding what was selected much easier. |
| [isChildrenSelectable](CustomGraphicsGroup_isChildrenSelectable.md) | Defines if the child custom graphic entities are selectable or if the entire group is selected in the UI. By default this is true. If false, the isSelectable property defines if this group is selectable. If true, the isSelectable property of each child entity defines if it is selectable. |
| [isSelectable](CustomGraphicsGroup_isSelectable.md) | Gets and sets if the graphics entity is selectable within the graphics window. By default, when a new entity is created it is selectable. |
| [isValid](CustomGraphicsGroup_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](CustomGraphicsGroup_isVisible.md) | Gets and sets if the graphics entity is visible in the graphics window. By default, when a new entity is created it is visible. |
| [name](CustomGraphicsGroup_name.md) | Gets and sets the name displayed when this entity is selected. If no name has been set, "Custom Graphics" will be displayed. |
| [objectType](CustomGraphicsGroup_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parent](CustomGraphicsGroup_parent.md) | Returns the parent Component for a top-level group or the CustomGraphicsGroup object for graphics entities and child groups. |
| [transform](CustomGraphicsGroup_transform.md) | Gets and sets the transform associated with the graphics entity. When a new graphics entity is created its default transform is an identity matrix which results in the graphics entity being displayed in model space using the original coordinate data used to define the entity. |
| [viewPlacement](CustomGraphicsGroup_viewPlacement.md) | Gets and sets the graphics view placement being applied to this graphics entity. A CustomGraphicsViewPlacement object can be created using the static create method of the class. When assigned to a graphics entity the position of the graphics is defined relative to the view in 2D view space (pixels) rather than in 3D model space (centimeters). |
| [viewScale](CustomGraphicsGroup_viewScale.md) | Gets and sets the graphics view scale being applied to this graphics entity. A CustomGraphicsViewScale object can be created using the static create method of the class. When assigned to a graphics entity the size of the graphics entity is defined in view space (pixels) instead of model space (centimeters). |

## Accessed From

[CustomGraphicsGroup.addGroup](CustomGraphicsGroup_addGroup.md), [CustomGraphicsGroups.add](CustomGraphicsGroups_add.md), [CustomGraphicsGroups.item](CustomGraphicsGroups_item.md)

## Version

Introduced in version September 2017  


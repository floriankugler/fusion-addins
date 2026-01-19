# CustomGraphicsMesh Object

Derived from: [CustomGraphicsEntity](CustomGraphicsEntity.md) Object  

## Description

Represents a custom triangle mesh drawn in the graphics window.

## Methods

| Name | Description |
|----|----|
| [classType](CustomGraphicsMesh_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](CustomGraphicsMesh_deleteMe.md) | Deletes the entity from the custom graphics group. |
| [getOpacity](CustomGraphicsMesh_getOpacity.md) | Gets the opacity of the graphics entity. |
| [setOpacity](CustomGraphicsMesh_setOpacity.md) | Sets the opacity of the graphics entity. By default, when a new entity is it is completely opaque and does not override the opacity defined by the material. |

## Properties

| Name | Description |
| --- | --- |
| [billBoarding](CustomGraphicsMesh_billBoarding.md) | Gets and sets the billboarding behavior of this custom graphics entity. To define billboarding you can set this property using a CustomGraphicsBillBoard objects that you statically create using the create method of the CustomGraphicsBillBoard class. To remove billboarding from this entity you can set this property to null. Billboarding is used to specify that the orientation of custom graphics is defined relative to the screen instead of model space. This is commonly used for legends and symbols that you want to always face the user, even as the camera is rotated. |
| [boundingBox](CustomGraphicsMesh_boundingBox.md) | Returns a box oriented parallel to the world x-y-x axes that contains the graphics entity. Depending on whether the graphics are drawn in model space or screen space this will return the bounding box in either centimeters (model) or pixels (screen). In the case where it returns the bounding box in pixel space, the Z coordinates of the box will be 0 and can be ignored. |
| [color](CustomGraphicsMesh_color.md) | Gets and sets the current color definition for this entity. The color of custom graphics can be defined in many ways; solid color, simple material, and appearance. |
| [coordinates](CustomGraphicsMesh_coordinates.md) | Gets and sets the coordinates associated with this CustomGraphicsMesh. |
| [cullMode](CustomGraphicsMesh_cullMode.md) | Gets and sets the culling model to use when rendering the entity. Culling is used when the entity contains a mesh or B-Rep faces and defines which sides of the mesh or face are rendered. This is primarily used for a watertight mesh or solid B-Rep so that the "inside" of the faces is not rendered since it's never visible to the user. When a new graphics entity is created its default cull mode is CustomGraphicsCullBack which will optimize the rendering of "solid" meshes so the inside is not rendered. |
| [depthPriority](CustomGraphicsMesh_depthPriority.md) | Gets and sets the depth priority associated with the graphics entity. The depth priority defines how one graphics entity will be drawn with respect to another entity. This is useful when there are entities that lie in the same space so it's ambiguous which should be drawn on the other. For example, if you draw a curve on a planar mesh and want the curve to be completely visible. You can set the depth priority of the curve to be greater than the mesh so it will be drawn after the mesh and will remain visible. When a new graphics entity is created it's default depth priority is 0. |
| [id](CustomGraphicsMesh_id.md) | An id you can specify for the entity. By default, all new graphics entities do not have an id and this property will return an empty string. But in cases where entities will be selected, assigning an id can make understanding what was selected much easier. |
| [isSelectable](CustomGraphicsMesh_isSelectable.md) | Gets and sets if the graphics entity is selectable within the graphics window. By default, when a new entity is created it is selectable. |
| [isValid](CustomGraphicsMesh_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](CustomGraphicsMesh_isVisible.md) | Gets and sets if the graphics entity is visible in the graphics window. By default, when a new entity is created it is visible. |
| [name](CustomGraphicsMesh_name.md) | Gets and sets the name displayed when this entity is selected. If no name has been set, "Custom Graphics" will be displayed. |
| [normalIndexList](CustomGraphicsMesh_normalIndexList.md) | Gets and sets an array of indices that define which normal is associated with each vertex in the mesh. This is used to look-up the normal in the normalVectors array. |
| [normalVectors](CustomGraphicsMesh_normalVectors.md) | Gets and sets the normal vectors of the mesh where there is a normal vector at each node. The normals are defined as an array of floats where they are the x, y, z components of each vector. |
| [objectType](CustomGraphicsMesh_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parent](CustomGraphicsMesh_parent.md) | Returns the parent Component for a top-level group or the CustomGraphicsGroup object for graphics entities and child groups. |
| [textureCoordinates](CustomGraphicsMesh_textureCoordinates.md) | Gets and sets the texture coordinates as an array of floats where they are the u,v components at each node. They are defined as an array of doubles where they are the u, v coordinates of each node. Defining texture coordinates for a mesh is optional. |
| [transform](CustomGraphicsMesh_transform.md) | Gets and sets the transform associated with the graphics entity. When a new graphics entity is created its default transform is an identity matrix which results in the graphics entity being displayed in model space using the original coordinate data used to define the entity. |
| [vertexIndexList](CustomGraphicsMesh_vertexIndexList.md) | Gets and sets an array of indices that define which coordinate in the coordinate list is used for each vertex in the mesh. Each set of three indices defines a triangle. For example: Indices 0, 1, and 2 define the coordinates to use for the first triangle and indices 3, 4, and 5 define the coordinates for the second triangle, and so on. |
| [viewPlacement](CustomGraphicsMesh_viewPlacement.md) | Gets and sets the graphics view placement being applied to this graphics entity. A CustomGraphicsViewPlacement object can be created using the static create method of the class. When assigned to a graphics entity the position of the graphics is defined relative to the view in 2D view space (pixels) rather than in 3D model space (centimeters). |
| [viewScale](CustomGraphicsMesh_viewScale.md) | Gets and sets the graphics view scale being applied to this graphics entity. A CustomGraphicsViewScale object can be created using the static create method of the class. When assigned to a graphics entity the size of the graphics entity is defined in view space (pixels) instead of model space (centimeters). |

## Accessed From

[CustomGraphicsGroup.addMesh](CustomGraphicsGroup_addMesh.md)

## Version

Introduced in version September 2017  


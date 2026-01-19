# CustomGraphicsText Object

Derived from: [CustomGraphicsEntity](CustomGraphicsEntity.md) Object  

## Description

Represents text drawn in the graphics window. The default position of the text is at (0,0,0) and orientation is the text lying on the x-y plane. To reposition and reorient the text you can use the transformation property.

## Methods

| Name | Description |
|----|----|
| [classType](CustomGraphicsText_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](CustomGraphicsText_deleteMe.md) | Deletes the entity from the custom graphics group. |
| [getOpacity](CustomGraphicsText_getOpacity.md) | Gets the opacity of the graphics entity. |
| [setOpacity](CustomGraphicsText_setOpacity.md) | Sets the opacity of the graphics entity. By default, when a new entity is it is completely opaque and does not override the opacity defined by the material. |

## Properties

| Name | Description |
| --- | --- |
| [billBoarding](CustomGraphicsText_billBoarding.md) | Gets and sets the billboarding behavior of this custom graphics entity. To define billboarding you can set this property using a CustomGraphicsBillBoard objects that you statically create using the create method of the CustomGraphicsBillBoard class. To remove billboarding from this entity you can set this property to null. Billboarding is used to specify that the orientation of custom graphics is defined relative to the screen instead of model space. This is commonly used for legends and symbols that you want to always face the user, even as the camera is rotated. |
| [boundingBox](CustomGraphicsText_boundingBox.md) | Returns a box oriented parallel to the world x-y-x axes that contains the graphics entity. Depending on whether the graphics are drawn in model space or screen space this will return the bounding box in either centimeters (model) or pixels (screen). In the case where it returns the bounding box in pixel space, the Z coordinates of the box will be 0 and can be ignored. |
| [color](CustomGraphicsText_color.md) | Gets and sets the current color definition for this entity. The color of custom graphics can be defined in many ways; solid color, simple material, and appearance. |
| [cullMode](CustomGraphicsText_cullMode.md) | Gets and sets the culling model to use when rendering the entity. Culling is used when the entity contains a mesh or B-Rep faces and defines which sides of the mesh or face are rendered. This is primarily used for a watertight mesh or solid B-Rep so that the "inside" of the faces is not rendered since it's never visible to the user. When a new graphics entity is created its default cull mode is CustomGraphicsCullBack which will optimize the rendering of "solid" meshes so the inside is not rendered. |
| [depthPriority](CustomGraphicsText_depthPriority.md) | Gets and sets the depth priority associated with the graphics entity. The depth priority defines how one graphics entity will be drawn with respect to another entity. This is useful when there are entities that lie in the same space so it's ambiguous which should be drawn on the other. For example, if you draw a curve on a planar mesh and want the curve to be completely visible. You can set the depth priority of the curve to be greater than the mesh so it will be drawn after the mesh and will remain visible. When a new graphics entity is created it's default depth priority is 0. |
| [font](CustomGraphicsText_font.md) | Gets and sets the font used to display the text. This is the default font and applies to all of text unless there is a font override defined within the text. |
| [formattedText](CustomGraphicsText_formattedText.md) | Gets and sets the formatted text definition. This is the full string, including the formatting information, that's used to define the displayed text. |
| [height](CustomGraphicsText_height.md) | The actual height of the text in centimeters. This is useful when you want to position several GraphicsText objects together. |
| [id](CustomGraphicsText_id.md) | An id you can specify for the entity. By default, all new graphics entities do not have an id and this property will return an empty string. But in cases where entities will be selected, assigning an id can make understanding what was selected much easier. |
| [isBold](CustomGraphicsText_isBold.md) | Specifies that the text displays using a bold style. This is the default bold style and applies to all of text unless there is a style override defined within the text. |
| [isItalic](CustomGraphicsText_isItalic.md) | Specifies that the text displays using an italic style. This is the default italic style and applies to all of text unless there is a style override defined within the text. |
| [isSelectable](CustomGraphicsText_isSelectable.md) | Gets and sets if the graphics entity is selectable within the graphics window. By default, when a new entity is created it is selectable. |
| [isStrikeThrough](CustomGraphicsText_isStrikeThrough.md) | Specifies that the text displays using a strike through style. This is the default strike through style and applies to all of text unless there is a style override defined within the text. |
| [isUnderline](CustomGraphicsText_isUnderline.md) | Specifies that the text displays using an underline style. This is the default underline style and applies to all of text unless there is a style override defined within the text. |
| [isValid](CustomGraphicsText_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](CustomGraphicsText_isVisible.md) | Gets and sets if the graphics entity is visible in the graphics window. By default, when a new entity is created it is visible. |
| [name](CustomGraphicsText_name.md) | Gets and sets the name displayed when this entity is selected. If no name has been set, "Custom Graphics" will be displayed. |
| [objectType](CustomGraphicsText_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parent](CustomGraphicsText_parent.md) | Returns the parent Component for a top-level group or the CustomGraphicsGroup object for graphics entities and child groups. |
| [size](CustomGraphicsText_size.md) | Gets and sets the size of the text in centimeters. This is the default size and applies to all of text unless there is a size override defined within the text. |
| [transform](CustomGraphicsText_transform.md) | Gets and sets the transform associated with the graphics entity. When a new graphics entity is created its default transform is an identity matrix which results in the graphics entity being displayed in model space using the original coordinate data used to define the entity. |
| [viewPlacement](CustomGraphicsText_viewPlacement.md) | Gets and sets the graphics view placement being applied to this graphics entity. A CustomGraphicsViewPlacement object can be created using the static create method of the class. When assigned to a graphics entity the position of the graphics is defined relative to the view in 2D view space (pixels) rather than in 3D model space (centimeters). |
| [viewScale](CustomGraphicsText_viewScale.md) | Gets and sets the graphics view scale being applied to this graphics entity. A CustomGraphicsViewScale object can be created using the static create method of the class. When assigned to a graphics entity the size of the graphics entity is defined in view space (pixels) instead of model space (centimeters). |
| [width](CustomGraphicsText_width.md) | The actual width of the text in centimeters. This is useful when you want to position several GraphicsText objects together. |

## Accessed From

[CustomGraphicsGroup.addText](CustomGraphicsGroup_addText.md)

## Version

Introduced in version September 2017  


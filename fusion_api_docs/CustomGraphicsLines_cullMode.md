# CustomGraphicsLines.cullMode Property

Parent Object: [CustomGraphicsLines](CustomGraphicsLines.md)  

## Description

Gets and sets the culling model to use when rendering the entity. Culling is used when the entity contains a mesh or B-Rep faces and defines which sides of the mesh or face are rendered. This is primarily used for a watertight mesh or solid B-Rep so that the "inside" of the faces is not rendered since it's never visible to the user.  

When a new graphics entity is created its default cull mode is CustomGraphicsCullBack which will optimize the rendering of "solid" meshes so the inside is not rendered.

## Syntax

"customGraphicsLines_var" is a variable referencing a CustomGraphicsLines object.  

```python
# Get the value of the property.
propertyValue = customGraphicsLines_var.cullMode

# Set the value of the property.
customGraphicsLines_var.cullMode = propertyValue
```

## Property Value

This is a read/write property whose value is a [CustomGraphicsCullModes](CustomGraphicsCullModes.md).

## Version

Introduced in version September 2017  


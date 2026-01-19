# MeshBody.visibleOpacity Property

Parent Object: [MeshBody](MeshBody.md)  

## Description

The user can set an override opacity for components and bodies these opacity overrides combine if children and parent components have overrides. This property returns the actual opacity that is being used to render the body. To set the opacity use the opacity property of the MeshBody object.

## Syntax

"meshBody_var" is a variable referencing a MeshBody object.  

```python
# Get the value of the property.
propertyValue = meshBody_var.visibleOpacity
```

## Property Value

This is a read only property whose value is a double.

## Samples

| Name                                          | Description                 |
|-----------------------------------------------|-----------------------------|
| [Mesh Body Sample](MeshBodySample_Sample.md) | Mesh body related functions |

## Version

Introduced in version December 2017  


# CustomGraphicsGroup.addBRepBody Method

Parent Object: [CustomGraphicsGroup](CustomGraphicsGroup.md)  

## Description

Adds a new CustomGraphicsBRepBody object to this group. This displays a real or transient BRepBody object as custom graphics. No relationship exists back to the original input body so if it is changed, the custom graphics will not change.  

The body associated with the CustomGraphicsBRep body is a copy of the original input body. Equivalent Faces, Edges, and vertices can be found by using the indexes in the collection. For example if you have a face of the original body and find that it is at index 24 in the BRepFaces collection of that body, the equivalent face in the custom graphics body will also be at index 24. This works as long as the original body is not modified in any way.

## Syntax

"customGraphicsGroup_var" is a variable referencing a [CustomGraphicsGroup](CustomGraphicsGroup.md) object.

```python
returnValue = customGraphicsGroup_var.addBRepBody(body)
```

## Return Value

| Type | Description |
|----|----|
| [CustomGraphicsBRepBody](CustomGraphicsBRepBody.md) | Returns the newly created CustomGraphicsBRepBody object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| body | [BRepBody](BRepBody.md) | The real or transient BRepBody object to draw using custom graphics. |

## Samples

| Name | Description |
| --- | --- |
| [Custom Graphics Sample](CustomGraphicsSample_Sample.md) | A sample demonstrating how to create custom graphics entities. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/GraphicsSampleResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version September 2017  


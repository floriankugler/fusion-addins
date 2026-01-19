# Sketch.projectToSurface Method

Parent Object: [Sketch](Sketch.md)  

## Description

Projects the specified set of curves onto the specified set of faces using the specified method of projection. if the projection type is along a vector, then the directionEntity argument must be supplied. if the projectionType is the closest point method, the directionEntity argument is ignored.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
# Uses no optional arguments.
returnValue = sketch_var.projectToSurface(faces, curves, projectType)

# Uses optional arguments.
returnValue = sketch_var.projectToSurface(faces, curves, projectType, directionEntity)
```

## Return Value

| Type | Description |
|----|----|
| [SketchEntity](SketchEntity.md)\[\] | Returns an array of the sketch entities that were created as a result of projection the specified curves onto the faces. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| faces | BRepFace[] | An array of BRepFace objects that the curves will be projected onto. |
| curves | Base[] | An array of various curve objects that will be projected onto the faces. The curves can be sketch curves and points, BRepEdge objects, ConstructionAxis objects, and ConstructionPoint objects. |
| projectType | [SurfaceProjectTypes](SurfaceProjectTypes.md) | Specifies which projection type to use which defines the direction of projection. If this is set to AlongVectorSurfaceProjectType the directionEntity argument must be provided. |
| directionEntity | [Base](Base.md) | if the projectType argument is AlongVectorSurfaceProjectType, this argument must be specified and defines the direction of projection. It can be a linear BRepEdge, a BRepFace where the normal will be used, a SketchLine, or a ConstructionLine. This is an optional argument whose default value is null. |

## Samples

| Name | Description |
|----|----|
| [Project To Surface API Sample](ProjectToSurface_Sample.md) | Projects the specified set of curves onto the specified set of faces using the specified method of projection. |

## Version

Introduced in version September 2017  


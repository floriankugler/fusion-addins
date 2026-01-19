# TemporaryBRepManager.imprintOverlapBodies Method

Parent Object: [TemporaryBRepManager](TemporaryBRepManager.md)  

## Description

Method that finds regions of faces on two bodies which overlap and creates new bodies where the faces are split at the edges of the overlaps. This does not modify the original bodies but creates new temporary bodies that contain the imprints.

## Remarks

The picture below shows an example of imprinting. The picture on the left shows the initial two bodies that are positioned so there are coincident faces. The picture on the right shows the two bodies individually so you can see the result of the imprint and how the coincident faces were split.  

The ability to imprint solids can be important to applications that need to mesh models. By creating edges at the points where solids connect, it guarantees that there will be mesh nodes along those boundaries.

## Syntax

"temporaryBRepManager_var" is a variable referencing a [TemporaryBRepManager](TemporaryBRepManager.md) object.  

```python
# Uses no optional arguments.
(returnValue, resultBodyOne, resultBodyTwo, bodyOneOverlappingFaces, bodyTwoOverlappingFaces, bodyOneOverlappingEdges, bodyTwoOverlappingEdges) = temporaryBRepManager_var.imprintOverlapBodies(bodyOne, bodyTwo, imprintCoincidentEdges)

# Uses optional arguments.
(returnValue, resultBodyOne, resultBodyTwo, bodyOneOverlappingFaces, bodyTwoOverlappingFaces, bodyOneOverlappingEdges, bodyTwoOverlappingEdges) = temporaryBRepManager_var.imprintOverlapBodies(bodyOne, bodyTwo, imprintCoincidentEdges, tolerance)
```

## Return Value

| Type    | Description                                             |
|---------|---------------------------------------------------------|
| boolean | Returns true if the imprint calculation was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| bodyOne | [BRepBody](BRepBody.md) | Input BRepBody that will participate in the imprint operation. This body can be either a parametric or temporary body. |
| bodyTwo | [BRepBody](BRepBody.md) | Input BRepBody that will participate in the imprint operation. This body can be either a parametric or temporary body. |
| imprintCoincidentEdges | boolean | Input Boolean that indicates if overlapping edges should be included in the result. The picture below shows an example of when this argument will make a difference. The two bodies have overlapping faces and there is also an overlapping edge. If this argument is true, then the edge shown in red below will be included in the output as an overlapping edge. If False it will not be included and only the edges of the overlapping faces will be in the overlapping faces collections. |
| resultBodyOne | [BRepBody](BRepBody.md) | Output temporary BRepBody that contains the imprinted body that corresponds to the body provided through the bodyOne argument. |
| resultBodyTwo | [BRepBody](BRepBody.md) | Output temporary BRepBody that contains the imprinted body that corresponds to the body provided through the bodyTwo argument. |
| bodyOneOverlappingFaces | BRepFace[] | Output array of BRepFace objects that represent the overlapping faces that are part of resultBodyOne. Faces at the same index within the collection returned here and that returned by the bodyTwoOverlappingFaces are overlapping. |
| bodyTwoOverlappingFaces | BRepFace[] | Output array of BRepFace objects that represent the overlapping faces that are part of resultBodyTwo. Faces at the same index within the collection returned here and that returned by the bodyOneOverlappingFaces are overlapping. |
| bodyOneOverlappingEdges | BRepEdge[] | Output array of BRepEdge objects that represent the overlapping edges that are part of resultBodyOne. Edges at the same index within the collection returned here and that returned by the bodyTwoOverlappingEdges are overlapping. |
| bodyTwoOverlappingEdges | BRepEdge[] | Output array of BRepEdge objects that represent the overlapping edges that are part of resultBodyTwo. Edges at the same index within the collection returned here and that returned by the bodyOneOverlappingEdges are overlapping. |
| tolerance | double | Optional Input double that specifies the tolerance, in centimeters, to use when comparing the bodies. If not specified, or a value of zero is specified, the internal modeling tolerance will be used. This is an optional argument whose default value is 0.0. |

## Samples

| Name | Description |
|----|----|
| [TemporaryBRepManager API Sample](TemporaryBRepManager_Sample.md) | TemporaryBRepManager related functions |

## Version

Introduced in version December 2017  


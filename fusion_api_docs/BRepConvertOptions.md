# BRepConvertOptions Enumerator

## Description

Defines the various options when converting the geometry of a B-Rep body or face to NURBS. This is used by the convert method of the BRepBody and BRepFace objects.  

## Methods

| Name | Value | Description |
|----|----|----|
| AnalyticsToNURBSConversion | 1 | Converts all analytic surfaces (cylinder, elliptical cylinder, cone, elliptical cone, sphere, and torus) except planes to NURBS surfaces. |
| PlanesToNURBSConversion | 2 | Converts all planar faces to NURBS surfaces. |
| ProceduralToNURBSConversion | 0 | Converts all procedurally calculated faces and edges into NURBS within the base tolerance. For example, an edge that is the intersection of two faces is represented as the exact analytical intersection of the two faces. This is converted into a NURBS curve as part of the conversion. |
| SplitPeriodicFacesConversion | 4 | Splits any periodic surfaces so they become open surfaces. |

## Version

Introduced in version August 2016  


# ChainedCurveOptions Enumerator

## Description

Controls options used when creating a Path and determining the rules for how curves are considered to be chained or connected.  

## Methods

| Name | Value | Description |
|----|----|----|
| connectedChainedCurves | 1 | Will find curves that are geometrically connected without regards to the geometry condition at the connection. This is limited to sketch curves. |
| noChainedCurves | 0 | No chaining is done. This is useful when inputting a single entity and you don't want any chaining to be done. |
| openEdgesChainedCurves | 3 | Will find edges that are geometrically end connected and are open edges of an open BRepBody. |
| tangentAndOpenEdgesChainedCurves | 4 | Will find edges that are geometrically end connected, are tangent at the connection, and are open edges of an open BRepBody. |
| tangentChainedCurves | 2 | Will find curves that are geometrically connected and tangent at the connection. This will work for both sketch curves and edges. |

## Version

Introduced in version August 2016  


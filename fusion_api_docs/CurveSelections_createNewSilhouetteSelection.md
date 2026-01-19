# CurveSelections.createNewSilhouetteSelection Method

Parent Object: [CurveSelections](CurveSelections.md)  

## Description

Creates a new silhouette selection and adds it to the end of the collection.

## Syntax

"curveSelections_var" is a variable referencing a [CurveSelections](CurveSelections.md) object.

```python
returnValue = curveSelections_var.createNewSilhouetteSelection()
```

## Return Value

| Type | Description |
|----|----|
| [SilhouetteSelection](SilhouetteSelection.md) | Returns newly created SilhouetteSelection. |

## Samples

| Name | Description |
| --- | --- |
| [Wood Routing Workflow Sample](WoodRoutingSample_Sample.md) | This script demonstrates routing wood panels. When running the sample, it assumes you have an open design containing one or more "panels" oriented flat in the X-Y plane. The script creates a setup and a 2D contour operation with tabs to route the panels from a standard sheet. |

## Version

Introduced in version April 2023  


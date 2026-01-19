# LoftSections.add Method

Parent Object: [LoftSections](LoftSections.md)  

## Description

Adds a new section to the loft. The initial end condition is "Free". Additional methods on the returned LoftSection can be used to further define the section.  

If this LoftSections object is associated with a created feature, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"loftSections_var" is a variable referencing a [LoftSections](LoftSections.md) object.

```python
returnValue = loftSections_var.add(entity)
```

## Return Value

| Type | Description |
|----|----|
| [LoftSection](LoftSection.md) | Returns the newly created LoftSection object. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entity | [Base](Base.md) | Specifies the BRepFace, Profile, Path, SketchPoint, ConstructionPoint, or an ObjectCollection containing a contiguous set of Profile objects that defines the section. |

## Samples

| Name | Description |
|----|----|
| [loftFeatures.add](loftFeatures_add_Sample.md) | Demonstrates the loftFeatures.add method. |
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |

## Version

Introduced in version August 2016  


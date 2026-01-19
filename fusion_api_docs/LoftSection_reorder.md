# LoftSection.reorder Method

Parent Object: [LoftSection](LoftSection.md)  

## Description

Repositions this section so that it has the new index specified.  

If this LoftSection object is associated with a created feature, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"loftSection_var" is a variable referencing a [LoftSection](LoftSection.md) object.

```python
returnValue = loftSection_var.reorder(newIndex)
```

## Return Value

| Type    | Description                                           |
|---------|-------------------------------------------------------|
| boolean | Returns true if the reorder operation was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| newIndex | integer | The new index value. For example, passing in zero as the new index will make this the first section in the loft and (LoftSections.count - 1) will make it the last section. All other sections will be maintain their existing order but be shifted to allow space for this section. |

## Version

Introduced in version August 2016  


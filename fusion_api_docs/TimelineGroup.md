# TimelineGroup Object

Derived from: [TimelineObject](TimelineObject.md) Object  

## Description

Represents a group in the timeline.

## Methods

| Name | Description |
| --- | --- |
| [canReorder](TimelineGroup_canReorder.md) | Checks to see if this object can be reordered to the specified position. The default value of -1 indicates the end of the timeline. This method will fail if this is a timelineGroup object and the group is expanded. |
| [classType](TimelineGroup_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](TimelineGroup_deleteMe.md) | Deletes the group with the option of deleting or keeping the contents. |
| [item](TimelineGroup_item.md) | Function that returns the specified timeline object within the group using an index into the collection. |
| [reorder](TimelineGroup_reorder.md) | Reorders this object to the position specified. The default value of -1 indicates the end of the timeline. |
| [rollTo](TimelineGroup_rollTo.md) | Rolls the timeline by repositioning the marker to either before or after this object. This method will fail if this is a timelineGroup object and the group is expanded. |

## Properties

| Name | Description |
| --- | --- |
| [count](TimelineGroup_count.md) | The number of items in the group. |
| [entity](TimelineGroup_entity.md) | Returns the entity associated with this timeline object. Edit operations can be performed by getting the object representing the associated entity and using the methods and properties on that entity to make changes. Returns null if this TimelineObject represents a TimelineGroup object, since it does not have an associated entity. |
| [errorOrWarningMessage](TimelineGroup_errorOrWarningMessage.md) | Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string. |
| [healthState](TimelineGroup_healthState.md) | Returns the current health state of the object associated with this TimelineObject. |
| [index](TimelineGroup_index.md) | Returns the position of this item within the timeline where the first item has an index of 0. This property can return -1 in the two cases where this object is not currently represented in the timeline. The two cases are: 1. When this is a TimelineGroup object and the group is expanded. 2. When this object is part of a group and the group is collapsed. |
| [isCollapsed](TimelineGroup_isCollapsed.md) | Indicates if the group is collapsed or expanded. |
| [isGroup](TimelineGroup_isGroup.md) | Indicates if this TimelineObject represents a group. If True you can operate on this object as a TimelineGroup object. |
| [isRolledBack](TimelineGroup_isRolledBack.md) | Indicates if this item is currently not being computed because it has been rolled back. If this is a timelineGroup object and the group is expanded the value of this property should be ignored. |
| [isSuppressed](TimelineGroup_isSuppressed.md) | Gets and sets if this object is suppressed. |
| [isValid](TimelineGroup_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](TimelineGroup_name.md) | Gets and sets the name of this timeline object. This name is shared by the object the timeline object represents. For example, if the TimelineObject represents a Sketch and you change the name using the TimelineObject, the name of the sketch in the browser is also changed. The reverse is also true. Setting the name of an object; sketch, feature construction geometry, etc, will also change the name of the associated node in the timeline. |
| [objectType](TimelineGroup_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentGroup](TimelineGroup_parentGroup.md) | Returns the parent group, if this object is part of a group. Returns null if this object is not part of a group. |

## Accessed From

[TimelineGroup.parentGroup](TimelineGroup_parentGroup.md), [TimelineGroups.add](TimelineGroups_add.md), [TimelineGroups.item](TimelineGroups_item.md), [TimelineObject.parentGroup](TimelineObject_parentGroup.md)

## Version

Introduced in version August 2014  


# Timeline Object

Derived from: [Base](Base.md) Object  

## Description

A collection of TimelineObjects in a parametric design.

## Methods

| Name | Description |
|----|----|
| [classType](Timeline_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteAllAfterMarker](Timeline_deleteAllAfterMarker.md) | Deletes all objects in the timeline that are after the current position of the marker. |
| [item](Timeline_item.md) | Function that returns the specified item in the timeline using an index into the collection. The items are returned in the order they appear in the timeline. |
| [moveToBeginning](Timeline_moveToBeginning.md) | Moves the marker to the beginning of the timeline. |
| [moveToEnd](Timeline_moveToEnd.md) | Moves the marker to the end of the timeline. |
| [movetoNextStep](Timeline_movetoNextStep.md) | Moves the marker to the next step in the timeline. |
| [moveToPreviousStep](Timeline_moveToPreviousStep.md) | Moves the marker to the previous step in the timeline. |
| [play](Timeline_play.md) | Plays the timeline beginning at the current position of the marker. |

## Properties

| Name | Description |
| --- | --- |
| [count](Timeline_count.md) | Returns the number of items in the collection. |
| [isValid](Timeline_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [markerPosition](Timeline_markerPosition.md) | Gets and sets the current position of the marker where 0 is at the beginning of the timeline and the value of Timeline.count is the end of the timeline. |
| [objectType](Timeline_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [timelineGroups](Timeline_timelineGroups.md) | Returns the collection of groups within the timeline. |

## Accessed From

[Design.timeline](Design_timeline.md), [FlatPatternProduct.timeline](FlatPatternProduct_timeline.md), [WorkingModel.timeline](WorkingModel_timeline.md)

## Samples

| Name | Description |  |
| --- | --- | --- |
| [Extrude Feature API Sample](ExtrudeFeatureSample_Sample.md) | Demonstrates creating a new extrude feature. |  |
| [Fillet Feature Edit API Sample](FilletFeatureEditSample_Sample.md) | Demonstrates editing a fillet feature. To successfully run this sample you can use this ../ExtraFiles/APISampleFilletEdgeSetData.f3d%3E%20file%3C/a%3E%20or%20create%20a%20new%20model%20with%20the%20described%20fillet%20feature.%3C/p%3E%0A%20%20%20%20%3Cp%3E%0A%20%20%20%20%3Col%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20new%20model%20and%20add%20a%20block%20feature.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20single%20fillet%20feature%20that%20defines%20three%20different%20fillets.%20The%20fillets%20need%20to%20be%20created%20in%20a%20way%20where%20they%20don't%20interact%20with%20one%20another.%20The%20easiest%20way%20is%20to%20create%20the%20fillets%20only%20on%20the%20vertical%20edges%20of%20the%20box.%0A%20%20%20%20%3Col%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20constant%20radius%20fillet%20with%20a%20radius%20that%20is%20about%201/4%20the%20size%20of%20the%20box.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20chord%20length%20fillet%20whose%20radius%20is%20also%20about%201/4%20the%20size%20of%20the%20box.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20variable%20radius%20fillet%20with%20one%20intermediate%20radius%20and%20the%20radii%20are%20about%201/4%20the%20size%20of%20the%20box%20and%20less.%3C/li%3E%0A%20%20%20%20%3C/ol%3E%0A%3C/ol%3E%0ARunning%20the%20sample%20script%20will%20modify%20various%20settings%20of%20each%20fillet%20and%20change%20the%20edge%20each%20fillet%20is%20applied%20to.%0A%20%20%20%20%3C/p%3E%3C/td%3E%0A%20%20%20%20%20%20%3C/tr%3E%0A%20%20%20%20%20%20%3Ctr%3E%0A%20%20%20%20%20%20%20%20%3Ctd%20class=[Ruled Surface Feature API Sample](RuledSurfaceFeatureSample_Sample.md) | Demonstrates creating a new ruled surface feature. |

## Version

Introduced in version August 2014  


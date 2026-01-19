# DataEvent.add Method

Parent Object: [DataEvent](DataEvent.md)  

## Description

Add a handler to be notified when the data event occurs.

## Syntax

"dataEvent_var" is a variable referencing a [DataEvent](DataEvent.md) object.

```python
returnValue = dataEvent_var.add(handler)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the addition of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [DataEventHandler](DataEventHandler.md) | The handler object to be called when this event is fired. |

## Samples

| Name | Description |
|----|----|
| [Save and Insert File API Sample](SaveAndInsertSample_Sample.md) | Demonstrates creating save a new file and then inserting it into a design. To use this sample, have a design open that has been saved and run the script. It will create a new design that contains a cylinder, save it to the same folder the active design was saved to, and then insert it into the active design. |

## Version

Introduced in version January 2022  


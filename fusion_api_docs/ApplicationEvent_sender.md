# ApplicationEvent.sender Property

Parent Object: [ApplicationEvent](ApplicationEvent.md)  

## Description

The object that is firing the event. For example, in the case of a command input event this will return the command.

## Syntax

"applicationEvent_var" is a variable referencing an ApplicationEvent object.  

```python
# Get the value of the property.
propertyValue = applicationEvent_var.sender
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version January 2016  


# HoleFeature.thread Property

Parent Object: [HoleFeature](HoleFeature.md)  

## Description

When a tapped hole is created, a thread feature is also automatically created and controls the tapped threads. The thread feature is tied to the hole and is not displayed in the timeline and is suppressed if the hole is suppressed and deleted if the hole is deleted. This property returns the thread feature associated with this hole if it is a tapped hole. It returns null for all other hole types.

## Syntax

"holeFeature_var" is a variable referencing a HoleFeature object.  

```python
# Get the value of the property.
propertyValue = holeFeature_var.thread
```

## Property Value

This is a read only property whose value is a [ThreadFeature](ThreadFeature.md).

## Version

Introduced in version September 2025  


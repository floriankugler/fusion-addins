# Occurrence.breakLink Method

Parent Object: [Occurrence](Occurrence.md)  

## Description

When the component this occurrence references is an external reference (the isReferencedComponent property returns true), this will break the link and create a local Component that this occurrence will reference. The new local Component can be accessed through the Occurrence using the component property.  

This method will fail if the occurrence is not referencing an external component.

## Syntax

"occurrence_var" is a variable referencing an [Occurrence](Occurrence.md) object.

```python
returnValue = occurrence_var.breakLink()
```

## Return Value

| Type    | Description                                    |
|---------|------------------------------------------------|
| boolean | Returns true if the break link was successful. |

## Samples

| Name | Description |
|----|----|
| [Break Link API Sample](BreakLink_Sample.md) | Iterates over all top-level occurrences and if it's a referenced component, it will break the link. |

## Version

Introduced in version September 2017  


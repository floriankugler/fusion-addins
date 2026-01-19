# AssemblyConstraints.add Method

Parent Object: [AssemblyConstraints](AssemblyConstraints.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a new assembly constraint.

## Syntax

"assemblyConstraints_var" is a variable referencing an [AssemblyConstraints](AssemblyConstraints.md) object.

```python
returnValue = assemblyConstraints_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [AssemblyConstraint](AssemblyConstraint.md) | Returns the newly created AssemblyConstraint or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [AssemblyConstraintInput](AssemblyConstraintInput.md) | The AssemblyConstraintInput object that defines the geometry and various inputs that define an assembly constraint. An AssemblyConstraintInput object is created using the AssemblyConstraints.createInput method. |

## Version

Introduced in version July 2025  


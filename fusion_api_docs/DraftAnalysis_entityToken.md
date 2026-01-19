# DraftAnalysis.entityToken Property

Parent Object: [DraftAnalysis](DraftAnalysis.md)  

## Description

Returns a token for the Analysis object. The token can be saved and used later with the Design.findEntityByToken method to get back the same Analysis.  

When using entity tokens, it's crucial to understand that the token string returned for a specific entity can be different over time. For example, you can have two different token strings obtained from the same entity at different times, and when you use findEntityByToken they will both return the same entity. Because of that, you should never compare entity tokens as a way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them.

## Syntax

"draftAnalysis_var" is a variable referencing a DraftAnalysis object.  

```python
# Get the value of the property.
propertyValue = draftAnalysis_var.entityToken
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version January 2023  


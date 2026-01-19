# ChordLengthFilletEdgeSetInput.chordLength Property

Parent Object: [ChordLengthFilletEdgeSetInput](ChordLengthFilletEdgeSetInput.md)  

## Description

Gets and sets a ValueInput object that defines the chord length of the fillet. If the ValueInput uses a real value then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current document units for length.

## Syntax

"chordLengthFilletEdgeSetInput_var" is a variable referencing a ChordLengthFilletEdgeSetInput object.  

```python
# Get the value of the property.
propertyValue = chordLengthFilletEdgeSetInput_var.chordLength

# Set the value of the property.
chordLengthFilletEdgeSetInput_var.chordLength = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version November 2022  


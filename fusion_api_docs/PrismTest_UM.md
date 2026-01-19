#### Test of the Prism Javascript Library

This page is to get the integration of the [Prism Javasript Library](https://prismjs.com/) in the Fusion help system.

Below is some sample code that should have line numbers and support copying the code.

```python
# Get the current position of the timeline marker.
currentPstn = design.timeline.markerPosition

# Reposition the timeline marker to just before the Arrange feature.
arrangeFeature.timelineObject.rollTo(True)

# Make the desired changes to the Arrange feature.
arrangeFeature.definition.grainDirection.value = math.radians(10)
arrangeFeature.envelopeDefinition.frameWidth.value = 0.5
arrangeFeature.envelopeDefinition.isPartialArrangeAllowed = True

# Reposition the timeline marker to its original position.
design.timeline.markerPosition = currentPstn
```

## Uses the css below.

To allow this to work, the following was added to APIHelp.css to make the line numbers and the code the same size so they line up.

And, the following is added below the

element.


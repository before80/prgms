# Making fine adjustments to a view’s position

Shift the position of a view by applying the offset or position modifier.

## Overview {#Overview}

Use SwiftUI to adaptively lay out and position your views. If you can’t achieve your design with composition alone, fine tune the layout with view modifiers. Add an offset modifier to shift the rendered content of a view from its current position, or a position modifier to set an explicit position within its parent.

### Create a view layout {#Create-a-view-layout}

The following example provides a view to illustrate how to position views, providing a rough layout of views composed within a [ZStack](https://developer.apple.com/documentation/swiftui/zstack). The stack contains a quadrant with an overlaid circle image:

```swift
struct Crosshairs: View { ... } // Draws crosshairs.

struct Quadrant: View {
    var body: some View {
        ZStack {
            Crosshairs()
            Rectangle()
                .stroke(Color.primary)
            Image(systemName: "circle")
        }
        .frame(width: 160, height: 160)
    }
}
```

![A figure of a square with hair-line crosshairs that divide the box into four equal sections. A small circle is at the apex of the crosshairs.](./images/Making-Fine-Adjustments-to-a-View-s-Position-1@2x.png)

For more detail on composing views with stacks, see [Building layouts with stack views](../../1-LayoutFundamentals/1.2-BuildingLayoutsWithStackViews/).

### Shift the location of a view’s content {#Shift-the-location-of-a-views-content}

Fine-tune the position of the circle within the quadrant by using an offset modifier to shift where the parent view places the circle. An offset modifier shifts the image from its default center position. For example, the [offset(x:y:)](https://developer.apple.com/documentation/swiftui/view/offset(x:y:)) modifier uses the parameters of `x` and `y` to represent a relative location within the view’s coordinate space.

In SwiftUI, the view’s coordinate space uses `x` to represent a horizontal direction and `y` to represent a vertical direction. The value of `x` starts at `0` at the leading edge of a view, and increases as the location moves toward the trailing edge of a view. The value of `y` starts at `0` at the top edge of a view, and increases as the location moves toward the bottom edge of a view. Don’t assume the leading edge is always on the left, because it changes with the layout direction. When the layout direction is set to right-to-left, the `0` horizontal value is on the right side of the view.

The following diagram shows the coordinates in the left-to-right layout direction against a rectangle, with the origin at the top, leading corner:

![A drawing of an opaque box that represents a coordinate rectangle. The left, bottom corner of the rectangle is labeled leading and the right, bottom corner is labeled trailing. The bottom of the rectangle is labeled x for the x coordinate. The left top of the rectangle is labeled top, and the left bottom is labeled bottom. The right side of the rectangle is labeled y to represent the y coordinate.](./images/Making-Fine-Adjustments-to-a-View-s-Position-2@2x.png)

The following example shifts the circle `40` points from the center, up and toward the trailing edge:

```swift
struct Quadrant: View {
    var body: some View {
        ZStack {
            Crosshairs()
            Rectangle()
                .stroke(Color.primary)
            Image(systemName: "circle")
                .offset(x: 40.0, y: -40.0)
        }
        .frame(width: 160, height: 160)
    }
}
```

![A figure of a square with hairline crosshairs that divide the box into four equal sections. A small circle is offset from the apex of the crosshairs, 40 points up and 40 points toward the trailing edge of the box.](./images/Making-Fine-Adjustments-to-a-View-s-Position-3@2x.png)

### Position view content explicitly {#Position-view-content-explicitly}

To explicitly position elements within a view, use the [position(x:y:)](https://developer.apple.com/documentation/swiftui/view/position(x:y:)) view modifier. A position modifier overrides where the parent view places its content. The modifier renders the view at a location offset from the origin of the parent view, unlike an offset modifier that shifts the view from the location chosen by the parent view. The position modifier uses the same `x`, `y` coordinate system as the offset modifier, and similarly doesn’t influence the size of the view. In this example, the position of the circle is set halfway down on the right side of the quadrant with explicit values:

```swift
struct Quadrant: View {
    var body: some View {
        ZStack {
            Crosshairs()
            Rectangle()
                .stroke(Color.primary)
            Image(systemName: "circle")
                .position(x: 144, y: 80)
        }
        .frame(width: 160, height: 160)
    }
}
```

![A figure of a square with hairline crosshairs that divide the box into four equal sections. A small circle is positioned to the right of the apex of the crosshairs, 80 points down from the top of the box and 144 points toward the trailing edge, measured from the origin coordinates of the square’s view.](./images/Making-Fine-Adjustments-to-a-View-s-Position-4@2x.png)

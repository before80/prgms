# Laying out a simple view

Create a view layout by adjusting the size of views.

## Overview {#Overview}

To create a layout for a view, start by composing a hierarchy of child views. Then, refine the size and spacing of the child views with configuration parameters, and by adding view modifiers, like those that affect a view’s frame and padding. To review how to compose layouts, see [Building layouts with stack views](../../1-LayoutFundamentals/1.2-BuildingLayoutsWithStackViews/).

### Establish a view hierarchy {#Establish-a-view-hierarchy}

The following example creates a view to display an incoming message from a messaging service. The view uses an [HStack](https://developer.apple.com/documentation/swiftui/hstack) to collect a view that identifies the sender and another that provides the content of the message:

```swift
struct MessageRow: View {
    let message: Message

    var body: some View {
        HStack {
            ZStack {
                Circle()
                    .fill(Color.yellow)
                Text(message.initials)
            }

            Text(message.content)
        }
    }
}
```

The following screenshot of a `MessageRow` view includes a border that shows its bounds. Note the large size of the circle, which fills the space available to it:

![A screenshot showing a black rectangle as the border of the view, inside of which is a large yellow circle on the left side of the view, with the letters “MR” in the center of the circle. On the right side of the view there are five lines of text. The text and circle are centered vertically in the view.](./images/Laying-Out-a-Simple-View-1@2x.png)

When SwiftUI renders a view hierarchy, it recursively evaluates each child view: The parent view proposes a size to the child views it contains, and the child views respond with a computed size.

![A vertically stacked view hierarchy shown as boxes, which each list names of views. The top box is labeled MessageRow, connected with a straight line to an HStack box, just below it. The HStack connects by a straight line to three views beneath it, labeled ZStack, Spacer, and Text. The ZStack has two views connected by straight line under it, labeled Circle and Text. Circle has a single view connected beneath it, labeled fill. Dashed arrows on the left of the hierarchy indicate the flow of requests for size for the circle, starting with MessageRow. The flow proceeds down to HStack, ZStack, and Circle. Solid arrows on the right of the hierarchy represent answers being returned, starting at the Circle, then moving back toward the top of the image, to ZStack, HStack, and MessageRow.](./images/Laying-Out-a-Simple-View-2@2x.png)

The `MessageRow` view proposes a size to its only child, the [HStack](https://developer.apple.com/documentation/swiftui/hstack), which is the full size proposed to it by its own parent. The stack proportionally divides this space between its child views, with system-default spacing between each child. This continues recursively:

- The [ZStack](https://developer.apple.com/documentation/swiftui/zstack) proposes a size to its child views, the [Circle](https://developer.apple.com/documentation/swiftui/circle) and [Text](https://developer.apple.com/documentation/swiftui/text) views.
- The [Circle](https://developer.apple.com/documentation/swiftui/circle) expands up to the size offered, while the [Text](https://developer.apple.com/documentation/swiftui/text) takes just enough space for the string it contains.
- The [ZStack](https://developer.apple.com/documentation/swiftui/zstack) returns the size of its largest child view, in this case the [Circle](https://developer.apple.com/documentation/swiftui/circle).

When all child views have reported their size, the parent view renders them.

### Limit the view size {#Limit-the-view-size}

In the example above, SwiftUI has built-in views that manage size in different ways, including views that:

- Expand to fill the space offered by their parent, like [Color](https://developer.apple.com/documentation/swiftui/color), [LinearGradient](https://developer.apple.com/documentation/swiftui/lineargradient), and [Circle](https://developer.apple.com/documentation/swiftui/circle).
- Have an ideal size that varies according to their contents, like [Text](https://developer.apple.com/documentation/swiftui/text) and the container views.
- Have an ideal size that never varies, like [Toggle](https://developer.apple.com/documentation/swiftui/toggle) or [DatePicker](https://developer.apple.com/documentation/swiftui/datepicker).

You can constrain a view to a fixed size by adding a frame modifier. For example, use the [frame(width:height:alignment:)](https://developer.apple.com/documentation/swiftui/view/frame(width:height:alignment:)) modifier to limit the width the circle to `40` points:

```swift
struct MessageRow: View {
    let message: Message

    var body: some View {
        HStack {
            ZStack {
                Circle()
                    .fill(Color.yellow)
                Text(message.initials)
            }
            .frame(width: 40)

            Text(message.content)
        }
    }
}
```

When you add a frame modifier, SwiftUI wraps the affected view, effectively adding a new view to the view hierarchy.

![A view hierarchy shown as boxes, in which are names of views. The top most box is labeled MessageRow, connected with a line to an HStack, just beneath it. The HStack connects to three view beneath it, boxes labeled frame, Spacer, and Text. Frame connects to a single view beneath it: ZStack. The ZStack has two views connected under it: box labeled Circle, and another labeled Text. The Circle has a single view connected beneath it, labeled fill. The view labeled frame is highlighted to indiciate that it was added compared to the previous view hierarchy example. Dashed arrows on the left of the hierarchy indicate the flow of requests for size for the circle, starting with HStack. The flow proceeds down to frame, ZStack, and then to Circle. Solid arrows on the right of the hierarchy represent answers being returned, starting at the Circle, then to ZStack, frame, and HStack.](./images/Laying-Out-a-Simple-View-3@2x.png)

When SwiftUI evaluates this new hierarchy, the frame modifier fixes the width of the [ZStack](https://developer.apple.com/documentation/swiftui/zstack) that it wraps by passing along the value you specified as its parameter. The remainder of the size evaluation proceeds as before, where the [Circle](https://developer.apple.com/documentation/swiftui/circle) now expands to fill a smaller space, constrained by the frame’s 40 point width. This enables the [HStack](https://developer.apple.com/documentation/swiftui/hstack) to provide more space to its other child, which displays the message text.

![A figure of a black rectangle as the border of a view, inside which is a small yellow circle on the left side, constrained to 40 points in diameter, with the letters “MR” at the center of the circle. On the right side are three lines of text. The text and circle are centered vertically.](./images/Laying-Out-a-Simple-View-4@2x.png)

### Position content with alignment {#Position-content-with-alignment}

If you want the top of the circle aligned with the top of the message content text, you can refine the view by applying an alignment to the [HStack](https://developer.apple.com/documentation/swiftui/hstack). To position the content vertically within the stack, specify the `alignment` parameter to [top](https://developer.apple.com/documentation/swiftui/verticalalignment/top):

```swift
struct MessageRow: View {
    let message: Message

    var body: some View {
        HStack(alignment: .top) {
            ZStack {
                Circle()
                    .fill(Color.yellow)
                Text(message.initials)
            }
            .frame(width: 40)

            Text(message.content)
        }
    }
}
```

With the alignment applied, you get an unexpected result. The tops of the views don’t appear to align:

![A figure of a black rectangle as the border of a view, inside which is a small yellow circle on the left side, constrained to 40 points in diameter, with the letters “MR” at the center of the circle. On the right side are three lines of text. The circle is centered vertically, while the text is aligned at the top of the view.](./images/Laying-Out-a-Simple-View-5@2x.png)

However, if you select the circle in Xcode, or temporarily add a border to the circle, you can see the tops of the views do in fact align. For more information on inspecting the size of a view, see [Inspecting view layout](../2.2-InspectingViewLayout/).

![A figure of a black rectangle as the border of a view, inside which is a small yellow circle on the left side, constrained to 40 points in diameter, with the letters “MR” at the center of the circle. On the right side are three lines of text. The circle appears to be centered vertically, while the text is aligned at the top of the view. A figure of a blue box shows the border of the view enclosing the circle, which takes the full height of its parent view.](./images/Laying-Out-a-Simple-View-6@2x.png)

In the previous section, you applied a frame with only a width constraint. SwiftUI drew a circle limited by that width. But because the height was left unspecified, the circle’s frame separately expanded to fill the available height, even though that extra space had no visible impact on the rendered circle. You can resolve this problem by adding an explicit `height` parameter:

```swift
struct MessageRow: View {
    let message: Message

    var body: some View {
        HStack(alignment: .top) {
            ZStack {
                Circle()
                    .fill(Color.yellow)
                Text(message.initials)
            }
            .frame(width: 40, height: 40)

            Text(message.content)
        }
    }
}
```

The contents of the [HStack](https://developer.apple.com/documentation/swiftui/hstack) are now top aligned, although the stack itself is centered in the `MessageRow` view as shown by the border displaying the row’s boundaries.

![A black rectangle shows the border of the view, inside which is a small yellow circle on the left, constrained to 40 points in diameter, with the letters “MR” at the center of the circle. On the right are three lines of text. The top of the circle is aligned with the top of the lines of text. The view shows extra space above and below the circle and text, but none to the left or right. The circle and text press against the left and right edges of the border of the view.](./images/Laying-Out-a-Simple-View-7@2x.png)

### Add padding to the view {#Add-padding-to-the-view}

To avoid visually crowding the outer edges of a view, add padding. This introduces a fixed amount of space along the specified edges, reducing the space available for the contents of the view by a corresponding amount. For example, you can use [padding(_:_:)](https://developer.apple.com/documentation/swiftui/view/padding(_:_:)) to add extra space along the [horizontal](https://developer.apple.com/documentation/swiftui/edge/set/horizontal) edges of the [HStack](https://developer.apple.com/documentation/swiftui/hstack):

```swift
struct MessageRow: View {
    let message: Message

    var body: some View {
        HStack(alignment: .top) {
            ZStack {
                Circle()
                    .fill(Color.yellow)
                Text(message.initials)
            }
            .frame(width: 40, height: 40)

            Text(message.content)
        }
        .padding([.horizontal])
    }
}
```

The padding modifier defaults to system-standard spacing, although you can alternatively choose different values for the padding modifier. ![A black rectangle shows the border of the view, inside which is a small yellow circle on the left, constrained to 40 points in diameter, with the letters “MR” at the center of the circle. On the right are three lines of text. The top of the circle is aligned with the top of the lines of text. The view shows extra space above and below the circle and text, and padding to the left and right of the circle and text, respectively.](./images/Laying-Out-a-Simple-View-8@2x.png)

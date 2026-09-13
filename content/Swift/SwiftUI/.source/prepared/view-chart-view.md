# Chart view modifiers

Configure charts that you declare with Swift Charts.

## Overview {#Overview}

Use these modifiers to configure a [Chart](https://developer.apple.com/documentation/charts/chart) view that you add to your SwiftUI app.

## Styles {#Styles}

- [chartBackground(alignment:content:)](https://developer.apple.com/documentation/swiftui/view/chartbackground(alignment:content:)) — Adds a background to a view that contains a chart.
- [chartForegroundStyleScale(_:)](https://developer.apple.com/documentation/swiftui/view/chartforegroundstylescale(_:)) — Configures the foreground style scale for charts.
- [chartForegroundStyleScale(domain:range:type:)](https://developer.apple.com/documentation/swiftui/view/chartforegroundstylescale(domain:range:type:)) — Configures the foreground style scale for charts.
- [chartForegroundStyleScale(domain:type:)](https://developer.apple.com/documentation/swiftui/view/chartforegroundstylescale(domain:type:)) — Configures the foreground style scale for charts.
- [chartForegroundStyleScale(domain:mapping:)](https://developer.apple.com/documentation/swiftui/view/chartforegroundstylescale(domain:mapping:)) — Configures the foreground style scale for charts.
- [chartForegroundStyleScale(mapping:)](https://developer.apple.com/documentation/swiftui/view/chartforegroundstylescale(mapping:)) — Configures the foreground style scale for charts.
- [chartForegroundStyleScale(range:type:)](https://developer.apple.com/documentation/swiftui/view/chartforegroundstylescale(range:type:)) — Configures the foreground style scale for charts.
- [chartForegroundStyleScale(type:)](https://developer.apple.com/documentation/swiftui/view/chartforegroundstylescale(type:)) — Configures the foreground style scale for charts.
- [chartPlotStyle(content:)](https://developer.apple.com/documentation/swiftui/view/chartplotstyle(content:)) — Configures the plot area of charts.

## 3D configuration {#3D-configuration}

- [chart3DCameraProjection(_:)](https://developer.apple.com/documentation/swiftui/view/chart3dcameraprojection(_:))
- [chart3DPose(_:)](https://developer.apple.com/documentation/swiftui/view/chart3dpose(_:)) — Associates a binding to be updated when the 3D chart’s pose is changed by an interaction.
- [chart3DRenderingStyle(_:)](https://developer.apple.com/documentation/swiftui/view/chart3drenderingstyle(_:))

## Legends {#Legends}

- [chartLegend(_:)](https://developer.apple.com/documentation/swiftui/view/chartlegend(_:)) — Configures the legend for charts.
- [chartLegend(position:alignment:spacing:)](https://developer.apple.com/documentation/swiftui/view/chartlegend(position:alignment:spacing:)) — Configures the legend for charts.
- [chartLegend(position:alignment:spacing:content:)](https://developer.apple.com/documentation/swiftui/view/chartlegend(position:alignment:spacing:content:)) — Configures the legend for charts.

## Overlays {#Overlays}

- [chartOverlay(alignment:content:)](https://developer.apple.com/documentation/swiftui/view/chartoverlay(alignment:content:)) — Adds an overlay to a view that contains a chart.

## Axes {#Axes}

- [chartXAxis(_:)](https://developer.apple.com/documentation/swiftui/view/chartxaxis(_:)) — Sets the visibility of the x axis.
- [chartXAxis(content:)](https://developer.apple.com/documentation/swiftui/view/chartxaxis(content:)) — Configures the x-axis for charts in the view.
- [chartXAxisStyle(content:)](https://developer.apple.com/documentation/swiftui/view/chartxaxisstyle(content:)) — Configures the x axis content of charts.
- [chartYAxis(_:)](https://developer.apple.com/documentation/swiftui/view/chartyaxis(_:)) — Sets the visibility of the y axis.
- [chartYAxis(content:)](https://developer.apple.com/documentation/swiftui/view/chartyaxis(content:)) — Configures the y-axis for charts in the view.
- [chartYAxisStyle(content:)](https://developer.apple.com/documentation/swiftui/view/chartyaxisstyle(content:)) — Configures the y axis content of charts.
- [chartZAxis(_:)](https://developer.apple.com/documentation/swiftui/view/chartzaxis(_:)) — Sets the visibility of the z axis.
- [chartZAxis(content:)](https://developer.apple.com/documentation/swiftui/view/chartzaxis(content:)) — Configures the z-axis for 3D charts in the view.

## Axis Labels {#Axis-Labels}

- [chartXAxisLabel(_:position:alignment:spacing:)](https://developer.apple.com/documentation/swiftui/view/chartxaxislabel(_:position:alignment:spacing:)) — Adds x axis label for charts in the view.
- [chartXAxisLabel(position:alignment:spacing:content:)](https://developer.apple.com/documentation/swiftui/view/chartxaxislabel(position:alignment:spacing:content:)) — Adds x axis label for charts in the view.
- [chartYAxisLabel(_:position:alignment:spacing:)](https://developer.apple.com/documentation/swiftui/view/chartyaxislabel(_:position:alignment:spacing:)) — Adds y axis label for charts in the view.
- [chartYAxisLabel(position:alignment:spacing:content:)](https://developer.apple.com/documentation/swiftui/view/chartyaxislabel(position:alignment:spacing:content:)) — Adds y axis label for charts in the view.
- [chartZAxisLabel(_:position:alignment:spacing:)](https://developer.apple.com/documentation/swiftui/view/chartzaxislabel(_:position:alignment:spacing:)) — Adds z axis label for charts in the view. It effects 3D charts only.

## Axis scales {#Axis-scales}

- [chartXScale(domain:range:type:)](https://developer.apple.com/documentation/swiftui/view/chartxscale(domain:range:type:)) — Configures the x scale for charts.
- [chartXScale(domain:type:)](https://developer.apple.com/documentation/swiftui/view/chartxscale(domain:type:)) — Configures the x scale for charts.
- [chartXScale(range:type:)](https://developer.apple.com/documentation/swiftui/view/chartxscale(range:type:)) — Configures the x scale for charts.
- [chartXScale(type:)](https://developer.apple.com/documentation/swiftui/view/chartxscale(type:)) — Configures the x scale for charts.
- [chartYScale(domain:range:type:)](https://developer.apple.com/documentation/swiftui/view/chartyscale(domain:range:type:)) — Configures the y scale for charts.
- [chartYScale(domain:type:)](https://developer.apple.com/documentation/swiftui/view/chartyscale(domain:type:)) — Configures the y scale for charts.
- [chartYScale(range:type:)](https://developer.apple.com/documentation/swiftui/view/chartyscale(range:type:)) — Configures the y scale for charts.
- [chartYScale(type:)](https://developer.apple.com/documentation/swiftui/view/chartyscale(type:)) — Configures the y scale for charts.
- [chartZScale(domain:range:type:)](https://developer.apple.com/documentation/swiftui/view/chartzscale(domain:range:type:)) — Configures the z scale for 3D charts.
- [chartZScale(domain:type:)](https://developer.apple.com/documentation/swiftui/view/chartzscale(domain:type:)) — Configures the z scale for 3D charts.
- [chartZScale(range:type:)](https://developer.apple.com/documentation/swiftui/view/chartzscale(range:type:)) — Configures the z scale for 3D charts.

## Symbol scales {#Symbol-scales}

- [chartSymbolScale(_:)](https://developer.apple.com/documentation/swiftui/view/chartsymbolscale(_:)) — Configures the symbol scale for charts.
- [chartSymbolScale(domain:)](https://developer.apple.com/documentation/swiftui/view/chartsymbolscale(domain:)) — Configures the symbol style scale for charts.
- [chartSymbolScale(domain:range:)](https://developer.apple.com/documentation/swiftui/view/chartsymbolscale(domain:range:)) — Configures the symbol style scale for charts.
- [chartSymbolScale(domain:mapping:)](https://developer.apple.com/documentation/swiftui/view/chartsymbolscale(domain:mapping:)) — Configures the symbol scale for charts.
- [chartSymbolScale(mapping:)](https://developer.apple.com/documentation/swiftui/view/chartsymbolscale(mapping:)) — Configures the symbol scale for charts.
- [chartSymbolScale(range:)](https://developer.apple.com/documentation/swiftui/view/chartsymbolscale(range:)) — Configures the symbol style scale for charts.

## Symbol size scales {#Symbol-size-scales}

- [chartSymbolSizeScale(_:)](https://developer.apple.com/documentation/swiftui/view/chartsymbolsizescale(_:)) — Configures the symbol size scale for charts.
- [chartSymbolSizeScale(domain:range:type:)](https://developer.apple.com/documentation/swiftui/view/chartsymbolsizescale(domain:range:type:)) — Configures the symbol size scale for charts.
- [chartSymbolSizeScale(domain:type:)](https://developer.apple.com/documentation/swiftui/view/chartsymbolsizescale(domain:type:)) — Configures the symbol size scale for charts.
- [chartSymbolSizeScale(domain:mapping:)](https://developer.apple.com/documentation/swiftui/view/chartsymbolsizescale(domain:mapping:)) — Configures the symbol size scale for charts.
- [chartSymbolSizeScale(mapping:)](https://developer.apple.com/documentation/swiftui/view/chartsymbolsizescale(mapping:)) — Configures the symbol size scale for charts.
- [chartSymbolSizeScale(range:type:)](https://developer.apple.com/documentation/swiftui/view/chartsymbolsizescale(range:type:)) — Configures the symbol size scale for charts.
- [chartSymbolSizeScale(type:)](https://developer.apple.com/documentation/swiftui/view/chartsymbolsizescale(type:)) — Configures the symbol size scale for charts.

## Line style scales {#Line-style-scales}

- [chartLineStyleScale(_:)](https://developer.apple.com/documentation/swiftui/view/chartlinestylescale(_:)) — Configures the line style scale for charts.
- [chartLineStyleScale(domain:)](https://developer.apple.com/documentation/swiftui/view/chartlinestylescale(domain:)) — Configures the line style scale for charts.
- [chartLineStyleScale(domain:range:)](https://developer.apple.com/documentation/swiftui/view/chartlinestylescale(domain:range:)) — Configures the line style scale for charts.
- [chartLineStyleScale(range:)](https://developer.apple.com/documentation/swiftui/view/chartlinestylescale(range:)) — Configures the line style scale for charts.
- [chartLineStyleScale(domain:mapping:)](https://developer.apple.com/documentation/swiftui/view/chartlinestylescale(domain:mapping:)) — Configures the line style scale for charts.
- [chartLineStyleScale(mapping:)](https://developer.apple.com/documentation/swiftui/view/chartlinestylescale(mapping:)) — Configures the line style scale for charts.

## Scrolling {#Scrolling}

- [chartScrollPosition(initialX:)](https://developer.apple.com/documentation/swiftui/view/chartscrollposition(initialx:)) — Sets the initial scroll position along the x-axis. Once the user scrolls the scroll view, the value provided to this modifier will have no effect.
- [chartScrollPosition(initialY:)](https://developer.apple.com/documentation/swiftui/view/chartscrollposition(initialy:)) — Sets the initial scroll position along the y-axis. Once the user scrolls the scroll view, the value provided to this modifier will have no effect.
- [chartScrollPosition(x:)](https://developer.apple.com/documentation/swiftui/view/chartscrollposition(x:)) — Associates a binding to be updated when the chart scrolls along the x-axis.
- [chartScrollPosition(y:)](https://developer.apple.com/documentation/swiftui/view/chartscrollposition(y:)) — Associates a binding to be updated when the chart scrolls along the y-axis.
- [chartScrollTargetBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/chartscrolltargetbehavior(_:)) — Sets the scroll behavior of the scrollable chart.
- [chartScrollableAxes(_:)](https://developer.apple.com/documentation/swiftui/view/chartscrollableaxes(_:)) — Configures the scrollable behavior of charts in this view.

## Selection {#Selection}

- [chartXSelection(range:)](https://developer.apple.com/documentation/swiftui/view/chartxselection(range:))
- [chartXSelection(value:)](https://developer.apple.com/documentation/swiftui/view/chartxselection(value:))
- [chartYSelection(range:)](https://developer.apple.com/documentation/swiftui/view/chartyselection(range:))
- [chartYSelection(value:)](https://developer.apple.com/documentation/swiftui/view/chartyselection(value:))
- [chartZSelection(range:)](https://developer.apple.com/documentation/swiftui/view/chartzselection(range:))
- [chartZSelection(value:)](https://developer.apple.com/documentation/swiftui/view/chartzselection(value:))
- [chartAngleSelection(value:)](https://developer.apple.com/documentation/swiftui/view/chartangleselection(value:))

## Visible domain {#Visible-domain}

- [chartXVisibleDomain(length:)](https://developer.apple.com/documentation/swiftui/view/chartxvisibledomain(length:)) — Sets the length of the visible domain in the X dimension.
- [chartYVisibleDomain(length:)](https://developer.apple.com/documentation/swiftui/view/chartyvisibledomain(length:)) — Sets the length of the visible domain in the Y dimension.

## Interaction {#Interaction}

- [chartGesture(_:)](https://developer.apple.com/documentation/swiftui/view/chartgesture(_:))

import AppKit

let root = URL(fileURLWithPath: CommandLine.arguments[1])
let width = 1200
let height = 630
let output = root.appendingPathComponent("dist/assets/brand/cor-og-preview.jpg")
let screenshotURL = root.appendingPathComponent("dist/assets/product/home.png")
guard let screenshot = NSImage(contentsOf: screenshotURL) else {
    fatalError("Missing native app screenshot: \(screenshotURL.path)")
}

let bitmap = NSBitmapImageRep(
    bitmapDataPlanes: nil,
    pixelsWide: width,
    pixelsHigh: height,
    bitsPerSample: 8,
    samplesPerPixel: 4,
    hasAlpha: true,
    isPlanar: false,
    colorSpaceName: .deviceRGB,
    bytesPerRow: 0,
    bitsPerPixel: 0
)!
let context = NSGraphicsContext(bitmapImageRep: bitmap)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = context
context.imageInterpolation = .high

NSColor(calibratedWhite: 0.015, alpha: 1).setFill()
NSBezierPath(rect: NSRect(x: 0, y: 0, width: width, height: height)).fill()

let glow = NSGradient(colors: [
    NSColor(calibratedRed: 0.20, green: 0.31, blue: 0.39, alpha: 0.36),
    NSColor(calibratedRed: 0.20, green: 0.31, blue: 0.39, alpha: 0.00)
])!
glow.draw(in: NSRect(x: 570, y: 30, width: 600, height: 570), relativeCenterPosition: NSPoint(x: 0.2, y: 0.1))

func drawText(_ text: String, at point: NSPoint, font: NSFont, color: NSColor, tracking: CGFloat = 0) {
    let paragraph = NSMutableParagraphStyle()
    paragraph.lineBreakMode = .byWordWrapping
    let attributed = NSAttributedString(string: text, attributes: [
        .font: font,
        .foregroundColor: color,
        .paragraphStyle: paragraph,
        .kern: tracking
    ])
    attributed.draw(at: point)
}

let ivory = NSColor(calibratedRed: 0.96, green: 0.95, blue: 0.92, alpha: 1)
let muted = NSColor(calibratedRed: 0.76, green: 0.79, blue: 0.79, alpha: 1)
drawText("COR ACTIVE  ·  COMING SOON", at: NSPoint(x: 74, y: 526),
         font: .systemFont(ofSize: 15, weight: .semibold), color: muted, tracking: 2.2)
drawText("Track the work.\nSee the payoff.", at: NSPoint(x: 70, y: 324),
         font: NSFont(name: "Georgia", size: 62)!, color: ivory)
drawText("Meals, weight, sets, reps, and body fat —\nplus calories, ingredients, and a score\nthat shows the math.",
         at: NSPoint(x: 74, y: 191), font: .systemFont(ofSize: 21, weight: .regular), color: muted)

let pill = NSBezierPath(roundedRect: NSRect(x: 74, y: 100, width: 190, height: 42), xRadius: 21, yRadius: 21)
NSColor(calibratedRed: 0.94, green: 0.93, blue: 0.89, alpha: 1).setFill()
pill.fill()
drawText("Coming soon", at: NSPoint(x: 94, y: 113), font: .systemFont(ofSize: 16, weight: .semibold), color: NSColor.black)

// Frame native COR content with Apple's original, upright device artwork.
let deviceURL = root.appendingPathComponent("dist/assets/brand/iphone-18-pro-max-glacier-apple.png")
guard let device = NSImage(contentsOf: deviceURL) else {
    fatalError("Missing official Apple device artwork: \(deviceURL.path)")
}
let scale: CGFloat = 554.0 / 3000.0
let frameRect = NSRect(x: 832, y: 38, width: 1470 * scale, height: 554)
let screenRect = NSRect(x: frameRect.minX + 75 * scale, y: frameRect.minY + 66 * scale,
                        width: 1320 * scale, height: 2868 * scale)
NSGraphicsContext.saveGraphicsState()
NSBezierPath(roundedRect: screenRect, xRadius: 250 * scale, yRadius: 250 * scale).addClip()
let fit = min(screenRect.width / screenshot.size.width, screenRect.height / screenshot.size.height)
let imageRect = NSRect(x: screenRect.midX - screenshot.size.width * fit / 2,
                       y: screenRect.midY - screenshot.size.height * fit / 2,
                       width: screenshot.size.width * fit, height: screenshot.size.height * fit)
screenshot.draw(in: imageRect, from: .zero, operation: .sourceOver, fraction: 1)
NSGraphicsContext.restoreGraphicsState()
device.draw(in: frameRect, from: .zero, operation: .sourceOver, fraction: 1)
drawText("iPhone is a trademark of Apple Inc., registered in the U.S. and other countries.",
         at: NSPoint(x: 74, y: 20), font: .systemFont(ofSize: 11), color: muted)

NSGraphicsContext.restoreGraphicsState()
guard let data = bitmap.representation(using: .jpeg, properties: [.compressionFactor: 0.9]) else {
    fatalError("Could not encode Open Graph image")
}
try data.write(to: output, options: .atomic)
print("Wrote \(output.path) (1200x630) using the native COR dashboard screenshot")

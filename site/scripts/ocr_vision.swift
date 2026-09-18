// OCR helper for check_source_names.py — macOS Vision text recognition.
//
// Reads image files (PNG/JPEG/...) and prints the recognized text of each, in
// reading order: one line per text row, pieces of the same row joined with
// " | " so the caller's column-split rules see table cells as separate cells.
//
//   ocr_vision [--langs pt-BR,en-US,es-ES,ru-RU] [--list-langs] img1.png img2.png ...
//
// Output format:
//   ===== FILE <path>
//   <text of that image>
// A file that cannot be read prints "===== ERROR <path> <message>" and is skipped.
//
// Build:  swiftc -O -o ocr_vision ocr_vision.swift

import Foundation
import CoreGraphics
import ImageIO
import Vision

let defaultLangs = ["pt-BR", "en-US", "es-ES", "ru-RU"]

func supported() -> [String] {
    let r = VNRecognizeTextRequest()
    r.recognitionLevel = .accurate
    return (try? r.supportedRecognitionLanguages()) ?? []
}

func loadImage(_ path: String) -> CGImage? {
    let url = URL(fileURLWithPath: path) as CFURL
    guard let src = CGImageSourceCreateWithURL(url, nil) else { return nil }
    return CGImageSourceCreateImageAtIndex(src, 0, nil)
}

/// Observations regrouped into visual rows: sort top-to-bottom, then left-to-right,
/// and join the pieces of one row with " | ". Vision's normalized boxes have their
/// origin at the bottom-left, so a larger midY means higher on the page.
func layout(_ obs: [VNRecognizedTextObservation]) -> String {
    struct Piece { let text: String; let x: Double; let y: Double; let h: Double }
    var pieces: [Piece] = []
    for o in obs {
        guard let c = o.topCandidates(1).first else { continue }
        let t = c.string.trimmingCharacters(in: .whitespacesAndNewlines)
        if t.isEmpty { continue }
        let b = o.boundingBox
        pieces.append(Piece(text: t, x: Double(b.minX), y: Double(b.midY), h: Double(b.height)))
    }
    if pieces.isEmpty { return "" }
    let heights = pieces.map { $0.h }.sorted()
    let median = heights[heights.count / 2]
    let tol = max(median * 0.6, 0.004)
    pieces.sort { $0.y > $1.y }
    var rows: [[Piece]] = []
    for p in pieces {
        if var last = rows.last, let ref = last.first, abs(ref.y - p.y) <= tol {
            last.append(p)
            rows[rows.count - 1] = last
        } else {
            rows.append([p])
        }
    }
    return rows.map { row in
        row.sorted { $0.x < $1.x }.map { $0.text }.joined(separator: " | ")
    }.joined(separator: "\n")
}

func recognize(_ image: CGImage, langs: [String]) throws -> String {
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false
    if !langs.isEmpty { req.recognitionLanguages = langs }
    try VNImageRequestHandler(cgImage: image, options: [:]).perform([req])
    return layout(req.results ?? [])
}

var langs = defaultLangs
var files: [String] = []
var args = Array(CommandLine.arguments.dropFirst())
var i = 0
while i < args.count {
    switch args[i] {
    case "--langs":
        i += 1
        if i < args.count {
            langs = args[i].split(separator: ",").map { String($0).trimmingCharacters(in: .whitespaces) }
        }
    case "--list-langs":
        print(supported().joined(separator: ","))
        exit(0)
    default:
        files.append(args[i])
    }
    i += 1
}

let ok = Set(supported())
let use = langs.filter { ok.contains($0) }
FileHandle.standardError.write("ocr_vision: languages \(use.joined(separator: ",")) (of \(langs.joined(separator: ",")))\n".data(using: .utf8)!)

for path in files {
    guard let img = loadImage(path) else {
        print("===== ERROR \(path) cannot decode image")
        continue
    }
    do {
        let text = try recognize(img, langs: use)
        print("===== FILE \(path)")
        print(text)
    } catch {
        print("===== ERROR \(path) \(error)")
    }
}

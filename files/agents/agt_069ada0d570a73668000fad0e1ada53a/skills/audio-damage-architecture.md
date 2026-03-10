---
name: audio-damage-architecture
description: Documented Audio Damage plugin UI architecture findings. Use when analyzing Audio Damage plugins, identifying JUCE vs VSTGUI patterns, or referencing known plugin signatures.
created_at: 2026-03-08T16:16:21.452601+00:00
updated_at: 2026-03-08T16:16:21.452601+00:00
---

# Audio Damage Plugin Architecture -- Reverse Engineered SOP
## Source: audio_damage_reverse_engineered_architecture.md

---

## Framework Taxonomy

### Modern Plugins -- JUCE-based
Plugins: Eos 2, Quanta 2, Enso (and other post-~2018 releases)

Key characteristics:
- Fully resizable vector UIs (no fixed pixel dimensions)
- Hi-DPI / Retina display support via JUCE's scaling pipeline
- Component tree rooted at `juce::AudioProcessorEditor`
- Uses `juce::LookAndFeel` subclasses for custom styling
- Parameter automation via `juce::AudioProcessorValueTreeState` (APVTS)
- XML/ValueTree state serialization for preset storage
- Binary signatures: look for `_ZN4juce` (JUCE namespaced symbols) in Mach-O symbol table
- Framework bundle typically embedded or linked as `JUCE modules` static lib
- Build artifacts: universal binary or arm64/x86_64 slices, min macOS 10.13+

### Legacy Plugins -- VSTGUI-based
Plugins: 907A, Bitcom, Discord, Dr. Device (pre-~2016 releases)

Key characteristics:
- Bitmap-heavy fixed-size UIs (PNG/BMP assets baked into Resources fork or binary)
- No resize support; fixed editor dimensions declared in `getEditorSize()`
- Component tree rooted at `CFrame` (VSTGUI root)
- Custom knob/slider bitmaps (sprite sheets or individual frames)
- Parameter state via raw `setParameter(index, float)` VST2 API
- Binary signatures: look for `vstgui` or `VSTGUI` strings, `CKnob`, `CSlider` symbols
- Older Mach-O i386/x86_64 fat binaries common

---

## Mach-O Binary Analysis Protocol

### Step 1 -- Identify Architecture Slices
```bash
file plugin.vst/Contents/MacOS/plugin
lipo -info plugin.vst/Contents/MacOS/plugin
```

### Step 2 -- Extract Symbol Table
```bash
nm -gU plugin.vst/Contents/MacOS/plugin | grep -E "(juce|VSTGUI|CKnob|AudioProcessor)"
```

### Step 3 -- Locate Framework Signatures
```bash
otool -L plugin.vst/Contents/MacOS/plugin        # linked dylibs
strings plugin.vst/Contents/MacOS/plugin | grep -iE "(juce|vstgui|auval|component)"
```

### Step 4 -- Inspect Resources
```bash
ls plugin.vst/Contents/Resources/
# JUCE: may contain BinaryData.cpp artifacts, XML presets
# VSTGUI: bitmap PNGs, skin directories
```

### Step 5 -- AU Component Metadata (AU plugins)
```bash
auval -v aufx XXXX Adm   # Audio Damage manufacturer code
pluginkit -mA -v -p com.apple.AudioUnit.Component
```

---

## Component Pattern Reference

| Pattern | JUCE Signal | VSTGUI Signal |
|---|---|---|
| Resize handle | `juce::ResizableCornerComponent` | Absent |
| Parameter binding | `SliderAttachment` / `ButtonAttachment` | Manual `setParameter()` |
| Preset XML | `ValueTree::toXmlString()` | Custom binary chunk |
| Custom look | `LookAndFeel_V4` subclass | `CBitmap` sprite sheets |
| Thread safety | `MessageManager::callAsync` | Manual locks |

---

## Known Audio Damage VST/AU IDs
- Manufacturer code: `Adm` (Audio Damage)
- Plugin type codes vary per product; use `auval -a` to enumerate all installed

---

## Decompilation Workflow (Hopper / Ghidra)

1. Load Mach-O slice: prefer arm64 for modern M-series analysis
2. Apply JUCE symbol file if available (community JUCE.sig for IDA/Ghidra)
3. Target entry: `createPluginFilter()` -- JUCE factory function
4. For VSTGUI: target `VSTGUIEditor::open()` and `CFrame` constructor chains
5. Document component hierarchy top-down: Editor -> Panels -> Controls
6. Cross-reference parameter index map with `PluginProcessor::getParameterName()`

---

## Notes
- Audio Damage moved to JUCE progressively; some mid-era plugins may be hybrid
- Check `Info.plist` CFBundleVersion and CFBundleShortVersionString for era clues
- AU v3 (AUv3) plugins require entitlements + App Sandbox -- affects binary layout

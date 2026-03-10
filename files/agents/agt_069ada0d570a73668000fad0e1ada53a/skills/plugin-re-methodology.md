---
name: plugin-re-methodology
description: General VST/AU plugin reverse engineering methodology for Mach-O binaries. Use when starting a new plugin analysis, identifying unknown frameworks, or documenting component patterns.
created_at: 2026-03-08T16:16:22.015387+00:00
updated_at: 2026-03-08T16:16:22.015387+00:00
---

# VST/AU Plugin Reverse Engineering Methodology

## Scope
Applicable to macOS VST2, VST3, AU (v2/v3), and AAX plugin formats.
Primary focus: JUCE-based and VSTGUI-based plugins, Mach-O binaries.

---

## Phase 1 -- Triage

### Format Identification
| Format | Bundle Extension | Entry Point |
|---|---|---|
| VST2 | .vst | `main` / `VSTPluginMain` |
| VST3 | .vst3 | `GetPluginFactory` |
| AU | .component | `AudioComponentFactoryFunction` |
| AAX | .aaxplugin | `ACFRegisterPlugin` |

### Quick Framework Fingerprint
```bash
# Single command triage
strings "$PLUGIN_BINARY" | grep -iE \
  "(juce|vstgui|wdl|ioplug|w-trees|maxim|rack)" | sort -u | head -30
```

Framework indicators:
- `juce::` or `_ZN4juce` -> JUCE
- `VSTGUI` / `CFrame` / `CKnob` -> VSTGUI
- `WDL_` -> Cockos WDL (iPlug)
- `MaximDSP` -> Maxim (rare)

---

## Phase 2 -- Binary Deep Dive

### Symbol Extraction
```bash
# Demangled C++ symbols
nm -gU "$BINARY" | c++filt | grep -v " U " | head -100

# Objective-C classes (AUv3, macOS UI bridges)
otool -oV "$BINARY" | grep "^[0-9a-f].*name" | head -50

# Segment layout
otool -l "$BINARY" | grep -A3 "segname"
```

### Embedded Resources
```bash
# JUCE BinaryData (base64 or raw embedded assets)
strings "$BINARY" | grep -E "^[A-Za-z][A-Za-z0-9_]{4,}(Png|Svg|Xml|Json)$"

# Bitmap sprite sheet filenames (VSTGUI)
strings "$BINARY" | grep -iE "\.(png|bmp|jpg)$"
```

---

## Phase 3 -- Parameter Map Reconstruction

### JUCE APVTS Parameters
Look for `AudioProcessorValueTreeState::ParameterLayout` construction.
In Ghidra: search for `createParameterLayout` or `addParameter` call chains.

Extract:
- Parameter ID strings (used in DAW automation)
- Range objects (min, max, default, skew)
- Parameter type (float, bool, choice)

### VST2 Legacy Parameters
`getParameterName(int index)` returns human-readable name.
`getParameterLabel(int index)` returns unit string.
Total count from `getNumParameters()`.

---

## Phase 4 -- UI Component Mapping

### JUCE Component Tree
Root: `AudioProcessorEditor` subclass
Common children:
- `juce::Slider` with `SliderAttachment`
- `juce::ComboBox` with `ComboBoxAttachment`
- `juce::ToggleButton` with `ButtonAttachment`
- Custom `juce::Component` subclasses for knobs/meters

Resize: look for `setResizable(true, true)` or `setResizeLimits()`

### VSTGUI Component Tree
Root: `CFrame`
Common children:
- `CKnob` (rotary, bitmap frames)
- `CSlider` (horizontal/vertical)
- `COnOffButton`
- `CAnimKnob` (sprite-sheet animation)

Fixed size set in editor constructor: `rect(0, 0, width, height)`

---

## Phase 5 -- Documentation Output Format

For each plugin analyzed, produce:
```
## Plugin: [Name] vX.X
- Format: VST2 / VST3 / AU
- Framework: JUCE [version estimate] / VSTGUI [version]
- UI Type: Resizable vector / Fixed bitmap
- Arch slices: arm64, x86_64
- Parameter count: N
- Notable patterns: [list]
- Decompiler notes: [Ghidra / Hopper observations]
```

---

## Tools Reference
- `file`, `lipo`, `nm`, `otool`, `strings` -- standard macOS CLI (no install needed)
- `c++filt` -- C++ symbol demangler (Xcode CLT)
- `auval` -- AU validation tool (Xcode CLT)
- `pluginkit` -- macOS plugin registry query
- Ghidra (free) -- full decompilation, scripting via Python/Java
- Hopper Disassembler -- macOS-native, fast Mach-O navigation
- JUCE community Ghidra scripts: github.com/juce-framework/JUCE (check Issues/Wiki)

"""
POD Image Generator v3 — Uses Gemini native image generation (gemini-2.5-flash-image).
"""

import os
import sys
import json
import time
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY not set")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

PODS_DIR = Path(r"C:\Users\Axiom\.openclaw\workspace\data\pods")
DESIGNS_FILE = PODS_DIR / "DesignArch" / "outputs.json"
IMAGES_DIR = PODS_DIR / "generated_images"
IMAGES_DIR.mkdir(exist_ok=True)

with open(DESIGNS_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

briefs = data[0]["outputs"]
print(f"Loaded {len(briefs)} design briefs")

results = []
errors = []

for brief in briefs:
    theme_id = brief["theme_id"]
    theme_name = brief["theme_name"]
    orientation = brief.get("layout", {}).get("orientation", "square")
    theme_dir = IMAGES_DIR / theme_id
    theme_dir.mkdir(exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"Theme: {theme_name} ({theme_id}) — {orientation}")
    print(f"{'='*60}")
    
    for prompt_data in brief["image_prompts"]:
        variant = prompt_data["variant"]
        prompt = prompt_data["prompt"]
        filename = f"{theme_id}-{variant}.png"
        filepath = theme_dir / filename
        
        if filepath.exists() and filepath.stat().st_size > 10000:
            print(f"  [SKIP] {filename} already exists ({filepath.stat().st_size} bytes)")
            results.append({"theme_id": theme_id, "variant": variant, "file": str(filepath), "status": "skipped"})
            continue
        
        print(f"  [GEN] {filename}...")
        print(f"    Prompt: {prompt[:100]}...")
        
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-09-2025",
                contents=f"Generate an image: {prompt}",
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                )
            )
            
            # Extract image from response
            saved = False
            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                        img_bytes = part.inline_data.data
                        with open(filepath, "wb") as img_file:
                            img_file.write(img_bytes)
                        size_kb = len(img_bytes) / 1024
                        print(f"    [OK] Saved {filename} ({size_kb:.0f} KB)")
                        results.append({"theme_id": theme_id, "variant": variant, "file": str(filepath), "status": "ok", "size_kb": round(size_kb)})
                        saved = True
                        break
            
            if not saved:
                # Check for text-only response
                text_resp = ""
                if response.candidates:
                    for part in response.candidates[0].content.parts:
                        if part.text:
                            text_resp = part.text[:200]
                print(f"    [WARN] No image in response. Text: {text_resp}")
                errors.append({"theme_id": theme_id, "variant": variant, "error": f"no image returned. Text: {text_resp}"})
                
        except Exception as e:
            err_msg = str(e)
            print(f"    [ERR] {err_msg[:300]}")
            errors.append({"theme_id": theme_id, "variant": variant, "error": err_msg[:300]})
        
        time.sleep(5)

# Summary
print(f"\n{'='*60}")
print(f"GENERATION COMPLETE")
print(f"{'='*60}")
ok_count = len([r for r in results if r['status'] == 'ok'])
skip_count = len([r for r in results if r['status'] == 'skipped'])
print(f"  Success: {ok_count}")
print(f"  Skipped: {skip_count}")
print(f"  Errors:  {len(errors)}")

if errors:
    print(f"\nErrors:")
    for e in errors:
        print(f"  {e['theme_id']}-{e['variant']}: {e['error'][:150]}")

manifest = {"generated": results, "errors": errors, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")}
with open(IMAGES_DIR / "manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print(f"\nManifest saved to {IMAGES_DIR / 'manifest.json'}")

"""
Test: Min/Max Sizes and Aspect Ratio
Tests the new constraint and aspect ratio features.
"""

import sys
from engine.src.ui import UIComponent, UICompiler, px, percent, vw, vh


def test_min_width():
    """Test minimum width constraint."""
    print("\n=== TEST 1: Min Width ===")
    
    compiler = UICompiler(1280, 720)
    
    # Component with 10vw width (128px) but min 200px
    component = UIComponent(
        width=vw(10),  # Would be 128px
        min_width=px(200)
    )
    
    compiler.compile_component(component)
    
    print(f"Width: vw(10) = {1280 * 0.1}px, min_width = 200px")
    print(f"Compiled width: {component.compiled_width}px")
    print(f"Expected: 200px (clamped to minimum)")
    
    assert component.compiled_width == 200, f"Expected 200, got {component.compiled_width}"
    print("✅ Min width clamping works!")


def test_max_width():
    """Test maximum width constraint."""
    print("\n=== TEST 2: Max Width ===")
    
    compiler = UICompiler(1280, 720)
    
    # Component with 80vw width (1024px) but max 800px
    component = UIComponent(
        width=vw(80),  # Would be 1024px
        max_width=px(800)
    )
    
    compiler.compile_component(component)
    
    print(f"Width: vw(80) = {1280 * 0.8}px, max_width = 800px")
    print(f"Compiled width: {component.compiled_width}px")
    print(f"Expected: 800px (clamped to maximum)")
    
    assert component.compiled_width == 800, f"Expected 800, got {component.compiled_width}"
    print("✅ Max width clamping works!")


def test_min_max_range():
    """Test width stays within min/max range."""
    print("\n=== TEST 3: Min/Max Range ===")
    
    compiler = UICompiler(1280, 720)
    
    # Component with responsive width, clamped between 200-800px
    component = UIComponent(
        width=vw(50),  # 640px (within range)
        min_width=px(200),
        max_width=px(800)
    )
    
    compiler.compile_component(component)
    
    print(f"Width: vw(50) = {1280 * 0.5}px")
    print(f"Range: 200px - 800px")
    print(f"Compiled width: {component.compiled_width}px")
    print(f"Expected: 640px (within range, unchanged)")
    
    assert component.compiled_width == 640, f"Expected 640, got {component.compiled_width}"
    print("✅ Width stays within range!")


def test_min_height():
    """Test minimum height constraint."""
    print("\n=== TEST 4: Min Height ===")
    
    compiler = UICompiler(1280, 720)
    
    # Component with 5vh height (36px) but min 50px
    component = UIComponent(
        height=vh(5),  # Would be 36px
        min_height=px(50)
    )
    
    compiler.compile_component(component)
    
    print(f"Height: vh(5) = {720 * 0.05}px, min_height = 50px")
    print(f"Compiled height: {component.compiled_height}px")
    print(f"Expected: 50px (clamped to minimum)")
    
    assert component.compiled_height == 50, f"Expected 50, got {component.compiled_height}"
    print("✅ Min height clamping works!")


def test_max_height():
    """Test maximum height constraint."""
    print("\n=== TEST 5: Max Height ===")
    
    compiler = UICompiler(1280, 720)
    
    # Component with 80vh height (576px) but max 400px
    component = UIComponent(
        height=vh(80),  # Would be 576px
        max_height=px(400)
    )
    
    compiler.compile_component(component)
    
    print(f"Height: vh(80) = {720 * 0.8}px, max_height = 400px")
    print(f"Compiled height: {component.compiled_height}px")
    print(f"Expected: 400px (clamped to maximum)")
    
    assert component.compiled_height == 400, f"Expected 400, got {component.compiled_height}"
    print("✅ Max height clamping works!")


def test_aspect_ratio_16_9():
    """Test 16:9 aspect ratio."""
    print("\n=== TEST 6: Aspect Ratio (16:9) ===")
    
    compiler = UICompiler(1280, 720)
    
    # Video player: 800px wide, 16:9 aspect ratio
    component = UIComponent(
        width=px(800),
        aspect_ratio=16/9  # height = width / (16/9)
    )
    
    compiler.compile_component(component)
    
    expected_height = 800 / (16/9)  # = 450px
    print(f"Width: 800px, aspect_ratio = 16:9")
    print(f"Compiled height: {component.compiled_height}px")
    print(f"Expected: {expected_height}px")
    
    assert abs(component.compiled_height - expected_height) < 0.1, \
        f"Expected {expected_height}, got {component.compiled_height}"
    print("✅ 16:9 aspect ratio works!")


def test_aspect_ratio_square():
    """Test 1:1 aspect ratio (square)."""
    print("\n=== TEST 7: Aspect Ratio (1:1 Square) ===")
    
    compiler = UICompiler(1280, 720)
    
    # Square thumbnail: 200px wide
    component = UIComponent(
        width=px(200),
        aspect_ratio=1.0  # Square
    )
    
    compiler.compile_component(component)
    
    print(f"Width: 200px, aspect_ratio = 1:1")
    print(f"Compiled height: {component.compiled_height}px")
    print(f"Expected: 200px (square)")
    
    assert component.compiled_height == 200, f"Expected 200, got {component.compiled_height}"
    print("✅ Square aspect ratio works!")


def test_aspect_ratio_portrait():
    """Test 3:4 aspect ratio (portrait)."""
    print("\n=== TEST 8: Aspect Ratio (3:4 Portrait) ===")
    
    compiler = UICompiler(1280, 720)
    
    # Portrait image: 300px wide, 3:4 aspect
    component = UIComponent(
        width=px(300),
        aspect_ratio=3/4  # height = width / (3/4) = width * 4/3
    )
    
    compiler.compile_component(component)
    
    expected_height = 300 / (3/4)  # = 400px
    print(f"Width: 300px, aspect_ratio = 3:4")
    print(f"Compiled height: {component.compiled_height}px")
    print(f"Expected: {expected_height}px")
    
    assert component.compiled_height == expected_height, \
        f"Expected {expected_height}, got {component.compiled_height}"
    print("✅ Portrait aspect ratio works!")


def test_aspect_ratio_with_responsive():
    """Test aspect ratio with responsive width."""
    print("\n=== TEST 9: Aspect Ratio with Responsive Width ===")
    
    compiler = UICompiler(1280, 720)
    
    # Video: 80% of viewport width, 16:9 aspect
    component = UIComponent(
        width=vw(80),  # 1024px
        aspect_ratio=16/9
    )
    
    compiler.compile_component(component)
    
    expected_width = 1280 * 0.8  # 1024px
    expected_height = expected_width / (16/9)  # 576px
    
    print(f"Width: vw(80) = {expected_width}px")
    print(f"Aspect ratio: 16:9")
    print(f"Compiled height: {component.compiled_height}px")
    print(f"Expected: {expected_height}px")
    
    assert abs(component.compiled_height - expected_height) < 0.1, \
        f"Expected {expected_height}, got {component.compiled_height}"
    print("✅ Responsive width with aspect ratio works!")


def test_viewport_resize_with_constraints():
    """Test that constraints adapt to viewport resize."""
    print("\n=== TEST 10: Viewport Resize with Constraints ===")
    
    compiler = UICompiler(1280, 720)
    
    # Component with responsive width and constraints
    component = UIComponent(
        width=vw(50),
        min_width=px(200),
        max_width=px(800)
    )
    
    # Initial compilation (1280x720)
    compiler.compile_component(component)
    print(f"Viewport 1280x720: width = {component.compiled_width}px (50% = 640px)")
    assert component.compiled_width == 640
    
    # Resize to small screen
    compiler.set_viewport(400, 300)
    compiler.compile_component(component)
    print(f"Viewport 400x300: width = {component.compiled_width}px (50% = 200px, clamped to min)")
    assert component.compiled_width == 200  # Clamped to min
    
    # Resize to large screen
    compiler.set_viewport(2000, 1000)
    compiler.compile_component(component)
    print(f"Viewport 2000x1000: width = {component.compiled_width}px (50% = 1000px, clamped to max)")
    assert component.compiled_width == 800  # Clamped to max
    
    print("✅ Constraints adapt to viewport resize!")


def test_percentage_constraints():
    """Test min/max with percentage units."""
    print("\n=== TEST 11: Percentage Constraints ===")
    
    compiler = UICompiler(1280, 720)
    
    # Parent panel
    parent = UIComponent(
        width=px(600),
        height=px(400)
    )
    compiler.compile_component(parent)
    
    # Child with percentage constraints
    child = UIComponent(
        width=percent(150),  # Would be 900px (150% of 600)
        min_width=percent(20),  # 120px (20% of 600)
        max_width=percent(100)  # 600px (100% of 600)
    )
    parent.add_child(child)
    
    compiler.compile_component(parent)
    
    print(f"Parent width: 600px")
    print(f"Child width: percent(150) = 900px (would overflow)")
    print(f"Child max_width: percent(100) = 600px")
    print(f"Compiled child width: {child.compiled_width}px")
    print(f"Expected: 600px (clamped to max)")
    
    assert child.compiled_width == 600, f"Expected 600, got {child.compiled_width}"
    print("✅ Percentage constraints work!")


def test_combined_aspect_and_constraints():
    """Test aspect ratio combined with min/max constraints."""
    print("\n=== TEST 12: Aspect Ratio + Constraints ===")
    
    compiler = UICompiler(1280, 720)
    
    # Component with aspect ratio and height constraints
    component = UIComponent(
        width=px(800),
        aspect_ratio=16/9,  # Would make height = 450px
        min_height=px(500),  # But minimum is 500px
        max_height=px(600)
    )
    
    compiler.compile_component(component)
    
    print(f"Width: 800px")
    print(f"Aspect ratio 16:9 would give height: 450px")
    print(f"But min_height = 500px")
    print(f"Compiled height: {component.compiled_height}px")
    print(f"Expected: 500px (aspect applied, then clamped)")
    
    assert component.compiled_height == 500, f"Expected 500, got {component.compiled_height}"
    print("✅ Aspect ratio + constraints work together!")


def main():
    """Run all tests."""
    print("╔═══════════════════════════════════════════════════╗")
    print("║  MIN/MAX SIZES & ASPECT RATIO TESTS               ║")
    print("╚═══════════════════════════════════════════════════╝")
    
    try:
        # Min/Max tests
        test_min_width()
        test_max_width()
        test_min_max_range()
        test_min_height()
        test_max_height()
        
        # Aspect ratio tests
        test_aspect_ratio_16_9()
        test_aspect_ratio_square()
        test_aspect_ratio_portrait()
        test_aspect_ratio_with_responsive()
        
        # Advanced tests
        test_viewport_resize_with_constraints()
        test_percentage_constraints()
        test_combined_aspect_and_constraints()
        
        print("\n" + "="*60)
        print("✨ ALL TESTS PASSED! ✨")
        print("="*60)
        print("\nMin/Max sizes and Aspect Ratio features are working!")
        print("You can now use:")
        print("  - min_width, max_width, min_height, max_height")
        print("  - aspect_ratio (width/height)")
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())


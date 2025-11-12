"""
Test: CSS-like Percentage Sizing System
Demonstrates: px, %, vw, vh units
"""

import sys
import glfw
from OpenGL.GL import *
from engine.src.ui import (
    UIComponent, UICompiler, px, percent, vw, vh
)


def test_size_compilation():
    """Test basic size compilation."""
    print("\n=== TEST 1: Size Compilation ===")
    
    # Create compiler (1280x720 viewport)
    compiler = UICompiler(1280, 720)
    
    # Test 1: Pixels (absolute)
    size_px = px(100)
    compiled = compiler.compile_size(size_px, parent_size=None, is_width=True)
    print(f"px(100) → {compiled}px (expected: 100)")
    assert compiled == 100
    
    # Test 2: Percentage of parent
    size_percent = percent(50)
    compiled = compiler.compile_size(size_percent, parent_size=200, is_width=True)
    print(f"percent(50) with parent=200 → {compiled}px (expected: 100)")
    assert compiled == 100
    
    # Test 3: Viewport width
    size_vw = vw(10)
    compiled = compiler.compile_size(size_vw, parent_size=None, is_width=True)
    print(f"vw(10) with viewport=1280 → {compiled}px (expected: 128)")
    assert compiled == 128
    
    # Test 4: Viewport height
    size_vh = vh(20)
    compiled = compiler.compile_size(size_vh, parent_size=None, is_width=False)
    print(f"vh(20) with viewport=720 → {compiled}px (expected: 144)")
    assert compiled == 144
    
    print("✅ All size compilation tests passed!")


def test_component_compilation():
    """Test component compilation."""
    print("\n=== TEST 2: Component Compilation ===")
    
    compiler = UICompiler(1280, 720)
    
    # Create parent (400x300, at 10vw, 10vh)
    parent = UIComponent(
        x=vw(10),      # 10% of 1280 = 128
        y=vh(10),      # 10% of 720 = 72
        width=px(400),
        height=px(300)
    )
    
    # Compile parent
    compiler.compile_component(parent)
    
    print(f"Parent: x={parent.compiled_x}, y={parent.compiled_y}, w={parent.compiled_width}, h={parent.compiled_height}")
    assert parent.compiled_x == 128
    assert parent.compiled_y == 72
    assert parent.compiled_width == 400
    assert parent.compiled_height == 300
    
    # Create child (50% of parent width)
    child = UIComponent(
        x=percent(10),    # 10% of parent = 40
        y=percent(10),    # 10% of parent = 30
        width=percent(80), # 80% of parent = 320
        height=px(50)
    )
    parent.add_child(child)
    
    # Compile (will compile children recursively)
    compiler.compile_component(parent)
    
    print(f"Child: x={child.compiled_x}, y={child.compiled_y}, w={child.compiled_width}, h={child.compiled_height}")
    assert child.compiled_x == 40  # 10% of 400
    assert child.compiled_y == 30  # 10% of 300
    assert child.compiled_width == 320  # 80% of 400
    assert child.compiled_height == 50
    
    print("✅ All component compilation tests passed!")


def test_responsive_layout():
    """Test responsive layout that adapts to viewport size."""
    print("\n=== TEST 3: Responsive Layout ===")
    
    # Simulate different screen sizes
    screen_sizes = [
        (1920, 1080, "Full HD"),
        (1280, 720, "HD"),
        (800, 600, "Small")
    ]
    
    for width, height, name in screen_sizes:
        print(f"\n{name} ({width}x{height}):")
        compiler = UICompiler(width, height)
        
        # Full-width header (100vw x 60px)
        header = UIComponent(
            x=vw(0), y=vh(0),
            width=vw(100), height=px(60)
        )
        compiler.compile_component(header)
        print(f"  Header: {header.compiled_width}x{header.compiled_height} (100% width)")
        assert header.compiled_width == width
        
        # Centered modal (80vw x 80vh)
        modal = UIComponent(
            x=vw(10), y=vh(10),
            width=vw(80), height=vh(80)
        )
        compiler.compile_component(modal)
        print(f"  Modal: {modal.compiled_width}x{modal.compiled_height} at ({modal.compiled_x}, {modal.compiled_y})")
        assert modal.compiled_width == width * 0.8
        assert modal.compiled_height == height * 0.8
    
    print("\n✅ Responsive layout tests passed!")


def test_mixed_units():
    """Test components with mixed units."""
    print("\n=== TEST 4: Mixed Units ===")
    
    compiler = UICompiler(1280, 720)
    
    # Button: centered horizontally (50vw), absolute vertical (100px),
    # responsive width (30vw), fixed height (50px)
    button = UIComponent(
        x=vw(35),      # 35% from left (centered with 30% width)
        y=px(100),     # 100px from top
        width=vw(30),  # 30% of viewport width
        height=px(50)  # 50px tall
    )
    compiler.compile_component(button)
    
    print(f"Button: pos=({button.compiled_x}, {button.compiled_y}), size={button.compiled_width}x{button.compiled_height}")
    assert button.compiled_x == 1280 * 0.35  # 448
    assert button.compiled_y == 100
    assert button.compiled_width == 1280 * 0.30  # 384
    assert button.compiled_height == 50
    
    print("✅ Mixed units test passed!")


def test_viewport_resize():
    """Test that sizes recompile when viewport changes."""
    print("\n=== TEST 5: Viewport Resize ===")
    
    compiler = UICompiler(1280, 720)
    
    # Component using viewport units
    component = UIComponent(
        x=vw(10), y=vh(10),
        width=vw(80), height=vh(80)
    )
    
    # Initial compilation
    compiler.compile_component(component)
    print(f"Initial (1280x720): {component.compiled_width}x{component.compiled_height}")
    assert component.compiled_width == 1024  # 80% of 1280
    assert component.compiled_height == 576  # 80% of 720
    
    # Resize viewport
    compiler.set_viewport(1920, 1080)
    compiler.compile_component(component)
    print(f"After resize (1920x1080): {component.compiled_width}x{component.compiled_height}")
    assert component.compiled_width == 1536  # 80% of 1920
    assert component.compiled_height == 864  # 80% of 1080
    
    print("✅ Viewport resize test passed!")


def test_nested_percentages():
    """Test nested percentage calculations."""
    print("\n=== TEST 6: Nested Percentages ===")
    
    compiler = UICompiler(1280, 720)
    
    # Root: 80% of viewport
    root = UIComponent(
        x=vw(10), y=vh(10),
        width=vw(80), height=vh(80)
    )
    compiler.compile_component(root)
    print(f"Root: {root.compiled_width}x{root.compiled_height}")
    
    # Child1: 50% of root
    child1 = UIComponent(
        x=px(0), y=px(0),
        width=percent(50), height=percent(50)
    )
    root.add_child(child1)
    compiler.compile_component(root)
    print(f"Child1: {child1.compiled_width}x{child1.compiled_height}")
    assert child1.compiled_width == root.compiled_width * 0.5
    
    # Child2 (of child1): 50% of child1
    child2 = UIComponent(
        x=px(0), y=px(0),
        width=percent(50), height=percent(50)
    )
    child1.add_child(child2)
    compiler.compile_component(root)
    print(f"Child2: {child2.compiled_width}x{child2.compiled_height}")
    assert child2.compiled_width == child1.compiled_width * 0.5
    
    # Chain: 80% → 50% → 50% = 20% of viewport
    expected = 1280 * 0.8 * 0.5 * 0.5  # 256
    print(f"Expected chain: 1280 * 0.8 * 0.5 * 0.5 = {expected}")
    assert child2.compiled_width == expected
    
    print("✅ Nested percentages test passed!")


def main():
    """Run all tests."""
    print("╔════════════════════════════════════════╗")
    print("║  CSS-LIKE PERCENTAGE SIZING TESTS      ║")
    print("╚════════════════════════════════════════╝")
    
    try:
        test_size_compilation()
        test_component_compilation()
        test_responsive_layout()
        test_mixed_units()
        test_viewport_resize()
        test_nested_percentages()
        
        print("\n" + "="*50)
        print("✨ ALL TESTS PASSED! ✨")
        print("="*50)
        print("\nPercentage sizing system is working correctly!")
        print("You can now use: px(), percent(), vw(), vh()")
        
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


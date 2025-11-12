"""
Test: Calc() Function
Tests CSS-like calc() for arithmetic with different units.
"""

import sys
from engine.src.ui import (
    UIComponent, UICompiler, calc, add, sub, mul, div,
    px, percent, vw, vh
)


def test_basic_addition():
    """Test basic calc addition."""
    print("\n=== TEST 1: Basic Addition ===")
    
    compiler = UICompiler(1280, 720)
    
    # 100px + 50px = 150px
    component = UIComponent(width=calc(px(100), px(50), '+'))
    compiler.compile_component(component)
    
    print(f"calc(px(100), px(50), '+') = {component.compiled_width}px")
    print(f"Expected: 150px")
    
    assert component.compiled_width == 150, f"Expected 150, got {component.compiled_width}"
    print("✅ Basic addition works!")


def test_basic_subtraction():
    """Test basic calc subtraction."""
    print("\n=== TEST 2: Basic Subtraction ===")
    
    compiler = UICompiler(1280, 720)
    
    # 100vw - 40px (full width minus padding)
    component = UIComponent(width=calc(vw(100), px(-40)))
    compiler.compile_component(component)
    
    expected = 1280 - 40  # 1240px
    print(f"calc(vw(100), px(-40)) = {component.compiled_width}px")
    print(f"Expected: {expected}px (1280 - 40)")
    
    assert component.compiled_width == expected, f"Expected {expected}, got {component.compiled_width}"
    print("✅ Subtraction works!")


def test_mixed_units():
    """Test calc with mixed units."""
    print("\n=== TEST 3: Mixed Units ===")
    
    compiler = UICompiler(1280, 720)
    
    # 50% of viewport + 100px
    component = UIComponent(width=calc(vw(50), px(100), '+'))
    compiler.compile_component(component)
    
    expected = (1280 * 0.5) + 100  # 640 + 100 = 740px
    print(f"calc(vw(50), px(100), '+') = {component.compiled_width}px")
    print(f"Expected: {expected}px (640 + 100)")
    
    assert component.compiled_width == expected, f"Expected {expected}, got {component.compiled_width}"
    print("✅ Mixed units work!")


def test_percentage_with_parent():
    """Test calc with percentage of parent."""
    print("\n=== TEST 4: Percentage with Parent ===")
    
    compiler = UICompiler(1280, 720)
    
    # Parent
    parent = UIComponent(width=px(600), height=px(400))
    compiler.compile_component(parent)
    
    # Child: 50% of parent + 50px
    child = UIComponent(width=calc(percent(50), px(50), '+'))
    parent.add_child(child)
    compiler.compile_component(parent)
    
    expected = (600 * 0.5) + 50  # 300 + 50 = 350px
    print(f"Parent: 600px")
    print(f"calc(percent(50), px(50), '+') = {child.compiled_width}px")
    print(f"Expected: {expected}px (300 + 50)")
    
    assert child.compiled_width == expected, f"Expected {expected}, got {child.compiled_width}"
    print("✅ Percentage with parent works!")


def test_multiplication():
    """Test calc multiplication."""
    print("\n=== TEST 5: Multiplication ===")
    
    compiler = UICompiler(1280, 720)
    
    # 200px * 1.5 = 300px
    component = UIComponent(width=calc(px(200), 1.5, '*'))
    compiler.compile_component(component)
    
    print(f"calc(px(200), 1.5, '*') = {component.compiled_width}px")
    print(f"Expected: 300px")
    
    assert component.compiled_width == 300, f"Expected 300, got {component.compiled_width}"
    print("✅ Multiplication works!")


def test_division():
    """Test calc division."""
    print("\n=== TEST 6: Division ===")
    
    compiler = UICompiler(1280, 720)
    
    # 600px / 2 = 300px
    component = UIComponent(width=calc(px(600), 2, '/'))
    compiler.compile_component(component)
    
    print(f"calc(px(600), 2, '/') = {component.compiled_width}px")
    print(f"Expected: 300px")
    
    assert component.compiled_width == 300, f"Expected 300, got {component.compiled_width}"
    print("✅ Division works!")


def test_helper_functions():
    """Test helper functions (add, sub, mul, div)."""
    print("\n=== TEST 7: Helper Functions ===")
    
    compiler = UICompiler(1280, 720)
    
    # add()
    comp1 = UIComponent(width=add(px(100), px(50)))
    compiler.compile_component(comp1)
    assert comp1.compiled_width == 150
    print(f"add(px(100), px(50)) = {comp1.compiled_width}px ✓")
    
    # sub()
    comp2 = UIComponent(width=sub(px(200), px(50)))
    compiler.compile_component(comp2)
    assert comp2.compiled_width == 150
    print(f"sub(px(200), px(50)) = {comp2.compiled_width}px ✓")
    
    # mul()
    comp3 = UIComponent(width=mul(px(100), 2))
    compiler.compile_component(comp3)
    assert comp3.compiled_width == 200
    print(f"mul(px(100), 2) = {comp3.compiled_width}px ✓")
    
    # div()
    comp4 = UIComponent(width=div(px(300), 3))
    compiler.compile_component(comp4)
    assert comp4.compiled_width == 100
    print(f"div(px(300), 3) = {comp4.compiled_width}px ✓")
    
    print("✅ All helper functions work!")


def test_nested_calc():
    """Test nested calc expressions."""
    print("\n=== TEST 8: Nested Calc ===")
    
    compiler = UICompiler(1280, 720)
    
    # ((100vw - 40px) - 20px) = 1280 - 40 - 20 = 1220px
    component = UIComponent(
        width=calc(
            calc(vw(100), px(-40)),  # Inner: 1280 - 40 = 1240
            px(-20)                   # Outer: 1240 - 20 = 1220
        )
    )
    compiler.compile_component(component)
    
    expected = 1280 - 40 - 20  # 1220px
    print(f"calc(calc(vw(100), px(-40)), px(-20)) = {component.compiled_width}px")
    print(f"Expected: {expected}px ((1280 - 40) - 20)")
    
    assert component.compiled_width == expected, f"Expected {expected}, got {component.compiled_width}"
    print("✅ Nested calc works!")


def test_complex_nested():
    """Test complex nested calc."""
    print("\n=== TEST 9: Complex Nested Calc ===")
    
    compiler = UICompiler(1280, 720)
    
    # (50vw + 100px) * 1.5
    component = UIComponent(
        width=calc(
            calc(vw(50), px(100), '+'),  # Inner: 640 + 100 = 740
            1.5,                          # Outer: 740 * 1.5 = 1110
            '*'
        )
    )
    compiler.compile_component(component)
    
    expected = ((1280 * 0.5) + 100) * 1.5  # 1110px
    print(f"calc(calc(vw(50), px(100), '+'), 1.5, '*') = {component.compiled_width}px")
    print(f"Expected: {expected}px ((640 + 100) * 1.5)")
    
    assert component.compiled_width == expected, f"Expected {expected}, got {component.compiled_width}"
    print("✅ Complex nested calc works!")


def test_center_element():
    """Test centering an element with calc."""
    print("\n=== TEST 10: Center Element ===")
    
    compiler = UICompiler(1280, 720)
    
    # Center a 200px element: 50vw - 100px
    component = UIComponent(
        x=calc(vw(50), px(-100)),  # 50% - half width
        width=px(200)
    )
    compiler.compile_component(component)
    
    expected_x = (1280 * 0.5) - 100  # 640 - 100 = 540px
    print(f"Element width: 200px")
    print(f"Position: calc(vw(50), px(-100)) = {component.compiled_x}px")
    print(f"Expected: {expected_x}px (center - half width)")
    
    assert component.compiled_x == expected_x, f"Expected {expected_x}, got {component.compiled_x}"
    print("✅ Element centering works!")


def test_full_width_minus_padding():
    """Test full width minus padding pattern."""
    print("\n=== TEST 11: Full Width Minus Padding ===")
    
    compiler = UICompiler(1280, 720)
    
    # Panel: full width minus 20px padding on each side
    panel = UIComponent(width=calc(vw(100), px(-40)))  # -40 for 20px each side
    compiler.compile_component(panel)
    
    expected = 1280 - 40  # 1240px
    print(f"calc(vw(100), px(-40)) = {panel.compiled_width}px")
    print(f"Expected: {expected}px (full width - 40px padding)")
    
    assert panel.compiled_width == expected, f"Expected {expected}, got {panel.compiled_width}"
    print("✅ Full width minus padding works!")


def test_viewport_resize_with_calc():
    """Test that calc adapts to viewport resize."""
    print("\n=== TEST 12: Viewport Resize with Calc ===")
    
    compiler = UICompiler(1280, 720)
    
    # Component: 100vw - 40px
    component = UIComponent(width=calc(vw(100), px(-40)))
    
    # Initial compilation
    compiler.compile_component(component)
    expected1 = 1280 - 40  # 1240px
    print(f"Viewport 1280x720: {component.compiled_width}px (expected: {expected1})")
    assert component.compiled_width == expected1
    
    # Resize viewport
    compiler.set_viewport(1920, 1080)
    compiler.compile_component(component)
    expected2 = 1920 - 40  # 1880px
    print(f"Viewport 1920x1080: {component.compiled_width}px (expected: {expected2})")
    assert component.compiled_width == expected2
    
    # Resize to small
    compiler.set_viewport(800, 600)
    compiler.compile_component(component)
    expected3 = 800 - 40  # 760px
    print(f"Viewport 800x600: {component.compiled_width}px (expected: {expected3})")
    assert component.compiled_width == expected3
    
    print("✅ Calc adapts to viewport resize!")


def test_division_by_zero():
    """Test division by zero handling."""
    print("\n=== TEST 13: Division by Zero ===")
    
    compiler = UICompiler(1280, 720)
    
    # Division by zero should return 0 (with warning)
    component = UIComponent(width=calc(px(100), 0, '/'))
    compiler.compile_component(component)
    
    print(f"calc(px(100), 0, '/') = {component.compiled_width}px")
    print(f"Expected: 0px (division by zero)")
    
    assert component.compiled_width == 0, f"Expected 0, got {component.compiled_width}"
    print("✅ Division by zero handled correctly!")


def main():
    """Run all tests."""
    print("╔═══════════════════════════════════════════════════╗")
    print("║  CALC() FUNCTION TESTS                            ║")
    print("╚═══════════════════════════════════════════════════╝")
    
    try:
        # Basic operations
        test_basic_addition()
        test_basic_subtraction()
        test_mixed_units()
        test_percentage_with_parent()
        test_multiplication()
        test_division()
        
        # Helper functions
        test_helper_functions()
        
        # Advanced
        test_nested_calc()
        test_complex_nested()
        
        # Practical patterns
        test_center_element()
        test_full_width_minus_padding()
        test_viewport_resize_with_calc()
        
        # Edge cases
        test_division_by_zero()
        
        print("\n" + "="*60)
        print("✨ ALL TESTS PASSED! ✨")
        print("="*60)
        print("\nCalc() function is working correctly!")
        print("You can now use:")
        print("  - calc(left, right, operator)")
        print("  - add(left, right)")
        print("  - sub(left, right)")
        print("  - mul(left, right)")
        print("  - div(left, right)")
        print("\nSupports: px, %, vw, vh, nested calc")
        
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


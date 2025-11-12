"""
Test: Rem/Em Units
Tests typography-relative sizing units.
"""

import sys
from engine.src.ui import (
    UIComponent, UICompiler, rem, em, px, percent
)


def test_rem_basic():
    """Test basic rem unit (root em)."""
    print("\n=== TEST 1: Basic REM ===")
    
    # Root font size: 16px (default)
    compiler = UICompiler(1280, 720, root_font_size=16.0)
    
    # Component with rem size
    component = UIComponent(width=rem(2))  # 2rem = 2 * 16 = 32px
    compiler.compile_component(component)
    
    print(f"Root font size: 16px")
    print(f"rem(2) = {component.compiled_width}px")
    print(f"Expected: 32px (2 * 16)")
    
    assert component.compiled_width == 32, f"Expected 32, got {component.compiled_width}"
    print("✅ Basic rem works!")


def test_rem_different_root():
    """Test rem with different root font sizes."""
    print("\n=== TEST 2: REM with Different Root Sizes ===")
    
    # Root font size: 20px
    compiler = UICompiler(1280, 720, root_font_size=20.0)
    
    component = UIComponent(width=rem(2.5))  # 2.5rem = 2.5 * 20 = 50px
    compiler.compile_component(component)
    
    print(f"Root font size: 20px")
    print(f"rem(2.5) = {component.compiled_width}px")
    print(f"Expected: 50px (2.5 * 20)")
    
    assert component.compiled_width == 50, f"Expected 50, got {component.compiled_width}"
    print("✅ REM with custom root size works!")


def test_em_no_parent():
    """Test em without parent (should use root font size)."""
    print("\n=== TEST 3: EM without Parent ===")
    
    compiler = UICompiler(1280, 720, root_font_size=16.0)
    
    # No parent, em falls back to root font size
    component = UIComponent(width=em(2))  # 2em = 2 * 16 = 32px (uses root)
    compiler.compile_component(component)
    
    print(f"Root font size: 16px (no parent)")
    print(f"em(2) = {component.compiled_width}px")
    print(f"Expected: 32px (uses root)")
    
    assert component.compiled_width == 32, f"Expected 32, got {component.compiled_width}"
    print("✅ EM without parent works!")


def test_em_with_parent():
    """Test em relative to parent font size."""
    print("\n=== TEST 4: EM with Parent ===")
    
    compiler = UICompiler(1280, 720, root_font_size=16.0)
    
    # Parent with 20px font
    parent = UIComponent(font_size=px(20))
    compiler.compile_component(parent)
    
    # Child with em size (relative to parent)
    child = UIComponent(width=em(1.5))  # 1.5em = 1.5 * 20 = 30px
    parent.add_child(child)
    compiler.compile_component(parent)
    
    print(f"Parent font: 20px")
    print(f"Child width: em(1.5) = {child.compiled_width}px")
    print(f"Expected: 30px (1.5 * 20)")
    
    assert child.compiled_width == 30, f"Expected 30, got {child.compiled_width}"
    print("✅ EM with parent works!")


def test_nested_em():
    """Test nested em inheritance."""
    print("\n=== TEST 5: Nested EM ===")
    
    compiler = UICompiler(1280, 720, root_font_size=16.0)
    
    # Root element
    root = UIComponent(font_size=rem(2))  # 32px
    compiler.compile_component(root)
    print(f"Root font: rem(2) = {root.compiled_font_size}px")
    
    # Child1 (em relative to root)
    child1 = UIComponent(font_size=em(1.5))  # 1.5 * 32 = 48px
    root.add_child(child1)
    compiler.compile_component(root)
    print(f"Child1 font: em(1.5) = {child1.compiled_font_size}px")
    assert child1.compiled_font_size == 48
    
    # Child2 (em relative to child1)
    child2 = UIComponent(font_size=em(0.5))  # 0.5 * 48 = 24px
    child1.add_child(child2)
    compiler.compile_component(root)
    print(f"Child2 font: em(0.5) = {child2.compiled_font_size}px")
    assert child2.compiled_font_size == 24
    
    print("✅ Nested em inheritance works!")


def test_rem_for_font_size():
    """Test rem for font sizes."""
    print("\n=== TEST 6: REM for Font Sizes ===")
    
    compiler = UICompiler(1280, 720, root_font_size=16.0)
    
    # Title: 2rem
    title = UIComponent(font_size=rem(2))
    compiler.compile_component(title)
    
    # Body: 1rem
    body = UIComponent(font_size=rem(1))
    compiler.compile_component(body)
    
    # Small: 0.875rem
    small = UIComponent(font_size=rem(0.875))
    compiler.compile_component(small)
    
    print(f"Title: rem(2) = {title.compiled_font_size}px")
    print(f"Body: rem(1) = {body.compiled_font_size}px")
    print(f"Small: rem(0.875) = {small.compiled_font_size}px")
    
    assert title.compiled_font_size == 32
    assert body.compiled_font_size == 16
    assert small.compiled_font_size == 14
    
    print("✅ REM for font sizes works!")


def test_rem_for_layout():
    """Test rem for layout sizes."""
    print("\n=== TEST 7: REM for Layout ===")
    
    compiler = UICompiler(1280, 720, root_font_size=16.0)
    
    # Panel with rem-based sizing
    panel = UIComponent(
        width=rem(20),   # 320px
        height=rem(15)   # 240px
    )
    compiler.compile_component(panel)
    
    print(f"Panel: rem(20) x rem(15) = {panel.compiled_width}x{panel.compiled_height}px")
    print(f"Expected: 320x240px")
    
    assert panel.compiled_width == 320
    assert panel.compiled_height == 240
    
    print("✅ REM for layout works!")


def test_em_for_padding():
    """Test em for spacing relative to font size."""
    print("\n=== TEST 8: EM for Padding ===")
    
    compiler = UICompiler(1280, 720, root_font_size=16.0)
    
    # Button with font-relative padding
    button = UIComponent(
        font_size=rem(1.25),  # 20px
        width=em(10),          # 10 * 20 = 200px (relative to own font!)
        height=em(2)           # 2 * 20 = 40px
    )
    compiler.compile_component(button)
    
    print(f"Button font: rem(1.25) = {button.compiled_font_size}px")
    print(f"Button width: em(10) = {button.compiled_width}px (10 * font)")
    print(f"Button height: em(2) = {button.compiled_height}px (2 * font)")
    
    # Note: em uses parent font, but if no parent, uses root
    # This component has no parent, so em uses root (16px), not own font (20px)
    # Expected: em(10) = 10 * 16 = 160px (not 200!)
    assert button.compiled_width == 160, f"Expected 160, got {button.compiled_width}"
    assert button.compiled_height == 32, f"Expected 32, got {button.compiled_height}"
    
    print("✅ EM uses parent font (or root if no parent)!")


def test_mixed_units():
    """Test mixing rem/em with other units."""
    print("\n=== TEST 9: Mixed Units ===")
    
    compiler = UICompiler(1280, 720, root_font_size=16.0)
    
    # Component with mixed units
    component = UIComponent(
        x=px(100),      # Absolute
        width=rem(20),  # Typography-relative
        height=percent(50)  # Parent-relative (needs parent)
    )
    compiler.compile_component(component)
    
    print(f"x: px(100) = {component.compiled_x}px")
    print(f"width: rem(20) = {component.compiled_width}px")
    
    assert component.compiled_x == 100
    assert component.compiled_width == 320  # 20 * 16
    
    print("✅ Mixed units work!")


def test_root_font_size_change():
    """Test changing root font size."""
    print("\n=== TEST 10: Change Root Font Size ===")
    
    compiler = UICompiler(1280, 720, root_font_size=16.0)
    
    # Component with rem
    component = UIComponent(width=rem(10))
    
    # Initial compilation
    compiler.compile_component(component)
    print(f"Root 16px: rem(10) = {component.compiled_width}px")
    assert component.compiled_width == 160  # 10 * 16
    
    # Change root font size
    compiler.set_root_font_size(20.0)
    compiler.compile_component(component)
    print(f"Root 20px: rem(10) = {component.compiled_width}px")
    assert component.compiled_width == 200  # 10 * 20
    
    # Change again
    compiler.set_root_font_size(12.0)
    compiler.compile_component(component)
    print(f"Root 12px: rem(10) = {component.compiled_width}px")
    assert component.compiled_width == 120  # 10 * 12
    
    print("✅ Root font size change works!")


def test_typography_scale():
    """Test typography scale with rem."""
    print("\n=== TEST 11: Typography Scale ===")
    
    compiler = UICompiler(1280, 720, root_font_size=16.0)
    
    # Typography scale (modular scale 1.25)
    h1 = UIComponent(font_size=rem(3))      # 48px
    h2 = UIComponent(font_size=rem(2.4))    # 38.4px
    h3 = UIComponent(font_size=rem(1.92))   # 30.72px
    body = UIComponent(font_size=rem(1))    # 16px
    small = UIComponent(font_size=rem(0.8)) # 12.8px
    
    compiler.compile_component(h1)
    compiler.compile_component(h2)
    compiler.compile_component(h3)
    compiler.compile_component(body)
    compiler.compile_component(small)
    
    print(f"H1: rem(3) = {h1.compiled_font_size}px")
    print(f"H2: rem(2.4) = {h2.compiled_font_size}px")
    print(f"H3: rem(1.92) = {h3.compiled_font_size}px")
    print(f"Body: rem(1) = {body.compiled_font_size}px")
    print(f"Small: rem(0.8) = {small.compiled_font_size}px")
    
    assert h1.compiled_font_size == 48
    assert h2.compiled_font_size == 38.4
    assert h3.compiled_font_size == 30.72
    assert body.compiled_font_size == 16
    assert small.compiled_font_size == 12.8
    
    print("✅ Typography scale works!")


def test_rem_em_comparison():
    """Test difference between rem and em."""
    print("\n=== TEST 12: REM vs EM ===")
    
    compiler = UICompiler(1280, 720, root_font_size=16.0)
    
    # Parent with large font
    parent = UIComponent(font_size=px(32))
    compiler.compile_component(parent)
    
    # Child with rem (relative to root, not parent!)
    child_rem = UIComponent(width=rem(2))  # 2 * 16 = 32px (uses root!)
    parent.add_child(child_rem)
    
    # Child with em (relative to parent)
    child_em = UIComponent(width=em(2))  # 2 * 32 = 64px (uses parent!)
    parent.add_child(child_em)
    
    compiler.compile_component(parent)
    
    print(f"Parent font: 32px")
    print(f"Child REM: rem(2) = {child_rem.compiled_width}px (2 * root 16px)")
    print(f"Child EM: em(2) = {child_em.compiled_width}px (2 * parent 32px)")
    
    assert child_rem.compiled_width == 32   # Uses root (16)
    assert child_em.compiled_width == 64    # Uses parent (32)
    
    print("✅ REM vs EM difference clear!")


def main():
    """Run all tests."""
    print("╔═══════════════════════════════════════════════════╗")
    print("║  REM/EM UNITS TESTS                               ║")
    print("╚═══════════════════════════════════════════════════╝")
    
    try:
        # Basic tests
        test_rem_basic()
        test_rem_different_root()
        test_em_no_parent()
        test_em_with_parent()
        test_nested_em()
        
        # Practical tests
        test_rem_for_font_size()
        test_rem_for_layout()
        test_em_for_padding()
        test_mixed_units()
        
        # Advanced tests
        test_root_font_size_change()
        test_typography_scale()
        test_rem_em_comparison()
        
        print("\n" + "="*60)
        print("✨ ALL TESTS PASSED! ✨")
        print("="*60)
        print("\nRem/Em units are working correctly!")
        print("You can now use:")
        print("  - rem(value) - Relative to root font size")
        print("  - em(value) - Relative to parent font size")
        print("\nPerfect for typography and scalable layouts!")
        
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


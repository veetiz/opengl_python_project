"""
Test: FlexContainer
Tests automatic flexbox layouts.
"""

import sys
from engine.src.ui import (
    FlexContainer, UIComponent, UICompiler, px, vw, percent
)


def test_flex_row_basic():
    """Test basic horizontal row layout."""
    print("\n=== TEST 1: Flex Row (Basic) ===")
    
    compiler = UICompiler(1280, 720)
    
    # Container: 600px wide
    container = FlexContainer(
        width=px(600),
        height=px(100),
        direction="row"
    )
    
    # Add 3 children (100px each)
    for i in range(3):
        child = UIComponent(width=px(100), height=px(50))
        container.add_child(child)
    
    compiler.compile_component(container)
    
    print(f"Container: 600px wide, 3 children (100px each)")
    print(f"Direction: row, Justify: flex-start")
    print(f"Child positions: {[c.compiled_x for c in container.children]}")
    print(f"Expected: [0, 100, 200] (no gaps)")
    
    assert container.children[0].compiled_x == 0
    assert container.children[1].compiled_x == 100
    assert container.children[2].compiled_x == 200
    
    print("✅ Basic flex row works!")


def test_flex_row_center():
    """Test centered horizontal row."""
    print("\n=== TEST 2: Flex Row (Center) ===")
    
    compiler = UICompiler(1280, 720)
    
    # Container: 600px wide
    container = FlexContainer(
        width=px(600),
        height=px(100),
        direction="row",
        justify="center"
    )
    
    # Add 2 children (100px each, total 200px)
    for i in range(2):
        child = UIComponent(width=px(100), height=px(50))
        container.add_child(child)
    
    compiler.compile_component(container)
    
    # Centered: (600 - 200) / 2 = 200px offset
    print(f"Container: 600px, Children: 200px total")
    print(f"Child positions: {[c.compiled_x for c in container.children]}")
    print(f"Expected: [200, 300] (centered)")
    
    assert container.children[0].compiled_x == 200
    assert container.children[1].compiled_x == 300
    
    print("✅ Centered row works!")


def test_flex_row_space_between():
    """Test space-between distribution."""
    print("\n=== TEST 3: Flex Row (Space Between) ===")
    
    compiler = UICompiler(1280, 720)
    
    # Container: 500px wide
    container = FlexContainer(
        width=px(500),
        height=px(100),
        direction="row",
        justify="space-between"
    )
    
    # Add 3 children (100px each, total 300px, 200px space → 100px between each)
    for i in range(3):
        child = UIComponent(width=px(100), height=px(50))
        container.add_child(child)
    
    compiler.compile_component(container)
    
    print(f"Container: 500px, Children: 300px, Space: 200px")
    print(f"Child positions: {[c.compiled_x for c in container.children]}")
    print(f"Expected: [0, 200, 400] (even spacing)")
    
    assert container.children[0].compiled_x == 0
    assert container.children[1].compiled_x == 200
    assert container.children[2].compiled_x == 400
    
    print("✅ Space-between works!")


def test_flex_column():
    """Test vertical column layout."""
    print("\n=== TEST 4: Flex Column ===")
    
    compiler = UICompiler(1280, 720)
    
    # Container: 400px tall
    container = FlexContainer(
        width=px(200),
        height=px(400),
        direction="column"
    )
    
    # Add 3 children (50px tall each)
    for i in range(3):
        child = UIComponent(width=px(150), height=px(50))
        container.add_child(child)
    
    compiler.compile_component(container)
    
    print(f"Container: 400px tall, 3 children (50px each)")
    print(f"Direction: column")
    print(f"Child positions (Y): {[c.compiled_y for c in container.children]}")
    print(f"Expected: [0, 50, 100]")
    
    assert container.children[0].compiled_y == 0
    assert container.children[1].compiled_y == 50
    assert container.children[2].compiled_y == 100
    
    print("✅ Flex column works!")


def test_flex_gap():
    """Test gap between items."""
    print("\n=== TEST 5: Flex with Gap ===")
    
    compiler = UICompiler(1280, 720)
    
    # Container with 20px gap
    container = FlexContainer(
        width=px(500),
        height=px(100),
        direction="row",
        gap=px(20)
    )
    
    # Add 3 children (100px each)
    for i in range(3):
        child = UIComponent(width=px(100), height=px(50))
        container.add_child(child)
    
    compiler.compile_component(container)
    
    print(f"Container: 500px, Gap: 20px")
    print(f"Child positions: {[c.compiled_x for c in container.children]}")
    print(f"Expected: [0, 120, 240] (100px + 20px gap)")
    
    assert container.children[0].compiled_x == 0
    assert container.children[1].compiled_x == 120  # 100 + 20
    assert container.children[2].compiled_x == 240  # 220 + 20
    
    print("✅ Gap works!")


def test_align_items_center():
    """Test cross-axis centering."""
    print("\n=== TEST 6: Align Items (Center) ===")
    
    compiler = UICompiler(1280, 720)
    
    # Container: 300px tall
    container = FlexContainer(
        width=px(500),
        height=px(300),
        direction="row",
        align="center"
    )
    
    # Add child: 50px tall (centered in 300px)
    child = UIComponent(width=px(100), height=px(50))
    container.add_child(child)
    
    compiler.compile_component(container)
    
    # Centered: (300 - 50) / 2 = 125px
    print(f"Container height: 300px, Child height: 50px")
    print(f"Child Y position: {child.compiled_y}px")
    print(f"Expected: 125px (centered)")
    
    assert child.compiled_y == 125
    
    print("✅ Align center works!")


def test_align_items_stretch():
    """Test cross-axis stretching."""
    print("\n=== TEST 7: Align Items (Stretch) ===")
    
    compiler = UICompiler(1280, 720)
    
    # Container: 300px tall
    container = FlexContainer(
        width=px(500),
        height=px(300),
        direction="row",
        align="stretch"
    )
    
    # Add child: will stretch to 300px
    child = UIComponent(width=px(100), height=px(50))
    container.add_child(child)
    
    compiler.compile_component(container)
    
    print(f"Container height: 300px")
    print(f"Child height: {child.compiled_height}px")
    print(f"Expected: 300px (stretched)")
    
    assert child.compiled_height == 300
    
    print("✅ Align stretch works!")


def test_responsive_flex():
    """Test flex with responsive units."""
    print("\n=== TEST 8: Responsive Flex ===")
    
    compiler = UICompiler(1280, 720)
    
    # Container: 80% of viewport width
    container = FlexContainer(
        width=vw(80),  # 1024px
        height=px(100),
        direction="row",
        justify="space-between"
    )
    
    # Add children
    for i in range(4):
        child = UIComponent(width=px(200), height=px(50))
        container.add_child(child)
    
    compiler.compile_component(container)
    
    # Container should be 1024px (80% of 1280)
    # 4 children at 200px each = 800px
    # Remaining space = 224px, divided into 3 gaps = ~74.67px each
    print(f"Container: vw(80) = {container.compiled_width}px")
    print(f"4 children at 200px each")
    print(f"Space-between layout")
    
    assert container.compiled_width == 1024
    assert container.children[0].compiled_x == 0
    # Last child should be at right edge
    assert abs(container.children[3].compiled_x + 200 - 1024) < 1
    
    print("✅ Responsive flex works!")


def test_flex_end():
    """Test flex-end alignment."""
    print("\n=== TEST 9: Flex End ===")
    
    compiler = UICompiler(1280, 720)
    
    # Container: 500px wide
    container = FlexContainer(
        width=px(500),
        height=px(100),
        direction="row",
        justify="flex-end"
    )
    
    # Add 2 children (100px each, total 200px)
    for i in range(2):
        child = UIComponent(width=px(100), height=px(50))
        container.add_child(child)
    
    compiler.compile_component(container)
    
    # Flex-end: 500 - 200 = 300px offset
    print(f"Container: 500px, Children: 200px")
    print(f"Child positions: {[c.compiled_x for c in container.children]}")
    print(f"Expected: [300, 400] (aligned to end)")
    
    assert container.children[0].compiled_x == 300
    assert container.children[1].compiled_x == 400
    
    print("✅ Flex-end works!")


def test_space_evenly():
    """Test space-evenly distribution."""
    print("\n=== TEST 10: Space Evenly ===")
    
    compiler = UICompiler(1280, 720)
    
    # Container: 500px wide
    container = FlexContainer(
        width=px(500),
        height=px(100),
        direction="row",
        justify="space-evenly"
    )
    
    # Add 2 children (100px each, total 200px, 300px space → 100px each gap)
    for i in range(2):
        child = UIComponent(width=px(100), height=px(50))
        container.add_child(child)
    
    compiler.compile_component(container)
    
    # Space-evenly: 300px / 3 spaces = 100px each
    # Positions: [100, 300]
    print(f"Container: 500px, Children: 200px, Space: 300px")
    print(f"Child positions: {[c.compiled_x for c in container.children]}")
    print(f"Expected: [100, 300] (even spacing including edges)")
    
    assert container.children[0].compiled_x == 100
    assert container.children[1].compiled_x == 300
    
    print("✅ Space-evenly works!")


def main():
    """Run all tests."""
    print("╔═══════════════════════════════════════════════════╗")
    print("║  FLEXCONTAINER TESTS                              ║")
    print("╚═══════════════════════════════════════════════════╝")
    
    try:
        # Basic tests
        test_flex_row_basic()
        test_flex_row_center()
        test_flex_row_space_between()
        test_flex_column()
        test_flex_gap()
        
        # Alignment tests
        test_align_items_center()
        test_align_items_stretch()
        
        # Advanced tests
        test_responsive_flex()
        test_flex_end()
        test_space_evenly()
        
        print("\n" + "="*60)
        print("✨ ALL TESTS PASSED! ✨")
        print("="*60)
        print("\nFlexContainer is working correctly!")
        print("You can now use:")
        print("  - FlexContainer(direction='row'|'column')")
        print("  - justify='flex-start'|'center'|'flex-end'|'space-between'|...")
        print("  - align='flex-start'|'center'|'flex-end'|'stretch'")
        print("  - gap=px(20) for spacing")
        print("\nAutomatic layouts for game UIs! 🎉")
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())


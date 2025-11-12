"""
Test: GridContainer
Tests automatic grid layouts.
"""

import sys
from engine.src.ui import (
    GridContainer, UIComponent, UICompiler, px, vw
)


def test_grid_basic():
    """Test basic 3x3 grid."""
    print("\n=== TEST 1: Basic 3x3 Grid ===")
    
    compiler = UICompiler(1280, 720)
    
    # Container: 600x600, 3 columns
    grid = GridContainer(
        width=px(600),
        height=px(600),
        columns=3
    )
    
    # Add 9 children (will auto-arrange in 3x3)
    for i in range(9):
        child = UIComponent(width=px(50), height=px(50))  # Size will be overridden
        grid.add_child(child)
    
    compiler.compile_component(grid)
    
    # Each cell: 200x200 (600/3)
    print(f"Grid: 600x600, 3 columns, 9 children")
    print(f"Cell size: 200x200")
    print(f"First row X positions: {[grid.children[i].compiled_x for i in range(3)]}")
    print(f"First column Y positions: {[grid.children[i*3].compiled_y for i in range(3)]}")
    
    # Check first row (Y=0, X=0,200,400)
    assert grid.children[0].compiled_x == 0
    assert grid.children[1].compiled_x == 200
    assert grid.children[2].compiled_x == 400
    
    # Check first column (X=0, Y=0,200,400)
    assert grid.children[0].compiled_y == 0
    assert grid.children[3].compiled_y == 200
    assert grid.children[6].compiled_y == 400
    
    # Check cell sizes
    assert grid.children[0].compiled_width == 200
    assert grid.children[0].compiled_height == 200
    
    print("✅ Basic 3x3 grid works!")


def test_grid_with_gap():
    """Test grid with gaps."""
    print("\n=== TEST 2: Grid with Gap ===")
    
    compiler = UICompiler(1280, 720)
    
    # Container: 620x620, 3 columns, 10px gap
    grid = GridContainer(
        width=px(620),
        height=px(620),
        columns=3,
        gap=px(10)
    )
    
    # Add 9 children
    for i in range(9):
        child = UIComponent(width=px(50), height=px(50))
        grid.add_child(child)
    
    compiler.compile_component(grid)
    
    # Cell size: (620 - 20) / 3 = 200px (20px = 2 gaps of 10px)
    # Positions: 0, 210, 420 (200 + 10 gap)
    print(f"Grid: 620x620, 3 columns, 10px gap")
    print(f"Cell size: 200x200")
    print(f"First row X positions: {[grid.children[i].compiled_x for i in range(3)]}")
    print(f"Expected: [0, 210, 420]")
    
    assert grid.children[0].compiled_x == 0
    assert grid.children[1].compiled_x == 210  # 200 + 10
    assert grid.children[2].compiled_x == 420  # 410 + 10
    
    assert grid.children[0].compiled_y == 0
    assert grid.children[3].compiled_y == 210
    
    print("✅ Grid with gap works!")


def test_grid_2_columns():
    """Test 2-column grid."""
    print("\n=== TEST 3: 2-Column Grid ===")
    
    compiler = UICompiler(1280, 720)
    
    # Container: 400x600, 2 columns
    grid = GridContainer(
        width=px(400),
        height=px(600),
        columns=2
    )
    
    # Add 6 children (will make 3 rows)
    for i in range(6):
        child = UIComponent(width=px(50), height=px(50))
        grid.add_child(child)
    
    compiler.compile_component(grid)
    
    # Cell size: 200x200 (400/2, 600/3)
    print(f"Grid: 400x600, 2 columns, 6 children")
    print(f"Cell size: 200x200")
    print(f"Layout: 2 columns x 3 rows")
    
    # Check layout
    assert grid.children[0].compiled_x == 0    # Row 0, Col 0
    assert grid.children[1].compiled_x == 200  # Row 0, Col 1
    assert grid.children[2].compiled_x == 0    # Row 1, Col 0
    assert grid.children[3].compiled_x == 200  # Row 1, Col 1
    
    assert grid.children[0].compiled_y == 0
    assert grid.children[2].compiled_y == 200  # Second row
    assert grid.children[4].compiled_y == 400  # Third row
    
    print("✅ 2-column grid works!")


def test_grid_responsive():
    """Test grid with responsive size."""
    print("\n=== TEST 4: Responsive Grid ===")
    
    compiler = UICompiler(1280, 720)
    
    # Container: 80% of viewport width, 4 columns
    grid = GridContainer(
        width=vw(80),  # 1024px
        height=px(600),
        columns=4
    )
    
    # Add 8 children (2 rows)
    for i in range(8):
        child = UIComponent(width=px(50), height=px(50))
        grid.add_child(child)
    
    compiler.compile_component(grid)
    
    # Cell width: 1024 / 4 = 256px
    # Cell height: 600 / 2 = 300px
    print(f"Grid: vw(80) = {grid.compiled_width}px, 4 columns")
    print(f"Cell size: 256x300")
    
    assert grid.compiled_width == 1024
    assert grid.children[0].compiled_width == 256
    assert grid.children[0].compiled_height == 300
    
    # Check positions
    assert grid.children[0].compiled_x == 0
    assert grid.children[1].compiled_x == 256
    assert grid.children[2].compiled_x == 512
    assert grid.children[3].compiled_x == 768
    
    print("✅ Responsive grid works!")


def test_grid_different_gaps():
    """Test grid with different column/row gaps."""
    print("\n=== TEST 5: Different Column/Row Gaps ===")
    
    compiler = UICompiler(1280, 720)
    
    # Container: 620x630, 3 columns
    grid = GridContainer(
        width=px(620),
        height=px(630),
        columns=3,
        column_gap=px(10),  # 10px between columns
        row_gap=px(15)       # 15px between rows
    )
    
    # Add 9 children
    for i in range(9):
        child = UIComponent(width=px(50), height=px(50))
        grid.add_child(child)
    
    compiler.compile_component(grid)
    
    # Cell width: (620 - 20) / 3 = 200px
    # Cell height: (630 - 30) / 3 = 200px
    print(f"Grid: 620x630, column_gap=10px, row_gap=15px")
    print(f"Cell size: 200x200")
    
    # Check column spacing (10px)
    assert grid.children[1].compiled_x == 210  # 200 + 10
    assert grid.children[2].compiled_x == 420  # 410 + 10
    
    # Check row spacing (15px)
    assert grid.children[3].compiled_y == 215  # 200 + 15
    assert grid.children[6].compiled_y == 430  # 415 + 15
    
    print("✅ Different column/row gaps work!")


def test_grid_auto_rows():
    """Test auto-calculated rows."""
    print("\n=== TEST 6: Auto Rows ===")
    
    compiler = UICompiler(1280, 720)
    
    # Container: 400x800, 3 columns (rows auto-calculated)
    grid = GridContainer(
        width=px(400),
        height=px(800),
        columns=3
        # rows=None (auto)
    )
    
    # Add 10 children (will make 4 rows: 3+3+3+1)
    for i in range(10):
        child = UIComponent(width=px(50), height=px(50))
        grid.add_child(child)
    
    compiler.compile_component(grid)
    
    # Auto rows: ceil(10 / 3) = 4 rows
    # Cell height: 800 / 4 = 200px
    print(f"Grid: 400x800, 3 columns, 10 children")
    print(f"Auto rows: 4 (ceil(10/3))")
    print(f"Cell height: 200px")
    
    assert grid.children[0].compiled_height == 200
    assert grid.children[9].compiled_y == 600  # 4th row (3 * 200)
    
    print("✅ Auto rows work!")


def test_grid_single_column():
    """Test single-column grid (vertical list)."""
    print("\n=== TEST 7: Single Column (List) ===")
    
    compiler = UICompiler(1280, 720)
    
    # Container: 200x600, 1 column
    grid = GridContainer(
        width=px(200),
        height=px(600),
        columns=1
    )
    
    # Add 3 children (stacked vertically)
    for i in range(3):
        child = UIComponent(width=px(50), height=px(50))
        grid.add_child(child)
    
    compiler.compile_component(grid)
    
    # Single column: all X=0, Y increases
    print(f"Grid: 200x600, 1 column, 3 children")
    print(f"Vertical stack")
    
    assert grid.children[0].compiled_x == 0
    assert grid.children[1].compiled_x == 0
    assert grid.children[2].compiled_x == 0
    
    assert grid.children[0].compiled_y == 0
    assert grid.children[1].compiled_y == 200
    assert grid.children[2].compiled_y == 400
    
    print("✅ Single column grid works!")


def main():
    """Run all tests."""
    print("╔═══════════════════════════════════════════════════╗")
    print("║  GRIDCONTAINER TESTS                              ║")
    print("╚═══════════════════════════════════════════════════╝")
    
    try:
        test_grid_basic()
        test_grid_with_gap()
        test_grid_2_columns()
        test_grid_responsive()
        test_grid_different_gaps()
        test_grid_auto_rows()
        test_grid_single_column()
        
        print("\n" + "="*60)
        print("✨ ALL TESTS PASSED! ✨")
        print("="*60)
        print("\nGridContainer is working correctly!")
        print("You can now use:")
        print("  - GridContainer(columns=3, gap=px(10))")
        print("  - Auto-calculated rows based on children")
        print("  - Separate column_gap and row_gap")
        print("  - Works with responsive units (vw, vh, etc.)")
        print("\nAutomatic 2D grid layouts! 🎉")
        
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


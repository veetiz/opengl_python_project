"""
Complete Demo: All CSS-like Sizing Features
Showcases: px, %, vw, vh, rem, em, calc, min/max, aspect ratio, flex, grid
"""

import sys
from engine.src.ui import (
    UIComponent, UICompiler,
    FlexContainer, GridContainer,
    px, percent, vw, vh, rem, em, calc
)


def demo_all_units():
    """Demo all 7 unit types."""
    print("\n" + "="*70)
    print("🎨 DEMO: ALL 7 UNIT TYPES")
    print("="*70)
    
    compiler = UICompiler(1280, 720, root_font_size=16.0)
    
    # Create components with each unit type
    components = {
        "px": UIComponent(width=px(200)),
        "%": UIComponent(width=percent(50)),
        "vw": UIComponent(width=vw(30)),
        "vh": UIComponent(height=vh(20)),
        "rem": UIComponent(font_size=rem(2)),
        "em": UIComponent(font_size=em(1.5)),
        "calc": UIComponent(width=calc(vw(100), px(-40)))
    }
    
    # Compile and display
    for name, comp in components.items():
        compiler.compile_component(comp)
        if name in ["px", "%", "vw", "calc"]:
            print(f"   {name:6s}: {comp.compiled_width:8.1f}px")
        elif name == "vh":
            print(f"   {name:6s}: {comp.compiled_height:8.1f}px")
        else:  # rem, em
            print(f"   {name:6s}: {comp.compiled_font_size:8.1f}px")
    
    print("\n✅ All units working!\n")


def demo_constraints():
    """Demo min/max and aspect ratio."""
    print("="*70)
    print("📏 DEMO: CONSTRAINTS & ASPECT RATIOS")
    print("="*70)
    
    compiler = UICompiler(1280, 720)
    
    # Responsive with constraints
    modal = UIComponent(
        width=vw(50),        # 640px
        min_width=px(200),
        max_width=px(800)
    )
    compiler.compile_component(modal)
    print(f"   Modal: vw(50) = {modal.compiled_width}px (constrained 200-800)")
    
    # Aspect ratio
    video = UIComponent(
        width=px(800),
        aspect_ratio=16/9
    )
    compiler.compile_component(video)
    print(f"   Video: 800px wide, 16:9 → {video.compiled_height:.1f}px tall")
    
    # Combined
    image = UIComponent(
        width=vw(30),
        min_width=px(200),
        max_width=px(500),
        aspect_ratio=1.0  # Square
    )
    compiler.compile_component(image)
    print(f"   Image: {image.compiled_width:.1f}x{image.compiled_height:.1f}px (square, constrained)")
    
    print("\n✅ Constraints working!\n")


def demo_calc():
    """Demo calc function."""
    print("="*70)
    print("🧮 DEMO: CALC FUNCTION")
    print("="*70)
    
    compiler = UICompiler(1280, 720)
    
    # Full width minus padding
    full_minus = UIComponent(width=calc(vw(100), px(-40)))
    compiler.compile_component(full_minus)
    print(f"   Full - padding: calc(vw(100), px(-40)) = {full_minus.compiled_width}px")
    
    # Centered element
    centered = UIComponent(x=calc(vw(50), px(-150)), width=px(300))
    compiler.compile_component(centered)
    print(f"   Centered 300px: calc(vw(50), px(-150)) = {centered.compiled_x}px")
    
    # Nested calc
    nested = UIComponent(width=calc(calc(vw(50), px(100), '+'), 1.5, '*'))
    compiler.compile_component(nested)
    print(f"   Nested: (50vw + 100px) * 1.5 = {nested.compiled_width}px")
    
    print("\n✅ Calc working!\n")


def demo_typography():
    """Demo rem/em units."""
    print("="*70)
    print("📝 DEMO: TYPOGRAPHY (REM/EM)")
    print("="*70)
    
    compiler = UICompiler(1280, 720, root_font_size=16.0)
    
    # Typography scale with rem
    h1 = UIComponent(font_size=rem(3))
    h2 = UIComponent(font_size=rem(2.4))
    body = UIComponent(font_size=rem(1))
    small = UIComponent(font_size=rem(0.875))
    
    compiler.compile_component(h1)
    compiler.compile_component(h2)
    compiler.compile_component(body)
    compiler.compile_component(small)
    
    print(f"   H1:    rem(3)     = {h1.compiled_font_size}px")
    print(f"   H2:    rem(2.4)   = {h2.compiled_font_size}px")
    print(f"   Body:  rem(1)     = {body.compiled_font_size}px")
    print(f"   Small: rem(0.875) = {small.compiled_font_size}px")
    
    # Em with parent
    parent = UIComponent(font_size=px(20))
    compiler.compile_component(parent)
    child = UIComponent(font_size=em(1.5))
    parent.add_child(child)
    compiler.compile_component(parent)
    
    print(f"\n   Parent: 20px, Child: em(1.5) = {child.compiled_font_size}px")
    
    print("\n✅ Typography working!\n")


def demo_flexbox():
    """Demo FlexContainer."""
    print("="*70)
    print("🔄 DEMO: FLEXBOX LAYOUT")
    print("="*70)
    
    compiler = UICompiler(1280, 720)
    
    # Horizontal row with space-between
    row = FlexContainer(
        width=px(600),
        height=px(100),
        direction="row",
        justify="space-between"
    )
    
    # Add 3 buttons
    for i in range(3):
        btn = UIComponent(width=px(150), height=px(50))
        row.add_child(btn)
    
    compiler.compile_component(row)
    
    print(f"   Flex Row (space-between):")
    print(f"   Button positions: {[c.compiled_x for c in row.children]}")
    print(f"   (Auto-spaced at start, middle, end)")
    
    # Vertical column with gap
    column = FlexContainer(
        width=px(200),
        height=px(300),
        direction="column",
        gap=px(20)
    )
    
    for i in range(3):
        item = UIComponent(width=px(180), height=px(50))
        column.add_child(item)
    
    compiler.compile_component(column)
    
    print(f"\n   Flex Column (20px gap):")
    print(f"   Item positions: {[c.compiled_y for c in column.children]}")
    print(f"   (Auto-stacked with gaps)")
    
    print("\n✅ Flexbox working!\n")


def demo_grid():
    """Demo GridContainer."""
    print("="*70)
    print("📐 DEMO: GRID LAYOUT")
    print("="*70)
    
    compiler = UICompiler(1280, 720)
    
    # 3x3 grid
    grid = GridContainer(
        width=px(620),
        height=px(620),
        columns=3,
        gap=px(10)
    )
    
    # Add 9 items
    for i in range(9):
        item = UIComponent(width=px(50), height=px(50))
        grid.add_child(item)
    
    compiler.compile_component(grid)
    
    print(f"   3x3 Grid (10px gap):")
    print(f"   Cell size: {grid.children[0].compiled_width:.0f}x{grid.children[0].compiled_height:.0f}px")
    print(f"   First row X: {[grid.children[i].compiled_x for i in range(3)]}")
    print(f"   First col Y: {[grid.children[i*3].compiled_y for i in range(3)]}")
    print(f"   (Auto-arranged in perfect grid)")
    
    print("\n✅ Grid working!\n")


def demo_real_world_layout():
    """Demo a real-world responsive layout."""
    print("="*70)
    print("🎮 DEMO: REAL-WORLD RESPONSIVE LAYOUT")
    print("="*70)
    print("\nBuilding a responsive game UI...")
    
    compiler = UICompiler(1280, 720, root_font_size=16.0)
    
    # Main container (full screen flex)
    main = FlexContainer(
        width=vw(100),
        height=vh(100),
        direction="column"
    )
    
    # Header (full width, fixed height)
    header = FlexContainer(
        width=vw(100),
        height=px(60),
        direction="row",
        justify="space-between",
        align="center"
    )
    main.add_child(header)
    
    # Content area (flex row)
    content = FlexContainer(
        width=vw(100),
        height=calc(vh(100), px(-120)),  # Full - header - footer
        direction="row"
    )
    
    # Sidebar (20% of screen, constrained)
    sidebar = UIComponent(
        width=vw(20),
        min_width=px(200),
        max_width=px(300)
    )
    content.add_child(sidebar)
    
    # Main content (remaining space)
    main_content = GridContainer(
        width=calc(vw(80), px(-40)),  # Remaining - padding
        columns=3,
        gap=px(20)
    )
    
    # Add 6 cards with aspect ratios
    for i in range(6):
        card = UIComponent(
            aspect_ratio=4/3,
            min_width=px(180)
        )
        main_content.add_child(card)
    
    content.add_child(main_content)
    main.add_child(content)
    
    # Footer (full width, fixed height)
    footer = UIComponent(
        width=vw(100),
        height=px(60)
    )
    main.add_child(footer)
    
    # Compile everything
    compiler.compile_component(main)
    
    print(f"\n   ✓ Header: {header.compiled_width:.0f}x{header.compiled_height:.0f}px")
    print(f"   ✓ Sidebar: {sidebar.compiled_width:.0f}px (constrained 200-300)")
    print(f"   ✓ Main Content: {main_content.compiled_width:.0f}px (calc'd)")
    print(f"   ✓ Grid: 3 columns, 6 cards auto-arranged")
    print(f"   ✓ Cards: {main_content.children[0].compiled_width:.0f}x{main_content.children[0].compiled_height:.0f}px (4:3 aspect)")
    print(f"   ✓ Footer: {footer.compiled_width:.0f}x{footer.compiled_height:.0f}px")
    
    print("\n✨ Complete responsive layout working!\n")


def main():
    """Run all demos."""
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║                                                            ║")
    print("║       CSS-LIKE SIZING SYSTEM - COMPLETE DEMO               ║")
    print("║                                                            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    try:
        demo_all_units()
        demo_constraints()
        demo_calc()
        demo_typography()
        demo_flexbox()
        demo_grid()
        demo_real_world_layout()
        
        print("="*70)
        print("✨ ALL FEATURES DEMONSTRATED! ✨")
        print("="*70)
        print("\nYour UI system has:")
        print("  ✓ 7 unit types (px, %, vw, vh, rem, em, calc)")
        print("  ✓ Min/max constraints")
        print("  ✓ Aspect ratios")
        print("  ✓ Automatic flexbox layouts")
        print("  ✓ Automatic grid layouts")
        print("\n🎉 World-class UI system ready to use! 🎉\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())


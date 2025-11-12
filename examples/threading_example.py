"""
Threading Manager Examples
Demonstrates multithreading for rendering and asset loading.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from engine.src.systems.threading_manager import ThreadingManager, TaskPriority
from engine.src.systems.asset_loader import AssetLoader
import time
import random


def simulate_asset_load(path: str):
    """Simulate loading an asset."""
    time.sleep(random.uniform(0.1, 0.3))  # Simulate I/O
    return f"Asset({path})"


def simulate_mesh_update(mesh_id: int):
    """Simulate updating a mesh."""
    time.sleep(0.01)  # Simulate processing
    return f"Mesh_{mesh_id}_updated"


def example_basic_threading():
    """Basic threading usage."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Task Submission")
    print("="*60)
    
    threading_mgr = ThreadingManager(num_workers=4)
    
    # Submit a task
    def heavy_computation(x):
        time.sleep(0.1)
        return x * x
    
    print("Submitting 10 tasks...")
    futures = []
    for i in range(10):
        future = threading_mgr.submit_task(heavy_computation, i)
        futures.append(future)
    
    # Wait and get results
    results = [f.result() for f in futures]
    print(f"Results: {results}")
    
    threading_mgr.print_stats()
    threading_mgr.shutdown()


def example_parallel_for():
    """Parallel processing of items."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Parallel For Loop")
    print("="*60)
    
    threading_mgr = ThreadingManager(num_workers=4)
    
    # Process multiple items in parallel
    meshes = list(range(20))
    
    print(f"Processing {len(meshes)} meshes in parallel...")
    start = time.time()
    results = threading_mgr.parallel_for(simulate_mesh_update, meshes)
    elapsed = time.time() - start
    
    print(f"Processed {len(results)} items in {elapsed:.3f}s")
    print(f"Average: {elapsed/len(results)*1000:.2f}ms per item")
    
    threading_mgr.shutdown()


def example_asset_loading():
    """Asynchronous asset loading."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Async Asset Loading")
    print("="*60)
    
    threading_mgr = ThreadingManager(num_workers=4)
    asset_loader = AssetLoader(threading_mgr, enable_cache=True)
    
    loaded_assets = []
    
    def on_asset_loaded(asset):
        loaded_assets.append(asset)
        print(f"  Loaded: {asset}")
    
    # Load multiple assets asynchronously
    assets = ["texture1.png", "texture2.png", "model.obj", "sound.wav"]
    
    print(f"Loading {len(assets)} assets asynchronously...")
    for path in assets:
        asset_loader.load(path, simulate_asset_load, callback=on_asset_loaded)
    
    # Wait for completion
    threading_mgr.wait_for_all()
    
    print(f"\nAll {len(loaded_assets)} assets loaded!")
    asset_loader.print_stats()
    
    threading_mgr.shutdown()


def example_batch_loading():
    """Batch asset loading."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Batch Asset Loading")
    print("="*60)
    
    threading_mgr = ThreadingManager(num_workers=4)
    asset_loader = AssetLoader(threading_mgr, enable_cache=True)
    
    # Prepare batch
    assets = [
        ("player_texture.png", simulate_asset_load),
        ("enemy_texture.png", simulate_asset_load),
        ("ground_texture.png", simulate_asset_load),
        ("player_model.obj", simulate_asset_load),
        ("enemy_model.obj", simulate_asset_load)
    ]
    
    def on_batch_complete(results):
        print(f"\n[OK] Batch complete! Loaded {len(results)} assets")
        for path, asset in results.items():
            print(f"  - {path}: {asset}")
    
    print(f"Loading {len(assets)} assets in batch...")
    start = time.time()
    asset_loader.load_batch(assets, callback=on_batch_complete)
    
    # Wait for completion
    threading_mgr.wait_for_all()
    elapsed = time.time() - start
    
    print(f"\nBatch loaded in {elapsed:.3f}s")
    print(f"Average: {elapsed/len(assets)*1000:.2f}ms per asset")
    
    asset_loader.print_stats()
    threading_mgr.shutdown()


def example_cache_performance():
    """Demonstrate cache performance."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Cache Performance")
    print("="*60)
    
    threading_mgr = ThreadingManager(num_workers=2)
    asset_loader = AssetLoader(threading_mgr, enable_cache=True)
    
    # Load same asset multiple times
    asset_path = "repeated_texture.png"
    
    print("First load (cache miss)...")
    start = time.time()
    threading_mgr.wait_for_all()
    asset1 = asset_loader.load(asset_path, simulate_asset_load)
    threading_mgr.wait_for_all()
    time1 = time.time() - start
    
    print(f"  Time: {time1*1000:.2f}ms")
    
    print("\nSecond load (cache hit)...")
    start = time.time()
    asset2 = asset_loader.load(asset_path, simulate_asset_load)
    time2 = time.time() - start
    
    print(f"  Time: {time2*1000:.2f}ms")
    print(f"  Speedup: {time1/time2 if time2 > 0 else 'Instant'}x faster")
    
    asset_loader.print_stats()
    threading_mgr.shutdown()


def example_performance_comparison():
    """Compare single-threaded vs multi-threaded performance."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Performance Comparison")
    print("="*60)
    
    assets = [f"asset_{i}.dat" for i in range(20)]
    
    # Single-threaded
    print("\nSingle-threaded loading:")
    threading_mgr_single = ThreadingManager(num_workers=1, enable_multithreading=False)
    asset_loader_single = AssetLoader(threading_mgr_single)
    
    start = time.time()
    for path in assets:
        asset_loader_single.load(path, simulate_asset_load)
    time_single = time.time() - start
    
    print(f"  Time: {time_single:.3f}s")
    print(f"  Throughput: {len(assets)/time_single:.1f} assets/sec")
    
    # Multi-threaded
    print("\nMulti-threaded loading (4 workers):")
    threading_mgr_multi = ThreadingManager(num_workers=4, enable_multithreading=True)
    asset_loader_multi = AssetLoader(threading_mgr_multi)
    
    start = time.time()
    for path in assets:
        asset_loader_multi.load(path, simulate_asset_load)
    threading_mgr_multi.wait_for_all()
    time_multi = time.time() - start
    
    print(f"  Time: {time_multi:.3f}s")
    print(f"  Throughput: {len(assets)/time_multi:.1f} assets/sec")
    
    # Comparison
    print(f"\n{'='*60}")
    print(f"SPEEDUP: {time_single/time_multi:.2f}x faster with multithreading!")
    print(f"{'='*60}")
    
    threading_mgr_multi.shutdown()


if __name__ == "__main__":
    print("\n" + "="*70)
    print(" THREADING & ASSET LOADING EXAMPLES")
    print("="*70)
    
    example_basic_threading()
    example_parallel_for()
    example_asset_loading()
    example_batch_loading()
    example_cache_performance()
    example_performance_comparison()
    
    print("\n" + "="*70)
    print(" ALL EXAMPLES COMPLETE")
    print("="*70 + "\n")


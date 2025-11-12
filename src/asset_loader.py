"""
Asset Loader Module
Asynchronous asset loading with caching and multithreading support.
"""

import os
from typing import Dict, Any, Optional, Callable, List
from pathlib import Path
from concurrent.futures import Future
import time


class AssetCache:
    """Cache for loaded assets to avoid duplicate loading."""
    
    def __init__(self, max_size_mb: int = 512):
        """
        Initialize asset cache.
        
        Args:
            max_size_mb: Maximum cache size in megabytes
        """
        self.max_size_mb = max_size_mb
        self.cache: Dict[str, Any] = {}
        self.load_times: Dict[str, float] = {}
        self.access_count: Dict[str, int] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get asset from cache."""
        if key in self.cache:
            self.access_count[key] = self.access_count.get(key, 0) + 1
            return self.cache[key]
        return None
    
    def put(self, key: str, asset: Any, load_time: float = 0.0):
        """Put asset in cache."""
        self.cache[key] = asset
        self.load_times[key] = load_time
        self.access_count[key] = 1
    
    def has(self, key: str) -> bool:
        """Check if asset is cached."""
        return key in self.cache
    
    def remove(self, key: str):
        """Remove asset from cache."""
        if key in self.cache:
            del self.cache[key]
            del self.load_times[key]
            del self.access_count[key]
    
    def clear(self):
        """Clear all cached assets."""
        self.cache.clear()
        self.load_times.clear()
        self.access_count.clear()
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        return {
            'cached_assets': len(self.cache),
            'total_accesses': sum(self.access_count.values()),
            'total_load_time': sum(self.load_times.values()),
            'cache_hits': sum(self.access_count.values()) - len(self.cache)
        }


class AssetLoader:
    """
    Asynchronous asset loader with caching and multithreading.
    Manages loading of textures, models, sounds, and other assets.
    """
    
    def __init__(self, threading_manager=None, enable_cache: bool = True):
        """
        Initialize asset loader.
        
        Args:
            threading_manager: ThreadingManager instance (optional)
            enable_cache: Enable asset caching
        """
        self.threading_manager = threading_manager
        self.cache_enabled = enable_cache
        
        # Asset cache
        self.cache = AssetCache() if enable_cache else None
        
        # Pending loads
        self.pending_loads: Dict[str, Future] = {}
        
        # Load callbacks
        self.load_callbacks: Dict[str, List[Callable]] = {}
        
        # Statistics
        self.stats = {
            'total_loaded': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'failed_loads': 0
        }
        
        print(f"[AssetLoader] Initialized (cache={enable_cache}, async={threading_manager is not None})")
    
    def load(
        self,
        asset_path: str,
        loader_func: Callable,
        force_reload: bool = False,
        callback: Optional[Callable] = None
    ) -> Any:
        """
        Load an asset (sync or async depending on threading manager).
        
        Args:
            asset_path: Path to asset file
            loader_func: Function to load the asset
            force_reload: Force reload even if cached
            callback: Callback when loaded (for async)
            
        Returns:
            Asset object (immediately if cached/sync, None if async)
            
        Example:
            # Synchronous
            texture = asset_loader.load("tex.png", Texture.load_from_file)
            
            # Asynchronous
            asset_loader.load(
                "model.obj",
                Model.load_from_file,
                callback=lambda model: scene.add(model)
            )
        """
        # Check cache
        if self.cache_enabled and not force_reload:
            cached = self.cache.get(asset_path)
            if cached is not None:
                self.stats['cache_hits'] += 1
                if callback:
                    callback(cached)
                return cached
            else:
                self.stats['cache_misses'] += 1
        
        # Check if already loading
        if asset_path in self.pending_loads:
            future = self.pending_loads[asset_path]
            if callback:
                # Add callback for when load completes
                if asset_path not in self.load_callbacks:
                    self.load_callbacks[asset_path] = []
                self.load_callbacks[asset_path].append(callback)
            return None if future else self.cache.get(asset_path)
        
        # Load asset
        if self.threading_manager and self.threading_manager.enabled:
            # Async loading
            return self._load_async(asset_path, loader_func, callback)
        else:
            # Sync loading
            return self._load_sync(asset_path, loader_func, callback)
    
    def _load_sync(
        self,
        asset_path: str,
        loader_func: Callable,
        callback: Optional[Callable] = None
    ) -> Any:
        """Load asset synchronously."""
        try:
            start_time = time.time()
            asset = loader_func(asset_path)
            load_time = time.time() - start_time
            
            # Cache it
            if self.cache_enabled:
                self.cache.put(asset_path, asset, load_time)
            
            # Stats
            self.stats['total_loaded'] += 1
            
            # Callback
            if callback:
                callback(asset)
            
            return asset
            
        except Exception as e:
            print(f"[AssetLoader] Failed to load {asset_path}: {e}")
            self.stats['failed_loads'] += 1
            return None
    
    def _load_async(
        self,
        asset_path: str,
        loader_func: Callable,
        callback: Optional[Callable] = None
    ) -> None:
        """Load asset asynchronously."""
        
        def async_loader():
            try:
                start_time = time.time()
                asset = loader_func(asset_path)
                load_time = time.time() - start_time
                
                # Cache it
                if self.cache_enabled:
                    self.cache.put(asset_path, asset, load_time)
                
                # Stats
                self.stats['total_loaded'] += 1
                
                # Execute callbacks
                if callback:
                    callback(asset)
                
                # Execute any queued callbacks
                if asset_path in self.load_callbacks:
                    for cb in self.load_callbacks[asset_path]:
                        cb(asset)
                    del self.load_callbacks[asset_path]
                
                # Remove from pending
                if asset_path in self.pending_loads:
                    del self.pending_loads[asset_path]
                
                return asset
                
            except Exception as e:
                print(f"[AssetLoader] Failed to load {asset_path}: {e}")
                self.stats['failed_loads'] += 1
                
                if asset_path in self.pending_loads:
                    del self.pending_loads[asset_path]
                
                return None
        
        future = self.threading_manager.load_asset_async(async_loader)
        self.pending_loads[asset_path] = future
        return None
    
    def load_batch(
        self,
        assets: List[tuple],
        callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Load multiple assets in parallel.
        
        Args:
            assets: List of (path, loader_func) tuples
            callback: Callback when all loaded
            
        Returns:
            Dictionary of {path: asset} (empty if async)
            
        Example:
            assets = [
                ("tex1.png", Texture.load_from_file),
                ("tex2.png", Texture.load_from_file),
                ("model.obj", Model.load_from_file)
            ]
            
            def on_all_loaded(assets):
                print(f"Loaded {len(assets)} assets!")
            
            asset_loader.load_batch(assets, callback=on_all_loaded)
        """
        if not self.threading_manager or not self.threading_manager.enabled:
            # Load synchronously
            results = {}
            for path, loader_func in assets:
                results[path] = self.load(path, loader_func)
            if callback:
                callback(results)
            return results
        
        # Load asynchronously
        results = {}
        loaded_count = [0]  # Use list for closure
        total = len(assets)
        
        def on_asset_loaded(path):
            def inner_callback(asset):
                results[path] = asset
                loaded_count[0] += 1
                
                # Check if all loaded
                if loaded_count[0] >= total and callback:
                    callback(results)
            return inner_callback
        
        for path, loader_func in assets:
            self.load(path, loader_func, callback=on_asset_loaded(path))
        
        return results
    
    def is_loading(self, asset_path: str) -> bool:
        """Check if an asset is currently loading."""
        return asset_path in self.pending_loads
    
    def get_pending_count(self) -> int:
        """Get number of pending asset loads."""
        return len(self.pending_loads)
    
    def get_stats(self) -> dict:
        """Get loading statistics."""
        stats = {
            'total_loaded': self.stats['total_loaded'],
            'cache_hits': self.stats['cache_hits'],
            'cache_misses': self.stats['cache_misses'],
            'failed_loads': self.stats['failed_loads'],
            'pending_loads': len(self.pending_loads),
            'cache_enabled': self.cache_enabled
        }
        
        if self.cache:
            stats.update(self.cache.get_stats())
        
        return stats
    
    def print_stats(self):
        """Print loading statistics."""
        stats = self.get_stats()
        print("\n" + "="*60)
        print("ASSET LOADER STATISTICS")
        print("="*60)
        print(f"Total Loaded: {stats['total_loaded']}")
        print(f"Cache Hits: {stats['cache_hits']}")
        print(f"Cache Misses: {stats['cache_misses']}")
        print(f"Failed Loads: {stats['failed_loads']}")
        print(f"Pending: {stats['pending_loads']}")
        if 'cached_assets' in stats:
            print(f"Cached Assets: {stats['cached_assets']}")
            print(f"Total Accesses: {stats['total_accesses']}")
        print("="*60 + "\n")
    
    def cleanup(self):
        """Clean up asset loader."""
        # Wait for pending loads
        if self.threading_manager:
            self.threading_manager.wait_for_all()
        
        # Clear cache
        if self.cache:
            self.cache.clear()
        
        self.pending_loads.clear()
        print("[AssetLoader] Cleaned up")


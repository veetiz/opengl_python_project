"""
Threading Manager Module
Manages multithreading for rendering, asset loading, and scene operations.
"""

import threading
import queue
import time
from typing import Callable, Any, Optional, List, Dict
from concurrent.futures import ThreadPoolExecutor, Future
from dataclasses import dataclass
from enum import Enum


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class Task:
    """Represents a task to be executed."""
    func: Callable
    args: tuple = ()
    kwargs: dict = None
    priority: TaskPriority = TaskPriority.NORMAL
    callback: Optional[Callable] = None
    
    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}
    
    def __lt__(self, other):
        """For priority queue sorting."""
        return self.priority.value > other.priority.value


class ThreadingManager:
    """
    Manages worker threads for various engine operations.
    Provides thread pools for asset loading, scene operations, and general tasks.
    """
    
    def __init__(self, num_workers: int = 4, enable_multithreading: bool = True):
        """
        Initialize the threading manager.
        
        Args:
            num_workers: Number of worker threads
            enable_multithreading: Enable/disable multithreading
        """
        self.num_workers = num_workers
        self.enabled = enable_multithreading
        
        # Thread pools
        self.asset_pool: Optional[ThreadPoolExecutor] = None
        self.scene_pool: Optional[ThreadPoolExecutor] = None
        self.general_pool: Optional[ThreadPoolExecutor] = None
        
        # Task queues (priority queues)
        self.asset_queue: queue.PriorityQueue = queue.PriorityQueue()
        self.scene_queue: queue.PriorityQueue = queue.PriorityQueue()
        
        # Active futures tracking
        self.active_futures: List[Future] = []
        
        # Statistics
        self.stats = {
            'assets_loaded': 0,
            'tasks_completed': 0,
            'total_time': 0.0
        }
        
        # Thread-safe locks
        self.lock = threading.Lock()
        
        # Initialize if enabled
        if self.enabled:
            self._initialize_pools()
        
        print(f"[Threading] Manager initialized: {num_workers} workers, enabled={enable_multithreading}")
    
    def _initialize_pools(self):
        """Initialize thread pools."""
        # Asset loading pool (I/O bound)
        self.asset_pool = ThreadPoolExecutor(
            max_workers=max(2, self.num_workers // 2),
            thread_name_prefix="asset_"
        )
        
        # Scene operations pool (CPU bound)
        self.scene_pool = ThreadPoolExecutor(
            max_workers=max(2, self.num_workers // 2),
            thread_name_prefix="scene_"
        )
        
        # General purpose pool
        self.general_pool = ThreadPoolExecutor(
            max_workers=self.num_workers,
            thread_name_prefix="worker_"
        )
        
        print(f"[Threading] Pools initialized")
    
    # === Asset Loading (Async I/O) ===
    
    def load_asset_async(
        self,
        loader_func: Callable,
        *args,
        callback: Optional[Callable] = None,
        priority: TaskPriority = TaskPriority.NORMAL,
        **kwargs
    ) -> Optional[Future]:
        """
        Load an asset asynchronously (texture, model, sound, etc.).
        
        Args:
            loader_func: Function to load the asset
            *args: Arguments for loader function
            callback: Optional callback when complete
            priority: Task priority
            **kwargs: Keyword arguments for loader function
            
        Returns:
            Future object or None if multithreading disabled
            
        Example:
            def load_texture(path):
                return Texture(path)
            
            future = threading_mgr.load_asset_async(
                load_texture, 
                "texture.png",
                callback=on_texture_loaded
            )
        """
        if not self.enabled:
            # Execute synchronously if multithreading disabled
            result = loader_func(*args, **kwargs)
            if callback:
                callback(result)
            return None
        
        def wrapped_loader():
            start_time = time.time()
            try:
                result = loader_func(*args, **kwargs)
                
                # Update stats
                with self.lock:
                    self.stats['assets_loaded'] += 1
                    self.stats['total_time'] += time.time() - start_time
                
                # Call callback on main thread (if provided)
                if callback:
                    # Note: Callback should be called on main thread for OpenGL operations
                    # Store result for main thread to process
                    callback(result)
                
                return result
            except Exception as e:
                print(f"[Threading] Error loading asset: {e}")
                return None
        
        future = self.asset_pool.submit(wrapped_loader)
        self.active_futures.append(future)
        return future
    
    def load_assets_batch(
        self,
        assets: List[tuple],
        callback: Optional[Callable] = None
    ) -> List[Future]:
        """
        Load multiple assets in parallel.
        
        Args:
            assets: List of (loader_func, args, kwargs) tuples
            callback: Optional callback when all complete
            
        Returns:
            List of Future objects
            
        Example:
            assets = [
                (load_texture, ("tex1.png",), {}),
                (load_model, ("model.obj",), {}),
                (load_sound, ("sound.wav",), {})
            ]
            futures = threading_mgr.load_assets_batch(assets)
        """
        futures = []
        for loader_func, args, kwargs in assets:
            future = self.load_asset_async(loader_func, *args, **kwargs)
            if future:
                futures.append(future)
        
        # Call callback when all complete
        if callback and futures:
            def check_completion():
                for f in futures:
                    f.result()  # Wait for completion
                callback()
            
            self.general_pool.submit(check_completion)
        
        return futures
    
    # === Scene Operations ===
    
    def process_scene_async(
        self,
        func: Callable,
        *args,
        callback: Optional[Callable] = None,
        **kwargs
    ) -> Optional[Future]:
        """
        Process scene operations asynchronously (culling, LOD, physics, etc.).
        
        Args:
            func: Function to execute
            *args: Arguments
            callback: Optional callback
            **kwargs: Keyword arguments
            
        Returns:
            Future object or None
            
        Example:
            future = threading_mgr.process_scene_async(
                scene.update_lod,
                camera_position
            )
        """
        if not self.enabled:
            result = func(*args, **kwargs)
            if callback:
                callback(result)
            return None
        
        def wrapped_func():
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                
                with self.lock:
                    self.stats['tasks_completed'] += 1
                    self.stats['total_time'] += time.time() - start_time
                
                if callback:
                    callback(result)
                
                return result
            except Exception as e:
                print(f"[Threading] Error in scene operation: {e}")
                return None
        
        future = self.scene_pool.submit(wrapped_func)
        self.active_futures.append(future)
        return future
    
    # === General Purpose ===
    
    def submit_task(
        self,
        func: Callable,
        *args,
        callback: Optional[Callable] = None,
        priority: TaskPriority = TaskPriority.NORMAL,
        **kwargs
    ) -> Optional[Future]:
        """
        Submit a general purpose task.
        
        Args:
            func: Function to execute
            *args: Arguments
            callback: Optional callback
            priority: Task priority
            **kwargs: Keyword arguments
            
        Returns:
            Future object or None
        """
        if not self.enabled:
            result = func(*args, **kwargs)
            if callback:
                callback(result)
            return None
        
        def wrapped_func():
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                
                with self.lock:
                    self.stats['tasks_completed'] += 1
                    self.stats['total_time'] += time.time() - start_time
                
                if callback:
                    callback(result)
                
                return result
            except Exception as e:
                print(f"[Threading] Error in task: {e}")
                return None
        
        future = self.general_pool.submit(wrapped_func)
        self.active_futures.append(future)
        return future
    
    # === Parallel Processing ===
    
    def parallel_for(
        self,
        func: Callable,
        items: List[Any],
        callback: Optional[Callable] = None
    ) -> List[Any]:
        """
        Process items in parallel (like OpenMP parallel for).
        
        Args:
            func: Function to apply to each item
            items: List of items to process
            callback: Optional callback when all complete
            
        Returns:
            List of results in same order as input
            
        Example:
            # Process all meshes in parallel
            def update_mesh(mesh):
                return mesh.update()
            
            results = threading_mgr.parallel_for(update_mesh, meshes)
        """
        if not self.enabled:
            return [func(item) for item in items]
        
        futures = [self.general_pool.submit(func, item) for item in items]
        results = [f.result() for f in futures]
        
        if callback:
            callback(results)
        
        return results
    
    # === Synchronization ===
    
    def wait_for_all(self, timeout: Optional[float] = None):
        """
        Wait for all pending tasks to complete.
        
        Args:
            timeout: Optional timeout in seconds
        """
        if not self.enabled:
            return
        
        # Clean up completed futures
        self.active_futures = [f for f in self.active_futures if not f.done()]
        
        # Wait for remaining
        for future in self.active_futures:
            try:
                future.result(timeout=timeout)
            except Exception as e:
                print(f"[Threading] Error waiting for task: {e}")
        
        self.active_futures.clear()
    
    def get_pending_count(self) -> int:
        """Get number of pending tasks."""
        if not self.enabled:
            return 0
        return len([f for f in self.active_futures if not f.done()])
    
    # === Statistics ===
    
    def get_stats(self) -> Dict[str, Any]:
        """Get threading statistics."""
        with self.lock:
            return {
                'enabled': self.enabled,
                'num_workers': self.num_workers,
                'assets_loaded': self.stats['assets_loaded'],
                'tasks_completed': self.stats['tasks_completed'],
                'total_time': self.stats['total_time'],
                'pending_tasks': self.get_pending_count(),
                'avg_task_time': (
                    self.stats['total_time'] / self.stats['tasks_completed']
                    if self.stats['tasks_completed'] > 0 else 0.0
                )
            }
    
    def print_stats(self):
        """Print threading statistics."""
        stats = self.get_stats()
        print("\n" + "="*60)
        print("THREADING STATISTICS")
        print("="*60)
        print(f"Enabled: {stats['enabled']}")
        print(f"Workers: {stats['num_workers']}")
        print(f"Assets Loaded: {stats['assets_loaded']}")
        print(f"Tasks Completed: {stats['tasks_completed']}")
        print(f"Pending Tasks: {stats['pending_tasks']}")
        print(f"Total Time: {stats['total_time']:.2f}s")
        print(f"Avg Task Time: {stats['avg_task_time']*1000:.2f}ms")
        print("="*60 + "\n")
    
    # === Cleanup ===
    
    def shutdown(self, wait: bool = True):
        """
        Shutdown all thread pools.
        
        Args:
            wait: Wait for tasks to complete
        """
        if not self.enabled:
            return
        
        print("[Threading] Shutting down thread pools...")
        
        if wait:
            self.wait_for_all()
        
        if self.asset_pool:
            self.asset_pool.shutdown(wait=wait)
        if self.scene_pool:
            self.scene_pool.shutdown(wait=wait)
        if self.general_pool:
            self.general_pool.shutdown(wait=wait)
        
        print("[Threading] Thread pools shut down")


# === Helper Functions ===

def is_main_thread() -> bool:
    """Check if currently on main thread."""
    return threading.current_thread() == threading.main_thread()


def get_thread_count() -> int:
    """Get number of active threads."""
    return threading.active_count()


def get_thread_name() -> str:
    """Get current thread name."""
    return threading.current_thread().name


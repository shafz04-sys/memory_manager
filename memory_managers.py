import copy
import random
import math

# ==========================================
#  ENGINE 1: CONTIGUOUS MEMORY (Variable Partition)
# ==========================================
class Block:
    def __init__(self, start, size, pid=None):
        self.start = start
        self.size = size
        self.pid = pid  # None = Free

    @property
    def end(self): return self.start + self.size
    def is_free(self): return self.pid is None

class ContiguousManager:
    def __init__(self, ram_size=500, disk_size=1000):
        self.ram_size = ram_size
        self.disk_size = disk_size
        self.ram_map = [Block(0, ram_size, None)]
        self.disk_map = [Block(0, disk_size, None)]
        self.log_func = None

    def log(self, msg):
        if self.log_func: self.log_func(msg)

    def _find_hole(self, m_map, size, algo):
        candidate = -1
        if algo == "First Fit":
            for i, b in enumerate(m_map):
                if b.is_free() and b.size >= size: return i
        elif algo == "Best Fit":
            best = float('inf')
            for i, b in enumerate(m_map):
                if b.is_free() and b.size >= size:
                    diff = b.size - size
                    if diff < best: best, candidate = diff, i
            return candidate
        elif algo == "Worst Fit":
            worst = -1
            for i, b in enumerate(m_map):
                if b.is_free() and b.size >= size:
                    diff = b.size - size
                    if diff > worst: worst, candidate = diff, i
            return candidate
        return -1

    def _insert(self, m_map, idx, pid, size):
        target = m_map[idx]
        new_b = Block(target.start, size, pid)
        rem = target.size - size
        m_map.pop(idx)
        m_map.insert(idx, new_b)
        if rem > 0: m_map.insert(idx+1, Block(new_b.end, rem, None))

    def allocate(self, pid, size, algo="First Fit"):
        # 1. Try RAM
        idx = self._find_hole(self.ram_map, size, algo)
        if idx != -1:
            self._insert(self.ram_map, idx, pid, size)
            self.log(f"✅ [RAM] Allocated {pid} ({size}KB)")
            return True
        
        # 2. Try Swapping
        self.log(f"⚠️ RAM Full. Attempting Swap...")
        active = [b for b in self.ram_map if not b.is_free()]
        for b in active:
            victim_pid, victim_size = b.pid, b.size
            d_idx = self._find_hole(self.disk_map, victim_size, "First Fit")
            if d_idx != -1:
                self.log(f"🔄 Swapping {victim_pid} to Disk...")
                self._insert(self.disk_map, d_idx, victim_pid, victim_size) # To Disk
                self.deallocate(victim_pid, target="RAM") # Clear RAM
                
                # Retry Allocation
                idx_retry = self._find_hole(self.ram_map, size, algo)
                if idx_retry != -1:
                    self._insert(self.ram_map, idx_retry, pid, size)
                    self.log(f"✅ Swapped & Allocated {pid} in RAM")
                    return True
        
        self.log("❌ Allocation Failed (RAM & Disk Full)")
        return False

    def deallocate(self, pid, target="BOTH"):
        def clear_map(m_map):
            found = False
            for b in m_map:
                if b.pid == pid:
                    b.pid = None
                    found = True
            # Coalesce
            i=0
            while i < len(m_map)-1:
                if m_map[i].is_free() and m_map[i+1].is_free():
                    m_map[i].size += m_map[i+1].size
                    m_map.pop(i+1)
                else: i+=1
            return found

        res_ram = clear_map(self.ram_map) if target in ["BOTH", "RAM"] else False
        res_disk = clear_map(self.disk_map) if target in ["BOTH", "DISK"] else False
        
        if res_ram or res_disk:
            if target == "BOTH": self.log(f"🗑️ Deallocated {pid}")
            return True
        return False

    def compact(self):
        self.log("⚙️ Compacting RAM...")
        active = [b for b in self.ram_map if not b.is_free()]
        new_map = []
        curr = 0
        for b in active:
            b.start = curr
            new_map.append(b)
            curr += b.size
        rem = self.ram_size - curr
        if rem > 0: new_map.append(Block(curr, rem, None))
        self.ram_map = new_map
        self.log("✅ Compaction Complete")


# ==========================================
#  ENGINE 2: PAGING MEMORY (Non-Contiguous)
# ==========================================
class PagingManager:
    def __init__(self, total_frames=50, frame_size=10):
        self.total_frames = total_frames 
        self.frame_size = frame_size
        # Frames: List of PIDs. None = Free
        self.frames = [None] * total_frames 
        self.page_table = {} # PID -> [Frame Indices]
        self.log_func = None

    def log(self, msg):
        if self.log_func: self.log_func(msg)

    def allocate(self, pid, size_kb):
        # Calculate needed frames
        needed = math.ceil(size_kb / self.frame_size)
        
        # Find free frames
        free_indices = [i for i, x in enumerate(self.frames) if x is None]
        
        if len(free_indices) < needed:
            self.log(f"❌ Paging Failed: Need {needed} frames, have {len(free_indices)}")
            return False
            
        # --- Random Selection for Visual Effect ---
        selected_frames = random.sample(free_indices, needed)
        selected_frames.sort() 
        
        for idx in selected_frames:
            self.frames[idx] = pid
            
        self.page_table[pid] = selected_frames
        self.log(f"✅ [Paging] {pid} allocated in frames: {selected_frames}")
        return True

    def deallocate(self, pid):
        if pid not in self.page_table:
            self.log(f"⚠️ Process {pid} not found")
            return
            
        # Free frames
        for idx in self.page_table[pid]:
            self.frames[idx] = None
            
        del self.page_table[pid]
        self.log(f"🗑️ Deallocated {pid} (Freed {len(self.frames)} frames)")
"""Approximate sampled RSS and system unified-memory pressure; never sums shared RSS."""
import threading,psutil,time
class Sampler:
    def __init__(self):self.stop=threading.Event();self.peaks={};self.available_min=None;self.system_used_max=0;self.started=time.perf_counter()
    def start(self):
        def sample():
            while not self.stop.is_set():
                vm=psutil.virtual_memory();self.available_min=vm.available if self.available_min is None else min(self.available_min,vm.available);self.system_used_max=max(self.system_used_max,vm.used)
                for p in psutil.process_iter(['pid','name','memory_info']):
                    try:
                        if p.pid==psutil.Process().pid or p.info['name'] in ('llama-server','ollama'):
                            key=f'{p.pid}:{p.info["name"]}';self.peaks[key]=max(self.peaks.get(key,0),p.info['memory_info'].rss)
                    except (psutil.NoSuchProcess,psutil.AccessDenied):pass
                self.stop.wait(.1)
        self.thread=threading.Thread(target=sample,daemon=True);self.thread.start();return self
    def finish(self):
        self.stop.set();self.thread.join()
        return {'sample_period_seconds':.1,'peak_rss_bytes_by_process':self.peaks,'minimum_system_available_bytes':self.available_min,'maximum_system_used_bytes':self.system_used_max,
            'wall_seconds':time.perf_counter()-self.started,'caveat':'Actual Mac unified memory; shared mappings prevent summing process RSS. System pressure includes unrelated applications. Samples can miss shorter peaks.'}

import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from turbodl.utils.logger import logger

class AutoTuner:
    """
    Advanced auto-tuning engine to optimize download configuration.
    """
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TurboDL/1.0'
        })

    def analyze_url(self, url):
        """
        Analyzes the URL to determine optimal download settings.
        Returns a dictionary with configuration.
        """
        logger.info(f"Analyzing URL: {url}")
        try:
            # 1. HEAD Request
            start_time = time.time()
            head = self.session.head(url, allow_redirects=True, timeout=10)
            latency = (time.time() - start_time) * 1000  # ms
            
            headers = head.headers
            file_size = int(headers.get('Content-Length', 0))
            accept_ranges = headers.get('Accept-Ranges', 'none') == 'bytes'
            etag = headers.get('ETag')
            
            logger.info(f"File Size: {file_size}, Accept-Ranges: {accept_ranges}, Latency: {latency:.2f}ms")

            if not accept_ranges or file_size == 0:
                return {
                    'connections': 1,
                    'split': 1,
                    'min_split_size': 0,
                    'supports_resume': False
                }

            # 2. Bandwidth Profiling (Range Probes)
            bandwidth_mbps = self._probe_bandwidth(url, file_size)
            logger.info(f"Estimated Bandwidth: {bandwidth_mbps:.2f} Mbps")

            # 3. Optimized Split Calculation
            # baseline_splits = clamp(int(bandwidth_mbps / 4), 2, 32)
            baseline_splits = max(2, min(int(bandwidth_mbps / 4), 32))
            
            # Adjust for latency
            if latency > 120:
                baseline_splits = int(baseline_splits * 0.6)
            
            # Ensure proper clamping after adjustment
            baseline_splits = max(2, min(baseline_splits, 32))
            
            # Segment size calculation: clamp(file_size / baseline_splits, 4MB, 128MB)
            # 4MB = 4 * 1024 * 1024
            min_seg = 4 * 1024 * 1024
            max_seg = 128 * 1024 * 1024
            
            calculated_seg_size = file_size / baseline_splits
            
            if calculated_seg_size < min_seg:
                # If segments act too small, reduce split count
                baseline_splits = max(1, int(file_size / min_seg))
            elif calculated_seg_size > max_seg:
                 # If segments are too huge, we might want more splits, but stick to max 32
                 pass

            logger.info(f"Optimal Splits: {baseline_splits}")

            return {
                'connections': baseline_splits,
                'split': baseline_splits,
                'min_split_size': str(min_seg),
                'supports_resume': True,
                'etag': etag
            }

        except Exception as e:
            logger.error(f"Error analyzing URL: {e}")
            return {'connections': 1, 'split': 1, 'min_split_size': '1M', 'supports_resume': False}

    def _probe_bandwidth(self, url, file_size):
        """
        Sends multiple small parallel range GET requests to estimate bandwidth.
        """
        probe_size = 512 * 1024 # 512KB
        num_probes = 4
        
        # Ensure we don't read past EOF
        if file_size < probe_size * num_probes:
             return 10.0 # Fallback for small files
             
        ranges = []
        for i in range(num_probes):
            start = i * probe_size
            end = start + probe_size - 1
            ranges.append((start, end))
            
        total_bytes = 0
        start_time = time.time()
        
        def fetch_range(r):
            headers = {'Range': f'bytes={r[0]}-{r[1]}'}
            try:
                resp = self.session.get(url, headers=headers, timeout=5, stream=True)
                # Actually read the content to measure throughput
                count = 0
                for _ in resp.iter_content(1024*32):
                    count += len(_)
                return count
            except:
                return 0

        with ThreadPoolExecutor(max_workers=num_probes) as executor:
            results = executor.map(fetch_range, ranges)
            total_bytes = sum(results)
            
        duration = time.time() - start_time
        if duration <= 0: duration = 0.01
        
        mbps = (total_bytes * 8) / (duration * 1000 * 1000)
        return mbps


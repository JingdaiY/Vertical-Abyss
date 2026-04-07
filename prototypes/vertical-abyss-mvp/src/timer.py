# PROTOTYPE - NOT FOR PRODUCTION
# Question: Does the core loop of descend -> scavenge -> escape feel engaging?
# Date: 2026-04-07

# 时间是这里唯一诚实的东西。它不会等你。
# Time is the only honest thing down here. It does not wait for you.


class CountdownTimer:
    """
    Counts down from `duration` seconds.
    Driven by delta-time in seconds (pass dt = clock.tick(FPS) / 1000.0).
    """

    def __init__(self, duration: float):
        self.duration  = duration
        self.remaining = duration
        self.running   = False

    # ── Control ────────────────────────────────────────────────────────────────

    def start(self):
        self.remaining = self.duration
        self.running   = True

    def stop(self):
        self.running = False

    def reset(self):
        self.remaining = self.duration
        self.running   = False

    # ── Update ─────────────────────────────────────────────────────────────────

    def tick(self, dt: float):
        """
        每一帧都在消耗你的时间。
        Every frame eats your time.
        """
        if self.running and self.remaining > 0:
            self.remaining -= dt
            if self.remaining < 0:
                self.remaining = 0

    # ── Query ──────────────────────────────────────────────────────────────────

    def is_expired(self) -> bool:
        return self.remaining <= 0

    def seconds_left(self) -> int:
        """Integer seconds for display."""
        return max(0, int(self.remaining))

    def fraction_remaining(self) -> float:
        """0.0 (empty) → 1.0 (full). Useful for bar rendering."""
        if self.duration <= 0:
            return 0.0
        return max(0.0, self.remaining / self.duration)

    def is_urgent(self) -> bool:
        """True when less than 15 seconds remain — time to run."""
        return self.remaining < 15.0

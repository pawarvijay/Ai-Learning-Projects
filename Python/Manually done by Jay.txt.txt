Here are the **Top 4** that represent 95% of real-world use:

| AnyIO API (Python) | Node.js Equivalent | What It Does |
| :--- | :--- | :--- |
| **`anyio.run(main)`** | Top-level `await main()` | Starts the event loop and executes your main async app. |
| **`anyio.create_task_group()`** | `Promise.all([p1, p2])` | Runs multiple async tasks concurrently and safely waits for all. |
| **`tg.start_soon(fn, arg)`** | `p1 = task1();` (unawaited call) | Spawns a background task inside the task group. |
| **`anyio.fail_after(seconds)`** | `AbortSignal.timeout(ms)` | Sets a strict timeout; cancels the task if it takes too long. |
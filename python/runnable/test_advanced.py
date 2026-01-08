import sys
import os
import asyncio
import time

# Add parent dir to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from runnable.lambda_runnable import RunnableLambda
from runnable.parallel import RunnableParallel
from runnable.retry import RunnableRetry

# --- Helpers ---
def sync_add(x):
    return x + 1

async def async_mul(x):
    await asyncio.sleep(0.1) # Simulate IO
    return x * 2

def fail_sometimes(x):
    if x < 0.5:
        raise ValueError("Fail!")
    return x

# --- Main Test ---
async def main():
    print("--- Testing Basic Chain ---")
    chain = RunnableLambda(sync_add) | RunnableLambda(async_mul)
    res = await chain.ainvoke(10) # (10+1)*2 = 22
    print(f"Result (10+1)*2: {res}")

    print("\n--- Testing Parallel ---")
    p_chain = RunnableParallel({
        "path1": RunnableLambda(sync_add),
        "path2": RunnableLambda(async_mul)
    })
    p_res = await p_chain.ainvoke(5)
    # path1: 5+1=6, path2: 5*2=10
    print(f"Parallel result (input 5): {p_res}")

    print("\n--- Testing Retry ---")
    # Wrap fail_sometimes method. 
    # Try input 0.1 (would fail) but with retry, well, it will always fail if deterministic.
    # Let's use a counter to fail only first time.
    
    class Flaky:
        def __init__(self):
            self.count = 0
        def run(self, x):
            self.count += 1
            if self.count < 3:
                print(f"  Attempt {self.count} failed...")
                raise ValueError("Temporary error")
            print(f"  Attempt {self.count} succeeded!")
            return x
            
    flaky = Flaky()
    retry_chain = RunnableRetry(RunnableLambda(flaky.run), max_retries=5, delay=0.1)
    
    print("Invoking retry chain...")
    r_res = retry_chain.invoke(100)
    print(f"Retry result: {r_res}")

if __name__ == "__main__":
    asyncio.run(main())

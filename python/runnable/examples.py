import sys
import os

# Add the parent directory to sys.path so we can import the 'runnable' package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from runnable.lambda_runnable import RunnableLambda

add_one = RunnableLambda(lambda x: x + 1)
mul_two = RunnableLambda(lambda x: x * 2)

chain = add_one | mul_two

print(chain.invoke(3))         # 8
print(chain.batch([1, 2, 3]))  # [4, 6, 8]
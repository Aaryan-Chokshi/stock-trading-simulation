# from circuitbreaker import circuit

# # Define a function that might fail
# @circuit
# def my_operation():
#     # Simulate a function that might fail
#     # print("Hello")
#     # import random
#     # if random.random() < 0.5:
#         raise Exception("Oops! Something went wrong.")
#     # else:
#     #     return "Success"

# # Execute the function that is wrapped with circuit breaker
# for _ in range(7):
#     try:
#         result = my_operation()
#         print("Result:", result)
#     except Exception as e:
#         print("Caught an exception:", e)


from circuitbreaker import circuit

@circuit(failure_threshold=2, recovery_timeout=5, fallback_function=lambda: "Fallback")
def my_operation():
    raise Exception("Oops! Something went wrong.")

# for _ in range(7):
#     try:
#         result = my_operation()
#         print("Result:", result)
#     except Exception as e:
#         print("Caught an exception:", e)

try:
    result = my_operation()
    print("Result:", result)
except Exception as e:
    print("Caught an exception:", e)
try:
    result = my_operation()
    print("Result:", result)
except Exception as e:
    print("Caught an exception:", e)

try:
    result = my_operation()
    # result = my_operation()
    # result = my_operation()
    print("Result:", result)
except Exception as e:
    print("Caught an exception:", e)

import time
time.sleep(5)
try:
    result = my_operation()
    print("Result:", result)
except Exception as e:
    print("Caught an exception:", e)
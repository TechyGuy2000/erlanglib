import math

def factorial(n):

    """
    Calculate factorial of n.
    """

    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def calculate_erlangs(call_duration_seconds, calls_per_second):

    """
    Calculate the traffic in Erlangs.

    Parameters:
    - call_duration_seconds (float): Average call duration in seconds.
    - calls_per_second (float): Calls initiated per second.

    Returns:
    - float: traffic in Erlangs
    """

    call_duration_hours = call_duration_seconds / 3600  # Convert call duration to hours
    calls_per_hour = calls_per_second * 3600  # Convert calls per second to calls per hour
    return call_duration_hours * calls_per_hour


def calls_per_second_from_erlangs(erlangs, call_duration_seconds):

    """
    Calculate calls per second given Erlangs and call duration.

    Parameters:
    - erlangs (float): Offered traffic in Erlangs.
    - call_duration_seconds (float): Average call duration in seconds.

    Returns:
    - float: Calls initiated per second.
    """

    call_duration_hours = call_duration_seconds / 3600
    calls_per_hour = erlangs / call_duration_hours
    return calls_per_hour / 3600


def call_duration_from_erlangs(erlangs, calls_per_second):

    """
    Calculate average call duration given Erlangs and calls per second.

    Parameters:
    - erlangs (float): Offered traffic in Erlangs.
    - calls_per_second (float): Calls initiated per second.

    Returns:
    - float: Average call duration in seconds.
    """

    calls_per_hour = calls_per_second * 3600
    return erlangs / calls_per_hour * 3600


def erlang_b(N, A):

    """
    Calculate the blocking probability using the Erlang B formula.

    Parameters:
    - N (int): number of channels
    - A (float): traffic load in Erlangs

    Returns:
    - float: blocking probability
    """

    B = ((A ** N) / (factorial(N))) / sum((A ** i) / factorial(i) for i in range(N + 1))
    return B


def required_channels(A, target_blocking):

    """
    Calculate the required number of channels for a given traffic and target blocking probability.

    Parameters:
    - A (float): traffic load in Erlangs
    - target_blocking (float): desired blocking probability

    Returns:
    - int: required number of channels
    """

    N = 1  # Start with 1 channel
    while True:
        blocking_probability = erlang_b(N, A)
        if blocking_probability <= target_blocking:
            return N
        N += 1


def calculate_erlangs_from_blocking(N, target_blocking, max_iterations=1000, tolerance=1e-6):

    """
    Calculate the traffic in Erlangs given the blocking probability and available lines.

    Parameters:
    - N (int): number of channels
    - target_blocking (float): desired blocking probability
    - max_iterations (int, optional): maximum iterations for the approximation. Default is 1000.
    - tolerance (float, optional): the difference in blocking probability to consider as converged. Default is 1e-6.

    Returns:
    - float: traffic in Erlangs
    """

    low, high = 0, N * 1000
    for _ in range(max_iterations):
        mid = (low + high) / 2.0
        current_blocking = erlang_b(N, mid)
        if abs(current_blocking - target_blocking) < tolerance:
            return mid
        elif current_blocking < target_blocking:
            low = mid
        else:
            high = mid
    return mid  # Return the last calculated value if not converged in max_iterations

def erlang_c(N, A):

    """
    Calculate the probability that a call is queued using the Erlang C formula.

    Parameters:
    - N (int): number of servers (agents)
    - A (float): traffic load in Erlangs

    Returns:
    - float: probability that a call is queued
    """

    numerator = (A ** N) / factorial(N) * N / (N - A)
    denominator_summation = sum((A ** i) / factorial(i) for i in range(N))
    denominator = denominator_summation + ((A ** N) / factorial(N)) * N / (N - A)
    return numerator / denominator

def service_level(N, A, Pw, target_time_seconds, AHT_seconds):

    """
    Calculate the service level given the probability a call is queued, number of agents, traffic in Erlangs, target answer time, and average handle time.

    Parameters:
    - N (int): number of servers (agents).
    - A (float): traffic load in Erlangs.
    - Pw (float): probability a call is queued.
    - target_time_seconds (float): desired answer time for the calls in seconds.
    - AHT_seconds (float): average handle time for the calls in seconds.

    Returns:
    - float: service level
    """

    exponent = - (N - A) * (target_time_seconds / AHT_seconds)
    return 1 - Pw * math.exp(exponent)

def average_speed_of_answer(N, A, Pw, average_handling_time):

    """
    Calculate the Average Speed of Answer (ASA) given the probability a call is queued, number of agents, traffic in Erlangs, and average handling time.

    Parameters:
    - N (int): number of servers (agents).
    - A (float): traffic load in Erlangs.
    - Pw (float): probability a call is queued.
    - average_handling_time (float): average duration for handling a call in seconds.

    Returns:
    - float: Average Speed of Answer in seconds
    """

    return (Pw * average_handling_time) / (N - A)

def immediate_answer_percentage(Pw):

    """
    Calculate the percentage of calls answered immediately given the probability a call is queued.

    Parameters:
    - Pw (float): probability a call is queued.

    Returns:
    - float: percentage of calls answered immediately
    """

    return (1 - Pw) * 100

def occupancy(A, N):

    """
    Calculate the Occupancy (Agent Utilization) given the traffic in Erlangs and the number of agents.

    Parameters:
    - A (float): traffic load in Erlangs.
    - N (int): number of servers (agents).

    Returns:
    - float: Occupancy (Agent Utilization) in percentage.
    """

    return (A / N) * 100

def required_agents(N_raw, shrinkage_percentage):

    """
    Calculate the number of agents required given the raw agents and shrinkage percentage.

    Parameters:
    - N_raw (int): number of raw agents.
    - shrinkage_percentage (float): shrinkage in percentage.

    Returns:
    - int: number of agents required.
    """

    return math.ceil(N_raw / (1 - shrinkage_percentage / 100))






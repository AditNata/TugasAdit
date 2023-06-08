import streamlit as st
import numpy as np

def north_west_corner_method(supply, demand, cost):
    supply = np.array(supply)
    demand = np.array(demand)
    cost = np.array(cost)
    m, n = cost.shape
    allocation = np.zeros((m, n))
    i, j = 0, 0
    while i < m and j < n:
        quantity = min(supply[i], demand[j])
        allocation[i, j] = quantity
        supply[i] -= quantity
        demand[j] -= quantity
        if supply[i] == 0:
            i += 1
        if demand[j] == 0:
            j += 1
    return allocation


def calculate_pert(tasks, optimistic_times, most_likely_times, pessimistic_times):
    expected_times = []
    variances = []
    std_deviations = []

    for i in range(len(tasks)):
        optimistic_time = optimistic_times[i]
        most_likely_time = most_likely_times[i]
        pessimistic_time = pessimistic_times[i]

        expected_time = (optimistic_time + 4 * most_likely_time + pessimistic_time) / 6
        variance = ((pessimistic_time - optimistic_time) / 6) ** 2
        std_deviation = np.sqrt(variance)

        expected_times.append(expected_time)
        variances.append(variance)
        std_deviations.append(std_deviation)

    return expected_times, variances, std_deviations


def main():

    activities = ["NWC for Transportation Problem","PERT Analysis"]	
    choice = st.sidebar.selectbox("Select Activities",activities)
    
    if choice == 'NWC for Transportation Problem':
        st.title("North-West Corner Method for Transportation Problem")
        m = st.number_input("Enter the number of sources (m):", min_value=1, step=1)
        n = st.number_input("Enter the number of destinations (n):", min_value=1, step=1)
        supply_str = st.text_input("Enter the supply for each source (separated by spaces):")
        demand_str = st.text_input("Enter the demand for each destination (separated by spaces):")
        cost_str = [st.text_input(f"Enter the cost matrix for source {i+1} (separated by spaces):") for i in range(m)]
        if not supply_str or not demand_str or not all(cost_str):
            st.error("Input cannot be empty")
            return
        supply = np.array(supply_str.split(), dtype=int)
        demand = np.array(demand_str.split(), dtype=int)
        cost = np.zeros((m, n))
        for i in range(m):
            cost[i] = np.array(cost_str[i].split(), dtype=int)
        if supply.shape != (m,) or demand.shape != (n,) or cost.shape != (m, n):
            st.error("Input format is incorrect")
            return
        allocation = north_west_corner_method(supply, demand, cost)
        st.write("Allocation matrix:\n", allocation)
        st.write("Total cost:", np.sum(allocation * cost))
    
    elif choice == 'PERT Analysis':
        st.title("PERT Analysis")

        st.header("Enter tasks and time estimates")
        tasks = st.text_area("Tasks (one per line)")
        optimistic_times = st.text_area("Optimistic Time Estimates (in days, one per line)")
        most_likely_times = st.text_area("Most Likely Time Estimates (in days, one per line)")
        pessimistic_times = st.text_area("Pessimistic Time Estimates (in days, one per line)")

        if st.button("Calculate Expected Time and Variance"):
            tasks = tasks.split("\n")
            optimistic_times = list(map(float, optimistic_times.split("\n")))
            most_likely_times = list(map(float, most_likely_times.split("\n")))
            pessimistic_times = list(map(float, pessimistic_times.split("\n")))

            expected_times, variances, std_deviations = calculate_pert(tasks, optimistic_times, most_likely_times, pessimistic_times)

            st.header("Expected Time Estimates")
            for i in range(len(tasks)):
                st.write(tasks[i] + ": " + str(expected_times[i]))

            st.header("Variance Estimates")
            for i in range(len(tasks)):
                st.write(tasks[i] + ": " + str(variances[i]))

            st.header("Standard Deviation")
            for i in range(len(tasks)):
                st.write(tasks[i] + ": " + str(std_deviations[i]))

            st.header("Expected Duration")
            expected_duration = sum(expected_times)
            st.write(expected_duration)

            # Find the critical path
            max_duration = max(expected_times)
            critical_path = []
            for i in range(len(tasks)):
                if expected_times[i] == max_duration:
                    critical_path.append(tasks[i])

            st.header("Critical Path")
            st.write(critical_path)

if __name__ == '__main__':
	main()
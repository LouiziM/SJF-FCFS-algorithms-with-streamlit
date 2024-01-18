import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


st.header("STR Simulation")

st.sidebar.header("Algorithms")

# Select algorithm
algorithme = st.sidebar.selectbox("Choose your algorithm", ["FCFS", "SJF","RM","DM"])

# Number of processes slider
num_processes = st.slider("Number of processes", 1, 10, 1)

processes_data = []

# Input data for each process
for i in range(num_processes):
    st.subheader(f"Process {i+1}")
    at = st.number_input(f'Arrival Time Process {i+1}', placeholder="Type a number...", key=f'at_{i}', max_value=20, min_value=0)
    bt = st.number_input(f'Burst Time Process {i+1}', placeholder="Type a number...", key=f'bt_{i}', max_value=20, min_value=0)
    dl = st.number_input(f'Deadline Process {i+1}', placeholder="Type a number...", key=f'dl_{i}', max_value=20, min_value=0)
    p = st.number_input(f'Period Process {i+1}', placeholder="Type a number...", key=f'p_{i}', max_value=20, min_value=0)

    processes_data.append({
        "at": at,
        "bt": bt,
        "dl": dl,
        "p": p,
        "pid": i + 1
    })

# Define a list of distinct colors for processes
colors = plt.cm.viridis(np.linspace(0, 1, num_processes))

def fcfs(processes_data):
    # Sort processes based on arrival time for FCFS
    processes_data.sort(key=lambda x: x["at"])
    current_time = 0
    waiting_times = []
    turnaround_times = []

    for i, process in enumerate(processes_data):
        if process["at"] > current_time:
            current_time = process["at"]
        
        waiting_times.append(max(0, current_time - process["at"]))
        current_time += process["bt"]
        turnaround_times.append(current_time - process["at"])

        # Display Gantt chart for each process with a different color
    gantt_chart(processes_data, waiting_times, turnaround_times, "FCFS", colors)

    # Display overall results
    st.write("Waiting Times:", waiting_times)
    st.write("Turnaround Times:", turnaround_times)
    st.write("Average Waiting Time:", sum(waiting_times) / len(waiting_times))
    st.write("Average Turnaround Time:", sum(turnaround_times) / len(turnaround_times))

    return waiting_times, turnaround_times

def sjf(processes_data):
    # Sort processes based on arrival time and burst time for SJF
    processes_data.sort(key=lambda x: (x["at"], x["bt"]))
    current_time = 0
    waiting_times = []
    turnaround_times = []

    for i, process in enumerate(processes_data):
        if process["at"] > current_time:
            current_time = process["at"]

        # Select the process with the shortest burst time
        next_process_index = i
        for j in range(i, len(processes_data)):
            if processes_data[j]["at"] <= current_time and processes_data[j]["bt"] < processes_data[next_process_index]["bt"]:
                next_process_index = j

        # Swap the selected process with the current process
        processes_data[i], processes_data[next_process_index] = processes_data[next_process_index], processes_data[i]

        waiting_times.append(max(0, current_time - process["at"]))
        current_time += process["bt"]
        turnaround_times.append(current_time - process["at"])

        # Display Gantt chart for each process with a different color
    gantt_chart(processes_data, waiting_times, turnaround_times, "SJF", colors)

    # Display overall results
    st.write("Waiting Times:", waiting_times)
    st.write("Turnaround Times:", turnaround_times)
    st.write("Average Waiting Time:", sum(waiting_times) / len(waiting_times))
    st.write("Average Turnaround Time:", sum(turnaround_times) / len(turnaround_times))

    return waiting_times, turnaround_times



def gantt_chart(processes_data, waiting_times, turnaround_times, algo_name, colors):
    fig, ax = plt.subplots()
    ax.set_title(f"Gantt Chart - {algo_name}")
    ax.set_xlabel("Time")
    ax.set_ylabel("Process")

    processes_data.sort(key=lambda x: x["at"])
    process_ids = [process["pid"] for process in processes_data]

    for i, process in enumerate(processes_data):
        if i < len(waiting_times):
            wait_time = waiting_times[i]
        else:
            wait_time = 0

        ax.barh(y=process["pid"], width=process["bt"], left=process["at"] + wait_time, color=colors[i], edgecolor='black')

    ax.set_yticks(process_ids)
    ax.invert_yaxis()
    ax.xaxis.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    st.pyplot(fig)





if algorithme == "FCFS":
    waiting_times, turnaround_times = fcfs(processes_data)
elif algorithme == "SJF":
    waiting_times, turnaround_times = sjf(processes_data)


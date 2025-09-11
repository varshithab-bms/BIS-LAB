import numpy as np

students_exams = {
    "S1": [0, 1],     
    "S2": [1, 2],     
    "S3": [0, 2, 3],  
}
num_exams = 4
num_slots = 3   
def fitness(schedule):
    penalty = 0
    for exams in students_exams.values():
        slots = [schedule[e] for e in exams]
        if len(slots) != len(set(slots)):
            penalty +=100
        slots_sorted = sorted(slots)
        for i in range(len(slots_sorted)-1):
            if slots_sorted[i+1] - slots_sorted[i] == 1:
                penalty += 10
    return penalty
    
def pso(num_particles=10, max_iter=50, w=0.5, c1=1.5, c2=1.5):
    positions = np.random.randint(0, num_slots, (num_particles, num_exams))
    velocities = np.zeros((num_particles, num_exams))
    
    pbest_positions = positions.copy()
    pbest_values = np.array([fitness(p) for p in positions])
    
    gbest_idx = np.argmin(pbest_values)
    gbest_position = pbest_positions[gbest_idx].copy()
    gbest_value = pbest_values[gbest_idx]
    
    for _ in range(max_iter):
        for i in range(num_particles):
            r1, r2 = np.random.rand(), np.random.rand()
            velocities[i] = (w * velocities[i] +
                             c1 * r1 * (pbest_positions[i] - positions[i]) +
                             c2 * r2 * (gbest_position - positions[i]))
            positions[i] = np.clip(np.round(positions[i] + velocities[i]), 0, num_slots-1).astype(int)
            
            val = fitness(positions[i])
            if val < pbest_values[i]:
                pbest_positions[i] = positions[i].copy()
                pbest_values[i] = val
        
        best_idx = np.argmin(pbest_values)
        if pbest_values[best_idx] < gbest_value:
            gbest_position = pbest_positions[best_idx].copy()
            gbest_value = pbest_values[best_idx]
    
    return gbest_position, gbest_value

best_schedule, best_penalty = pso()
print("Best Schedule (exam->slot):", best_schedule)
print("Penalty:", best_penalty)

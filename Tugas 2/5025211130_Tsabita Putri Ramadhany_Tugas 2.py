from matplotlib.offsetbox import AnchoredText
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from typing import List
import random
import numpy
import math

def get_city_coordinates() -> List[List[int]]:
    print("Masukkan koordinat kota (format: x,y). Masukkan 'selesai' jika sudah selesai.")
    city_coordinates = []
    while True:
        city_input = input()
        if city_input == "selesai":
            break
        try:
            x, y = map(int, city_input.split(","))
            city_coordinates.append([x, y])
        except ValueError:
            print("Format input salah. Masukkan input dalam format x,y.")
    return city_coordinates

koor_kota = get_city_coordinates()

kromosom_total = len(koor_kota) - 1

besar_populasi = int(input("Masukkan nilai besar populasi : "))
maks_generasi = int(input("Masukkan nilai generasi maksimal : "))
rasio_mutasi = float(input("Masukkan nilai rasio mutasi : "))
weakness = float(input("Masukkan nilai weakness : "))

class Genome():
    def __init__(self):
        self.kromosom = []
        self.fitness = 0

    def __str__(self):
        return "Chromosome: {0} Fitness: {1}\n".format(self.kromosom, self.fitness) 
    
    def __repr__(self):
        return str(self)

def create_genome() -> Genome:
    genome = Genome()
    
    genome.kromosom = random.sample(range(1, kromosom_total + 1), kromosom_total)
    genome.fitness = eval_kromosom(genome.kromosom)
    return genome

def distance(a, b) -> float:
    jarak = math.sqrt(((a[0] - b[0])**2) + ((a[1] - b[1])**2))
    return numpy.round(jarak, 2)

def get_fittest_genome(genomes: List[Genome]) -> Genome:
    genome_fitness = [genome.fitness for genome in genomes]
    return genomes[genome_fitness.index(min(genome_fitness))]

def eval_kromosom(kromosom: List[int]) -> float:
    arr = [0] * (len(kromosom) + 2)
    arr[1:-1] = kromosom

    fitness = 0
    for i in range(len(arr) - 1):
        p1 = koor_kota[arr[i]]
        p2 = koor_kota[arr[i + 1]]
        fitness += distance(p1, p2)
    return numpy.round(fitness, 2)

def tournament_selection(populasi:List[Genome], k:int) -> List[Genome]:
    selected_genomes = random.sample(populasi, k)
    selected_parent = get_fittest_genome(selected_genomes)
    return selected_parent

def order_crossover(parents: List[Genome]) -> Genome:
    child_chro = [-1] * kromosom_total

    subset_length = random.randrange(2, 5)
    crossover_point = random.randrange(0, kromosom_total - subset_length)

    child_chro[crossover_point:crossover_point+subset_length] = parents[0].kromosom[crossover_point:crossover_point+subset_length]

    j, k = crossover_point + subset_length, crossover_point + subset_length
    while -1 in child_chro:
        if parents[1].kromosom[k] not in child_chro:
            child_chro[j] = parents[1].kromosom[k]
            j = j+1 if (j != kromosom_total-1) else 0
        
        k = k+1 if (k != kromosom_total-1) else 0

    child = Genome()
    child.kromosom = child_chro
    child.fitness = eval_kromosom(child.kromosom)
    return child

def scramble_mutation(genome: Genome) -> Genome:
    subset_length = random.randint(2, 6)
    start_point = random.randint(0, kromosom_total - subset_length)
    subset_index = [start_point, start_point + subset_length]

    subset = genome.kromosom[subset_index[0]:subset_index[1]]
    random.shuffle(subset)

    genome.kromosom[subset_index[0]:subset_index[1]] = subset
    genome.fitness = eval_kromosom(genome.kromosom)
    return genome

def reproduction(population: List[Genome]) -> Genome:
    parents = [tournament_selection(population, 20), random.choice(population)] 

    child = order_crossover(parents)
    
    if random.random() < rasio_mutasi:
        scramble_mutation(child)

    return child

def visualisasi(all_fittest: List[Genome], all_pop_size: List[int]):
    fig = plt.figure(tight_layout=True, figsize=(12, 8))
    gs = gridspec.GridSpec(3, 1)

    kromosom = [0] * (len(all_fittest[-1].kromosom) + 2)
    kromosom[1:-1] = all_fittest[-1].kromosom
    koor = [koor_kota[i] for i in kromosom]
    x, y = zip(*koor)

    ax = fig.add_subplot(gs[0, :])
    ax.plot(x, y, color="darkolivegreen")
    ax.scatter(x, y, color="olive")

    for i, xy in enumerate(koor[:-1]):
        ax.annotate(i, xy, xytext=(-16, -4), textcoords="offset points", color="tab:brown")

    ax.set_title("Rute")
    ax.set_ylabel('Y')
    ax.set_xlabel('X')

    ax = fig.add_subplot(gs[1, :])
    all_fitness = [genome.fitness for genome in all_fittest]
    ax.plot(all_fitness, color="darkolivegreen")

    color = 'tab:brown'
    ax2 = ax.twinx()
    ax2.set_ylabel('Populasi', color=color)
    ax2.plot(all_pop_size, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    
    at = AnchoredText(
        "Best Fitness: {0}".format(all_fittest[-1].fitness), prop=dict(size=10), 
        frameon=True, loc='upper right')
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(at)
    
    ax.set_title("Fitness dan Besar Populasi")
    ax.set_ylabel("Fitness")
    ax.set_xlabel("Generasi")
    
    fig.align_labels()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    generasi = 0

    populasi = [create_genome() for x in range (besar_populasi)]

    all_fittest = []
    all_pop_size = []
    
    while generasi != maks_generasi:
        generasi += 1
        print("Generasi: {0} -- Besar Populasi: {1} -- Best Fitness: {2}"
            .format(generasi, len(populasi), get_fittest_genome(populasi).fitness))

        childs = []
        for x in range(int(besar_populasi * 0.2)):
            child = reproduction(populasi)
            childs.append(child)
        populasi.extend(childs)

        for genome in populasi:
            if genome.fitness > weakness:
                populasi.remove(genome)

        all_fittest.append(get_fittest_genome(populasi))
        all_pop_size.append(len(populasi))

    visualisasi(all_fittest, all_pop_size)
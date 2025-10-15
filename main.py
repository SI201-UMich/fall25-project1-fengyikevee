# Project 1: Penguin Data Analysis
# Team Members: Eve Feng, Alexia Zaidi
# 
# Function Attribution:
# - Eve: load_csv, count_island_gender, calculate_ratio, calculate_body_weights, also integrating the codes from eve and alexia (both main.py and test.py)
# - Alexia: count_total_penguins, count_species_by_island
# - Both: load_csv (the final version integrates our code) write_comprehensive_results, test cases for our own part of functions
#
# AI Tools Used: 
# Eve: used claude to ask it help load_csv function and write_comprehensive_results function; also use it to come up with edge cases for test cases.


import csv

# import data from csv file and data cleaning

def load_csv(penguins_file):
    """
    Load penguin data from a CSV file.
    
    Parameters:
        penguins_file (str): Path to the CSV file
    
    Returns:
        list: List of dictionaries, each representing a penguin record
    """
    penguins = []
    
    try:
        with open(penguins_file, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                penguin = {}
                
                for key, value in row.items():
                    # Skip the index column if it exists
                    if key == '' or key is None:
                        continue
                        
                    if key in ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']:
                        if value and value.strip() and value.strip().upper() != 'NA':
                            penguin[key] = float(value)
                        else: 
                            penguin[key] = None
                    elif key == 'year':
                        if value and value.strip() and value.strip().upper() != 'NA':
                            penguin[key] = int(value)
                        else: 
                            penguin[key] = None
                    else:
                        if value and value.strip().upper() != 'NA':
                            penguin[key] = value
                        else:
                            penguin[key] = ""
                
                penguins.append(penguin)
    except FileNotFoundError:
        print(f"Error: The file {penguins_file} was not found.")
    
    return penguins


# eve's part of analysis functions

def count_island_gender(penguins):
    """
    Count male and female penguins on each island.
    
    Parameters:
        penguins (list): List of penguin dictionaries
    
    Returns:
        dict: Dictionary with island names as keys and gender counts as values
    """
    counts = {}

    for penguin in penguins:
        island = penguin.get('island', '')
        sex = penguin.get('sex','')
        if not island or not sex:
            continue
        if island not in counts:
            counts[island] = {'male':0, 'female':0}
        if sex.lower() == 'male':
            counts[island]['male']+=1
        elif sex.lower() == 'female':
            counts[island]['female']+=1
    return counts


def calculate_ratio(counts):
    """
    Calculate male to female ratio for each island.
    
    Parameters:
        counts (dict): Dictionary of gender counts by island
    
    Returns:
        dict: Dictionary with island names as keys and ratios as values
    """
    ratios={}
    for island, gender_counts in counts.items():
        male_count = gender_counts.get('male',0)
        female_count = gender_counts.get ('female',0)

        if female_count == 0:
            if male_count == 0:
                ratios[island] = "No data"
            else:
                ratios[island] = "No females"
        else:
            ratio = male_count / female_count
            ratios[island] = round(ratio,2)

    return ratios


def calculate_body_weights(penguins):
    """
    Calculate average body weights by species, island, and gender.
    
    Parameters:
        penguins (list): List of penguin dictionaries
    
    Returns:
        dict: Nested dictionary with average weights
    """
    weights_data = {}
    
    for penguin in penguins:
        species = penguin.get('species','')
        island = penguin.get('island','')
        sex = penguin.get('sex','')
        body_mass = penguin.get('body_mass_g')

        if not species or not island or not sex or body_mass is None:
            continue

        if species not in weights_data:
            weights_data[species]= {}
        if island not in weights_data[species]:
            weights_data[species][island] = {}
        if sex not in weights_data[species][island]:
            weights_data[species][island][sex]=[]

        weights_data[species][island][sex].append(body_mass)

    weights_stats = {}
    
    for species, islands in weights_data.items():
        weights_stats[species] = {}
        for island,genders in islands.items():
            weights_stats[species][island] = {}
            for gender, weights in genders.items():
                if weights:
                    avg_weight = sum(weights)/len(weights)
                    weights_stats[species][island][gender]=round(avg_weight,2)
                else:
                    weights_stats[species][island][gender] = 'No data'
    return weights_stats


# alexia's part of analysis functions

def count_total_penguins(penguins):
    
    return len(penguins)


def count_species_by_island(penguins):

    species_data = {}
    
    for penguin in penguins:
        species = penguin.get('species', '').strip()
        island = penguin.get('island', '').strip()
        
        if not species or not island:
            continue
        
        if species not in species_data:
            species_data[species] = {'total': 0, 'islands': {}}
        
        species_data[species]['total'] += 1
        species_data[species]['islands'][island] = species_data[species]['islands'].get(island, 0) + 1
    
    return species_data


# output functions

def write_to_file(gender_stats, weight_stats, ratios, filename='penguin_analysis_results.txt'):

    with open(filename,'w') as file:
        file.write('='*60+'\n')
        file.write('Penguin Analysis Results\n')
        file.write('='*60+'\n\n')

        file.write('Gender distribution by island:\n')
        file.write('-'*30+'\n')
        for island, counts in sorted(gender_stats.items()):
            file.write(f"Island: {island}\n")
            file.write(f"  Males: {counts.get('male',0)}\n")
            file.write(f"  Females: {counts.get('female', 0)}\n")
            file.write(f"  Male:Female Ratio: {ratios.get(island, 'N/A')}\n")

        file.write("\n" + "=" * 60 + "\n")
        file.write("AVERAGE BODY WEIGHT (g) BY SPECIES, ISLAND, AND GENDER\n")
        file.write("-" * 30 + "\n")
        
        for species, islands in sorted(weight_stats.items()):
            file.write(f"\n{species}:\n")
            for island, genders in sorted(islands.items()):
                file.write(f"  {island}:\n")
                for gender in ['male', 'female']:
                    if gender in genders:
                        weight = genders[gender]
                        if weight != 'No data':
                            file.write(f"    {gender.capitalize()}: {weight} g\n")
                        else:
                            file.write(f"    {gender.capitalize()}: {weight}\n")
        
        file.write("\n" + "=" * 60 + "\n")
        file.write("Analysis complete.\n")


def write_comprehensive_results(total_count, species_data, gender_stats, ratios, 
                                 weight_stats, filename='comprehensive_penguin_analysis.txt'):

    with open(filename, 'w') as file:
        file.write('='*70+'\n')
        file.write('COMPREHENSIVE PENGUIN DATA ANALYSIS\n')
        file.write('='*70+'\n\n')
        
        # Section 1: Overall Summary
        file.write('DATASET OVERVIEW\n')
        file.write('-'*40+'\n')
        file.write(f'Total number of penguins: {total_count}\n')
        file.write(f'Number of species: {len(species_data)}\n')
        file.write(f'Number of islands: {len(gender_stats)}\n')
        file.write('\n')
        
        # Section 2: Species Distribution
        file.write('='*70+'\n')
        file.write('SPECIES DISTRIBUTION BY ISLAND\n')
        file.write('-'*40+'\n')
        
        for i, (species, info) in enumerate(sorted(species_data.items()), 1):
            file.write(f'\nSpecies {i}: {species}\n')
            file.write(f'  Total count: {info["total"]}\n')
            file.write(f'  Island distribution:\n')
            for island, count in sorted(info['islands'].items()):
                percentage = (count / info['total']) * 100
                file.write(f'    - {island}: {count} ({percentage:.1f}%)\n')
        
        # Section 3: Gender Distribution
        file.write('\n' + '='*70+'\n')
        file.write('GENDER DISTRIBUTION BY ISLAND\n')
        file.write('-'*40+'\n')
        for island, counts in sorted(gender_stats.items()):
            total_island = counts.get('male', 0) + counts.get('female', 0)
            file.write(f"\nIsland: {island}\n")
            file.write(f"  Males: {counts.get('male',0)}\n")
            file.write(f"  Females: {counts.get('female', 0)}\n")
            file.write(f"  Total: {total_island}\n")
            file.write(f"  Male:Female Ratio: {ratios.get(island, 'N/A')}\n")
        
        # Section 4: Body Weight Analysis
        file.write("\n" + "=" * 70 + "\n")
        file.write("AVERAGE BODY WEIGHT (g) BY SPECIES, ISLAND, AND GENDER\n")
        file.write("-" * 40 + "\n")
        
        for species, islands in sorted(weight_stats.items()):
            file.write(f"\n{species}:\n")
            for island, genders in sorted(islands.items()):
                file.write(f"  {island}:\n")
                for gender in ['male', 'female']:
                    if gender in genders:
                        weight = genders[gender]
                        if weight != 'No data':
                            file.write(f"    {gender.capitalize()}: {weight} g\n")
                        else:
                            file.write(f"    {gender.capitalize()}: {weight}\n")
        
        file.write("\n" + "=" * 70 + "\n")
        file.write("Analysis complete. Data processed successfully!\n")
        file.write("=" * 70 + "\n")

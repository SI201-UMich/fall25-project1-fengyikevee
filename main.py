import csv

def load_csv(penguins_file):
    
    penguins = []
    
    try:
        with open(penguins_file, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                penguin = {}  # Create ONE penguin dict per row
                
                for key, value in row.items():
                    if key in ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']:
                        if value and value.strip():
                            penguin[key] = float(value)
                        else: 
                            penguin[key] = None
                    elif key == 'year':
                        if value and value.strip():
                            penguin[key] = int(value)
                        else: 
                            penguin[key] = None
                    else:
                        penguin[key] = value if value else ""
                
                penguins.append(penguin)  # This line MUST be at same indent as penguin = {}
    except FileNotFoundError:
        print(f"Error: The file {penguins_file} was not found.")
    
    return penguins

   


def count_island_gender(penguins):

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

def write_to_file(gender_stats, weight_stats, ratios, filename='penguin_analysis_results.txt'):

    with open(filename,'w') as file:
        file.write('='*60+'\n')
        file.write('Penguin Analysis Results\n')
        file.write('='*60+'\n\n')

        file.write('Gender distribution by island:\n')
        file.write('-'*30+'\n')
        for island, counts in sorted(gender_stats.items()):
            file.write(f"Island: {island}\n")
            file.write(f' Males: {counts.get('male',0)}\n')
            file.write(f"  Females: {counts.get('female', 0)}\n")
            file.write(f"  Male:Female Ratio: {ratios.get(island, 'N/A')}\n")

        file.write("\n" + "=" * 60 + "\n")
        file.write("AVERAGE BODY WEIGHT (g) BY SPECIES, ISLAND, AND GENDER\n")
        file.write("-" * 30 + "\n")
        
        for species, islands in sorted(weight_stats.items()):
            file.write(f"\n{species}:\n")
            for island, genders in sorted(islands.items()):
                file.write(f"  {island}:\n")
                for gender in ['male', 'female']:  # Ensure consistent ordering
                    if gender in genders:
                        weight = genders[gender]
                        if weight != 'No data':
                            file.write(f"    {gender.capitalize()}: {weight} g\n")
                        else:
                            file.write(f"    {gender.capitalize()}: {weight}\n")
        
        file.write("\n" + "=" * 60 + "\n")
        file.write("Analysis complete.\n")
       
                       
        

                


    



    
    
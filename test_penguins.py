# Project 1: Penguin Data Analysis - Test File
# Team Members: Eve Feng, Alexia Zaidi
# 
# Test Function Attribution:
# - Eve: test_load_csv, test_count_island_gender, test_calculate_ratio, test_calculate_body_weights
# - Alexia: test_count_total_penguins, test_count_species_by_island, avg_bill_length
#


import os

from main import (load_csv, count_island_gender, calculate_ratio, 
                  calculate_body_weights, write_to_file,
                  count_total_penguins, count_species_by_island,
                  write_comprehensive_results, avg_bill_length)


# helper function to parse CSV string to dict
def parse_csv_string_to_dict(csv_string):
    parts = csv_string.split(',')
    # Clean up quotes and whitespace
    parts = [p.strip().strip('"') for p in parts]
    
    penguin = {
        'species': parts[1] if len(parts) > 1 else '',
        'island': parts[2] if len(parts) > 2 else '',
        'bill_length_mm': float(parts[3]) if len(parts) > 3 and parts[3] else None,
        'bill_depth_mm': float(parts[4]) if len(parts) > 4 and parts[4] else None,
        'flipper_length_mm': float(parts[5]) if len(parts) > 5 and parts[5] else None,
        'body_mass_g': float(parts[6]) if len(parts) > 6 and parts[6] else None,
        'sex': parts[7] if len(parts) > 7 else '',
        'year': int(parts[8]) if len(parts) > 8 and parts[8] else None
    }
    return penguin


# eve tests

def test_load_csv():
    print("Testing load_csv...")
    
    # Test 1: Valid CSV with all fields
    test_csv_content = """species,island,bill_length_mm,bill_depth_mm,flipper_length_mm,body_mass_g,sex,year
Adelie,Biscoe,37.8,18.3,174,3400,female,2007
Adelie,Biscoe,37.7,18.7,180,3600,male,2007
Gentoo,Dream,,,200,4500,male,2008
"""
    
    # Create test file using only open() 
    test_filename = 'test_data_1.csv'
    with open(test_filename, 'w') as f:
        f.write(test_csv_content)
    
    try:
        result = load_csv(test_filename)
        assert len(result) == 3, f"Should load 3 records, got {len(result)}"
        assert result[0]['species'] == 'Adelie', "Should load species correctly"
        assert result[0]['body_mass_g'] == 3400.0, "Should convert body_mass to float"
        assert result[0]['year'] == 2007, "Should convert year to int"
        assert result[2]['bill_length_mm'] is None, "Should handle empty numeric fields as None"
        print("✓ Test 1 passed: Valid CSV loads correctly")
    finally:
        # Clean up 
        if os.path.exists(test_filename):
            os.remove(test_filename)
    
    # Test 2: General case - verify all fields are loaded
    test_csv_content2 = """species,island,body_mass_g,sex,year
Chinstrap,Torgersen,3800,female,2009
"""
    test_filename2 = 'test_data_2.csv'
    with open(test_filename2, 'w') as f:
        f.write(test_csv_content2)
    
    try:
        result = load_csv(test_filename2)
        penguin = result[0]
        assert penguin['species'] == 'Chinstrap', "Species loaded"
        assert penguin['island'] == 'Torgersen', "Island loaded"
        assert penguin['body_mass_g'] == 3800.0, "Body mass loaded as float"
        assert penguin['sex'] == 'female', "Sex loaded"
        assert penguin['year'] == 2009, "Year loaded as int"
        print("✓ Test 2 passed: All fields loaded with correct types")
    finally:
        if os.path.exists(test_filename2):
            os.remove(test_filename2)
    
    # Test 3: Edge case - non-existent file
    result = load_csv('nonexistent_file_xyz.csv')
    assert result == [], "Non-existent file should return empty list"
    print("✓ Test 3 passed: Handles missing file")
    
    # Test 4: Edge case - empty values
    test_csv_empty = """species,island,body_mass_g,sex,year
Adelie,,,male,
"""
    test_filename3 = 'test_data_3.csv'
    with open(test_filename3, 'w') as f:
        f.write(test_csv_empty)
    
    try:
        result = load_csv(test_filename3)
        assert result[0]['island'] == "", "Empty string fields become empty strings"
        assert result[0]['body_mass_g'] is None, "Empty numeric fields become None"
        assert result[0]['year'] is None, "Empty year becomes None"
        print("✓ Test 4 passed: Handles empty values")
    finally:
        if os.path.exists(test_filename3):
            os.remove(test_filename3)


def test_count_island_gender():
    """Test the count_island_gender function."""
    print("\nTesting count_island_gender...")
    
    # Test 1: General case
    test_data = [
        {'island': 'Biscoe', 'sex': 'male'},
        {'island': 'Biscoe', 'sex': 'female'},
        {'island': 'Biscoe', 'sex': 'male'},
        {'island': 'Dream', 'sex': 'female'},
        {'island': 'Dream', 'sex': 'female'}
    ]
    result = count_island_gender(test_data)
    assert result['Biscoe']['male'] == 2, "Biscoe should have 2 males"
    assert result['Biscoe']['female'] == 1, "Biscoe should have 1 female"
    assert result['Dream']['male'] == 0, "Dream should have 0 males"
    assert result['Dream']['female'] == 2, "Dream should have 2 females"
    print("✓ Test 1 passed: Normal distribution counted")
    
    # Test 2: General case 
    test_data2 = [
        {'island': 'Torgersen', 'sex': 'Male'},
        {'island': 'Torgersen', 'sex': 'FEMALE'},
        {'island': 'Torgersen', 'sex': 'male'}
    ]
    result2 = count_island_gender(test_data2)
    assert result2['Torgersen']['male'] == 2, "Should handle case variations"
    assert result2['Torgersen']['female'] == 1, "Should handle uppercase FEMALE"
    print("✓ Test 2 passed: Case insensitive counting")
    
    # Test 3: Edge case - empty list
    result3 = count_island_gender([])
    assert result3 == {}, "Empty list returns empty dict"
    print("✓ Test 3 passed: Empty input handled")
    
    # Test 4: Edge case - missing data
    test_data4 = [
        {'island': '', 'sex': 'male'},      # Missing island
        {'island': 'Biscoe', 'sex': ''},    # Missing sex
        {'island': 'Dream', 'sex': 'other'}, # Invalid sex
        {'island': 'Dream', 'sex': 'male'}   # Valid entry
    ]
    result4 = count_island_gender(test_data4)
    assert len(result4) == 1, "Should only have one island"
    assert result4['Dream']['male'] == 1, "Should count valid entry"
    assert result4['Dream']['female'] == 0, "Should initialize female to 0"
    print("✓ Test 4 passed: Missing data handled")


def test_calculate_ratio():
    """Test the calculate_ratio function."""
    print("\nTesting calculate_ratio...")
    
    # Test 1: General case 
    test_counts = {
        'Biscoe': {'male': 100, 'female': 50},
        'Dream': {'male': 30, 'female': 40}
    }
    result = calculate_ratio(test_counts)
    assert result['Biscoe'] == 2.0, "100:50 ratio should be 2.0"
    assert result['Dream'] == 0.75, "30:40 ratio should be 0.75"
    print("✓ Test 1 passed: Normal ratios calculated")
    
    # Test 2: General case 
    test_counts2 = {
        'Island1': {'male': 25, 'female': 25},
        'Island2': {'male': 1, 'female': 1}
    }
    result2 = calculate_ratio(test_counts2)
    assert result2['Island1'] == 1.0, "Equal counts should give 1.0"
    assert result2['Island2'] == 1.0, "1:1 should be 1.0"
    print("✓ Test 2 passed: Equal ratios calculated")
    
    # Test 3: Edge case - division by zero
    test_counts3 = {
        'MaleOnly': {'male': 75, 'female': 0}
    }
    result3 = calculate_ratio(test_counts3)
    assert result3['MaleOnly'] == "No females", "Should handle no females"
    print("✓ Test 3 passed: Division by zero handled")
    
    # Test 4: Edge case - no penguins
    test_counts4 = {
        'Empty': {'male': 0, 'female': 0},
        'FemaleOnly': {'male': 0, 'female': 100}
    }
    result4 = calculate_ratio(test_counts4)
    assert result4['Empty'] == "No data", "0:0 should be 'No data'"
    assert result4['FemaleOnly'] == 0.0, "0:100 should be 0.0"
    print("✓ Test 4 passed: Edge cases handled")


def test_calculate_body_weights():
    """Test the calculate_body_weights function."""
    print("\nTesting calculate_body_weights...")
    
    # Test 1: General case 
    test_data = [
        {'species': 'Adelie', 'island': 'Biscoe', 'sex': 'male', 'body_mass_g': 4000.0},
        {'species': 'Adelie', 'island': 'Biscoe', 'sex': 'male', 'body_mass_g': 4100.0},
        {'species': 'Adelie', 'island': 'Biscoe', 'sex': 'male', 'body_mass_g': 4200.0},
        {'species': 'Adelie', 'island': 'Biscoe', 'sex': 'female', 'body_mass_g': 3600.0}
    ]
    result = calculate_body_weights(test_data)
    expected_male_avg = (4000 + 4100 + 4200) / 3
    assert result['Adelie']['Biscoe']['male'] == round(expected_male_avg, 2), "Male average should be 4100.0"
    assert result['Adelie']['Biscoe']['female'] == 3600.0, "Female average should be 3600.0"
    print("✓ Test 1 passed: Averages calculated correctly")
    
    # Test 2: General case 
    test_data2 = [
        {'species': 'Gentoo', 'island': 'Dream', 'sex': 'male', 'body_mass_g': 5000.0},
        {'species': 'Gentoo', 'island': 'Dream', 'sex': 'male', 'body_mass_g': 5200.0},
        {'species': 'Chinstrap', 'island': 'Torgersen', 'sex': 'female', 'body_mass_g': 3800.0}
    ]
    result2 = calculate_body_weights(test_data2)
    assert 'Gentoo' in result2, "Should have Gentoo species"
    assert 'Chinstrap' in result2, "Should have Chinstrap species"
    assert result2['Gentoo']['Dream']['male'] == 5100.0, "Gentoo average"
    assert result2['Chinstrap']['Torgersen']['female'] == 3800.0, "Chinstrap average"
    print("✓ Test 2 passed: Multiple species handled")
    
    # Test 3: Edge case - empty list
    result3 = calculate_body_weights([])
    assert result3 == {}, "Empty input returns empty dict"
    print("✓ Test 3 passed: Empty input handled")
    
    # Test 4: Edge case - missing values
    test_data4 = [
        {'species': 'Adelie', 'island': 'Biscoe', 'sex': 'male', 'body_mass_g': None},
        {'species': 'Adelie', 'island': 'Biscoe', 'sex': 'male', 'body_mass_g': 4000.0},
        {'species': '', 'island': 'Dream', 'sex': 'female', 'body_mass_g': 3500.0},
        {'species': 'Gentoo', 'island': '', 'sex': 'male', 'body_mass_g': 5000.0},
        {'species': 'Chinstrap', 'island': 'Dream', 'sex': '', 'body_mass_g': 3700.0}
    ]
    result4 = calculate_body_weights(test_data4)
    assert result4['Adelie']['Biscoe']['male'] == 4000.0, "Should skip None values"
    assert 'Gentoo' not in result4 or '' not in result4.get('Gentoo', {}), "Should skip empty islands"
    print("✓ Test 4 passed: Missing values handled")


# alexia's tests

def test_count_total_penguins():
    """Test the count_total_penguins function - Using teammate's test cases."""
    print("\nTesting count_total_penguins...")
    
    # Test 1: Single penguin (from teammate's test)
    test_data = [parse_csv_string_to_dict('"1","Adelie","Torgersen",39.1,18.7,181,3750,"male",2007')]
    result = count_total_penguins(test_data)
    assert result == 1, f"Should count 1 penguin, got {result}"
    print(" Test 1 passed: Single penguin counted")
    
    # Test 2: Empty list 
    test_data2 = []
    result2 = count_total_penguins(test_data2)
    assert result2 == 0, "Empty list should return 0"
    print(" Test 2 passed: Empty list handled")
    
    # Test 3: Two penguins 
    test_data3 = [
        parse_csv_string_to_dict('"1","Adelie","Torgersen",39.1,18.7,181,3750,"male",2007'),
        parse_csv_string_to_dict('"2","Adelie","Torgersen",39.5,17.4,186,3800,"female",2007')
    ]
    result3 = count_total_penguins(test_data3)
    assert result3 == 2, "Should count 2 penguins"
    print(" Test 3 passed: Two penguins counted")
    
    # Test 4: Three penguins 
    test_data4 = [
        parse_csv_string_to_dict('"1","Adelie","Torgersen",39.1,18.7,181,3750,"male",2007'),
        parse_csv_string_to_dict('"2","Adelie","Torgersen",39.5,17.4,186,3800,"female",2007'),
        parse_csv_string_to_dict('"3","Adelie","Torgersen",40.3,18,195,3250,"female",2007')
    ]
    result4 = count_total_penguins(test_data4)
    assert result4 == 3, "Should count 3 penguins"
    print(" Test 4 passed: Three penguins counted")


def test_count_species_by_island():
    """Test the count_species_by_island function - Using teammate's test cases."""
    print("\nTesting count_species_by_island...")
    
    # Test 1: Multiple species and islands (from teammate's test)
    test_data = [
        parse_csv_string_to_dict('"1","Adelie","Torgersen",39.1,18.7,181,3750,"male",2007'),
        parse_csv_string_to_dict('"2","Adelie","Torgersen",39.5,17.4,186,3800,"female",2007'),
        parse_csv_string_to_dict('"3","Adelie","Dream",37.8,18.3,174,3400,"female",2007'),
        parse_csv_string_to_dict('"4","Chinstrap","Dream",46.5,17.9,192,3500,"female",2007'),
        parse_csv_string_to_dict('"5","Gentoo","Biscoe",46.1,13.2,211,4500,"male",2007')
    ]
    result = count_species_by_island(test_data)
    expected = {
        "Adelie": {"total": 3, "islands": {"Torgersen": 2, "Dream": 1}},
        "Chinstrap": {"total": 1, "islands": {"Dream": 1}},
        "Gentoo": {"total": 1, "islands": {"Biscoe": 1}}
    }
    assert result == expected, f"Test 1 failed. Expected {expected}, got {result}"
    print(" Test 1 passed: Multiple species and islands counted correctly")
    
    # Test 2: Different distribution (from teammate's test)
    test_data2 = [
        parse_csv_string_to_dict('"10","Gentoo","Biscoe",45.2,14.8,215,4550,"male",2008'),
        parse_csv_string_to_dict('"11","Gentoo","Biscoe",45.0,14.9,210,4600,"female",2008'),
        parse_csv_string_to_dict('"12","Adelie","Dream",38.1,18.0,180,3400,"female",2008'),
        parse_csv_string_to_dict('"13","Chinstrap","Dream",46.8,17.5,195,3650,"male",2008')
    ]
    result2 = count_species_by_island(test_data2)
    expected2 = {
        "Gentoo": {"total": 2, "islands": {"Biscoe": 2}},
        "Adelie": {"total": 1, "islands": {"Dream": 1}},
        "Chinstrap": {"total": 1, "islands": {"Dream": 1}}
    }
    assert result2 == expected2, f"Test 2 failed. Expected {expected2}, got {result2}"
    print(" Test 2 passed: Different distribution calculated")
    
    # Test 3: Empty list (from teammate's test)
    test_data3 = []
    result3 = count_species_by_island(test_data3)
    expected3 = {}
    assert result3 == expected3, "Empty list should return empty dict"
    print(" Test 3 passed: Empty input handled")
    
    # Test 4: Whitespace handling (from teammate's test)
    test_data4 = [
        parse_csv_string_to_dict(' "21" ,  "Adelie" ,  "Torgersen" ,39.1,18.7,181,3750,"male",2007'),
        parse_csv_string_to_dict('"22","Adelie"," Torgersen " ,39.5,17.4,186,3800,"female",2007'),
        parse_csv_string_to_dict('"23","Adelie" , "Dream",37.8,18.3,174,3400,"female",2007'),
        parse_csv_string_to_dict('"24","Chinstrap"," Dream " ,46.5,17.9,192,3500,"female",2007'),
        parse_csv_string_to_dict('"25","Gentoo" , "Biscoe" ,46.1,13.2,211,4500,"male",2007')
    ]
    result4 = count_species_by_island(test_data4)
    expected4 = {
        "Adelie": {"total": 3, "islands": {"Torgersen": 2, "Dream": 1}},
        "Chinstrap": {"total": 1, "islands": {"Dream": 1}},
        "Gentoo": {"total": 1, "islands": {"Biscoe": 1}}
    }
    assert result4 == expected4, f"Test 4 failed. Expected {expected4}, got {result4}"
    print(" Test 4 passed: Whitespace handled correctly")


def test_avg_bill_length():
    """Test the avg_bill_length function."""
    print("\nTesting avg_bill_length...")

    # Test 1: General case - multiple species
    test_data1 = [
        parse_csv_string_to_dict('"1","Adelie","Biscoe",40.1,18.7,181,3750,"male",2007'),
        parse_csv_string_to_dict('"2","Adelie","Biscoe",39.9,18.2,180,3600,"female",2007'),
        parse_csv_string_to_dict('"3","Gentoo","Dream",46.3,14.8,215,4500,"male",2008'),
        parse_csv_string_to_dict('"4","Gentoo","Dream",45.7,14.5,210,4600,"female",2008')
    ]
    result1 = avg_bill_length(test_data1)
    assert result1['Adelie'] == 40.0, "Adelie average should be 40.0"
    assert result1['Gentoo'] == 46.0, "Gentoo average should be 46.0"
    print(" Test 1 passed: Correct averages for multiple species")

    # Test 2: Whitespace handling
    test_data2 = [
        parse_csv_string_to_dict('"5"," Adelie ","Biscoe",40.0,18.2,180,3600,"female",2007'),
        parse_csv_string_to_dict('"6"," Adelie ","Biscoe",41.0,18.2,180,3600,"male",2007')
    ]
    result2 = avg_bill_length(test_data2)
    assert 'Adelie' in result2, "Species name with whitespace should normalize"
    assert result2['Adelie'] == 40.5, "Average should be 40.5"
    print(" Test 2 passed: Whitespace handled correctly")

    # Edge Test 3: Missing values
    test_data3 = [
        parse_csv_string_to_dict('"7","Adelie","Biscoe",,18.7,181,3750,"male",2007'),
        parse_csv_string_to_dict('"8","Adelie","Biscoe",40.0,18.2,180,3600,"female",2007'),
        parse_csv_string_to_dict('"9","Chinstrap","Dream",,17.9,192,3500,"female",2007')
    ]
    result3 = avg_bill_length(test_data3)
    assert result3['Adelie'] == 40.0, "Should average only valid entry"
    assert 'Chinstrap' not in result3, "Species with all None values skipped"
    print(" Test 3 passed: Handles missing values")

    # Edge Test 4: Empty list
    result4 = avg_bill_length([])
    assert result4 == {}, "Empty input should return {}"
    print(" Test 4 passed: Handles empty input")

# main

def main():
    """Main function to run the penguin data analysis."""
    print("Starting Penguin Data Analysis...")
    print("-" * 40)
    
    # Run tests
    print("Running tests...")
    print("=" * 40)
    
    # eve tests
    test_load_csv()
    test_count_island_gender()
    test_calculate_ratio()
    test_calculate_body_weights()
    
    # alexia tests
    test_count_total_penguins()
    test_count_species_by_island()
    
    print("\n" + "=" * 40)
    print("All 24 tests passed! ✓")
    print("=" * 40)
    
    print("\n" + "=" * 40)
    print("Performing actual analysis...")
    print("-" * 40)
    
    # Load data
    penguins = load_csv('penguins.csv')
    
    if not penguins:
        print("Error: Could not load penguin data.")
        return
    
    print(f"Loaded {len(penguins)} penguin records.")
    
    # Perform all analyses
    
    # Analysis 1: Total count (teammate's function)
    total_count = count_total_penguins(penguins)
    print(f"Total penguins: {total_count}")
    
    # Analysis 2: Species by island (teammate's function)
    species_data = count_species_by_island(penguins)
    print(f"Analyzed {len(species_data)} species across multiple islands.")
    
    # Analysis 3: Gender distribution (your function)
    gender_counts = count_island_gender(penguins)
    print(f"Analyzed gender distribution across {len(gender_counts)} islands.")
    
    # Analysis 4: Gender ratios (your function)
    ratios = calculate_ratio(gender_counts)
    print("Calculated male:female ratios.")
    
    # Analysis 5: Body weights (your function)
    weight_stats = calculate_body_weights(penguins)
    print(f"Calculated body weight statistics for {len(weight_stats)} species.")
    
    # Write results to files
    
    # Original output (for backward compatibility with your tests)
    output_file1 = 'penguin_analysis_results.txt'
    write_to_file(gender_counts, weight_stats, ratios, output_file1)
    print(f"\nOriginal results written to '{output_file1}'")
    
    # Comprehensive output (combining both teammates' work)
    output_file2 = 'comprehensive_penguin_analysis.txt'
    write_comprehensive_results(total_count, species_data, gender_counts, 
                                 ratios, weight_stats, output_file2)
    print(f"Comprehensive results written to '{output_file2}'")
    
    print("\nAnalysis complete!")
    print("=" * 40)


if __name__ == "__main__":
    main()
    
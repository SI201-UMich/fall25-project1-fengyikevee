import tempfile
from main import load_csv, count_island_gender, calculate_ratio, calculate_body_weights, write_to_file


def test_load_csv():
    
    print("Testing load_csv...")
    
    
    import os
    
    test_csv_content = """species,island,bill_length_mm,bill_depth_mm,flipper_length_mm,body_mass_g,sex,year
Adelie,Biscoe,37.8,18.3,174,3400,female,2007
Adelie,Biscoe,37.7,18.7,180,3600,male,2007
Gentoo,Dream,,,200,4500,male,2008
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
        temp_file.write(test_csv_content)
        temp_filename = temp_file.name
    
    try:
        result = load_csv(temp_filename)
        assert len(result) == 3, f"Should load 3 records, got {len(result)}"
        assert result[0]['species'] == 'Adelie', "Should load species correctly"
        assert result[0]['body_mass_g'] == 3400.0, "Should convert body_mass to float"
        assert result[0]['year'] == 2007, "Should convert year to int"
        assert result[2]['bill_length_mm'] is None, "Should handle empty numeric fields as None"
        print("✓ Test 1 passed: Valid CSV loads correctly")
    finally:
        os.unlink(temp_filename)
    
    # Test 2: General case - verify all fields are loaded
    test_csv_content2 = """species,island,body_mass_g,sex,year
Chinstrap,Torgersen,3800,female,2009
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
        temp_file.write(test_csv_content2)
        temp_filename = temp_file.name
    
    try:
        result = load_csv(temp_filename)
        penguin = result[0]
        assert penguin['species'] == 'Chinstrap', "Species loaded"
        assert penguin['island'] == 'Torgersen', "Island loaded"
        assert penguin['body_mass_g'] == 3800.0, "Body mass loaded as float"
        assert penguin['sex'] == 'female', "Sex loaded"
        assert penguin['year'] == 2009, "Year loaded as int"
        print("✓ Test 2 passed: All fields loaded with correct types")
    finally:
        os.unlink(temp_filename)
    
    # Test 3: Edge case - non-existent file
    result = load_csv('nonexistent_file_xyz.csv')
    assert result == [], "Non-existent file should return empty list"
    print("✓ Test 3 passed: Handles missing file")
    
    # Test 4: Edge case - empty values
    test_csv_empty = """species,island,body_mass_g,sex,year
Adelie,,,male,
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
        temp_file.write(test_csv_empty)
        temp_filename = temp_file.name
    
    try:
        result = load_csv(temp_filename)
        assert result[0]['island'] == "", "Empty string fields become empty strings"
        assert result[0]['body_mass_g'] is None, "Empty numeric fields become None"
        assert result[0]['year'] is None, "Empty year becomes None"
        print("✓ Test 4 passed: Handles empty values")
    finally:
        os.unlink(temp_filename)


def test_count_island_gender():
    """Test the count_island_gender function."""
    print("\nTesting count_island_gender...")
    
    # Test 1: General case - normal distribution
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
    
    # Test 2: General case - case insensitive
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
    
    # Test 1: General case - normal ratios
    test_counts = {
        'Biscoe': {'male': 100, 'female': 50},
        'Dream': {'male': 30, 'female': 40}
    }
    result = calculate_ratio(test_counts)
    assert result['Biscoe'] == 2.0, "100:50 ratio should be 2.0"
    assert result['Dream'] == 0.75, "30:40 ratio should be 0.75"
    print("✓ Test 1 passed: Normal ratios calculated")
    
    # Test 2: General case - 1:1 ratio
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
    
    # Test 1: General case - calculate averages
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
    
    # Test 2: General case - multiple species/islands
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


def main():
    """Main function to run the penguin data analysis."""
    print("Starting Penguin Data Analysis...")
    print("-" * 40)
    
    # Run tests first
    print("Running tests...")
    test_load_csv()
    test_count_island_gender()
    test_calculate_ratio()
    test_calculate_body_weights()
    
    print("\n" + "=" * 40)
    print("Performing actual analysis...")
    print("-" * 40)
    
    # Load data
    penguins = load_csv('penguins.csv')
    
    if not penguins:
        print("Error: Could not load penguin data.")
        return
    
    print(f"Loaded {len(penguins)} penguin records.")
    
    # Perform analyses
    gender_counts = count_island_gender(penguins)
    print(f"Analyzed gender distribution across {len(gender_counts)} islands.")
    
    ratios = calculate_ratio(gender_counts)
    print("Calculated male:female ratios.")
    
    weight_stats = calculate_body_weights(penguins)
    print(f"Calculated body weight statistics for {len(weight_stats)} species.")
    
    # Write results to file
    output_file = 'penguin_analysis_results.txt'
    write_to_file(gender_counts, weight_stats, ratios, output_file)
    print(f"\nResults written to '{output_file}'")
    print("Analysis complete!")


if __name__ == "__main__":
    main()
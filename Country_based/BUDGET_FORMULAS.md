# Budget Allocation Formulas

## Spending Policy Calculation

### Step 1: Base Allocation
All four categories start with equal 25% allocation:

```
base_military = 25.0
base_healthcare = 25.0
base_education = 25.0
base_research_and_infra = 25.0
```

### Step 2: Random Variation
Each category gets unique random variation (±10%):

```
random_military = uniform(-10, 10)
random_healthcare = uniform(-10, 10)
random_education = uniform(-10, 10)
random_research = uniform(-10, 10)
```

### Step 3: Democracy Effect (Military Only)
More democratic countries spend less on military:

```
democracy_factor = (100 - democracy_index) / 100
military_adjustment = democracy_factor * 15

where:
- democracy_index = 0 to 100
- military_adjustment ranges from -15 (high democracy) to +15 (low democracy)
```

### Step 4: Age Distribution Effect (Healthcare Only)
Older populations need more healthcare:

```
elderly_percentage = elderly_population / total_population
healthcare_adjustment = elderly_percentage * 20

where:
- elderly_percentage = 0.0 to 1.0
- healthcare_adjustment ranges from 0 to +20
```

### Step 5: Apply Adjustments
Combine base, random, and adjustments:

```
military = base_military + random_military + military_adjustment
healthcare = base_healthcare + random_healthcare + healthcare_adjustment
education = base_education + random_education
research_and_infra = base_research_and_infra + random_research
```

### Step 6: Ensure Positive Values
All values must be at least 5%:

```
military = max(5, military)
healthcare = max(5, healthcare)
education = max(5, education)
research_and_infra = max(5, research_and_infra)
```

### Step 7: Auto-Normalize to 100%
Normalize so all four categories sum to exactly 100%:

```
total = military + healthcare + education + research_and_infra

military = (military / total) * 100
healthcare = (healthcare / total) * 100
education = (education / total) * 100
research_and_infra = (research_and_infra / total) * 100
```

**Result**: All four values sum to exactly 100%

## Budget Allocation Conversion

Convert 4-category spending policy to 5-category budget allocation:

```
research_ratio = parameter (0.0 to 1.0)
research_and_infra_total = research_and_infra / 100

military_budget = military / 100
healthcare_budget = healthcare / 100
education_budget = education / 100
research_budget = research_and_infra_total * research_ratio
infrastructure_budget = research_and_infra_total * (1 - research_ratio)
```

**Result**: Five budget categories that sum to 100%

## Absolute Spending Calculation

Convert budget percentages to absolute currency amounts:

```
government_revenue = GDP * (tax_rate / 100)
effective_revenue = government_revenue * (1 - corruption / 100)

military_spending = effective_revenue * military_budget
healthcare_spending = effective_revenue * healthcare_budget
education_spending = effective_revenue * education_budget
research_spending = effective_revenue * research_budget
infrastructure_spending = effective_revenue * infrastructure_budget
```

## Example Calculation

### Country: "Democracia"
- Democracy Index: 85
- Elderly Population: 12% of total
- Random Factors: [+3, -2, +5, -1]
- GDP: $500B
- Tax Rate: 25%
- Corruption: 15%

### Step 1-2: Base + Random
```
military = 25 + 3 = 28
healthcare = 25 - 2 = 23
education = 25 + 5 = 30
research_and_infra = 25 - 1 = 24
```

### Step 3-4: Adjustments
```
democracy_factor = (100 - 85) / 100 = 0.15
military_adjustment = 0.15 * 15 = 2.25

elderly_percentage = 0.12
healthcare_adjustment = 0.12 * 20 = 2.4

military = 28 + 2.25 = 30.25
healthcare = 23 + 2.4 = 25.4
education = 30
research_and_infra = 24
```

### Step 7: Normalize
```
total = 30.25 + 25.4 + 30 + 24 = 109.65

military = (30.25 / 109.65) * 100 = 27.6%
healthcare = (25.4 / 109.65) * 100 = 23.2%
education = (30 / 109.65) * 100 = 27.4%
research_and_infra = (24 / 109.65) * 100 = 21.9%

Total = 27.6 + 23.2 + 27.4 + 21.9 = 100.1% ≈ 100%
```

### Budget Allocation (research_ratio = 0.6)
```
research_and_infra_total = 21.9 / 100 = 0.219

military = 27.6 / 100 = 0.276
healthcare = 23.2 / 100 = 0.232
education = 27.4 / 100 = 0.274
research = 0.219 * 0.6 = 0.1314 = 13.14%
infrastructure = 0.219 * 0.4 = 0.0876 = 8.76%

Total = 27.6 + 23.2 + 27.4 + 13.14 + 8.76 = 100%
```

### Absolute Spending
```
government_revenue = 500B * (25 / 100) = 125B
effective_revenue = 125B * (1 - 15 / 100) = 106.25B

military_spending = 106.25B * 0.276 = 29.3B
healthcare_spending = 106.25B * 0.232 = 24.7B
education_spending = 106.25B * 0.274 = 29.1B
research_spending = 106.25B * 0.1314 = 13.9B
infrastructure_spending = 106.25B * 0.0876 = 9.3B

Total = 29.3 + 24.7 + 29.1 + 13.9 + 9.3 = 106.2B ≈ 106.25B
```

## Key Insights

1. **Democracy Effect**: 
   - High democracy (90): military reduced by ~1.5%
   - Low democracy (20): military increased by ~12%
   - Difference: ~13.5 percentage points

2. **Age Effect**:
   - Young population (5% elderly): healthcare +1%
   - Aging population (30% elderly): healthcare +6%
   - Difference: ~5 percentage points

3. **Random Variation**:
   - Creates natural diversity between countries
   - ±10% per category before normalization
   - After normalization, effect is smaller

4. **Self-Balancing**:
   - No matter what adjustments are applied
   - Final result always sums to exactly 100%
   - No manual intervention needed

5. **Effective Revenue Impact**:
   - Corruption reduces absolute spending
   - Tax rate determines government revenue
   - Budget percentages determine allocation
   - All three factors compound together

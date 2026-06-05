# Budget Allocation System

## Overview

The budget allocation system determines how each country distributes its government revenue across four spending categories. The system is **self-balancing** and always sums to 100%.

## Spending Policy (4 Categories)

The `SpendingPolicy` class represents budget allocation as 4 values that always sum to 100%:

1. **Military** - Defense and security spending
2. **Healthcare** - Health services and medical infrastructure
3. **Education** - Educational institutions and training
4. **Research & Infrastructure** - Technology research and infrastructure development

### Formula

Each category starts with a **base allocation of 25%**, then adjustments are applied:

```
military = 25 + random(-10, 10) + military_adjustment
healthcare = 25 + random(-10, 10) + healthcare_adjustment
education = 25 + random(-10, 10)
research_and_infrastructure = 25 + random(-10, 10)
```

**Random Factor**: Each country gets a unique ±10% random variation per category, creating natural diversity.

## Adjustments

### Democracy Index Effect (Military Spending)

More democratic countries spend **less** on military; authoritarian states spend **more**.

```
democracy_factor = (100 - democracy_index) / 100
military_adjustment = democracy_factor * 15
```

**Effect Range**: 
- Democracy 100 (highly democratic): -15% adjustment → ~10% military spending
- Democracy 0 (totalitarian): +15% adjustment → ~40% military spending

### Age Distribution Effect (Healthcare Spending)

Countries with older populations spend **more** on healthcare.

```
elderly_percentage = elderly_population / total_population
healthcare_adjustment = elderly_percentage * 20
```

**Effect Range**:
- 5% elderly: +1% adjustment → ~26% healthcare
- 25% elderly: +5% adjustment → ~30% healthcare
- 40% elderly: +8% adjustment → ~33% healthcare

## Self-Balancing Mechanism

The `SpendingPolicy.__post_init__()` method automatically normalizes all values:

```python
total = military + healthcare + education + research_and_infrastructure
military = (military / total) * 100
healthcare = (healthcare / total) * 100
education = (education / total) * 100
research_and_infrastructure = (research_and_infrastructure / total) * 100
```

This ensures that even with adjustments, the four categories always sum to exactly 100%.

## Conversion to Detailed Budget

The `SpendingPolicy.to_budget_allocation()` method converts the 4-category policy into a 5-category `BudgetAllocation`:

```python
budget = spending_policy.to_budget_allocation(research_ratio=0.6)
```

The `research_ratio` parameter (0-1) determines how the "Research & Infrastructure" category is split:

- **research_ratio = 0.6**: 60% to research, 40% to infrastructure
- **research_ratio = 0.5**: 50% to research, 50% to infrastructure
- **research_ratio = 0.3**: 30% to research, 70% to infrastructure

## Usage in Country Simulation

### Initialization

When a country is created, its spending policy is calculated based on initial conditions:

```python
economy = Economy(
    population=pop.total_population,
    stability=70,
    technology=60,
    corruption=20,
    democracy_index=90,
    age_groups=pop.age_groups  # Needed for age-based adjustments
)
```

### Yearly Updates

Each year, the spending policy is **recalculated** based on current conditions:

```python
economy.yearly_update(
    population=self.population.total_population,
    stability=self.stability,
    technology=self.technology,
    corruption=self.corruption,
    democracy_index=self.democracy_index,
    age_groups=self.population.age_groups,  # Current age distribution
    agriculture_penalty=self.industries.agriculture_penalty,
    resource_penalty=self.industries.resource_penalty
)
```

This allows spending priorities to shift as the country's demographics and political system evolve.

## Absolute Spending Calculation

Once the budget allocation is determined, absolute spending amounts are calculated:

```python
healthcare_spending = effective_revenue * budget.healthcare
education_spending = effective_revenue * budget.education
research_spending = effective_revenue * budget.research
military_spending = effective_revenue * budget.military
infrastructure_spending = effective_revenue * budget.infrastructure
```

Where `effective_revenue = government_revenue * (1 - corruption / 100)`

## Example Scenarios

### Scenario 1: Young, Democratic Country
- Democracy Index: 85
- Elderly %: 8%
- Result: Low military (~18%), moderate healthcare (~26%), balanced others

### Scenario 2: Aging, Authoritarian State
- Democracy Index: 25
- Elderly %: 30%
- Result: High military (~35%), very high healthcare (~40%), lower education/research

### Scenario 3: Middle-aged, Hybrid Regime
- Democracy Index: 50
- Elderly %: 15%
- Result: Balanced across all categories (~25% each)

## Design Benefits

1. **Self-balancing**: Always sums to 100%, no manual normalization needed
2. **Realistic**: Democracy and demographics drive spending priorities
3. **Dynamic**: Adjusts yearly as country conditions change
4. **Flexible**: Random factors create unique country behaviors
5. **Reusable**: `SpendingPolicy` can be used in other contexts beyond Economy

Create a terminal-based economy simulation in Python.

The goal is just to make define basic rules of a society for now. Interactions will be defined more in detial later. 



## General Requirements

* No GUI.
* Use object-oriented design.
* The main class must be called `Country`.
* The simulation runs in yearly turns.
* Simulate at least 50 countries.
* Print a summary of the world economy every simulated year.

---

# Country Properties

Each `Country` should contain:

## Basic Information

* Name (randomly selected from names.txt file)
* Population
* Area
* GDP
* Stability
* Technology level
* Corruption level
* Democracy Index

### Country Names

Each country is assigned a unique random name from the `names.txt` file. This file contains a list of fantasy/realistic country names that are used to give each country a distinct identity in the simulation.

The names are selected randomly without replacement to ensure each country has a unique name during a simulation run.

### Corruption Level

Corruption level is a random number from 0 to 100, where 50 means 50% of tax revenue is lost to corruption.

**Formula reference:**

```
if random_uniform(0, 1) < 0.4:
    # Uniform distribution between 15 and 30 (40% probability)
    corruption = random_uniform(15, 30)
else:
    # Not in normal range (60% probability)
    if random_uniform(0, 1) < 0.4:
        # Logarithmic distribution from 15 down to 0 (24% probability)
        corruption = 15 * exp(-random_uniform(0, 3))
    else:
        # Logarithmic distribution from 30 up to 100 (36% probability)
        corruption = 30 + 70 * (1 - exp(-random_uniform(0, 3)))

where:
- random_uniform(a, b) returns a random value between a and b
- exp(x) is the exponential function: e^x
```

This makes values near 0 and 100 extremely rare, while 15-30 is the most common range.

Corruption affects government revenue:

```
effective_revenue = government_revenue * (1 - corruption / 100)
```

### Stability

Stability represents social order, trust in institutions, and political cohesion.

**Range:** 0 - 100

* 0 = failed state
* 100 = extremely stable state

**Yearly change:**

```
stability_change = (
    education_bonus
    + healthcare_bonus
    + infrastructure_bonus
    + gdp_growth_bonus
) - (
    corruption_penalty
    + unemployment_penalty
    + inequality_penalty
)
```

**Effects:**

Higher stability:

* Increases GDP growth
* Reduces emigration
* Increases immigration
* Reduces mortality

Lower stability:

* Reduces economic growth
* Increases emigration
* Increases mortality

### Democracy Index

Each country has a Democracy Index from 0 to 100.

**Scale:**

* 0 = Totalitarian dictatorship
* 25 = Authoritarian state
* 50 = Hybrid regime
* 75 = Imperfect democracy
* 100 = Highly democratic society

**Effects on corruption:**

Higher democracy generally reduces corruption.

```
corruption_modifier = 1 - democracy_index / 200
```

**Effects on immigration:**

People generally prefer moving to freer countries when economic conditions are similar.

```
immigration_attractiveness = GDP_per_capita_score + stability_score + democracy_index * 0.2
```

**Effects on emigration:**

People are more likely to leave highly restrictive states.

```
emigration_pressure += (100 - democracy_index) * factor
```

**Yearly change:**

```
democracy_change = (
    cultural_education / 100
    + transparency_bonus
) - (
    corruption / 100
    + instability_penalty
)
```


## Population

Generate a random population between 500,000 and 500,000,000.

Use a logarithmic or weighted distribution so that:

* small and medium countries are common
* extremely large countries are rare

**Formula reference:**

```
population = exp(random_uniform(log(min_pop), log(max_pop)))

where:
- min_pop = 500,000
- max_pop = 500,000,000
- random_uniform(a, b) returns a random value between a and b
- exp(x) is the exponential function: e^x, where e ≈ 2.71828
- log(x) is the natural logarithm: the inverse of exp(), returns the power to which e must be raised to get x
```

This ensures that smaller population values are more likely than larger ones.

### Age Distribution

Population is divided into 4 age groups:

* Children (0-17 years)
* Young Adults (18-39 years)
* Older Adults (40-65 years)
* Elderly (66-90 years)

The total population is distributed across these age groups based on a realistic demographic distribution.

**Demographic Age Factor:**

A random factor influenced by GDP, stability, and technology determines the overall age distribution of the population:

```
age_factor = random_uniform(0, 1) * (gdp / max_gdp) * (stability / 100) * (technology / 100)

where:
- gdp = country's total GDP
- max_gdp = reference maximum GDP for normalization
- stability = country's stability score (0-100)
- technology = country's technology level (0-100)
- random_uniform(0, 1) returns a random value between 0 and 1
```

Higher age_factor results in:
- Higher percentage of elderly population
- Higher average life expectancy
- Lower percentage of children and young adults

Lower age_factor results in:
- Higher percentage of children and young adults
- Lower average life expectancy
- Lower percentage of elderly population

### Population Dynamics

Each country has:

* Birth rate (random percentage)
* Immigration rate (random percentage)
* Emigration rate (random percentage)

**Formula reference:**

```
birth_rate = (
    random_uniform(0.4, 1.0)
    * (1 - gdp_per_capita / max_gdp_per_capita)
    * (stability / 100)
    * max_birth_rate
)

immigration_rate = (
    random_uniform(0, 1)
    * (gdp_per_capita / max_gdp_per_capita)
    * (stability / 100)
    * (1 - corruption / 100)
    * max_immigration_rate
)

immigration_rate *= (1 - unemployment_rate / 100)

emigration_rate = (
    random_uniform(0, 1)
    * (1 - gdp_per_capita / max_gdp_per_capita)
    * (1 - stability / 100)
    * (corruption / 100)
    * max_emigration_rate
)

emigration_rate *= (1 + unemployment_rate / 50)

where:
- gdp_per_capita = GDP / Population
- max_gdp_per_capita = reference maximum GDP per capita for normalization
- stability = country's stability score (0-100)
- corruption = country's corruption level (0-100)
- unemployment_rate = country's unemployment rate (0-40)
- max_birth_rate = maximum possible birth rate (e.g., 5%)
- max_immigration_rate = maximum possible immigration rate (e.g., 3%)
- max_emigration_rate = maximum possible emigration rate (e.g., 3%)
- random_uniform(a, b) returns a random value between a and b
```

Birth rate tends to be:

Higher when:
* GDP per capita is low
* Population is young

Lower when:
* GDP per capita is high
* Population is older
* Education is high

Extremely low stability may also reduce birth rates.

Immigration is attracted by:
* High GDP per capita
* High stability
* Low corruption
* Low unemployment

Emigration becomes higher when:
* GDP per capita is low
* Stability is low
* Corruption is high
* Unemployment is high

These rates influence population changes over time during simulation.

## Mortality Rate

Each age group has its own yearly mortality rate:

* Children (0-17): 0.05% - 0.50%
* Young Adults (18-39): 0.05% - 0.30%
* Older Adults (40-65): 0.20% - 1.50%
* Elderly (66-90): 2.00% - 12.00%

Mortality is affected by:

* Health care spending
* Technology
* Stability
* Fresh water availability

Higher health care spending and technology reduce mortality.

Lower stability increases mortality.

**Yearly update:**

```
deaths = age_group_population * mortality_rate
```

### Wealth Distribution

Each country has an inequality/disparity factor from 0.0 to 1.0.

Population is divided into 4 economic classes:

* Lower class
* Middle class
* Upper class
* Elite class

The disparity factor determines:

* percentage of population in each class
* percentage of wealth owned by each class

Higher inequality should increase instability over time.

### Education

Each country has two education scores from 0 to 100:

* Technical education
* Cultural education

**Education System Type:**

Each country has one of the following education system types:

* Public only
* Private only
* Mixed (both public and private)

The education system type influences the cost and accessibility of education.


## Area

Generate a total land area in square kilometers. The area should be related to total population, so a country with higher population is also more likely to be larger. The population shoould define a range of size. 

---

# Natural Resources

Each country has harvestable resources.

## Minerals

* Stone
* Iron
* Lithium
* Silicon

Each mineral has:

* total reserves
* yearly extraction capacity

**Formula reference:**

```
total_reserves = random_uniform(min_reserve, max_reserve) * (area / base_area)

where:
- min_reserve = 5,000 (units)
- max_reserve = 1,000,000 (units)
- area = country's total land area in square kilometers
- base_area = reference area (e.g., 100,000 km²) for normalization
- random_uniform(a, b) returns a random value between a and b
```

Larger countries have proportionally larger mineral reserves.


## Fossil Fuels

### Oil

Generate multiple oil fields.

Each oil field contains:

* total oil amount (0–100 billion barrels)
* extraction difficulty
* oil quality

### Natural Gas

Generate reserves similarly to oil.


## Wood

Represents forest resources. Forest should be generated in a similar manner to fossil fuels, with fields in spots of total area and differenet density. 


## Geographical characteristics 

Each country has a general amount of temperature, sismic level, and mountain percentage. It should also have total farmable land. This will be impacted by the amount of forest that is present. 

## Fresh Water

Represents renewable water access.

This sould be influenced by the country geographical caraterestics. 


---

# Economy

Each country has:

* Total GDP
* GDP growth rate
* Inflation
* Government revenue
* Tax rate (random percentage from 10 to 50)

### GDP Growth Rate

**Initial growth rate:**

Random uniform between -2% and 5%.

**Yearly growth rate calculation:**

The growth rate is calculated after GDP is updated based on industry outputs and other factors.

```
gdp_growth_rate = (current_gdp - previous_gdp) / previous_gdp
```

This represents the actual percentage change in GDP from the previous year to the current year.

**GDP is updated yearly based on:**

* Industry outputs (resource extraction, agriculture, manufacturing, technology)
* Productivity factors
* Worker distribution
* Market prices

The growth rate is then calculated from the resulting GDP change.

Government revenue is proportional to tax rate, but reduced by corruption:

```
government_revenue = GDP * (tax_rate / 100)
effective_revenue = government_revenue * (1 - corruption / 100)
```

### Budget Allocation

Each country allocates its effective revenue across five budget categories:

* Military
* Healthcare
* Education
* Research
* Infrastructure

**Spending Policy (4 Categories):**

Budget allocation is determined by a `SpendingPolicy` that represents spending as 5 categories summing to 100%:

```
spending_policy = {
    military: percentage,
    healthcare: percentage,
    education: percentage,
    research: percentage,
    infrastructure: percentage
}
```

**Calculation Formula:**

Each category starts with a 25% base allocation, then adjustments are applied:

```
military = 25 + random(-10, 10) + military_adjustment
healthcare = 25 + random(-10, 10) + healthcare_adjustment
education = 25 + random(-10, 10)
research_and_infrastructure = 25 + random(-10, 10)
```

Then all values are normalized to sum to exactly 100%.

**Democracy Index Effect (Military):**

More democratic countries spend less on military; authoritarian states spend more.

```
democracy_factor = (100 - democracy_index) / 100
military_adjustment = democracy_factor * 15

where:
- democracy_index ranges from 0 (totalitarian) to 100 (highly democratic)
- military_adjustment ranges from -15 to +15 percentage points
```

**Age Distribution Effect (Healthcare):**

Countries with older populations spend more on healthcare.

```
elderly_percentage = elderly_population / total_population
healthcare_adjustment = elderly_percentage * 20

where:
- elderly_percentage ranges from 0.0 to 1.0
- healthcare_adjustment ranges from 0 to +20 percentage points
```

**Random Factors:**

Each country receives unique random variation (±10%) per category, creating natural diversity in spending priorities.

**Absolute Spending:**

Once the spending policy is determined, absolute spending amounts are calculated:

```
military_spending = effective_revenue * military_budget
healthcare_spending = effective_revenue * healthcare_budget
education_spending = effective_revenue * education_budget
research_spending = effective_revenue * research_budget
infrastructure_spending = effective_revenue * infrastructure_budget
```

**Yearly Updates:**

The spending policy is recalculated each year based on current democracy index and age distribution, allowing spending priorities to shift as the country evolves.

### Effects of Government Spending

Government spending directly impacts multiple aspects of the country's development and stability. Effects are scaled relative to population and maximum GDP per capita to ensure fairness across countries of different sizes.

**Normalization Constants:**

```
max_gdp_per_capita = 50,000 (reference maximum)
spending_per_capita = spending / population
spending_efficiency = spending_per_capita / max_gdp_per_capita

where:
- spending_per_capita represents how much is spent per person
- spending_efficiency normalizes spending relative to world reference
- Larger countries need proportionally more spending for same effect
```

#### Healthcare Spending Effects

Healthcare spending reduces mortality rates and increases life expectancy.

**Mortality Rate Reduction:**

```
spending_per_capita = healthcare_spending / population
spending_efficiency = spending_per_capita / max_gdp_per_capita
healthcare_factor = 1.0 - (spending_efficiency * 0.3)

where:
- spending_efficiency ranges from 0 (no spending) to 1.0+ (high spending)
- Each unit of spending_efficiency reduces mortality by up to 30%
- healthcare_factor ranges from 0.7 (high spending) to 1.0 (no spending)

adjusted_mortality_rate = base_mortality_rate * healthcare_factor
```

**Life Expectancy Improvement:**

```
life_expectancy_bonus = spending_efficiency * 2.5

where:
- Each unit of spending_efficiency adds up to 2.5 years to life expectancy
```

#### Education Spending Effects

Education spending improves both cultural and technical education scores.

**Education Score Improvement:**

```
spending_per_capita = education_spending / population
spending_efficiency = spending_per_capita / max_gdp_per_capita
education_improvement = (spending_efficiency * 5) + (technology_level / 100) * 0.5

where:
- Each unit of spending_efficiency improves education by 5 points
- Technology level provides additional synergy (up to 0.5 bonus)
- Both cultural_education and technical_education improve equally
- Scores are capped at 100
```

#### Military Spending Effects

Military spending improves national stability by increasing security and reducing internal unrest.

**Stability Bonus:**

```
spending_per_capita = military_spending / population
spending_efficiency = spending_per_capita / max_gdp_per_capita
military_stability_bonus = spending_efficiency * 3

where:
- Each unit of spending_efficiency provides +3 stability points per year
- This bonus is added to the stability change calculation
```

#### Infrastructure Spending Effects

Infrastructure spending improves the efficiency of resource harvesting and industrial productivity across all sectors.

**Resource Extraction Efficiency:**

```
spending_per_capita = infrastructure_spending / population
spending_efficiency = spending_per_capita / max_gdp_per_capita
infrastructure_efficiency = 1.0 + (spending_efficiency * 0.15)

where:
- Each unit of spending_efficiency increases extraction efficiency by 15%
- Applies to all resource extraction (minerals, oil, gas, wood)
- Extracted_resources *= infrastructure_efficiency
```

**Industry Productivity Multiplier:**

```
spending_per_capita = infrastructure_spending / population
spending_efficiency = spending_per_capita / max_gdp_per_capita
infrastructure_productivity_bonus = spending_efficiency * 0.10

where:
- Each unit of spending_efficiency adds 10% to base productivity
- Applies to all industries: extraction, agriculture, manufacturing, technology
- Affects the productivity multiplier used in industry output calculations
```

**Stability Bonus:**

```
spending_per_capita = infrastructure_spending / population
spending_efficiency = spending_per_capita / max_gdp_per_capita
infrastructure_stability_bonus = spending_efficiency * 3

where:
- Each unit of spending_efficiency provides +3 stability points per year
- Infrastructure improves quality of life and public satisfaction
```

#### Research Spending Effects

Research spending improves technology education and boosts productivity in technology-intensive sectors.

**Technology Education Improvement:**

```
spending_per_capita = research_spending / population
spending_efficiency = spending_per_capita / max_gdp_per_capita
tech_education_improvement = spending_efficiency * 4

where:
- Each unit of spending_efficiency improves technical_education by 4 points
- Capped at 100
```

**Technology Level Improvement:**

```
spending_per_capita = research_spending / population
spending_efficiency = spending_per_capita / max_gdp_per_capita
technology_improvement = (spending_efficiency * 2) + random(0, 0.5)

where:
- Each unit of spending_efficiency improves technology level by 2 points
- Random variation (0-0.5) adds unpredictability to research outcomes
- Capped at 100
```

**Sector Productivity Bonuses:**

Research spending provides varying productivity boosts to different sectors:

```
spending_per_capita = research_spending / population
spending_efficiency = spending_per_capita / max_gdp_per_capita

technology_sector_bonus = spending_efficiency * 0.20
agriculture_sector_bonus = spending_efficiency * 0.10
manufacturing_sector_bonus = spending_efficiency * 0.05
extraction_sector_bonus = spending_efficiency * 0.03

where:
- Technology sector receives the strongest boost (20% per unit efficiency)
- Agriculture receives moderate boost (10% per unit efficiency)
- Manufacturing receives smaller boost (5% per unit efficiency)
- Extraction receives minimal boost (3% per unit efficiency)
- These bonuses are applied to industry output calculations
```

#### Combined Spending Effects on Stability

Multiple spending categories contribute to overall stability:

```
spending_per_capita_health = healthcare_spending / population
spending_per_capita_edu = education_spending / population
spending_per_capita_mil = military_spending / population
spending_per_capita_infra = infrastructure_spending / population
spending_per_capita_res = research_spending / population

efficiency_health = spending_per_capita_health / max_gdp_per_capita
efficiency_edu = spending_per_capita_edu / max_gdp_per_capita
efficiency_mil = spending_per_capita_mil / max_gdp_per_capita
efficiency_infra = spending_per_capita_infra / max_gdp_per_capita
efficiency_res = spending_per_capita_res / max_gdp_per_capita

total_spending_stability_bonus = (
    efficiency_health * 5
    + efficiency_edu * 2
    + efficiency_mil * 3
    + efficiency_infra * 3
    + efficiency_res * 1
)

where:
- Healthcare has the strongest stability impact (5 points per unit efficiency)
- Military and infrastructure tied (3 points per unit efficiency)
- Education provides moderate boost (2 points per unit efficiency)
- Research provides minimal stability boost (1 point per unit efficiency)
```

## GDP Per Capita

Each country has:

* GDP per capita

**Formula reference:**

```
GDP_per_capita = GDP / Population
```

GDP per capita is used as a proxy for average economic prosperity and influences:

* Immigration
* Emigration
* Stability
* Education quality
* Birth rate

## Unemployment Rate

Each country has an unemployment rate from 0% to 40%.

Initial unemployment is influenced by:

* Technology
* Education
* GDP per capita
* Stability

**Formula reference:**

```
unemployment_rate = random_uniform(2, 25)

Adjusted by:
+ low stability
+ low education
+ low GDP per capita
```

Higher unemployment reduces:

* GDP growth
* Stability

Higher unemployment increases:

* Emigration
* Poverty pressure

## Industries

Each country contains companies operating in multiple industries.

**Industries:**

* Natural Resource Extraction
* Agriculture
* Manufacturing
* Technology

The percentage of companies in each industry is determined by:

* Resource availability
* Farmable land
* Technology level
* GDP per capita

Countries evolve economically over time.

**Low-technology countries tend to have:**

* More extraction companies
* More agricultural companies

**High-technology countries tend to have:**

* More manufacturing companies
* More technology companies

**Industry productivity depends on:**

* Technology
* Education
* Infrastructure
* Stability

Industry output generates jobs and GDP.

The total GDP of a country is the sum of all industry outputs.

### Industry Distribution

Each country has four industry shares:

* Resource Extraction Share
* Agriculture Share
* Manufacturing Share
* Technology Share

The shares must sum to 100%.

**Industry Weights:**

Compute raw weights first.

```
Resource Extraction:
resource_weight = (
    mineral_abundance
    + oil_abundance
    + gas_abundance
    + forest_abundance
)

Agriculture:
agriculture_weight = (
    farmable_land_percent
    * fresh_water_factor
)

Manufacturing:
manufacturing_weight = (
    technology_level
    + technical_education
    + infrastructure
)

Technology:
technology_weight = (
    technology_level * 2
    + technical_education
    + GDP_per_capita_factor
)

total_weight = (
    resource_weight
    + agriculture_weight
    + manufacturing_weight
    + technology_weight
)

resource_share = resource_weight / total_weight
agriculture_share = agriculture_weight / total_weight
manufacturing_share = manufacturing_weight / total_weight
technology_share = technology_weight / total_weight
```

**Worker Distribution:**

The working population is determined by the total working-age population and unemployment rate.

```
working_age_population = young_adults + older_adults
working_population = working_age_population * (1 - unemployment_rate / 100)
```

Workers are then distributed across industries:

```
resource_workers = working_population * resource_share
agriculture_workers = working_population * agriculture_share
manufacturing_workers = working_population * manufacturing_share
technology_workers = working_population * technology_share
```

### Productivity

All industries use a common productivity multiplier.

```
productivity = (
    0.30 * technology_level
    + 0.25 * technical_education
    + 0.20 * infrastructure
    + 0.15 * stability
    + 0.10 * cultural_education
) / 100
```

This gives a value roughly between 0 and 1.

### Industry Profits

**Resource Extraction Profit:**

Extraction depends heavily on available resources.

```
resource_output = (
    extracted_resources
    * resource_market_price
)

resource_cost = (
    resource_workers * worker_cost
) + (
    extraction_difficulty
    * difficulty_cost
)

resource_profit = resource_output - resource_cost
```

**Agriculture Profit:**

Agriculture depends on land and water.

```
agriculture_output = (
    agriculture_workers
    * productivity
    * farmable_land_factor
    * fresh_water_factor
)

agriculture_profit = (
    agriculture_output
    * food_price
) - (
    agriculture_workers
    * worker_cost
)
```

**Manufacturing Profit:**

Manufacturing converts labor and technology into value.

```
manufacturing_output = (
    manufacturing_workers
    * productivity
    * (1 + technology_level / 100)
)

manufacturing_profit = (
    manufacturing_output
    * manufactured_goods_price
) - (
    manufacturing_workers
    * worker_cost
)
```

**Technology Profit:**

Technology scales hardest with education and technology.

```
technology_output = (
    technology_workers
    * productivity
    * (1 + technology_level / 50)
    * (1 + technical_education / 100)
)

technology_profit = (
    technology_output
    * technology_price
) - (
    technology_workers
    * worker_cost
)
```

**Total GDP and Profit:**

```
GDP = (
    resource_output
    + agriculture_output
    + manufacturing_output
    + technology_output
)

total_corporate_profit = (
    resource_profit
    + agriculture_profit
    + manufacturing_profit
    + technology_profit
)
```

### Resource Shortage Penalties

Industries should not only generate output — they should also unlock each other's efficiency. Resource shortages apply penalties to productivity and stability.

**Minimum Structural Needs:**

Each country has baseline consumption needs proportional to population.

```
food_demand = population * food_per_capita
resource_demand = population * resource_intensity

resource_intensity = depends on tech level (higher tech → more input demand)

food_supply = agriculture_output
resource_supply = extraction_output

food_ratio = food_supply / food_demand
resource_ratio = resource_supply / resource_demand

ratio = min(1.0, food_supply / demand)
```

**Nonlinear Shortage Penalty:**

Instead of linear punishment, use a nonlinear curve so collapse becomes possible.

```
def shortage_penalty(ratio):
    return max(0.0, (1.0 - ratio) ** 2)

agriculture_penalty = shortage_penalty(food_ratio)
resource_penalty = shortage_penalty(resource_ratio)
```

**Effects on Productivity:**

```
effective_productivity = (
    productivity
    * (1 - 0.4 * agriculture_penalty)
    * (1 - 0.4 * resource_penalty)
)
```

**Effects on Stability:**

```
stability -= (
    20 * agriculture_penalty
    + 10 * resource_penalty
)
```

**Effects on Emigration:**

```
emigration_pressure += (
    30 * agriculture_penalty
    + 15 * resource_penalty
)
```

**Effects on Inflation:**

```
inflation += 10 * (1 - food_ratio)
```

**Overall Dependency:**

```
dependency = max(food_penalty, resource_penalty)
``` 


---

## Culture 

Each country has:

* Language ID (1–100)
* Religion ID (1–10)
* Religious intensity (0–100)


---

# Simulation Mechanics

Every year, all variables are recalculated based on the previous year's values.

## Yearly Update Process

### Population Changes

Population changes are calculated as:

```
population_change = (births - deaths) + (immigration - emigration)

where:
- births = total_population * birth_rate
- deaths = sum(age_group_population * age_group_mortality_rate)
- immigration = total_population * immigration_rate
- emigration = total_population * emigration_rate
```

**Age distribution updates:**

* Children age into Young Adults
* Young Adults age into Older Adults
* Older Adults age into Elderly
* Elderly who exceed maximum age are removed (deaths)
* New births are added to Children age group

**Average age changes:**

The average age of the population shifts based on:
* Birth rate (higher births = younger population)
* Mortality rates by age group
* Migration patterns (immigrants/emigrants tend to be specific age groups)

**Birth rate and death rate updates:**

Birth rate and mortality rates are recalculated yearly based on:
* Updated GDP per capita
* Updated stability
* Updated health care spending
* Updated technology level
* Updated democracy index

### Economic Updates

* GDP changes based on growth rate
* GDP per capita recalculated
* Inflation adjusted
* Government revenue recalculated based on new GDP and tax rate
* Effective revenue adjusted for corruption
* Budget allocations may be adjusted
* Unemployment rate updated

### Social Updates

* Stability changes based on yearly change formula
* Democracy index evolves based on cultural education, corruption, and stability
* Education scores slowly evolve based on budget spending
* Corruption may change based on democracy index and stability
* Wealth distribution may shift based on economic changes

### Resource Updates

* Resources are extracted based on extraction capacity
* Resource reserves decrease
* Resources may become depleted when reserves reach zero
* Extraction capacity may decrease as resources deplete

### Migration Updates

* Immigration rate recalculated based on updated GDP per capita, stability, corruption, democracy, and unemployment
* Emigration rate recalculated based on updated GDP per capita, stability, corruption, democracy, and unemployment
* Actual migration flows calculated and applied to population

# Output

## Improved Output Specification (Summary)

### Goals of the Output System

- Provide clear, readable, and traceable yearly simulation logs.
- Offer both human‑readable summaries and machine‑readable data.
- Highlight major events, trends, and anomalies in a concise format.

### Output Files

Each simulation run creates a timestamped folder to keep results organized.

**Folder Structure:**

```
output/
└── YYYYMMDD_HHMMSS/          # Timestamped folder for each run
    ├── metadata.json
    ├── world_summary.txt
    ├── yearly_data.csv
    ├── yearly_data.json
    └── events.log
```

The folder name uses the format `YYYYMMDD_HHMMSS` (e.g., `20260604_202130`) representing the date and time when the simulation started.

**Files in each run folder:**

- Human Summary: `world_summary.txt`
- Machine Logs: `yearly_data.csv`, `yearly_data.json`
- Event Log: `events.log`
- Metadata: `metadata.json`

### Metadata Header

```
Random seed: <value>
Software version: <value>
Creation date: <timestamp>
Number of countries: <N>
Simulation duration: <years>
Configuration: <key parameters>
```

### Yearly Summary Structure

#### 1. Year Header

```
Year <N> | World GDP: <value> | World Population: <value> | Avg Stability: <value>
```

#### 2. Top 5 Highlights

Short, cause‑and‑effect statements summarizing the most important events of the year.

#### 3. Ranked Lists

- Top GDP countries
- Richest per capita
- Most stable
- Most democratic
- Most unequal

#### 4. Notable Events (Tagged)

```
[CRITICAL] Country A: Oil reserves depleted → GDP -11%, unemployment +3.2pp
```

#### 5. Migration Summary

- Net global flows
- Largest migration corridors
- Countries with highest immigration/emigration pressure

#### 6. Resource Warnings

List resources nearing depletion with estimated years remaining.

#### 7. Appendix Links

Pointers to:
- yearly CSV/JSON
- event log
- per‑country snapshots

### Machine Log Schema

#### CSV Columns

```
year,country_id,country_name,population,gdp,gdp_per_capita,
stability,democracy,corruption,unemployment,net_migration,
birth_rate,death_rate,inflation,resource_reserve_index
```

#### JSON Structure

```
{
  "year": <N>,
  "countries": [
    {
      "id": <id>,
      "name": "<name>",
      "population": <value>,
      "gdp": <value>,
      ...
    }
  ]
}
```

### Event Log Format

```
[YYYY-MM-DD] [Year N] [SEVERITY] Country X: <event description>
```

### Optional Enhancements

- ASCII sparklines for trends
- One‑line country snapshots
- Configurable verbosity levels (`SUMMARY`, `DETAILED`, `DEBUG`)
- Short narrative paragraphs explaining major shifts

---

# Technical Requirements

* Use clean class design.
* Separate simulation logic into multiple files.
* Avoid external libraries unless necessary.
* Use type hints where appropriate.
* Include comments explaining major systems.

The goal is not realism, but an interesting emergent simulation with believable economic behavior.

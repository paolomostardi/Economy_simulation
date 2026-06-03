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

* Name
* Population
* Area
* GDP
* Stability
* Technology level
* Corruption level
* Democracy Index

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

**Yearly growth rate update:**

The growth rate is recalculated each year based on multiple factors:

```
base_growth = random_uniform(-0.01, 0.04)  # -1% to 4%

stability_bonus = (stability / 100 - 0.5) * 0.05
tech_bonus = (technology / 100) * 0.02
unemployment_penalty = (unemployment / 40) * 0.03
corruption_penalty = (corruption / 100) * 0.02
resource_bonus = 0.005  # 0.5% from resource extraction

new_growth = (base_growth + stability_bonus + tech_bonus + resource_bonus
             - unemployment_penalty - corruption_penalty)

# Smooth transition to avoid extreme fluctuations
gdp_growth_rate = gdp_growth_rate * 0.7 + new_growth * 0.3
gdp_growth_rate = clamp(-0.1, 0.15, gdp_growth_rate)  # -10% to 15%

where:
- stability = country's stability score (0-100)
- technology = country's technology level (0-100)
- unemployment = country's unemployment rate (0-40)
- corruption = country's corruption level (0-100)
- random_uniform(a, b) returns a random value between a and b
- clamp(min, max, value) constrains value between min and max
```

**Effects:**

- Higher stability increases growth
- Higher technology increases growth
- Higher unemployment reduces growth
- Higher corruption reduces growth
- Resource extraction provides a small bonus

Government revenue is proportional to tax rate, but reduced by corruption:

```
government_revenue = GDP * (tax_rate / 100)
effective_revenue = government_revenue * (1 - corruption / 100)
```

**Budget Spending:**

Each country allocates its effective revenue across budget categories:

* Military
* Health care
* Education
* Research
* Infrastructure

The sum of all budget allocations cannot exceed effective revenue.

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

Instead of printing to console, simulation results are written to a structured text file in the output folder.

## File Structure

The output file is structured as a grid/table format to log changes over time.

## File Header

At the beginning of the file, include metadata:

* **Random seed**: For reproducibility and replication
* **Software version**: Version number of the simulation software
* **Creation date**: Date and time when the simulation was created
* **Number of countries**: Total countries in the simulation
* **Simulation duration**: Number of years simulated
* **Other metadata**: Any additional relevant configuration parameters

## Yearly Data Logged

For each year, log:

* Top GDP countries
* Richest population per capita
* Most unequal countries
* Most stable countries
* Most democratic countries
* Resource depletion warnings
* Population growth rates
* Migration flows
* Other significant changes or events

---

# Technical Requirements

* Use clean class design.
* Separate simulation logic into multiple files.
* Avoid external libraries unless necessary.
* Use type hints where appropriate.
* Include comments explaining major systems.

The goal is not realism, but an interesting emergent simulation with believable economic behavior.

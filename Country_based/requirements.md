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
birth_rate = random_uniform(0, 1) * (gdp / max_gdp) * (stability / 100) * (technology / 100) * max_birth_rate

immigration_rate = random_uniform(0, 1) * (gdp / max_gdp) * max_immigration_rate

emigration_rate = random_uniform(0, 1) * (1 - gdp / max_gdp) * max_emigration_rate

where:
- gdp = country's total GDP
- max_gdp = reference maximum GDP for normalization
- stability = country's stability score (0-100)
- technology = country's technology level (0-100)
- max_birth_rate = maximum possible birth rate (e.g., 5%)
- max_immigration_rate = maximum possible immigration rate (e.g., 3%)
- max_emigration_rate = maximum possible emigration rate (e.g., 3%)
- random_uniform(0, 1) returns a random value between 0 and 1
```

These rates influence population changes over time during simulation.

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

Initial GDP should depend on:

* resource extraction
* education
* technology
* population
* stability

---

## Culture 

Each country has:

* Language ID (1–100)
* Religion ID (1–10)
* Religious intensity (0–100)


---

# Simulation Mechanics

Every year:

* Population changes
* Resources are extracted
* GDP changes
* Education slowly evolves
* Stability changes
* Resources may become depleted

Print yearly statistics such as:

* Top GDP countries
* Richest population per capita
* Most unequal countries
* Resource depletion warnings

---

# Technical Requirements

* Use clean class design.
* Separate simulation logic into multiple files.
* Avoid external libraries unless necessary.
* Use type hints where appropriate.
* Include comments explaining major systems.

The goal is not realism, but an interesting emergent simulation with believable economic behavior.

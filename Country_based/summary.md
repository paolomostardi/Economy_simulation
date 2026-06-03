# Economy Simulation Summary

## Overview
Terminal-based economy simulation in Python using object-oriented design. Main class: `Country`. Simulates 50+ countries in yearly turns with output to structured text file.

## Country Properties

### Basic Information
- Name, Population, Area, GDP, Stability, Technology level, Corruption level, Democracy Index

### Key Metrics (0-100 scale)
- **Corruption**: Affects government revenue (revenue loss = corruption%). Most common range: 15-30
- **Stability**: Social order and political cohesion. Affects GDP growth, migration, mortality
- **Democracy Index**: 0=totalitarian to 100=highly democratic. Affects corruption and migration

### Population
- Range: 500K to 500M (logarithmic distribution favoring smaller countries)
- 4 age groups: Children (0-17), Young Adults (18-39), Older Adults (40-65), Elderly (66-90)
- Age distribution influenced by GDP, stability, technology
- Dynamics: Birth rate, Immigration rate, Emigration rate (all influenced by economic conditions)

### Mortality
- Age-specific rates: Children 0.05-0.50%, Young Adults 0.05-0.30%, Older Adults 0.20-1.50%, Elderly 2.00-12.00%
- Reduced by healthcare spending and technology, increased by low stability

### Wealth & Education
- 4 economic classes: Lower, Middle, Upper, Elite
- Inequality factor (0.0-1.0) affects class distribution and stability
- 2 education scores: Technical and Cultural (0-100)
- 3 education system types: Public, Private, Mixed

### Area
- Land area correlated with population size

## Natural Resources

### Minerals
- Stone, Iron, Lithium, Silicon
- Each has total reserves and yearly extraction capacity
- Reserves proportional to country area

### Fossil Fuels
- Oil fields: total amount (0-100B barrels), extraction difficulty, quality
- Natural Gas: similar to oil

### Wood
- Forest resources with fields and density

### Geography
- Temperature, seismic level, mountain percentage, farmable land
- Fresh water availability influenced by geography

## Economy

### GDP
- Initial growth rate: -2% to 5%
- Yearly growth influenced by: stability, technology, unemployment, corruption, resource extraction
- Smoothed to avoid extreme fluctuations (-10% to 15% range)

### Government
- Tax rate: 10-50%
- Revenue = GDP × (tax_rate/100)
- Effective revenue reduced by corruption
- Budget categories: Military, Healthcare, Education, Research, Infrastructure

### Employment
- Unemployment rate: 0-40%
- Influenced by technology, education, GDP per capita, stability
- Affects GDP growth, stability, emigration

## Culture
- Language ID (1-100)
- Religion ID (1-10)
- Religious intensity (0-100)

## Simulation Mechanics

### Yearly Updates
1. **Population**: births - deaths + immigration - emigration
2. **Age distribution**: aging progression, new births to children
3. **Economy**: GDP changes, inflation, revenue, unemployment
4. **Social**: stability, democracy, education, corruption evolution
5. **Resources**: extraction, depletion
6. **Migration**: rates recalculated based on updated conditions

### Interdependencies
- GDP per capita influences immigration, emigration, stability, education, birth rate
- Stability affects GDP growth, migration, mortality
- Democracy affects corruption and migration
- Education affects democracy and stability
- Corruption reduces revenue and stability
- Inequality increases instability over time

## Output

### File Structure
- Written to structured text file in output folder
- Header: random seed, version, creation date, country count, simulation duration
- Yearly data: top GDP countries, richest per capita, most unequal, most stable, most democratic, resource warnings, population growth, migration flows

## Technical Requirements
- Clean class design
- Separate simulation logic into multiple files
- Minimal external libraries
- Type hints where appropriate
- Comments explaining major systems

**Goal**: Interesting emergent simulation with believable economic behavior (not strict realism)

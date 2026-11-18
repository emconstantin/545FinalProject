# Tickets Tell a Story: Exploring Traffic Violations Through Data

Exploratory analysis of traffic stops in Montgomery County, Maryland: how stops changed over time, where and when they happen, and why they dropped sharply in 2020 and have not fully recovered.

**Team:** Emily Constantin, Sarah Gaddis, Ava Sangiuliano, Sydney Wilson
**Course:** COSC 545 Fall 2026

## Summary

Using the county's Traffic Violations dataset (about 2.1 million rows), we answered six questions:

- Do some seasons (winter, summer, etc) have more traffic violations compared to others?
- What are the most and least common reasons for getting a traffic violation? 
- Are the number of traffic stops increasing or decreasing since 2012?
- Does the time of day affect the amount of traffic violations? 
- Are there certain locations in Montgomery County where violations are more frequent than others, and why? 
- What is the pattern of fatalities involving motorized vehicles since 2012, and why? 

**Full methods, results, limitations, and references are in the report:** [report_file.pdf](report_file.pdf)

## Data

- **Source:** Montgomery County, Maryland dataset on Data.gov [*Traffic Violations* dataset](https://data.montgomerycountymd.gov/Public-Safety/Traffic-Violations/4mse-ku6q/about_data). It is not stored in this repo because of its size.
- - **Data snapshot:** We downloaded the dataset on October 14, 2026. The county updates it regularly, so a newer download will include more recent stops and may produce different counts than our report, especially for 2026.
- **One row per violation, not per stop.** Count unique `SeqID` values to get stops.
- **The dataset's `Year` column is the vehicle's model year.** We create a separate stop-year column from `Date Of Stop`.
- 2026 is a partial year (dataset last updated October 14, 2026).

## Getting Started

1. Install dependencies:
   ```bash
   pip install pandas matplotlib seaborn plotly
   ```
   Plotly 5.24 or newer is needed for `px.density_map` and `px.scatter_map`.
2. Download the data from the link above
3. Open either notebook in `notebooks` and run all cells. Update the file path in the first data-loading cell if needed.

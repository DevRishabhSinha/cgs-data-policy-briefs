# README

Welcome to this multi-faceted codebase that covers **Location Classification, Data Gathering (Google Reviews, Google Search, Web Scraping), EV Charging Analysis, Industrial Park GeoJSON Visualizations, and more**. This repository is organized into several folders, each containing a unique purpose, set of scripts, and assets. Below is a comprehensive overview of every folder and its contents, along with detailed explanations of the workflow, file functionality, dependencies, and usage instructions. The goal is to provide you with a **one-stop reference** for understanding, maintaining, and extending this codebase.

---

## Table of Contents

1. [Repository Structure](#repository-structure)
2. [Directory-by-Directory Overview](#directory-by-directory-overview)
   - [.gitignore](#gitignore)
   - [.idea/](#idea)
   - [Address Type/](#address-type)
   - [Google Bot/](#google-bot)
   - [Google Reviews/](#google-reviews)
   - [Google Search/](#google-search)
   - [Industrial Park/](#industrial-park)
   - [OCM/](#ocm)
   - [Playground/](#playground)
   - [Tianyancha/](#tianyancha)
   - [README.md](#readmemd)
3. [Key Python and Notebook Scripts](#key-python-and-notebook-scripts)
   - [Address Type Scripts](#address-type-scripts)
   - [Google Bot Scripts](#google-bot-scripts)
   - [Google Reviews Scripts](#google-reviews-scripts)
   - [Google Search Scripts](#google-search-scripts)
   - [Industrial Park Scripts](#industrial-park-scripts)
   - [OCM Scripts](#ocm-scripts)
   - [Playground Scripts / Notebooks](#playground-scripts--notebooks)
   - [Tianyancha Scripts](#tianyancha-scripts)
4. [Development Environment and Dependencies](#development-environment-and-dependencies)
5. [Usage Instructions and Workflows](#usage-instructions-and-workflows)
   - [Location Type Classification Pipeline](#location-type-classification-pipeline)
   - [Google Scraping (Reviews/Bot) Workflow](#google-scraping-reviewsbot-workflow)
   - [Industrial Park Geospatial Analysis](#industrial-park-geospatial-analysis)
   - [Open Charge Map (OCM) Integration](#open-charge-map-ocm-integration)
6. [Additional Notes and Best Practices](#additional-notes-and-best-practices)
7. [Future Extensions](#future-extensions)

---

## Repository Structure

Below is the directory tree for quick reference:

```
.
├── .gitignore
├── .idea
│   ├── .gitignore
│   ├── CGS_9_11.iml
│   ├── inspectionProfiles
│   │   └── profiles_settings.xml
│   ├── misc.xml
│   ├── modules.xml
│   └── workspace.xml
├── Address Type
│   ├── charging_ports_heatmap.png
│   ├── claude.py
│   ├── enhanced_classification.py
│   ├── ev_station_types.png
│   ├── keyword_based_classification.py
│   ├── location_types.png
│   ├── location_types_bar.png
│   ├── location_types_pie.png
│   ├── nlp_based_classification.py
│   ├── parallel_processing_implementation.py
│   ├── port_config_based_classification.py
│   └── tf-idf.py
├── Google Bot
│   ├── test.py
│   ├── test2.py
│   ├── test3.py
│   └── test4.py
├── Google Reviews
│   ├── concat.py
│   ├── pruner.py
│   ├── test.py
│   ├── test10.py
│   ├── test11.py
│   ├── test12.py
│   ├── test2.py
│   ├── test3.py
│   ├── test4.py
│   ├── test5.py
│   ├── test6.py
│   ├── test7.py
│   ├── test8.py
│   └── test9.py
├── Google Search
│   ├── search_results
│   └── test.py
├── Industrial Park
│   ├── Basic_Industrial_Parks.geojson
│   ├── CGS_DASHBOARD_WORKING.html
│   ├── CGS_FINAL_BUILD.html
│   ├── Dashboard V1.html
│   ├── Dashboard V2.html
│   ├── Dashboard V3.html
│   ├── Dashboard V4.html
│   ├── Dashboard V5.html
│   ├── Dashboard V6.html
│   ├── Dispute_Industrial_Parks.geojson
│   ├── Energy_Industrial_Parks.geojson
│   ├── Filtered_Dispute_Industrial_Parks.geojson
│   ├── Filtered_Energy_Industrial_Parks.geojson
│   ├── Filtered_Foreign_Involvement_Industrial_Parks.geojson
│   ├── Filtered_Metals_Industrial_Parks.geojson
│   ├── Foreign_Involvement_Industrial_Parks.geojson
│   ├── Industrial_Parks.geojson
│   ├── Metals_Industrial_Parks.geojson
│   ├── Renewable_Energy_Industrial_Parks.geojson
│   ├── Status_Industrial_Parks.geojson
│   ├── cgs_logo.png
│   ├── dashboard.html
│   ├── filter.py
│   ├── geoplot.py
│   ├── geoplot_v2.py
│   ├── i.html
│   ├── indus_parks_complete_columns_oct24.xlsx
│   ├── industrial_park_geojson_generator.py
│   ├── industrial_parks.html
│   ├── industrial_parks_map.html
│   ├── industrial_parks_updated.html
│   ├── ipark.png
│   └── map_only.html
├── OCM
│   ├── test.py
│   └── test1.py
├── Playground
│   ├── combiner.py
│   ├── ev_station_types.png
│   ├── location_map.html
│   ├── location_types.png
│   ├── misc.py
│   ├── misc2.py
│   ├── ps1_stat470_rs.ipynb
│   ├── ps2_stat470_rs.ipynb
│   ├── ps3_stat470_rs.ipynb
│   ├── ps4_stat470_rs.ipynb
│   ├── test.py
│   ├── test2.py
│   ├── test3.py
│   └── test4.py
├── README.md
└── Tianyancha
    └── test.py
```

We also have a combined file dump (`final_code_dump_py_ipynb.log`) containing a concatenation of major Python scripts and Jupyter notebooks for deeper reference.

---

## Directory-by-Directory Overview

Below is a more detailed look at the purpose and contents of each major folder. 

### `.gitignore`
- Standard Git ignore file that prevents certain files (e.g., local environment, `.idea/`, compiled artifacts, etc.) from being committed.

### `.idea/`
- **IntelliJ / PyCharm** project settings:
  - `CGS_9_11.iml` and `.gitignore` for IDEA-based ignoring.
  - `inspectionProfiles/` includes code inspection settings (`profiles_settings.xml`).
  - `misc.xml`, `modules.xml`, `workspace.xml` are typical JetBrains IDE project files.

**No direct user scripts here**. This folder primarily manages your JetBrains/IDE configuration.

### Address Type/
Contains scripts and images related to **location-type classification** and **NLP** approaches to categorize addresses into location categories:

- **Images**:
  - `charging_ports_heatmap.png`, `ev_station_types.png`, `location_types.png`, `location_types_bar.png`, `location_types_pie.png`  
    - These are generated visualizations from classification scripts.
- **Scripts**:
  1. `claude.py`  
     - A classification script that demonstrates a high-level or alternative approach. (Potentially an internal name or a different LLM reference.)
  2. `enhanced_classification.py`  
     - A more comprehensive classification pipeline applying advanced logic (including text cleaning, advanced rules, or a combined approach).
  3. `keyword_based_classification.py`  
     - Straightforward regex or string-based classification approach. 
  4. `nlp_based_classification.py`  
     - NLP (TF-IDF / word embeddings / cosine similarity) approach for ambiguous location classification.
  5. `parallel_processing_implementation.py`  
     - Demonstration of using Python’s `concurrent.futures` or `multiprocessing` to handle classification in parallel.
  6. `port_config_based_classification.py`  
     - Classification that heavily relies on the number and type of EV charging ports (Level1, Level2, Level3) to label the location as EV charging or otherwise.
  7. `tf-idf.py`  
     - Likely a snippet or tutorial focusing on TF-IDF vectorization, possibly a second approach to unsupervised classification or cluster labeling.

**Purpose**: This folder is the core location classification logic repository, generating heatmaps, bar charts, pie charts, and detailed classification results.

### Google Bot/
Simple experimentation with **Selenium** or **requests**-based scripts for Google automation:

- `test.py`, `test2.py`, `test3.py`, `test4.py`
  - These typically demonstrate some form of automated Google searching or web scraping, possibly to gather search results, or test infiltration or the reliability of the scraping approach. 
  - Might be stepping stones or partial scripts for your final Google searching approach.

**Purpose**: R&D on basic **Google** automation, experimental code for search results or interactions.  

### Google Reviews/
A dedicated set of scripts for **scraping and handling Google Reviews**:

- **Scripts**:
  1. `concat.py`  
     - Possibly merges multiple partial CSV or JSON files of scraped reviews into a single consolidated dataset.
  2. `pruner.py`  
     - Tool to remove duplicates or filter out rows (perhaps for cleaning repeated reviews or removing incomplete data).
  3. `test.py`, `test2.py`, ..., `test12.py`  
     - A wide range of attempts at either scraping logic or partial code segments for collecting Google reviews.  
     - Some scripts incorporate multi-threading (`ThreadPoolExecutor`), advanced Selenium usage, or special logic to handle pagination in reviews.

**Purpose**: Gathering, merging, cleaning, and analyzing **Google user reviews** for addresses or stations.  

### Google Search/
Holds specialized scripts or subfolders about **search result retrieval** from Google:

- `search_results/`
  - Possibly an output folder containing CSV or JSON storing raw search result data.
- `test.py`
  - A reference script that likely queries the Google SERP and saves top results.  

**Purpose**: Acquire raw search data from Google programmatically.

### Industrial Park/
A broad and more substantial folder focusing on:
1. **GeoJSON** data for industrial parks**:
   - E.g., `Basic_Industrial_Parks.geojson`, `Energy_Industrial_Parks.geojson`, `Metals_Industrial_Parks.geojson`, etc.
   - Filtered versions, e.g., `Filtered_Energy_Industrial_Parks.geojson`.
2. Various `.html` dash-type or single-page web dashboards:
   - `CGS_DASHBOARD_WORKING.html`, `CGS_FINAL_BUILD.html`, `Dashboard V1.html`... through `Dashboard V6.html`.
   - `industrial_parks.html`, `industrial_parks_map.html`, `industrial_parks_updated.html`, `map_only.html`.
3. Supporting images:
   - `cgs_logo.png`, `ipark.png`.
4. Data frames and scripts:
   - `indus_parks_complete_columns_oct24.xlsx` - A detailed listing or spreadsheet with industrial park data.
   - `filter.py`, `geoplot.py`, `geoplot_v2.py`, `industrial_park_geojson_generator.py` 
     - Tools for reading, filtering, visualizing, or generating geojson data.

**Purpose**:  
- Provide robust geospatial analysis for Industrial Parks (with layers for metals, foreign involvement, disputes, energy).  
- Generate interactive dashboards or maps in HTML using libraries like **folium**, **geopandas**, or standard HTML frameworks.

### OCM/
Contains scripts referencing **Open Charge Map** integration:

- `test.py`, `test1.py`
  - Typically test retrieval from OCM’s public API. Possibly includes logic to parse EV station data, usage info, or comment fields.

**Purpose**:  
- Demonstrates how to integrate with the **Open Charge Map** API to gather EV charge station data.  

### Playground/
A more free-form or R&D space with:

- **Scripts**:
  - `combiner.py`  
    - Possibly merges or manipulates data from multiple CSVs or other data sources.
  - `misc.py`, `misc2.py`  
    - Grab-bag scripts: might contain snippets, utility functions, or partial code for testing.
  - `test.py`, `test2.py`, `test3.py`, `test4.py`
    - Additional test scripts, perhaps for new libraries or quick experiments.
- **Notebooks**:
  - `ps1_stat470_rs.ipynb`, `ps2_stat470_rs.ipynb`, `ps3_stat470_rs.ipynb`, `ps4_stat470_rs.ipynb`
    - Possibly problem sets or project-based Jupyter notebooks exploring various data manipulations, statistical methods, or prototypes for data analysis.
- **Images**:
  - `ev_station_types.png`, `location_types.png` (another copy?), `location_map.html`

**Purpose**:  
- A **sandbox** or “playground” for exploring new ideas, prototypes, or partial solutions.  

### README.md
- The root repository’s main readme. (This document you’re reading might replace or expand upon it with thorough instructions.)

### Tianyancha/
- **Scripts**:
  - `test.py`: Basic Selenium or requests-based script for scraping data from [Tianyancha](https://www.tianyancha.com/), a Chinese business data platform. Possibly a minimal example fetching table data or parsing company info.

**Purpose**:
- Demonstrate or test scraping from **Tianyancha** for business/financial data.

---

## Key Python and Notebook Scripts

In addition to the top-level descriptions, here is a deeper look at some major scripts:

### Address Type Scripts

1. **`enhanced_classification.py`**  
   - Reads a CSV of locations (`locations.csv` or similar).
   - Cleans text fields by removing quotes, lowercasing, or removing punctuation.
   - Implements a more advanced classification approach that integrates:
     - EV port checks (Level1/2/3).
     - Keyword-based logic for known patterns (e.g., “hotel”, “hospital”).
     - Possibly calls deeper NLP steps (vector embeddings, clustering).
   - Exports a CSV with a new column `Category`.
   - Generates data visualizations for location distribution.

2. **`nlp_based_classification.py`**  
   - Illustrates usage of TF-IDF, vector embeddings, or cosine similarity to disambiguate location categories.
   - Typically merges reference categories with ambiguous cases.
   - Example usage:
     ```bash
     python nlp_based_classification.py
     ```
   - Relies on scikit-learn or spaCy for advanced text processing.

3. **`parallel_processing_implementation.py`**  
   - Demonstrates chunk-based classification using `ProcessPoolExecutor` or `ThreadPoolExecutor`.
   - Gains speed improvement for large CSV datasets.

4. **`port_config_based_classification.py`**  
   - Focuses on labeling addresses as “EV Charging Station,” “High Capacity,” “Level2,” etc., purely from port counts.

5. **`keyword_based_classification.py`**  
   - Basic rule-based approach with simple regex patterns for “hotel,” “restaurant,” etc.

6. **`tf-idf.py`**  
   - Possibly a skeleton or demonstration script focusing on the TF-IDF concept for textual data classification or clustering.

Images in this folder (`charging_ports_heatmap.png`, etc.) are **outputs** from the classification scripts, e.g., distribution charts.

---

### Google Bot Scripts

- **`test.py`, `test2.py`, `test3.py`, `test4.py`**:  
  - Showcases various attempts at automating or interacting with Google (like searching or scraping).
  - Some might use `selenium.webdriver` to open a Chrome session, input queries, and parse results.  
  - Typically used for R&D or small tasks.  
  - May not be fully production-ready but can serve as references or test harnesses.

---

### Google Reviews Scripts

- **`concat.py`**:  
  - Merges multiple partial “reviews” CSVs (like `output_reviews2567final.csv`, etc.) into a single file `combined_output_reviews.csv`.
  - It ensures consistent columns. This is critical if your scraping job was segmented or partial.

- **`pruner.py`**:  
  - Helps remove duplicates, handle “N/A” strings, or unify columns across multiple merges.  
  - Typically after merging, you might run a pruner to keep data consistent.

- **`test.py`** through **`test12.py`**:  
  - Each enumerated script demonstrates a different iteration or approach for:
    1. **Selenium** usage with or without headless Chrome.
    2. Handling concurrency (`ThreadPoolExecutor`) to parallelize review scraping.
    3. Error handling (try/except for captchas, timeouts, or rate-limits).
    4. Additional logging (debug, error logs).
    5. CSV write logic to ensure partial results are stored even if a crash occurs.
  - Common usage might be:
    ```bash
    python testX.py
    ```
    (Pick the script best matching your environment or feature needs.)

**Note**: These scripts often rely on user agents and polite time delays to avoid Google blocking or captchas.  

---

### Google Search Scripts

- **`test.py`**:  
  - Possibly demonstrates using the `googlesearch` Python library or manual scraping logic to gather top results for a list of queries in `input.csv`.
  - Writes results to CSV in `search_results` or a named output file.  
  - Rate-limiting might be used to avoid “Too Many Requests” from Google.

- **`search_results/`**:
  - Contains CSV outputs for queries.

---

### Industrial Park Scripts

1. **`filter.py`**  
   - Possibly filters or merges multiple geojson files to produce subsets like `Filtered_Energy_Industrial_Parks.geojson`.
   - Example usage might be:
     ```bash
     python filter.py
     ```
     and it reads from the base geojson, then writes filtered versions.

2. **`geoplot.py`, `geoplot_v2.py`**  
   - Visualizes industrial parks on a map using **matplotlib**, **geopandas**, or **folium**.
   - Potentially merges CSV data with geometry to produce `.html` maps.

3. **`industrial_park_geojson_generator.py`**  
   - Takes raw spreadsheet data (like `indus_parks_complete_columns_oct24.xlsx`) and outputs a `.geojson` file.
   - This is crucial to build the final geospatial data sets used in dashboards.

4. Various `.html` dashboards:
   - `CGS_DASHBOARD_WORKING.html`, `Dashboard V1.html`, `Dashboard V2.html`, etc.  
   - Possibly partial or final interactive dashboards.  
   - They can be viewed in a browser to see map layers, popups, and dynamic filters.

5. **`ipark.png`, `cgs_logo.png`**  
   - Used by the dashboards or map markers.

**Purpose**: Combine geospatial data with metadata about industrial parks.  

---

### OCM Scripts

- **`test.py` / `test1.py`**  
  - Demonstration of hitting the [Open Charge Map API](https://openchargemap.org/site/develop/api) to retrieve station info. 
  - The typical usage flow:
    1. Provide an API key.
    2. Query by lat/lng or bounding box. 
    3. Parse the result for station name, usage cost, operator, connections, etc.

**Potential**: This can integrate with the `Address Type` classification, cross-referencing if a location is an official OCM entry.

---

### Playground Scripts / Notebooks

**Contents** vary widely; some highlights:

1. **`combiner.py`**  
   - Another aggregator script for CSV or JSON merges. Possibly distinct from `concat.py` in the `Google Reviews` folder.

2. **`misc.py`, `misc2.py`**  
   - Arbitrary utility code or demonstration scripts (e.g., quick data transformations, random test code).

3. **`psX_stat470_rs.ipynb`**  
   - Jupyter notebooks that might involve problem sets or extended analysis in a statistical class context. Examples:
     - Probability distributions, hypothesis tests, or time-series. 
     - Possibly uses libraries like `numpy`, `pandas`, `scipy.stats`, `matplotlib`.

4. **`test.py`, `test2.py`, `test3.py`, `test4.py`**  
   - Further demonstration or minimal test scripts.

5. Additional visuals:
   - `ev_station_types.png`, `location_types.png`, `location_map.html`: 
     - Reiterations of classification or geospatial outputs.

---

### Tianyancha Scripts

- **`test.py`**  
  - Minimal script that uses Selenium to visit a Tianyancha company page. 
  - Waits for page load, scrapes table data from `.table-wrap` or similar. 
  - Logs to console.  
  - Example usage:
    ```bash
    python test.py
    ```
    (Ensure to have proper credentials or usage rights for the site.)

---

## Development Environment and Dependencies

1. **Python Version**: Typically tested on Python 3.7+ (varies across scripts).  
2. **Key Libraries**:
   - **pandas**, **numpy**, **requests**, **re**, **csv**, **argparse**, **time**
   - **scikit-learn** (TF-IDF, KMeans, etc.)
   - **folium**, **geopandas**, **matplotlib**, **seaborn** for geospatial or plotting.
   - **Selenium** + a driver manager (`webdriver_manager`) to scrape dynamic websites.
   - **googlesearch-python** for minimal SERP retrieval.
   - Possibly **spacy** for advanced NLP in `nlp_based_classification.py`.

**Installation**:  
```bash
pip install -r requirements.txt
```
*(No `requirements.txt` is explicitly included here, so you may want to generate it by `pip freeze` or manually gather package versions.)*

---

## Usage Instructions and Workflows

### Location Type Classification Pipeline

1. **Data**: A CSV file, e.g., `locations.csv`, with columns such as `LocName`, `address`, `Level1Ports`, `Level2Ports`, `Level3Ports`, etc.
2. **Run**:
   ```bash
   python enhanced_classification.py path/to/locations.csv
   ```
   or you can open each classification script:
   - **`keyword_based_classification.py`** for simple rules.
   - **`nlp_based_classification.py`** for advanced text-based disambiguation.
3. **Outputs**:
   - A new CSV, e.g., `locations_classified.csv`, with an added `Category` or `NLPClassification` column.
   - Optional **visualizations** (`.png` files) showing category distribution.

### Google Scraping (Reviews/Bot) Workflow

1. Prepare an **input CSV** containing addresses or queries (e.g., `input.csv`).
2. Decide on a script: e.g., `test10.py` or `test11.py` from `Google Reviews/`.
3. **Check** for concurrency or single-thread use. 
   - Example usage:
     ```bash
     python test10.py
     ```
   - This might open headless Chrome sessions, do queries, scrape reviews, store them in `output_reviews.csv`.
4. Merging partial results:
   - Use `concat.py` in `Google Reviews/` if you had separate run outputs. 
   - Then optionally run `pruner.py` to remove duplicates or unify columns.

### Industrial Park Geospatial Analysis

1. Collect or refine CSV data about parks (like `indus_parks_complete_columns_oct24.xlsx`).
2. Use `industrial_park_geojson_generator.py` to convert to **.geojson**.  
3. Optionally run `filter.py` to make subsets (like “Energy_Industrial_Parks.geojson”).
4. Plot or generate interactive maps:
   - `geoplot.py` or `geoplot_v2.py` or open the `.html` dashboards.  
   - Some dashboards require local references or an offline environment. They can be opened in any modern browser.

### Open Charge Map (OCM) Integration

1. Obtain an OCM API key from [https://openchargemap.org/](https://openchargemap.org/).
2. Run a script from `OCM/`, e.g., `test.py`, providing lat/long bounding boxes or in the code itself. 
3. The script downloads local station data, which you can cross-reference with your classification pipeline.

---

## Additional Notes and Best Practices

- **Rate Limiting**: For Google Reviews, Google Search, or other services, always add `time.sleep()` calls, as these scripts do.  
- **API Keys**: The OCM examples store the key in the code or read from an environment variable. Keep them out of version control in production.  
- **Large Data**: If handling tens or hundreds of thousands of rows, consider chunked reading (e.g., `pandas.read_csv(..., chunksize=5000)`) and parallel classification.  
- **Geospatial**: If using large `.geojson` files, be mindful of memory usage or switch to streaming solutions in `geopandas`.  
- **Selenium**: Requires installing **ChromeDriver** or **geckodriver**. The `webdriver_manager` library helps automatically manage driver versions.

---

## Future Extensions

- **Dockerization**: Containerize each subproject for reproducible environments.
- **Central Config**: Have a global `.env` for sensitive keys (API, etc.) and unify logs in a single folder.
- **Refactor**: Merge all classification scripts into a single cohesive pipeline with sub-commands (`argparse`).
- **CI/CD**: Add unit tests for each key function, integrate with a pipeline that checks code formatting, runs tests, and updates docstrings.
